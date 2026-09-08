"""GoodNext application API. Food planning needs no account, no notice, no benefits questions."""

import hashlib
import logging
import os
import uuid
from datetime import date, datetime, timedelta
from typing import Literal
from zoneinfo import ZoneInfo

import httpx
from fastapi import Depends, FastAPI, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from goodnext_api.agent_client import AgentClient, default_agent_client

LOCAL_TZ = ZoneInfo("America/Chicago")
SESSION_COOKIE = "gn_session"
DEV = os.environ.get("GOODNEXT_ENV", "dev") == "dev"
log = logging.getLogger(__name__)

app = FastAPI(title="GoodNext API", version="0.1.0", docs_url="/api/docs", openapi_url="/api/openapi.json")


# Mirrors app/goodnext/schemas.py HouseholdConstraints. Validate at this trust
# boundary too; the agent validates again. Keep the two in step by hand for now.
class HouseholdConstraints(BaseModel):
    zip_code: str = Field(pattern=r"^\d{5}$")
    household_size: Literal["1", "2-3", "4-5", "6+"] = "1"
    budget_usd: float = Field(ge=0)
    travel: list[Literal["walk", "bus", "car", "ride"]] = ["walk"]
    max_travel_minutes: int | None = Field(default=None, ge=0)
    kitchen: Literal["full", "microwave_only", "none"] = "full"
    refrigeration: bool = True
    food_on_hand: list[str] = Field(default=[], max_length=50)
    restrictions: list[str] = Field(default=[], max_length=20)
    urgency: Literal["today", "this_week"] = "today"


class PlanRequest(BaseModel):
    workflow: Literal["food_today"] = "food_today"
    constraints: HouseholdConstraints


def local_now() -> datetime:
    """Current Milwaukee time, or the pinned GOODNEXT_DEMO_NOW when GOODNEXT_ENV=demo.

    Env is read here (not at import time) so tests can monkeypatch it per-call.
    """
    pinned = os.environ.get("GOODNEXT_DEMO_NOW")
    if pinned and os.environ.get("GOODNEXT_ENV") == "demo":
        return datetime.fromisoformat(pinned)
    if pinned:
        log.warning("GOODNEXT_DEMO_NOW is set but GOODNEXT_ENV is not 'demo'; ignoring pinned time")
    return datetime.now(LOCAL_TZ)


def seven_local_dates(today: date | None = None) -> list[str]:
    start = today or local_now().date()
    return [(start + timedelta(days=i)).isoformat() for i in range(7)]


def runtime_session_id(session: str) -> str:
    # AgentCore requires 33+ chars; derive, never expose the raw cookie value.
    return hashlib.sha256(session.encode()).hexdigest()[:48]


def get_session(request: Request, response: Response) -> str:
    session = request.cookies.get(SESSION_COOKIE)
    if not session or len(session) != 36:
        session = str(uuid.uuid4())
        response.set_cookie(SESSION_COOKIE, session, httponly=True, samesite="strict", secure=not DEV, max_age=60 * 60 * 4)
    return session


def get_agent_client() -> AgentClient:
    return default_agent_client()


@app.get("/api/health")
def health() -> dict:
    return {"ok": True, "service": "goodnext-api"}


@app.post("/api/plans")
def create_plan(
    body: PlanRequest,
    response: Response,
    session: str = Depends(get_session),
    agent: AgentClient = Depends(get_agent_client),
):
    request_id = str(uuid.uuid4())
    now = local_now()
    payload = {
        "workflow": body.workflow,
        "constraints": body.constraints.model_dump(),
        "dates": seven_local_dates(now.date()),
        "now_local": now.isoformat(),
        "request_id": request_id,
    }
    try:
        envelope = agent.invoke(payload, runtime_session_id(session))
    except (httpx.HTTPError, OSError) as exc:
        return JSONResponse(
            status_code=503,
            headers=dict(response.headers),
            content={"status": "temporarily_unavailable", "data": None, "evidence": [], "missing": [],
                     "warnings": [f"agent unavailable: {exc.__class__.__name__}"], "retryable": True, "request_id": request_id},
        )
    response.headers["Cache-Control"] = "no-store"
    return envelope
