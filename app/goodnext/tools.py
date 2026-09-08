"""Application tools the resident agent may call.

Contract: docs/FoodShare-Bridge-APIs-Data-and-Prompts.md section 4 and the
Execution Design section 11. Every tool returns the shared envelope shape as a
plain dict. Tools never reserve food, verify stock, or contact providers.
"""

import contextvars
import json
import os
from datetime import date
from pathlib import Path

from strands import tool

from schemas import FoodResource, HouseholdConstraints

# ponytail: request-scoped ledger of resource IDs the tools actually returned.
# The validator rejects any ID outside it. Lives in-process; move to receipts
# storage only if audit requirements demand it.
returned_ids: contextvars.ContextVar[set[str]] = contextvars.ContextVar("returned_ids")

STALE_AFTER_DAYS = 14
FIXTURE_PATH = Path(os.environ.get("GOODNEXT_FIXTURE_PATH", Path(__file__).parent / "fixtures" / "milwaukee-food-resources.json"))


def load_directory() -> dict[str, FoodResource]:
    raw = json.loads(FIXTURE_PATH.read_text())
    return {r["resource_id"]: FoodResource(**r) for r in raw["resources"]}


def _ledger() -> set[str]:
    try:
        return returned_ids.get()
    except LookupError:
        fresh: set[str] = set()
        returned_ids.set(fresh)
        return fresh


def _envelope(status: str, data=None, evidence=(), missing=(), warnings=(), retryable=False) -> dict:
    return {
        "status": status,
        "data": data,
        "evidence": list(evidence),
        "missing": list(missing),
        "warnings": list(warnings),
        "retryable": retryable,
    }


def _visible(resource: FoodResource, zip_code: str, start: str, end: str) -> list[dict]:
    """Windows for a published resource serving this ZIP inside the date range."""
    if resource.status != "published" or zip_code not in resource.zip_codes_served:
        return []
    return [w.model_dump() for w in resource.windows if start <= w.date <= end]


def _staleness_warning(resource: FoodResource, start: str) -> str | None:
    age = (date.fromisoformat(start) - date.fromisoformat(resource.last_verified)).days
    if age > STALE_AFTER_DAYS:
        return f"{resource.resource_id}: hours last verified {age} days ago; call to confirm"
    return None


@tool
def find_food_resources(zip_code: str, start_date: str, end_date: str) -> dict:
    """Search published, reviewed food-service records for the supplied ZIP area and date window.
    Returns resource IDs, service windows, cost, requirements and unknown fields.
    This lookup does not reserve food, verify stock or contact providers.
    Records marked closed or withdrawn, and providers that do not serve the ZIP, are excluded.
    """
    try:
        directory = load_directory()
    except (OSError, ValueError) as exc:
        return _envelope("temporarily_unavailable", warnings=[f"directory unavailable: {exc.__class__.__name__}"], retryable=True)

    candidates, warnings = [], []
    for resource in directory.values():
        windows = _visible(resource, zip_code, start_date, end_date)
        if not windows:
            continue
        record = resource.model_dump()
        record["windows"] = windows
        record["quantity_per_visit"] = "unknown"
        candidates.append(record)
        if stale := _staleness_warning(resource, start_date):
            warnings.append(stale)

    if not candidates:
        return _envelope("no_match", data=[], missing=["No published resource serves this ZIP in the requested dates"])

    _ledger().update(r["resource_id"] for r in candidates)
    return _envelope(
        "success",
        data=candidates,
        evidence=[r["resource_id"] for r in candidates],
        missing=["quantity_per_visit unknown for every record"],
        warnings=warnings,
    )


@tool
def check_food_constraints(resource_ids: list[str], budget_usd: float, kitchen: str, travel: list[str]) -> dict:
    """Deterministically check candidate resources against confirmed household constraints.
    kitchen is one of full, microwave_only, none. travel lists walk, bus, car, ride.
    Returns each resource as supported, conditional or unsuitable with reasons.
    This check does not determine benefit eligibility and does not verify stock.
    """
    try:
        directory = load_directory()
    except (OSError, ValueError) as exc:
        return _envelope("temporarily_unavailable", warnings=[f"directory unavailable: {exc.__class__.__name__}"], retryable=True)

    results = []
    for rid in resource_ids:
        resource = directory.get(rid)
        if resource is None or rid not in _ledger():
            results.append({"resource_id": rid, "verdict": "unsuitable", "reasons": ["not a returned resource"]})
            continue
        reasons, verdict = [], "supported"
        if resource.cost != "free" and budget_usd <= 0:
            verdict, reasons = "unsuitable", ["costs money; household budget is zero"]
        elif resource.cost != "free":
            verdict, reasons = "conditional", ["paid option; must fit stated budget"]
        if resource.appointment_required:
            verdict = "conditional" if verdict != "unsuitable" else verdict
            reasons.append("appointment required; not booked by this service")
        if kitchen == "none" and resource.service_type == "free_pantry":
            verdict = "conditional" if verdict != "unsuitable" else verdict
            reasons.append("no kitchen; ask for no-cook items")
        if travel == ["walk"]:
            reasons.append("walking only; travel time unknown, confirm distance")
        results.append({"resource_id": rid, "verdict": verdict, "reasons": reasons})

    return _envelope("success", data=results, evidence=[r["resource_id"] for r in results])


def constraints_for_tool(c: HouseholdConstraints) -> dict:
    return {"budget_usd": c.budget_usd, "kitchen": c.kitchen, "travel": list(c.travel)}
