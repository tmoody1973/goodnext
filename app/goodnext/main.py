"""GoodNext resident agent: AgentCore Runtime entrypoint.

Flow (AgentCore Explained, section 3): FastAPI sends a typed request; this
entrypoint runs Strands with the shared system prompt plus the workflow the
request selects, and only that workflow's scoped tools; the matching validator
strips anything the tools did not support; the envelope goes back to FastAPI.

Two workflows share this entrypoint: food_today (P01 + P03, find/check food
tools) and understand_notice (P01 + P02, read_notice / get_policy_evidence /
resolve_help_route). invoke() dispatches on the request's workflow field.
"""

import json
import uuid
from typing import Any

from bedrock_agentcore.runtime import BedrockAgentCoreApp
from pydantic import BaseModel, Field, ValidationError
from strands import Agent

from help_routes import HELP_ROUTES
from model.load import load_model
from prompts import FOOD_PLAN_INSTRUCTION, NOTICE_PLAN_INSTRUCTION, RESIDENT_SYSTEM_PROMPT
from schemas import Envelope, FoodPlanProposal, HouseholdConstraints, NoticePlanProposal
from tools import (
    check_food_constraints,
    find_food_resources,
    get_policy_evidence,
    load_directory,
    load_notices,
    load_official_routes,
    load_policy_evidence,
    read_notice,
    resolve_help_route,
    returned_evidence,
    returned_ids,
)
from validators import validate_food_plan, validate_notice_plan

app = BedrockAgentCoreApp()
log = app.logger


class FoodTodayRequest(BaseModel):
    workflow: str = Field(pattern=r"^food_today$")
    constraints: HouseholdConstraints
    dates: list[str] = Field(min_length=7, max_length=7, description="Seven local calendar dates from the server")
    now_local: str = Field(description="Current Milwaukee local time, ISO datetime with UTC offset, from the server")
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))


class NoticeRequest(BaseModel):
    workflow: str = Field(pattern=r"^understand_notice$")
    notice_ids: list[str] = Field(min_length=1, max_length=10, description="Authorized synthetic notice IDs to read")
    now_local: str = Field(description="Current Milwaukee local time, ISO datetime with UTC offset, from the server")
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))


def build_agent(model=None) -> Agent:
    return Agent(
        model=model or load_model(),
        system_prompt=RESIDENT_SYSTEM_PROMPT + "\n\n" + FOOD_PLAN_INSTRUCTION,
        tools=[find_food_resources, check_food_constraints],
        callback_handler=None,
    )


def build_notice_agent(model=None) -> Agent:
    return Agent(
        model=model or load_model(),
        system_prompt=RESIDENT_SYSTEM_PROMPT + "\n\n" + NOTICE_PLAN_INSTRUCTION,
        tools=[read_notice, get_policy_evidence, resolve_help_route],
        callback_handler=None,
    )


def task_text(req: FoodTodayRequest) -> str:
    # Resident data is delimited and labeled as data, never merged into the system prompt.
    return (
        "<server_context>\n"
        f"seven_local_dates: {json.dumps(req.dates)}\n"
        f"now_local: {req.now_local}\n"
        "language: en\n"
        "</server_context>\n"
        "<resident_constraints>\n"
        f"{req.constraints.model_dump_json(indent=2)}\n"
        "</resident_constraints>\n"
        "Propose the seven-day food access plan. Call find_food_resources first, "
        "then check_food_constraints on the returned IDs. Be brief: at most three "
        "visits per day, explanation under 120 words, no repeated text across days."
    )


def no_match_envelope(request_id: str) -> Envelope:
    """The no-match envelope for the tool-level short-circuit: no model call, no visits."""
    return Envelope(
        status="no_match",
        data=None,
        evidence=[],
        missing=["No feasible resource found; see help route"],
        warnings=[],
        retryable=False,
        request_id=request_id,
        help_routes=HELP_ROUTES,
    )


def envelope_for(proposal: FoodPlanProposal, violations: list[str], request_id: str) -> Envelope:
    visits = [v for d in proposal.days for v in d.visits] + proposal.food_today
    if not visits:
        status = "no_match"
        missing = ["No feasible resource found; see help route"]
    else:
        status, missing = ("partial", []) if violations else ("success", [])
    return Envelope(
        status=status,
        data=proposal.model_dump(),
        evidence=proposal.resource_ids_used,
        missing=missing + proposal.unmet_needs,
        warnings=violations,
        retryable=False,
        request_id=request_id,
        help_routes=HELP_ROUTES,
    )


def run_food_today(req: FoodTodayRequest, model=None) -> Envelope:
    token = returned_ids.set(set())
    try:
        # Tool-level no-match short-circuit (MOO-773): skip the model entirely
        # when the search would come back empty for this ZIP and date range.
        precheck = find_food_resources(req.constraints.zip_code, req.dates[0], req.dates[-1], req.now_local)
        if precheck["status"] == "no_match":
            return no_match_envelope(req.request_id)
        agent = build_agent(model)
        result = agent(task_text(req), structured_output_model=FoodPlanProposal)
        proposal = result.structured_output
        if proposal is None:
            return Envelope(status="temporarily_unavailable", warnings=["model returned no structured output"], retryable=True, request_id=req.request_id)
        cleaned, violations = validate_food_plan(proposal, returned_ids.get(), load_directory(), req.constraints, req.dates, req.now_local)
        return envelope_for(cleaned, violations, req.request_id)
    finally:
        returned_ids.reset(token)


def notice_task_text(req: NoticeRequest) -> str:
    # Notice references are delimited and labeled as data. The notice passages
    # themselves arrive as read_notice tool results, never merged into the prompt.
    return (
        "<server_context>\n"
        f"now_local: {req.now_local}\n"
        "language: en\n"
        "</server_context>\n"
        "<requested_notices>\n"
        f"{json.dumps(req.notice_ids)}\n"
        "</requested_notices>\n"
        "Read each requested notice with read_notice, then call get_policy_evidence for "
        "the identified topic and resolve_help_route for the official route. Return the "
        "NoticePlanProposal. Keep each notice and person separate. Do not infer a missing "
        "date or case status. Be brief; explanation under 120 words."
    )


def needs_clarification_envelope(request_id: str, missing: list[str]) -> Envelope:
    """No official action could be identified without more from the resident (FR03)."""
    return Envelope(
        status="needs_clarification",
        data=None,
        evidence=[],
        missing=missing,
        warnings=[],
        retryable=False,
        request_id=request_id,
        help_routes=HELP_ROUTES,
    )


def envelope_for_notice(proposal: NoticePlanProposal, violations: list[str], request_id: str) -> Envelope:
    if not proposal.actions:
        status = "needs_clarification"
        missing = ["No official action identified in the information provided; confirm the notice or contact the agency"]
    else:
        status, missing = ("partial", []) if violations else ("success", [])
    return Envelope(
        status=status,
        data=proposal.model_dump(),
        evidence=proposal.evidence_ids_used,
        missing=missing + proposal.unresolved,
        warnings=violations,
        retryable=False,
        request_id=request_id,
        help_routes=HELP_ROUTES,
    )


def run_understand_notice(req: NoticeRequest, model=None) -> Envelope:
    token = returned_evidence.set(set())
    try:
        # Skip the model when none of the requested notices exist, mirroring the
        # food-today no-match short-circuit: there is nothing to interpret.
        findings = load_notices()
        if not any(nid in findings for nid in req.notice_ids):
            return needs_clarification_envelope(req.request_id, ["notice not found; confirm the notice you selected"])
        agent = build_notice_agent(model)
        result = agent(notice_task_text(req), structured_output_model=NoticePlanProposal)
        proposal = result.structured_output
        if proposal is None:
            return Envelope(status="temporarily_unavailable", warnings=["model returned no structured output"], retryable=True, request_id=req.request_id)
        cleaned, violations = validate_notice_plan(
            proposal, returned_evidence.get(), findings, load_policy_evidence(), load_official_routes(), req.now_local
        )
        return envelope_for_notice(cleaned, violations, req.request_id)
    finally:
        returned_evidence.reset(token)


def with_help_routes(envelope: Envelope) -> dict:
    """MOO-780: every answer that leaves the agent carries the three reviewed help
    routes (CONTEXT.md "Help route"), whatever its status. One boundary, no copies."""
    return envelope.model_copy(update={"help_routes": HELP_ROUTES}).model_dump()


def _clarification_from(exc: ValidationError, payload: dict) -> Envelope:
    return Envelope(
        status="needs_clarification",
        missing=[e["loc"][-1] if e["loc"] else "?" for e in exc.errors()][:10],
        warnings=["invalid request"],
        request_id=str(payload.get("request_id", "invalid")),
    )


def _invoke_food(payload: dict) -> dict:
    log.info("GoodNext food_today invocation")
    try:
        req = FoodTodayRequest(**payload)
    except ValidationError as exc:
        return with_help_routes(_clarification_from(exc, payload))
    try:
        return with_help_routes(run_food_today(req))
    except Exception as exc:  # noqa: BLE001 - boundary: never leak a stack trace to the caller
        log.exception("food_today failed")
        return with_help_routes(Envelope(status="temporarily_unavailable", warnings=[exc.__class__.__name__], retryable=True, request_id=req.request_id))


def _invoke_notice(payload: dict) -> dict:
    log.info("GoodNext understand_notice invocation")
    try:
        req = NoticeRequest(**payload)
    except ValidationError as exc:
        return with_help_routes(_clarification_from(exc, payload))
    try:
        return with_help_routes(run_understand_notice(req))
    except Exception as exc:  # noqa: BLE001 - boundary: never leak a stack trace to the caller
        log.exception("understand_notice failed")
        return with_help_routes(Envelope(status="temporarily_unavailable", warnings=[exc.__class__.__name__], retryable=True, request_id=req.request_id))


@app.entrypoint
def invoke(payload: Any, context: Any = None) -> dict:
    if not isinstance(payload, dict):
        return with_help_routes(Envelope(status="denied", warnings=["payload must be a JSON object"], request_id="invalid"))
    # Dispatch on the selected workflow. Anything but understand_notice keeps the
    # food-today path, so a missing or unknown workflow still fails food validation.
    if payload.get("workflow") == "understand_notice":
        return _invoke_notice(payload)
    return _invoke_food(payload)


if __name__ == "__main__":
    app.run()
