"""The eight permitted resident-facing claims, and nothing else, per visit.

docs/specs/food-today.md D9: the eight allowed statements are rendered from
record fields, never free text from the model. Claims 6 (inventory_text) and
8 (travel_text) are always present verbatim. NEVER_LIST is the single
reviewed constant a test scans every resident-facing response against.
Pure; no I/O.
"""

import re
from datetime import datetime
from urllib.parse import quote_plus

from schemas import Claims, FoodResource, HouseholdConstraints, PlannedVisit

# CONTEXT.md glossary + PRD FR04: words that promise stock, a reservation, or
# a computed travel time. Reviewed 2026-09-08.
NEVER_LIST = [
    "in stock",
    "reserved",
    "available",
    "guaranteed",
    "confirmed for you",
    "secured",
    "food covered",
]

# MOO-789: prohibited notice claims — statements that decide eligibility, approve an
# exemption, promise benefit continuity or claim an official outcome. P01/P02 and PRD
# FR02/FR03 forbid all of these. Reviewed 2026-09-10. Scanned by the same mechanism.
NOTICE_NEVER_LIST = [
    "you are eligible",
    "you are ineligible",
    "you are exempt",
    "exemption approved",
    "exemption granted",
    "benefits will continue",
    "benefits will stop",
    "your case is closed",
    "your case is resolved",
    "you must work 80 hours",
    "everyone must work",
    "successfully submitted",
    "deadline has been extended",
    "appeal has been filed",
]

_COST_LABELS = {"free": "Free", "paid": "Paid", "sliding": "Sliding scale", "unknown": "Cost not stated; ask"}


def _compile(terms: list[str]) -> list[re.Pattern]:
    return [re.compile(r"\b" + re.escape(term) + r"\b", re.I) for term in terms]


_NEVER_RE = _compile(NEVER_LIST)
_NOTICE_NEVER_RE = _compile(NOTICE_NEVER_LIST)
# A denial is honest: "stock cannot be guaranteed", "not reserved", "no food secured".
_NEGATED = re.compile(r"\b(?:not|no|nothing|none|never|cannot|can't|can not|isn't|aren't|without|nor)\b(?:\s+\w+){0,2}\s+$", re.I)


def _hits(obj: object, terms: list[str], regexes: list[re.Pattern]) -> list[str]:
    """Walk any JSON-like structure's string values for prohibited terms as whole words
    (so 'unavailable' in a status does not count as 'available'), skipping honest denials."""
    hits: list[str] = []

    def walk(node: object) -> None:
        if isinstance(node, str):
            for term, rx in zip(terms, regexes):
                for m in rx.finditer(node):
                    if not _NEGATED.search(node[max(0, m.start() - 40):m.start()]):
                        hits.append(term)
        elif isinstance(node, dict):
            for value in node.values():
                walk(value)
        elif isinstance(node, (list, tuple)):
            for value in node:
                walk(value)

    walk(obj)
    return hits


def never_list_hits(obj: object) -> list[str]:
    """Food never-list: promises of stock, a reservation, or a computed travel time."""
    return _hits(obj, NEVER_LIST, _NEVER_RE)


def notice_never_list_hits(obj: object) -> list[str]:
    """Notice never-list: eligibility decisions, exemption approvals, benefit-continuity
    or official-outcome claims the agent must never make (MOO-789)."""
    return _hits(obj, NOTICE_NEVER_LIST, _NOTICE_NEVER_RE)


def _fmt_12h(hhmm: str) -> str:
    hour_str, minute = hhmm.split(":")
    hour = int(hour_str)
    period = "AM" if hour < 12 else "PM"
    hour12 = hour % 12 or 12
    return f"{hour12}:{minute} {period}"


def _open_today_text(visit: PlannedVisit, resource: FoodResource, now: datetime) -> str:
    """Claim 1. Today's visit reads "Open today …"; a later-day visit names its own
    weekday (MOO-781). "Not open" wording appears only when the record has no window
    on the visit's day, and next open is then never earlier than that day."""
    today = now.date().isoformat()
    day_word = "today" if visit.date == today else datetime.fromisoformat(visit.date).strftime("%A")
    window = next((w for w in resource.windows if w.date == visit.date), None)
    if window is not None and (visit.date != today or window.close > now.strftime("%H:%M")):
        return f"Open {day_word} from {_fmt_12h(window.open)} to {_fmt_12h(window.close)}"
    if visit.next_open is not None:
        return f"Not open {day_word}; next open {visit.next_open.date} at {_fmt_12h(visit.next_open.open)}"
    return "Opening time unknown"


def _requirements_text(resource: FoodResource) -> str:
    return f"May require: {'; '.join(resource.requirements)}" if resource.requirements else "No requirements listed"


def _freshness_text(visit: PlannedVisit, resource: FoodResource) -> str:
    if visit.freshness_tier == "verified":
        return f"Last checked {resource.last_verified}"
    if visit.freshness_tier == "call_to_confirm":
        return f"Last checked {resource.last_verified}; call to confirm"
    return "Unconfirmed"


def _travel_echo(constraints: HouseholdConstraints) -> str:
    echo = f"You said: {'/'.join(constraints.travel)}"
    if constraints.max_travel_minutes is not None:
        echo += f", up to {constraints.max_travel_minutes} minutes"
    return echo


def build_claims(visit: PlannedVisit, resource: FoodResource, constraints: HouseholdConstraints, now: datetime) -> Claims:
    """Turn a cleaned visit, its resource, and the resident's constraints into the eight
    permitted claims plus directions and the travel echo. Caller must apply freshness_tier
    and next_open to `visit` first; both are read here, never recomputed."""
    return Claims(
        open_today_text=_open_today_text(visit, resource, now),
        cost_label=_COST_LABELS[resource.cost],
        requirements_text=_requirements_text(resource),
        appointment_text={True: "Appointment required, not booked", "unknown": "Appointment: not stated; call to ask"}.get(resource.appointment_required, ""),
        freshness_text=_freshness_text(visit, resource),
        inventory_text="We can't confirm they have food today.",
        service_area_text="Confirm they serve your area" if not getattr(visit, "service_area_known", True) else "",
        travel_text="Travel time unknown, check the map.",
        directions_url="https://www.google.com/maps/search/?api=1&query=" + quote_plus(resource.address),
        travel_echo=_travel_echo(constraints),
        source_text=f"Source: {resource.source}" if resource.source else "",
    )
