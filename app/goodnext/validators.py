"""Deterministic post-generation checks on a FoodPlanProposal.

PRD section 6: model output may only reference records returned by authorized
tools; a zero-budget plan cannot rely on a purchase; closed resources cannot be
proposed; unknowns stay visible. Decision (2026-09-08): a violating visit is
stripped and the plan returns as partial. No retry in this slice.
"""

from datetime import date

from schemas import DayPlan, FoodPlanProposal, FoodResource, HouseholdConstraints, PlannedVisit
from tools import STALE_AFTER_DAYS


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


def _with_staleness(v: PlannedVisit, resource: FoodResource, start: str) -> PlannedVisit:
    age = (date.fromisoformat(start) - date.fromisoformat(resource.last_verified)).days
    note = f"Hours last verified {age} days ago; call to confirm"
    if age > STALE_AFTER_DAYS and note not in v.uncertainty:
        return v.model_copy(update={"uncertainty": [*v.uncertainty, note]})
    return v


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

    def keep(visits: list[PlannedVisit]) -> list[PlannedVisit]:
        kept = []
        for v in visits:
            if problem := _visit_violation(v, ledger, directory, constraints):
                violations.append(problem)
            else:
                kept.append(_with_staleness(v, directory[v.resource_id], start))
        return kept

    by_date = {d.date: d for d in proposal.days}
    if [d.date for d in proposal.days] != expected_dates:
        violations.append(f"days did not match the seven server dates; rebuilt from {start}")
    days = []
    for d in expected_dates:
        day = by_date.get(d, DayPlan(date=d, unmet_needs=["No plan proposed for this day"]))
        days.append(day.model_copy(update={"visits": keep(day.visits)}))

    food_today = keep([v for v in proposal.food_today if v.date == start])
    used = sorted({v.resource_id for day in days for v in day.visits} | {v.resource_id for v in food_today})
    cleaned = proposal.model_copy(
        update={"start_date": start, "days": days, "food_today": food_today, "resource_ids_used": used}
    )
    return cleaned, violations
