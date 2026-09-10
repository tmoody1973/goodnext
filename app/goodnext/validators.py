"""Deterministic post-generation checks on a FoodPlanProposal.

PRD section 6: model output may only reference records returned by authorized
tools; a zero-budget plan cannot rely on a purchase; closed resources cannot be
proposed; unknowns stay visible. Decision (2026-09-08): a violating visit is
stripped and the plan returns as partial. No retry in this slice.
"""

from datetime import date, datetime, time

from claims import build_claims, notice_never_list_hits
from schemas import (
    DayPlan,
    FoodPlanProposal,
    FoodResource,
    HouseholdConstraints,
    NextOpen,
    NoticeAction,
    NoticeFinding,
    NoticePlanProposal,
    OfficialRoute,
    PlannedVisit,
    PolicyEvidence,
    UnconfirmedRecord,
)
from tools import freshness_tier, next_open_after, window_open_at


def _visit_violation(
    v: PlannedVisit, ledger: set[str], directory: dict[str, FoodResource], constraints: HouseholdConstraints, now: datetime
) -> str | None:
    if v.resource_id not in ledger:
        return f"{v.resource_id}: not returned by any tool (possible fabrication)"
    resource = directory.get(v.resource_id)
    if resource is None:
        return f"{v.resource_id}: unknown resource"
    if resource.status != "published":
        return f"{v.resource_id}: status is {resource.status}"
    if constraints.budget_usd <= 0 and resource.cost in ("paid", "sliding"):
        return f"{v.resource_id}: paid option in a zero-budget plan"
    window = next((w for w in resource.windows if w.date == v.date), None)
    if window is None:
        return f"{v.resource_id}: no opening window on {v.date}"
    if not window_open_at(window.model_dump(), now):
        return f"{v.resource_id}: closed before request time"
    return None


def _with_freshness(v: PlannedVisit, resource: FoodResource, tier: str, now: datetime, constraints: HouseholdConstraints) -> PlannedVisit:
    uncertainty = list(v.uncertainty)
    if tier == "call_to_confirm":
        note = f"Last checked {resource.last_verified}; call to confirm"
        if note not in uncertainty:
            uncertainty.append(note)
    for note in resource.uncertainties:
        if note not in uncertainty:
            uncertainty.append(note)
    if resource.cost == "unknown" and "Cost not stated by the provider; ask" not in uncertainty:
        uncertainty.append("Cost not stated by the provider; ask")
    service_area_known = bool(resource.zip_codes_served) or resource.serves_all_milwaukee
    if not service_area_known:
        # MOO-772 (D5): keep the visit, never let it read as a plain confirmed one.
        note = "Confirm they serve your area"
        if note not in uncertainty:
            uncertainty.append(note)
    # MOO-781: a later-day visit's next-open window is judged from the start of
    # its own day, not from today's clock; today's visit keeps the live clock.
    anchor = now if v.date == now.date().isoformat() else datetime.combine(date.fromisoformat(v.date), time.min, tzinfo=now.tzinfo)
    nxt = next_open_after([w.model_dump() for w in resource.windows], anchor)
    updated = v.model_copy(update={
        "freshness_tier": tier,
        "uncertainty": uncertainty,
        "service_area_known": service_area_known,
        "next_open": NextOpen(date=nxt["date"], open=nxt["open"], close=nxt["close"]) if nxt else None,
    })
    # MOO-775 (D9): every kept visit carries the permitted claims, built after
    # freshness_tier, next_open, and service_area_known are set since claims read them.
    return updated.model_copy(update={"claims": build_claims(updated, resource, constraints, now)})


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
    now_local: str,
) -> tuple[FoodPlanProposal, list[str]]:
    """Return a cleaned proposal and the list of violations found. Never mutates input.
    now_local is authoritative regardless of what the model passed to its tool calls (MOO-774)."""
    violations: list[str] = []
    start = expected_dates[0]
    now = datetime.fromisoformat(now_local)

    def keep(visits: list[PlannedVisit], strip_unconfirmed: bool) -> list[PlannedVisit]:
        kept = []
        for v in visits:
            if problem := _visit_violation(v, ledger, directory, constraints, now):
                violations.append(problem)
                continue
            resource = directory[v.resource_id]
            tier = freshness_tier(resource.last_verified, start)
            if strip_unconfirmed and tier == "unconfirmed":
                violations.append(f"{v.resource_id}: unconfirmed tier; kept out of Food today")
                continue
            kept.append(_with_freshness(v, resource, tier, now, constraints))
        return kept

    by_date = {d.date: d for d in proposal.days}
    if [d.date for d in proposal.days] != expected_dates:
        violations.append(f"days did not match the seven server dates; rebuilt from {start}")
    days = []
    for d in expected_dates:
        day = by_date.get(d, DayPlan(date=d, unmet_needs=["No plan proposed for this day"]))
        days.append(day.model_copy(update={"visits": keep(day.visits, strip_unconfirmed=(d == start))}))

    # MOO-774: food_today is DERIVED from the surviving day-one visits, not the model's own
    # food_today list (that list came back incomplete in the first live run).
    food_today = days[0].visits
    used = sorted({v.resource_id for day in days for v in day.visits})
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


# --- Understand notice slice (MOO-789) ---
#
# PRD FR02, FR03 and APIs doc section 7: a next action may only cite notice findings
# and policy evidence that authorized tools returned; a prohibited claim (eligibility,
# exemption approval, benefit continuity, official outcome) is never shown; missing
# dates are not inferred. A violating action is stripped and the plan returns partial,
# mirroring the food-today validator. The literal deadline text and its passed/upcoming
# state come from the finding, never from the model.


def _deadline_status(parsed_deadline: str | None, now: datetime) -> str:
    """passed / upcoming / unknown, judged by the server clock. Never inferred."""
    if parsed_deadline is None:
        return "unknown"
    return "passed" if date.fromisoformat(parsed_deadline) < now.date() else "upcoming"


def _action_strings(a: NoticeAction) -> list[str]:
    return [a.instruction, *a.prerequisites, *a.confirm_fields, *a.unknowns]


def _action_violation(
    a: NoticeAction,
    ledger: set[str],
    findings: dict[str, NoticeFinding],
    evidence: dict[str, PolicyEvidence],
    routes: dict[str, OfficialRoute],
) -> str | None:
    if a.notice_id not in ledger or a.notice_id not in findings:
        return f"{a.action_id}: cites notice {a.notice_id} not returned by read_notice (possible fabrication)"
    for eid in a.evidence_ids:
        if eid not in ledger or eid not in evidence:
            return f"{a.action_id}: cites policy {eid} not returned by get_policy_evidence"
    if a.route_id is not None and (a.route_id not in ledger or a.route_id not in routes):
        return f"{a.action_id}: cites route {a.route_id} not returned by resolve_help_route"
    if notice_never_list_hits(_action_strings(a)):
        return f"{a.action_id}: prohibited notice claim"
    return None


def _rendered_action(a: NoticeAction, finding: NoticeFinding, now: datetime) -> NoticeAction:
    """Overwrite the trustworthy fields from the cited finding, and add the confirmations
    and urgent step the deadline state requires. The model never sets these."""
    status = _deadline_status(finding.parsed_deadline, now)
    confirm_fields = list(a.confirm_fields)
    if status == "unknown":
        note = "Confirm the deadline date with the agency"
        if note not in confirm_fields:
            confirm_fields.append(note)
    unknowns = list(a.unknowns)
    if status == "passed":
        note = "This date has passed; call the agency about next steps right away"
        if note not in unknowns:
            unknowns.append(note)
    if finding.missing_pages:
        note = f"Some notice pages are missing (pages {finding.missing_pages}); confirm the full notice"
        if note not in unknowns:
            unknowns.append(note)
    return a.model_copy(update={
        "program": finding.program,
        "person_ref": finding.person_ref,
        "deadline_text": finding.literal_deadline_text,
        "deadline_status": status,
        "confirm_fields": confirm_fields,
        "unknowns": unknowns,
    })


def validate_notice_plan(
    proposal: NoticePlanProposal,
    ledger: set[str],
    findings: dict[str, NoticeFinding],
    evidence: dict[str, PolicyEvidence],
    routes: dict[str, OfficialRoute],
    now_local: str,
) -> tuple[NoticePlanProposal, list[str]]:
    """Return a cleaned proposal and the list of violations found. Never mutates input."""
    violations: list[str] = []
    now = datetime.fromisoformat(now_local)

    kept: list[NoticeAction] = []
    for a in proposal.actions:
        if problem := _action_violation(a, ledger, findings, evidence, routes):
            violations.append(problem)
            continue
        kept.append(_rendered_action(a, findings[a.notice_id], now))

    # Free text outside actions is scanned too, so no prohibited claim survives anywhere.
    checklist: list[str] = []
    for item in proposal.checklist:
        if notice_never_list_hits(item):
            violations.append("checklist item stripped: prohibited notice claim")
        else:
            checklist.append(item)
    explanation = proposal.explanation
    if notice_never_list_hits(explanation):
        violations.append("explanation stripped: prohibited notice claim")
        explanation = "See the actions above and the source for each one."

    kept_ids = {a.action_id for a in kept}
    next_step = proposal.next_step if proposal.next_step in kept_ids else (kept[0].action_id if kept else "")
    confirmations: list[str] = []
    for a in kept:
        for c in a.confirm_fields:
            if c not in confirmations:
                confirmations.append(c)

    cleaned = proposal.model_copy(update={
        "actions": kept,
        "checklist": checklist,
        "explanation": explanation,
        "next_step": next_step,
        "notice_ids": sorted({a.notice_id for a in kept}),
        "supported_dates": sorted({a.deadline_text for a in kept if a.deadline_status != "unknown" and a.deadline_text}),
        "evidence_ids_used": sorted({eid for a in kept for eid in a.evidence_ids}),
        "route_ids_used": sorted({a.route_id for a in kept if a.route_id}),
        "confirmations_needed": confirmations,
    })
    return cleaned, violations
