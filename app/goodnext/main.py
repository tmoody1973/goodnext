"""GoodNext resident agent: AgentCore Runtime entrypoint for the food-today slice.

Flow (AgentCore Explained, section 3): FastAPI sends a typed request; this
entrypoint runs Strands with P01 + P03 and two scoped tools; the validator
strips anything the tools did not support; the envelope goes back to FastAPI.
"""

import json
import uuid
from typing import Any

from bedrock_agentcore.runtime import BedrockAgentCoreApp
from pydantic import BaseModel, Field, ValidationError
from strands import Agent

from help_routes import HELP_ROUTES
from model.load import load_model
from prompts import FOOD_PLAN_INSTRUCTION, RESIDENT_SYSTEM_PROMPT
from schemas import Envelope, FoodPlanProposal, HouseholdConstraints
from tools import check_food_constraints, find_food_resources, load_directory, returned_ids
from validators import validate_food_plan

app = BedrockAgentCoreApp()
log = app.logger


class FoodTodayRequest(BaseModel):
    workflow: str = Field(pattern=r"^food_today$")
    constraints: HouseholdConstraints
    dates: list[str] = Field(min_length=7, max_length=7, description="Seven local calendar dates from the server")
    now_local: str = Field(description="Current Milwaukee local time, ISO datetime with UTC offset, from the server")
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))


def build_agent(model=None) -> Agent:
    return Agent(
        model=model or load_model(),
        system_prompt=RESIDENT_SYSTEM_PROMPT + "\n\n" + FOOD_PLAN_INSTRUCTION,
        tools=[find_food_resources, check_food_constraints],
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
        "then check_food_constraints on the returned IDs."
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
        help_routes=HELP_ROUTES if status == "no_match" else [],
    )


def run_food_today(req: FoodTodayRequest, model=None) -> Envelope:
    token = returned_ids.set(set())
    try:
        # Tool-level no-match short-circuit (MOO-773): skip the model entirely
        # when the search would come back empty for this ZIP and date range.
        precheck = find_food_resources(req.constraints.zip_code, req.dates[0], req.dates[-1])
        if precheck["status"] == "no_match":
            return no_match_envelope(req.request_id)
        agent = build_agent(model)
        result = agent(task_text(req), structured_output_model=FoodPlanProposal)
        proposal = result.structured_output
        if proposal is None:
            return Envelope(status="temporarily_unavailable", warnings=["model returned no structured output"], retryable=True, request_id=req.request_id)
        cleaned, violations = validate_food_plan(proposal, returned_ids.get(), load_directory(), req.constraints, req.dates)
        return envelope_for(cleaned, violations, req.request_id)
    finally:
        returned_ids.reset(token)


@app.entrypoint
def invoke(payload: Any, context: Any = None) -> dict:
    log.info("GoodNext food_today invocation")
    if not isinstance(payload, dict):
        return Envelope(status="denied", warnings=["payload must be a JSON object"], request_id="invalid").model_dump()
    try:
        req = FoodTodayRequest(**payload)
    except ValidationError as exc:
        return Envelope(status="needs_clarification", missing=[e["loc"][-1] if e["loc"] else "?" for e in exc.errors()][:10], warnings=["invalid request"], request_id=str(payload.get("request_id", "invalid"))).model_dump()
    try:
        return run_food_today(req).model_dump()
    except Exception as exc:  # noqa: BLE001 - boundary: never leak a stack trace to the caller
        log.exception("food_today failed")
        return Envelope(status="temporarily_unavailable", warnings=[exc.__class__.__name__], retryable=True, request_id=req.request_id).model_dump()


if __name__ == "__main__":
    app.run()
