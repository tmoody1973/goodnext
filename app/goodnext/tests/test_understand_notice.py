"""Offline checks for the understand-notice slice. No Bedrock or AgentCore needed."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

import main
from claims import notice_never_list_hits
from help_routes import HELP_ROUTES
from main import NoticeRequest, envelope_for_notice, invoke, notice_task_text, run_understand_notice
from schemas import NoticeAction, NoticePlanProposal
from tools import (
    get_policy_evidence,
    load_notices,
    load_official_routes,
    load_policy_evidence,
    read_notice,
    resolve_help_route,
    returned_evidence,
)
from validators import validate_notice_plan

# 2026-09-10: proof-of-address deadline (09-01) is passed; SMRF (09-20) and proof (09-15) are upcoming.
NOW_LOCAL = "2026-09-10T09:00:00-05:00"


@pytest.fixture(autouse=True)
def fresh_evidence_ledger():
    token = returned_evidence.set(set())
    yield
    returned_evidence.reset(token)


def action(action_id, notice_id, evidence_ids=("pol-smrf-001",), route_id="route-smrf", instruction="Return the six-month report form"):
    return NoticeAction(
        action_id=action_id,
        notice_id=notice_id,
        instruction=instruction,
        evidence_ids=list(evidence_ids),
        route_id=route_id,
    )


def proposal_with(actions, explanation="Here is your next step, with its source.", checklist=None):
    return NoticePlanProposal(
        actions=list(actions),
        next_step=actions[0].action_id if actions else "",
        checklist=checklist or ["Complete the form", "Call the number on your notice if unsure"],
        explanation=explanation,
    )


def ledger_from_tools(notice_ids=("ntc-smrf-001",), topics=("six_month_report",)):
    """Populate the request-scoped ledger by calling the tools, as the model would."""
    for nid in notice_ids:
        read_notice(nid)
    for topic in topics:
        get_policy_evidence(topic)
        resolve_help_route(topic)
    return returned_evidence.get()


# --- Tools ---


def test_read_notice_returns_finding_and_records_it():
    result = read_notice("ntc-smrf-001")
    assert result["status"] == "success"
    assert result["data"]["parsed_deadline"] == "2026-09-20"
    assert result["evidence"] == ["ntc-smrf-001"]
    assert "ntc-smrf-001" in returned_evidence.get()


def test_read_notice_unknown_id_is_no_match_and_records_nothing():
    result = read_notice("ntc-nope-999")
    assert result["status"] == "no_match" and result["data"] is None
    assert returned_evidence.get() == set()


def test_read_notice_flags_missing_dates_and_pages():
    no_date = read_notice("ntc-nodate-001")
    assert any("no clear deadline date" in m for m in no_date["missing"])
    proof = read_notice("ntc-proof-001")
    assert any("pages [3]" in w for w in proof["warnings"])


def test_get_policy_evidence_matches_topic_only():
    result = get_policy_evidence("work_requirement")
    assert result["status"] == "success"
    assert [e["evidence_id"] for e in result["data"]] == ["pol-work-001"]
    assert get_policy_evidence("no_such_topic")["status"] == "no_match"


def test_resolve_help_route_returns_route_for_topic():
    result = resolve_help_route("proof_request")
    assert result["status"] == "success"
    assert result["data"][0]["route_id"] == "route-proof"
    assert resolve_help_route("no_such_topic")["status"] == "no_match"


# --- Validator ---


def test_validator_keeps_cited_action_and_derives_deadline_from_finding():
    ledger = ledger_from_tools()
    proposal = proposal_with([action("act-1", "ntc-smrf-001")])
    cleaned, violations = validate_notice_plan(
        proposal, ledger, load_notices(), load_policy_evidence(), load_official_routes(), NOW_LOCAL
    )
    assert violations == []
    kept = cleaned.actions[0]
    assert kept.deadline_text == "Return by September 20, 2026"  # verbatim from the finding
    assert kept.deadline_status == "upcoming"
    assert kept.person_ref == "Household member A (synthetic)"
    assert cleaned.supported_dates == ["Return by September 20, 2026"]
    assert cleaned.evidence_ids_used == ["pol-smrf-001"] and cleaned.route_ids_used == ["route-smrf"]


def test_validator_strips_action_citing_notice_not_returned_by_tool():
    # The action names a real fixture notice, but no tool returned it this request.
    ledger = ledger_from_tools(notice_ids=(), topics=())
    proposal = proposal_with([action("act-1", "ntc-smrf-001")])
    cleaned, violations = validate_notice_plan(
        proposal, ledger, load_notices(), load_policy_evidence(), load_official_routes(), NOW_LOCAL
    )
    assert cleaned.actions == []
    assert any("not returned by read_notice" in v for v in violations)


def test_validator_strips_action_citing_unreturned_policy_or_route():
    ledger = ledger_from_tools(notice_ids=("ntc-smrf-001",), topics=())  # notice only, no policy/route
    proposal = proposal_with([action("act-1", "ntc-smrf-001", evidence_ids=("pol-smrf-001",))])
    cleaned, violations = validate_notice_plan(
        proposal, ledger, load_notices(), load_policy_evidence(), load_official_routes(), NOW_LOCAL
    )
    assert cleaned.actions == []
    assert any("not returned by get_policy_evidence" in v for v in violations)


def test_validator_strips_action_with_prohibited_claim():
    ledger = ledger_from_tools()
    bad = action("act-1", "ntc-smrf-001", instruction="Good news: you are eligible and your benefits will continue.")
    cleaned, violations = validate_notice_plan(
        proposal_with([bad]), ledger, load_notices(), load_policy_evidence(), load_official_routes(), NOW_LOCAL
    )
    assert cleaned.actions == []
    assert any("prohibited notice claim" in v for v in violations)


def test_validator_does_not_infer_a_missing_date():
    ledger = ledger_from_tools(notice_ids=("ntc-nodate-001",))
    a = action("act-1", "ntc-nodate-001", instruction="Complete the six-month report form")
    cleaned, violations = validate_notice_plan(
        proposal_with([a]), ledger, load_notices(), load_policy_evidence(), load_official_routes(), NOW_LOCAL
    )
    kept = cleaned.actions[0]
    assert kept.deadline_status == "unknown"
    assert kept.deadline_text == "Return the form promptly"  # the notice's own words, no invented date
    assert "Confirm the deadline date with the agency" in kept.confirm_fields
    assert cleaned.supported_dates == []


def test_validator_retains_a_passed_deadline_with_an_urgent_step():
    ledger = ledger_from_tools(notice_ids=("ntc-passed-001",), topics=("proof_request",))
    a = action("act-1", "ntc-passed-001", evidence_ids=("pol-proof-001",), route_id="route-proof", instruction="Send proof of address")
    cleaned, _ = validate_notice_plan(
        proposal_with([a]), ledger, load_notices(), load_policy_evidence(), load_official_routes(), NOW_LOCAL
    )
    kept = cleaned.actions[0]
    assert kept.deadline_status == "passed"
    assert kept.deadline_text == "Send by September 1, 2026"
    assert any("call the agency" in u.lower() for u in kept.unknowns)


def test_validator_strips_prohibited_claim_from_checklist_and_explanation():
    ledger = ledger_from_tools()
    proposal = proposal_with(
        [action("act-1", "ntc-smrf-001")],
        explanation="Your case is closed, so nothing else is needed.",
        checklist=["Complete the form", "You are exempt from the work requirement"],
    )
    cleaned, violations = validate_notice_plan(
        proposal, ledger, load_notices(), load_policy_evidence(), load_official_routes(), NOW_LOCAL
    )
    assert cleaned.checklist == ["Complete the form"]
    assert "your case is closed" not in cleaned.explanation.lower()
    assert sum("stripped" in v for v in violations) == 2
    assert notice_never_list_hits(cleaned.model_dump()) == []


# --- Envelope ---


def test_envelope_status_rules_for_notice():
    ledger = ledger_from_tools()
    ok, _ = validate_notice_plan(
        proposal_with([action("act-1", "ntc-smrf-001")]), ledger, load_notices(), load_policy_evidence(), load_official_routes(), NOW_LOCAL
    )
    success = envelope_for_notice(ok, [], "r1")
    assert success.status == "success" and success.help_routes == HELP_ROUTES
    partial = envelope_for_notice(ok, ["something stripped"], "r1")
    assert partial.status == "partial"
    empty = envelope_for_notice(proposal_with([]).model_copy(update={"actions": []}), [], "r1")
    assert empty.status == "needs_clarification" and len(empty.help_routes) == 3


# --- Entrypoint wiring ---


def test_run_understand_notice_not_found_short_circuits_without_model(monkeypatch):
    def refuse(model=None):
        raise AssertionError("build_notice_agent must not be called when no notice is found")

    monkeypatch.setattr(main, "build_notice_agent", refuse)
    req = NoticeRequest(workflow="understand_notice", notice_ids=["ntc-nope-999"], now_local=NOW_LOCAL)
    envelope = run_understand_notice(req)
    assert envelope.status == "needs_clarification"
    assert envelope.data is None and envelope.help_routes == HELP_ROUTES


def test_run_understand_notice_end_to_end_with_a_fake_model(monkeypatch):
    class FakeResult:
        def __init__(self, proposal):
            self.structured_output = proposal

    class FakeNoticeAgent:
        def __call__(self, task_text, structured_output_model=None):
            ledger_from_tools()  # the model's tool calls populate the request ledger
            return FakeResult(proposal_with([action("act-1", "ntc-smrf-001")]))

    monkeypatch.setattr(main, "build_notice_agent", lambda model=None: FakeNoticeAgent())
    req = NoticeRequest(workflow="understand_notice", notice_ids=["ntc-smrf-001"], now_local=NOW_LOCAL)
    envelope = run_understand_notice(req)
    assert envelope.status == "success"
    assert envelope.evidence == ["pol-smrf-001"]
    assert envelope.data["actions"][0]["deadline_text"] == "Return by September 20, 2026"
    assert notice_never_list_hits(envelope.model_dump()) == []


def test_invoke_dispatches_understand_notice_and_needs_clarification_on_bad_payload():
    result = invoke({"workflow": "understand_notice"})
    assert result["status"] == "needs_clarification" and "notice_ids" in result["missing"]
    assert [r["name"] for r in result["help_routes"]] == [r.name for r in HELP_ROUTES]


def test_invoke_notice_not_found_is_needs_clarification():
    result = invoke({"workflow": "understand_notice", "notice_ids": ["ntc-nope-999"], "now_local": NOW_LOCAL})
    assert result["status"] == "needs_clarification"
    assert any("notice not found" in m for m in result["missing"])


def test_notice_task_text_keeps_notice_data_delimited_and_carries_now_local():
    req = NoticeRequest(workflow="understand_notice", notice_ids=["ntc-smrf-001", "ntc-proof-001"], now_local=NOW_LOCAL)
    text = notice_task_text(req)
    assert "<requested_notices>" in text and "ntc-smrf-001" in text
    assert f"now_local: {NOW_LOCAL}" in text
    # The notice passages themselves are never inlined; they arrive as tool results.
    assert "keep your FoodShare benefits" not in text


def test_notice_never_list_catches_claims_but_ignores_honest_denials():
    assert notice_never_list_hits({"t": "You are eligible for FoodShare."}) == ["you are eligible"]
    assert notice_never_list_hits({"t": "We cannot say whether you are eligible."}) == []
    assert notice_never_list_hits({"t": "This service does not decide whether your case is closed."}) == []
