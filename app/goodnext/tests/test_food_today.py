"""Offline checks for the food-today slice. No Bedrock or AgentCore needed."""

import json
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

import main
import tools
from help_routes import HELP_ROUTES
from main import FoodTodayRequest, envelope_for, invoke, run_food_today, task_text
from schemas import DayPlan, FoodPlanProposal, FoodResource, HouseholdConstraints, PlannedVisit, ServiceWindow
from tools import check_food_constraints, find_food_resources, freshness_tier, load_directory, returned_ids
from validators import validate_food_plan

DATES = [f"2026-09-{d:02d}" for d in range(8, 15)]
NOW_LOCAL = "2026-09-08T10:00:00-05:00"
ZERO_BUDGET_NO_KITCHEN = HouseholdConstraints(zip_code="53206", budget_usd=0, kitchen="none", travel=["bus"])


@pytest.fixture(autouse=True)
def fresh_ledger():
    token = returned_ids.set(set())
    yield
    returned_ids.reset(token)


def visit(rid: str, date: str, cost: str = "free") -> PlannedVisit:
    r = load_directory().get(rid)
    return PlannedVisit(
        resource_id=rid, provider=r.provider if r else "Invented", date=date,
        service_type=r.service_type if r else "free_pantry", cost=cost,
        schedule_text="see record", last_verified=r.last_verified if r else "2026-09-01", contact="x",
    )


def proposal_with(visits: list[PlannedVisit], dates=DATES) -> FoodPlanProposal:
    days = [DayPlan(date=d, visits=[v for v in visits if v.date == d]) for d in dates]
    return FoodPlanProposal(start_date=dates[0], days=days, food_today=[v for v in visits if v.date == dates[0]], explanation="test")


def small_resource(rid: str, last_verified: str | None, dates=DATES) -> FoodResource:
    """A minimal synthetic FoodResource for freshness-tier tests, no fixture edits needed."""
    return FoodResource(
        resource_id=rid, provider="Freshness Test Pantry (synthetic)", service_type="free_pantry", cost="free",
        address="1 Test St, Milwaukee, WI 53206", zip_codes_served=["53206"],
        windows=[ServiceWindow(date=d, open="10:00", close="12:00") for d in dates],
        contact="(414) 555-0199", last_verified=last_verified, verifier="demo-reviewer",
        status="published", source_url="https://example.invalid/freshnesstest", notes="synthetic test record",
    )


def test_find_excludes_closed_and_out_of_area():
    result = find_food_resources("53206", DATES[0], DATES[-1], NOW_LOCAL)
    ids = {r["resource_id"] for r in result["data"]}
    assert result["status"] == "success"
    assert "res-005" not in ids, "closed resource must not be returned"
    assert "res-006" not in ids, "out-of-area resource must not be returned"
    assert {"res-001", "res-002", "res-003", "res-004"} <= ids
    assert "quantity_per_visit unknown for every record" in result["missing"]
    assert any("res-004" in w for w in result["warnings"]), "stale verification should warn"


def test_find_no_match_for_unserved_zip(fixture_without_res009):
    result = find_food_resources("53999", DATES[0], DATES[-1], NOW_LOCAL)
    assert result["status"] == "no_match" and result["data"] == []


def test_zero_budget_marks_paid_unsuitable():
    find_food_resources("53206", DATES[0], DATES[-1], NOW_LOCAL)
    result = check_food_constraints(["res-003", "res-001"], 0.0, "none", ["bus"])
    verdicts = {r["resource_id"]: r for r in result["data"]}
    assert verdicts["res-003"]["verdict"] == "unsuitable"
    assert verdicts["res-001"]["verdict"] == "conditional"
    assert any("no-cook" in reason for reason in verdicts["res-001"]["reasons"])


def test_constraint_check_rejects_unreturned_id():
    result = check_food_constraints(["res-001"], 0.0, "full", ["bus"])
    assert result["data"][0]["verdict"] == "unsuitable"


def test_validator_strips_fabricated_id():
    find_food_resources("53206", DATES[0], DATES[-1], NOW_LOCAL)
    proposal = proposal_with([visit("res-001", DATES[0]), visit("res-999", DATES[0])])
    cleaned, violations = validate_food_plan(proposal, returned_ids.get(), load_directory(), ZERO_BUDGET_NO_KITCHEN, DATES, NOW_LOCAL)
    assert [v.resource_id for v in cleaned.days[0].visits] == ["res-001"]
    assert any("res-999" in v for v in violations)


def test_validator_strips_paid_visit_in_zero_budget_plan():
    find_food_resources("53206", DATES[0], DATES[-1], NOW_LOCAL)
    proposal = proposal_with([visit("res-003", DATES[1], cost="paid")])
    cleaned, violations = validate_food_plan(proposal, returned_ids.get(), load_directory(), ZERO_BUDGET_NO_KITCHEN, DATES, NOW_LOCAL)
    assert cleaned.days[1].visits == [] and any("zero-budget" in v for v in violations)


def test_validator_strips_visit_on_a_day_with_no_window():
    find_food_resources("53206", DATES[0], DATES[-1], NOW_LOCAL)
    proposal = proposal_with([visit("res-001", DATES[1])])  # res-001 is not open on 09-09
    cleaned, violations = validate_food_plan(proposal, returned_ids.get(), load_directory(), ZERO_BUDGET_NO_KITCHEN, DATES, NOW_LOCAL)
    assert cleaned.days[1].visits == [] and any("no opening window" in v for v in violations)


def test_validator_rebuilds_seven_dates_and_flags_stale():
    find_food_resources("53206", DATES[0], DATES[-1], NOW_LOCAL)
    short = proposal_with([visit("res-004", "2026-09-11")], dates=DATES[:4])
    cleaned, violations = validate_food_plan(short, returned_ids.get(), load_directory(), ZERO_BUDGET_NO_KITCHEN, DATES, NOW_LOCAL)
    assert [d.date for d in cleaned.days] == DATES
    assert any("seven server dates" in v for v in violations)
    stale_visit = cleaned.days[3].visits[0]
    assert any("call to confirm" in u for u in stale_visit.uncertainty)


def test_envelope_status_rules():
    find_food_resources("53206", DATES[0], DATES[-1], NOW_LOCAL)
    ok = proposal_with([visit("res-001", DATES[0])])
    success = envelope_for(ok, [], "r1")
    assert success.status == "success" and success.help_routes == []
    assert envelope_for(ok, ["something stripped"], "r1").status == "partial"
    no_match = envelope_for(proposal_with([]), [], "r1")
    assert no_match.status == "no_match"
    assert no_match.help_routes == HELP_ROUTES and len(no_match.help_routes) == 3


def test_run_food_today_no_match_short_circuits_without_calling_model(monkeypatch, fixture_without_res009):
    def refuse_to_build(model=None):
        raise AssertionError("build_agent must not be called on a no-match ZIP")

    monkeypatch.setattr(main, "build_agent", refuse_to_build)
    req = FoodTodayRequest(
        workflow="food_today",
        constraints=HouseholdConstraints(zip_code="53999", budget_usd=0, kitchen="none", travel=["bus"]),
        dates=DATES,
        now_local=NOW_LOCAL,
    )
    envelope = run_food_today(req)
    assert envelope.status == "no_match"
    assert envelope.evidence == []
    assert envelope.data is None
    assert envelope.help_routes == HELP_ROUTES
    assert [r.name for r in envelope.help_routes] == [
        "2-1-1",
        "Hunger Task Force emergency food",
        "FoodShare member line",
    ]


def test_invoke_rejects_bad_payloads_without_calling_model():
    assert invoke("not a dict")["status"] == "denied"
    bad = invoke({"workflow": "food_today", "constraints": {"zip_code": "abc", "budget_usd": 0}, "dates": DATES, "now_local": NOW_LOCAL})
    assert bad["status"] == "needs_clarification" and "zip_code" in bad["missing"]


def test_invoke_needs_clarification_when_now_local_missing():
    payload = {"workflow": "food_today", "constraints": ZERO_BUDGET_NO_KITCHEN.model_dump(), "dates": DATES}
    result = invoke(payload)
    assert result["status"] == "needs_clarification" and "now_local" in result["missing"]


def test_task_text_keeps_resident_data_out_of_system_prompt():
    req = FoodTodayRequest(workflow="food_today", constraints=ZERO_BUDGET_NO_KITCHEN, dates=DATES, now_local=NOW_LOCAL)
    text = task_text(req)
    assert "<resident_constraints>" in text and "53206" in text
    assert f"now_local: {NOW_LOCAL}" in text


@pytest.mark.parametrize(
    "days_ago,expected_tier",
    [(0, "verified"), (14, "verified"), (15, "call_to_confirm"), (60, "call_to_confirm"), (61, "call_to_confirm"), (400, "call_to_confirm")],
)
def test_freshness_tier_thresholds(days_ago, expected_tier):
    last_verified = (date.fromisoformat(DATES[0]) - timedelta(days=days_ago)).isoformat()
    resource = small_resource("res-fresh", last_verified)
    assert freshness_tier(resource.last_verified, DATES[0]) == expected_tier


def test_freshness_tier_missing_date_is_unconfirmed():
    resource = small_resource("res-fresh", None)
    assert freshness_tier(resource.last_verified, DATES[0]) == "unconfirmed"


def test_find_call_to_confirm_warning_names_check_date():
    result = find_food_resources("53206", DATES[0], DATES[-1], NOW_LOCAL)
    assert any("res-004" in w and "2026-08-20" in w for w in result["warnings"])


def test_validator_strips_unconfirmed_visit_from_food_today_and_lists_it():
    resource = small_resource("res-900", None, dates=[DATES[0]])
    directory = {resource.resource_id: resource}
    ledger = {resource.resource_id}
    v = visit(resource.resource_id, DATES[0])
    v = v.model_copy(update={"provider": resource.provider, "contact": resource.contact})
    proposal = proposal_with([v])

    cleaned, violations = validate_food_plan(proposal, ledger, directory, ZERO_BUDGET_NO_KITCHEN, DATES, NOW_LOCAL)

    assert cleaned.food_today == []
    assert cleaned.days[0].visits == []
    assert any("unconfirmed" in w for w in violations)
    assert [u.resource_id for u in cleaned.unconfirmed] == ["res-900"]
    assert cleaned.unconfirmed[0].contact == resource.contact


# --- MOO-774: closed-earlier-today windows are not Food today; next open carried ---

AFTERNOON = "2026-09-08T15:00:00-05:00"
MORNING = "2026-09-08T09:00:00-05:00"


def test_find_marks_closed_earlier_today_resource_not_open_today_with_next_open():
    result = find_food_resources("53206", DATES[0], DATES[-1], AFTERNOON)
    by_id = {r["resource_id"]: r for r in result["data"]}
    assert by_id["res-001"]["open_today"] is False
    assert by_id["res-001"]["next_open"] == {"date": "2026-09-10", "open": "10:00", "close": "14:00"}
    assert by_id["res-002"]["open_today"] is True


def test_find_marks_both_open_today_in_the_morning():
    result = find_food_resources("53206", DATES[0], DATES[-1], MORNING)
    by_id = {r["resource_id"]: r for r in result["data"]}
    assert by_id["res-001"]["open_today"] is True
    assert by_id["res-002"]["open_today"] is True


def test_validator_strips_day_one_visit_closed_before_request_time():
    find_food_resources("53206", DATES[0], DATES[-1], AFTERNOON)
    proposal = proposal_with([visit("res-001", DATES[0])])

    cleaned, violations = validate_food_plan(
        proposal, returned_ids.get(), load_directory(), ZERO_BUDGET_NO_KITCHEN, DATES, AFTERNOON
    )

    assert cleaned.food_today == [] and cleaned.days[0].visits == []
    assert any("res-001" in v and "closed before request time" in v for v in violations)


def test_food_today_derived_from_surviving_day_one_visits_not_models_list():
    find_food_resources("53206", DATES[0], DATES[-1], NOW_LOCAL)
    day_one_visit = visit("res-001", DATES[0])
    proposal = proposal_with([day_one_visit]).model_copy(update={"food_today": []})  # model omitted it

    cleaned, violations = validate_food_plan(
        proposal, returned_ids.get(), load_directory(), ZERO_BUDGET_NO_KITCHEN, DATES, NOW_LOCAL
    )

    assert [v.resource_id for v in cleaned.food_today] == ["res-001"]
    assert cleaned.food_today == cleaned.days[0].visits


# --- MOO-772: unknown service area shown as conditional, never confirmed ---


def test_find_returns_unknown_service_area_record_for_its_own_address_zip():
    """Decision 006 refinement of D5: an unknown-area record is visible only for the
    ZIP in its own address, still conditional. (Real map data has 54 such records;
    'any ZIP' returned the whole county for every search.)"""
    result = find_food_resources("53206", DATES[0], DATES[-1], NOW_LOCAL)
    by_id = {r["resource_id"]: r for r in result["data"]}
    assert "res-009" in by_id
    assert by_id["res-009"]["service_area_known"] is False
    assert any("res-009" in w and "service area unknown; confirm they serve your area" in w for w in result["warnings"])


def test_find_hides_unknown_service_area_record_for_other_zips(fixture_without_res009):
    result = find_food_resources("53999", DATES[0], DATES[-1], NOW_LOCAL)
    assert result["status"] == "no_match"


def test_find_known_service_area_record_keeps_service_area_known_true():
    result = find_food_resources("53206", DATES[0], DATES[-1], NOW_LOCAL)
    by_id = {r["resource_id"]: r for r in result["data"]}
    assert by_id["res-001"]["service_area_known"] is True


def test_find_still_excludes_out_of_area_resource_for_wrong_zip():
    result = find_food_resources("53206", DATES[0], DATES[-1], NOW_LOCAL)
    ids = {r["resource_id"] for r in result["data"]}
    assert "res-006" not in ids, "res-006 serves only 53225; must stay excluded for 53206"


def test_check_food_constraints_reports_unknown_area_as_conditional_never_supported():
    find_food_resources("53206", DATES[0], DATES[-1], NOW_LOCAL)
    result = check_food_constraints(["res-009"], 0.0, "full", ["bus"])
    verdict = result["data"][0]
    assert verdict["verdict"] == "conditional"
    assert "confirm they serve your area" in verdict["reasons"]


def test_validator_keeps_unknown_area_visit_with_confirm_uncertainty():
    find_food_resources("53206", DATES[0], DATES[-1], NOW_LOCAL)
    proposal = proposal_with([visit("res-009", DATES[0])])
    cleaned, violations = validate_food_plan(proposal, returned_ids.get(), load_directory(), ZERO_BUDGET_NO_KITCHEN, DATES, NOW_LOCAL)
    kept = cleaned.days[0].visits
    assert [v.resource_id for v in kept] == ["res-009"]
    assert kept[0].service_area_known is False
    assert "Confirm they serve your area" in kept[0].uncertainty
