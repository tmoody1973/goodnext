"""GoodNext application API. Food planning needs no account, no notice, no benefits questions."""

import hashlib
import logging
import os
import uuid
from datetime import date, datetime, timedelta
from typing import Literal
from zoneinfo import ZoneInfo

import httpx
from fastapi import Depends, FastAPI, File, Request, Response, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from goodnext_api.agent_client import AgentClient, default_agent_client
from goodnext_api.help_routes import help_routes
from goodnext_api import notices

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
    except Exception as exc:  # noqa: BLE001 - boundary: network, AWS session, or runtime failure all read the same to a resident
        log.warning("agent unavailable: %s", exc.__class__.__name__)
        return error_envelope(response, 503, "temporarily_unavailable", request_id,
                              warning=f"agent unavailable: {exc.__class__.__name__}", retryable=True)
    response.headers["Cache-Control"] = "no-store"
    return envelope


# Content types the letter reader supports, with a size cap. A resident's phone
# photo or a downloaded PDF fits well under this.
NOTICE_CONTENT_TYPES = {"application/pdf", "image/png", "image/jpeg"}
MAX_NOTICE_BYTES = 10 * 1024 * 1024


def error_envelope(response: Response, status_code: int, status: str, request_id: str,
                   *, warning: str, retryable: bool, missing: list[str] | None = None) -> JSONResponse:
    """A non-2xx envelope, shared by both endpoints and every non-2xx exit. Keeps
    whatever headers the session dependency set (the Set-Cookie for a first-time
    visitor), marks the answer no-store like the success path, and carries the
    reviewed help routes so a resident always has a human to reach."""
    headers = dict(response.headers)
    headers["Cache-Control"] = "no-store"
    return JSONResponse(
        status_code=status_code,
        headers=headers,
        content={"status": status, "data": None, "evidence": [], "missing": missing or [],
                 "warnings": [warning], "retryable": retryable, "request_id": request_id,
                 "help_routes": help_routes()},
    )


@app.post("/api/notices")
async def read_notice(
    response: Response,
    file: UploadFile = File(...),
    session: str = Depends(get_session),
):
    """Read a FoodShare letter and return what it appears to ask for beside the
    reviewed policy passages it matches. No model writes any of it (PRD FR02)."""
    request_id = str(uuid.uuid4())
    if file.content_type not in NOTICE_CONTENT_TYPES:
        return error_envelope(response, 415, "denied", request_id,
                              warning=f"unsupported content type: {file.content_type}",
                              retryable=False, missing=["unsupported_file_type"])
    data = await file.read()
    if len(data) > MAX_NOTICE_BYTES:
        return error_envelope(response, 413, "denied", request_id,
                              warning="file too large", retryable=False, missing=["file_too_large"])
    try:
        text = notices.extract_text(data, file.content_type)
    except notices.ExtractionUnavailable as exc:
        log.warning("notice unreadable: %s", exc.__class__.__name__)
        return error_envelope(response, 503, "temporarily_unavailable", request_id,
                              warning=f"could not read the letter: {exc.__class__.__name__}", retryable=True)

    passages, notice_class = notices.analyze(text)
    status = "success" if passages else "no_match"
    data_out = {
        "notice_class": notice_class,
        "found_dates": notices.found_dates(text),
        "extracted_text": text,
        "passages": passages,
    }
    response.headers["Cache-Control"] = "no-store"
    return {"status": status, "data": data_out, "evidence": [p["passage_id"] for p in passages],
            "missing": [] if passages else ["no_reviewed_passage_matched"], "warnings": [], "retryable": False,
            "request_id": request_id, "help_routes": help_routes()}
