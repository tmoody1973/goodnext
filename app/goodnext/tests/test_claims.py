"""MOO-775: every option carries the permitted claims and nothing from the never-list."""

import sys
from pathlib import Path
from urllib.parse import quote_plus

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from claims import never_list_hits
from main import FoodTodayRequest, envelope_for, run_food_today
from schemas import Envelope, HouseholdConstraints
from tools import find_food_resources, load_directory, returned_ids
from validators import validate_food_plan

import pytest

DATES = [f"2026-09-{d:02d}" for d in range(8, 15)]
MORNING = "2026-09-08T09:00:00-05:00"
ZERO_BUDGET_BUS = HouseholdConstraints(zip_code="53206", budget_usd=0, kitchen="none", travel=["bus"])


@pytest.fixture(autouse=True)
def fresh_ledger():
    token = returned_ids.set(set())
    yield
    returned_ids.reset(token)


def visit(rid: str, date: str, cost: str = "free"):
    from schemas import PlannedVisit

    r = load_directory()[rid]
    return PlannedVisit(
        resource_id=rid, provider=r.provider, date=date, service_type=r.service_type, cost=cost,
        schedule_text="see record", last_verified=r.last_verified, contact=r.contact,
    )


def proposal_with(visits, dates=DATES):
    from schemas import DayPlan, FoodPlanProposal

    days = [DayPlan(date=d, visits=[v for v in visits if v.date == d]) for d in dates]
    return FoodPlanProposal(start_date=dates[0], days=days, food_today=[v for v in visits if v.date == dates[0]], explanation="test")


def test_validator_populates_permitted_claims_for_every_kept_visit():
    find_food_resources("53206", DATES[0], DATES[-1], MORNING)
    proposal = proposal_with([visit("res-001", DATES[0]), visit("res-002", DATES[0])])
    directory = load_directory()

    cleaned, violations = validate_food_plan(proposal, returned_ids.get(), directory, ZERO_BUDGET_BUS, DATES, MORNING)

    kept = cleaned.days[0].visits
    assert violations == []
    assert {v.resource_id for v in kept} == {"res-001", "res-002"}
    for v in kept:
        resource = directory[v.resource_id]
        assert v.claims is not None
        assert v.claims.inventory_text == "We can't confirm they have food today."
        assert v.claims.travel_text == "Travel time unknown, check the map."
        assert v.claims.cost_label == "Free"
        assert v.claims.freshness_text.startswith("Last checked")
        assert quote_plus(resource.address) in v.claims.directions_url
        assert v.claims.travel_echo == "You said: bus"


def test_never_list_hits_empty_over_success_and_no_match_envelopes(fixture_without_res009):
    find_food_resources("53206", DATES[0], DATES[-1], MORNING)
    proposal = proposal_with([visit("res-001", DATES[0]), visit("res-002", DATES[0])])
    cleaned, violations = validate_food_plan(proposal, returned_ids.get(), load_directory(), ZERO_BUDGET_BUS, DATES, MORNING)
    success = envelope_for(cleaned, violations, "r1")
    assert never_list_hits(success.model_dump()) == []

    req = FoodTodayRequest(
        workflow="food_today",
        constraints=HouseholdConstraints(zip_code="53999", budget_usd=0, kitchen="none", travel=["bus"]),
        dates=DATES,
        now_local=MORNING,
    )
    no_match = run_food_today(req)
    assert no_match.status == "no_match"
    assert never_list_hits(no_match.model_dump()) == []


def test_envelope_schema_has_no_forbidden_travel_fields():
    forbidden = {"distance", "duration", "minutes", "miles", "fare"}
    schema = Envelope.model_json_schema()

    def walk(node) -> set[str]:
        found: set[str] = set()
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "properties" and isinstance(value, dict):
                    found |= forbidden & value.keys()
                found |= walk(value)
        elif isinstance(node, list):
            for item in node:
                found |= walk(item)
        return found

    assert walk(schema) == set()


def test_real_map_records_are_listed_with_source_and_call_to_confirm():
    """MOO-777 / decision 006: real Milwaukee Food Environment Map records are listed for
    53206 with a parsed window, tier call_to_confirm, and a source line on every claim."""
    now = "2026-09-09T09:00:00-05:00"
    dates = [f"2026-09-{d:02d}" for d in range(9, 16)]
    result = find_food_resources("53206", dates[0], dates[-1], now)
    real = [r for r in result["data"] if r["resource_id"].startswith("mfc-")]
    assert real, "expected at least one real map record for 53206"
    assert all(r["freshness_tier"] == "call_to_confirm" for r in real)
    assert all(r["source"].startswith("Milwaukee Food Environment Map") for r in real)
    open_now = next(r for r in real if r["open_today"])
    v = visit(open_now["resource_id"], dates[0])
    cleaned, violations = validate_food_plan(proposal_with([v], dates=dates), returned_ids.get(), load_directory(), ZERO_BUDGET_BUS, dates, now)
    kept = cleaned.days[0].visits
    assert kept and kept[0].claims.source_text.startswith("Source: Milwaukee Food Environment Map")
    assert kept[0].claims.freshness_text == "Last checked 2024-08-27; call to confirm"
    assert never_list_hits(envelope_for(cleaned, violations, "r1").model_dump()) == []


def test_reviewed_directory_records_are_verified_and_honest_about_unknowns():
    """Reviewed directory (checked against official pages 2026-09-08): Thursday Sep 10 in 53206
    lists the Salvation Army Citadel pantry as verified, with cost unknown kept as a caveat,
    and a serves-everyone meal site is listed without a service-area caveat."""
    now = "2026-09-10T09:00:00-05:00"
    dates = [f"2026-09-{d:02d}" for d in range(10, 17)]
    result = find_food_resources("53206", dates[0], dates[-1], now)
    by_id = {r["resource_id"]: r for r in result["data"]}
    citadel = by_id["mke-salvation-army-citadel-food-pantry"]
    assert citadel["freshness_tier"] == "verified" and citadel["open_today"] is True
    assert citadel["service_area_known"] is True and citadel["cost"] == "unknown"
    meal = next(r for r in result["data"] if r.get("serves_all_milwaukee"))
    assert meal["service_area_known"] is True
    directory = load_directory()
    assert sum(1 for r in directory.values() if "Bay View Community Center" in r.provider) == 1, "map duplicate must yield to the reviewed record"
    v = visit(citadel["resource_id"], dates[0])
    cleaned, violations = validate_food_plan(proposal_with([v], dates=dates), returned_ids.get(), directory, ZERO_BUDGET_BUS, dates, now)
    kept = cleaned.days[0].visits
    assert kept, f"unknown cost must not be stripped at zero budget: {violations}"
    assert kept[0].claims.cost_label == "Cost not stated; ask"
    assert kept[0].claims.appointment_text == "Appointment: not stated; call to ask"
    assert any("Cost not stated" in u for u in kept[0].uncertainty)
    assert kept[0].claims.freshness_text == "Last checked 2026-09-08"
    assert never_list_hits(envelope_for(cleaned, violations, "r1").model_dump()) == []


def test_never_list_matches_whole_words_only():
    assert never_list_hits({"status": "temporarily_unavailable"}) == []
    assert never_list_hits({"t": "Food is available now"}) == ["available"]
