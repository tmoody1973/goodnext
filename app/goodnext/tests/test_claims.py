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
