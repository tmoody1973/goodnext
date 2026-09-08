"""Deterministic post-generation checks on a FoodPlanProposal.

PRD section 6: model output may only reference records returned by authorized
tools; a zero-budget plan cannot rely on a purchase; closed resources cannot be
proposed; unknowns stay visible. Decision (2026-09-08): a violating visit is
stripped and the plan returns as partial. No retry in this slice.
"""

from schemas import DayPlan, FoodPlanProposal, FoodResource, HouseholdConstraints, PlannedVisit, UnconfirmedRecord
from tools import freshness_tier


def _visit_violation(
    v: PlannedVisit, ledger: set[str], directory: dict[str, FoodResource], constraints: HouseholdConstraints
) -> str | None:
    if v.resource_id not in ledger:
        return f"{v.resource_id}: not returned by any tool (possible fabrication)"
    resource = directory.get(v.resource_id)
    if resource is None:
        return f"{v.resource_id}: unknown resource"
    if resource.status != "published":
        return f"{v.resource_id}: status is {resource.status}"
    if constraints.budget_usd <= 0 and resource.cost != "free":
        return f"{v.resource_id}: paid option in a zero-budget plan"
    if not any(w.date == v.date for w in resource.windows):
        return f"{v.resource_id}: no opening window on {v.date}"
    return None


def _with_freshness(v: PlannedVisit, resource: FoodResource, tier: str) -> PlannedVisit:
    update = {"freshness_tier": tier}
    if tier == "call_to_confirm":
        note = f"Last checked {resource.last_verified}; call to confirm"
        if note not in v.uncertainty:
            update["uncertainty"] = [*v.uncertainty, note]
    return v.model_copy(update=update)


def _unconfirmed_records(ledger: set[str], directory: dict[str, FoodResource], start: str) -> list[UnconfirmedRecord]:
    """Tool-returned records that are unconfirmed-tier: phone number only, never a visit."""
    records = [
        UnconfirmedRecord(resource_id=r.resource_id, provider=r.provider, contact=r.contact)
        for rid in ledger
        if (r := directory.get(rid)) is not None and freshness_tier(r.last_verified, start) == "unconfirmed"
    ]
    return sorted(records, key=lambda r: r.resource_id)


def validate_food_plan(
    proposal: FoodPlanProposal,
    ledger: set[str],
    directory: dict[str, FoodResource],
    constraints: HouseholdConstraints,
    expected_dates: list[str],
) -> tuple[FoodPlanProposal, list[str]]:
    """Return a cleaned proposal and the list of violations found. Never mutates input."""
    violations: list[str] = []
    start = expected_dates[0]

    def keep(visits: list[PlannedVisit], strip_unconfirmed: bool) -> list[PlannedVisit]:
        kept = []
        for v in visits:
            if problem := _visit_violation(v, ledger, directory, constraints):
                violations.append(problem)
                continue
            resource = directory[v.resource_id]
            tier = freshness_tier(resource.last_verified, start)
            if strip_unconfirmed and tier == "unconfirmed":
                violations.append(f"{v.resource_id}: unconfirmed tier; kept out of Food today")
                continue
            kept.append(_with_freshness(v, resource, tier))
        return kept

    by_date = {d.date: d for d in proposal.days}
    if [d.date for d in proposal.days] != expected_dates:
        violations.append(f"days did not match the seven server dates; rebuilt from {start}")
    days = []
    for d in expected_dates:
        day = by_date.get(d, DayPlan(date=d, unmet_needs=["No plan proposed for this day"]))
        days.append(day.model_copy(update={"visits": keep(day.visits, strip_unconfirmed=(d == start))}))

    food_today = keep([v for v in proposal.food_today if v.date == start], strip_unconfirmed=True)
    used = sorted({v.resource_id for day in days for v in day.visits} | {v.resource_id for v in food_today})
    unconfirmed = _unconfirmed_records(ledger, directory, start)
    cleaned = proposal.model_copy(
        update={
            "start_date": start,
            "days": days,
            "food_today": food_today,
            "resource_ids_used": used,
            "unconfirmed": unconfirmed,
        }
    )
    return cleaned, violations
