"""The eight permitted resident-facing claims, and nothing else, per visit.

docs/specs/food-today.md D9: the eight allowed statements are rendered from
record fields, never free text from the model. Claims 6 (inventory_text) and
8 (travel_text) are always present verbatim. NEVER_LIST is the single
reviewed constant a test scans every resident-facing response against.
Pure; no I/O.
"""

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

_COST_LABELS = {"free": "Free", "paid": "Paid", "sliding": "Sliding scale"}


def never_list_hits(obj: object) -> list[str]:
    """Walk any JSON-like structure's string values, case-insensitively, for never-list terms."""
    hits: list[str] = []

    def walk(node: object) -> None:
        if isinstance(node, str):
            low = node.lower()
            hits.extend(term for term in NEVER_LIST if term in low)
        elif isinstance(node, dict):
            for value in node.values():
                walk(value)
        elif isinstance(node, (list, tuple)):
            for value in node:
                walk(value)

    walk(obj)
    return hits


def _fmt_12h(hhmm: str) -> str:
    hour_str, minute = hhmm.split(":")
    hour = int(hour_str)
    period = "AM" if hour < 12 else "PM"
    hour12 = hour % 12 or 12
    return f"{hour12}:{minute} {period}"


def _open_today_text(visit: PlannedVisit, resource: FoodResource, now: datetime) -> str:
    today = now.date().isoformat()
    if visit.date == today:
        window = next((w for w in resource.windows if w.date == today), None)
        if window is not None:
            return f"Open today from {_fmt_12h(window.open)} to {_fmt_12h(window.close)}"
    if visit.next_open is not None:
        return f"Not open today; next open {visit.next_open.date} at {_fmt_12h(visit.next_open.open)}"
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
        appointment_text="Appointment required, not booked" if resource.appointment_required else "",
        freshness_text=_freshness_text(visit, resource),
        inventory_text="We can't confirm they have food today.",
        service_area_text="Confirm they serve your area" if not getattr(visit, "service_area_known", True) else "",
        travel_text="Travel time unknown, check the map.",
        directions_url="https://www.google.com/maps/search/?api=1&query=" + quote_plus(resource.address),
        travel_echo=_travel_echo(constraints),
        source_text=f"Source: {resource.source}" if resource.source else "",
    )
