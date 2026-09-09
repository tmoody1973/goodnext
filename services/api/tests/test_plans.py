import sys
from datetime import date, datetime
from pathlib import Path

import httpx
from fastapi.testclient import TestClient

from goodnext_api.main import LOCAL_TZ, app, get_agent_client, seven_local_dates, runtime_session_id

# MOO-775: claims.py is a pure agent-package module (pydantic only, no
# strands/bedrock imports) — reuse it here instead of duplicating never_list_hits.
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "app" / "goodnext"))
from claims import never_list_hits  # noqa: E402

BODY = {"constraints": {"zip_code": "53206", "budget_usd": 0, "kitchen": "none", "travel": ["bus"]}}


class FakeAgent:
    def __init__(self, reply=None, fail=False, error: Exception | None = None):
        self.calls, self.reply, self.fail, self.error = [], reply, fail, error

    def invoke(self, payload, runtime_session_id):
        self.calls.append((payload, runtime_session_id))
        if self.error is not None:
            raise self.error
        if self.fail:
            raise httpx.ConnectError("refused")
        return self.reply or {"status": "no_match", "data": None, "evidence": [], "missing": ["none"], "warnings": [], "retryable": False, "request_id": payload["request_id"]}


def client_with(agent):
    app.dependency_overrides[get_agent_client] = lambda: agent
    return TestClient(app)


def test_seven_consecutive_local_dates():
    dates = seven_local_dates(date(2026, 9, 8))
    assert dates == [f"2026-09-{d:02d}" for d in range(8, 15)]


def test_runtime_session_id_is_long_and_not_the_cookie():
    rid = runtime_session_id("abc")
    assert len(rid) >= 33 and "abc" not in rid


def test_plan_passes_server_dates_and_sets_session_cookie():
    agent = FakeAgent()
    r = client_with(agent).post("/api/plans", json=BODY)
    assert r.status_code == 200 and r.json()["status"] == "no_match"
    payload, sid = agent.calls[0]
    assert len(payload["dates"]) == 7 and payload["constraints"]["zip_code"] == "53206"
    assert len(sid) >= 33
    assert "gn_session" in r.cookies and r.headers["cache-control"] == "no-store"


def test_client_cannot_supply_dates_or_request_id():
    agent = FakeAgent()
    client_with(agent).post("/api/plans", json={**BODY, "dates": ["1999-01-01"], "request_id": "forged"})
    payload, _ = agent.calls[0]
    assert payload["dates"][0] != "1999-01-01" and payload["request_id"] != "forged"


def test_invalid_zip_rejected_before_agent():
    agent = FakeAgent()
    r = client_with(agent).post("/api/plans", json={"constraints": {"zip_code": "5320", "budget_usd": 0}})
    assert r.status_code == 422 and agent.calls == []


def test_agent_outage_is_truthful_503():
    r = client_with(FakeAgent(fail=True)).post("/api/plans", json=BODY)
    assert r.status_code == 503
    body = r.json()
    assert body["status"] == "temporarily_unavailable" and body["retryable"] is True
    # MOO-780: even when the agent is unreachable, the API's own answer carries the
    # three reviewed help routes, read from the same file the agent reads.
    assert [route["name"] for route in body["help_routes"]] == [
        "2-1-1 (IMPACT 211 in Milwaukee County)",
        "Hunger Task Force emergency food",
        "FoodShare member line",
    ]
    assert never_list_hits(body) == []


def test_expired_aws_session_is_still_a_truthful_503():
    """Found live 2026-09-08: an expired `aws login` surfaced as a bare 500 with a
    traceback. Any failure to reach the agent is the same honest envelope."""
    class LoginRefreshRequired(Exception):
        pass

    r = client_with(FakeAgent(error=LoginRefreshRequired("Your session has expired"))).post("/api/plans", json=BODY)
    assert r.status_code == 503
    body = r.json()
    assert body["status"] == "temporarily_unavailable" and body["retryable"] is True
    assert len(body["help_routes"]) == 3
    assert "expired" not in body["warnings"][0].lower()  # class name only, never the message
    assert never_list_hits(body) == []


def test_api_help_routes_match_the_agent_file():
    from goodnext_api.help_routes import help_routes
    import json
    agent_file = Path(__file__).resolve().parents[3] / "app" / "goodnext" / "help_routes.json"
    assert help_routes() == json.loads(agent_file.read_text())


def test_api_help_routes_missing_file_is_empty_not_fatal(monkeypatch, tmp_path):
    from goodnext_api.help_routes import help_routes
    monkeypatch.setenv("GOODNEXT_HELP_ROUTES_FILE", str(tmp_path / "nowhere.json"))
    assert help_routes() == []


def test_demo_env_pins_date_and_now_local(monkeypatch):
    monkeypatch.setenv("GOODNEXT_ENV", "demo")
    monkeypatch.setenv("GOODNEXT_DEMO_NOW", "2026-09-08T10:00:00-05:00")
    agent = FakeAgent()
    r = client_with(agent).post("/api/plans", json=BODY)
    assert r.status_code == 200
    payload, _ = agent.calls[0]
    assert payload["dates"][0] == "2026-09-08"
    assert payload["now_local"] == "2026-09-08T10:00:00-05:00"


def test_no_match_envelope_passes_through_three_help_routes():
    routes = [
        {"name": "2-1-1", "purpose": "Find local food and other help by phone, any day.",
         "phone": "2-1-1", "url": "https://www.211.org", "source_url": "https://www.211.org", "last_checked": "2026-09-08"},
        {"name": "Hunger Task Force emergency food", "purpose": "Milwaukee County pantry and meal map.",
         "phone": None, "url": "https://www.hungertaskforce.org/get-help/emergency-food/",
         "source_url": "https://www.hungertaskforce.org/get-help/emergency-food/", "last_checked": "2026-09-08"},
        {"name": "FoodShare member line", "purpose": "Questions about your FoodShare case or QUEST card.",
         "phone": "1-800-362-3002", "url": "https://www.dhs.wisconsin.gov/foodshare/index.htm",
         "source_url": "https://www.dhs.wisconsin.gov/foodshare/index.htm", "last_checked": "2026-09-08"},
    ]
    reply = {"status": "no_match", "data": None, "evidence": [], "missing": ["No feasible resource found; see help route"],
             "warnings": [], "retryable": False, "request_id": "r1", "help_routes": routes}
    agent = FakeAgent(reply=reply)
    r = client_with(agent).post("/api/plans", json={**BODY, "constraints": {**BODY["constraints"], "zip_code": "53999"}})
    body = r.json()
    assert r.status_code == 200
    assert body["status"] == "no_match"
    assert len(body["help_routes"]) == 3
    assert body["data"] is None


def test_demo_now_ignored_outside_demo_env(monkeypatch, caplog):
    monkeypatch.delenv("GOODNEXT_ENV", raising=False)
    monkeypatch.setenv("GOODNEXT_DEMO_NOW", "2026-09-08T10:00:00-05:00")
    real_today = datetime.now(LOCAL_TZ).date().isoformat()
    agent = FakeAgent()
    r = client_with(agent).post("/api/plans", json=BODY)
    assert r.status_code == 200
    payload, _ = agent.calls[0]
    assert payload["dates"][0] == real_today
    assert "GOODNEXT_DEMO_NOW is set" in caplog.text


def test_success_envelope_with_claims_passes_through_and_has_no_never_list_hits():
    claims = {
        "open_today_text": "Open today from 10:00 AM to 2:00 PM",
        "cost_label": "Free",
        "requirements_text": "No requirements listed",
        "appointment_text": "",
        "freshness_text": "Last checked 2026-09-05",
        "inventory_text": "We can't confirm they have food today.",
        "service_area_text": "",
        "travel_text": "Travel time unknown, check the map.",
        "directions_url": "https://www.google.com/maps/search/?api=1&query=1200+W+Demo+St%2C+Milwaukee%2C+WI+53206",
        "travel_echo": "You said: bus",
    }
    visit = {
        "resource_id": "res-001", "provider": "Northside Community Pantry (synthetic)", "date": "2026-09-08",
        "service_type": "free_pantry", "cost": "free", "schedule_text": "see record",
        "requirements": [], "last_verified": "2026-09-05", "contact": "(414) 555-0101",
        "freshness_tier": "verified", "uncertainty": [], "backup_resource_id": None, "next_open": None,
        "claims": claims,
    }
    reply = {
        "status": "success", "data": {"start_date": "2026-09-08", "days": [], "food_today": [visit]},
        "evidence": ["res-001"], "missing": [], "warnings": [], "retryable": False, "request_id": "r1",
    }
    agent = FakeAgent(reply=reply)

    r = client_with(agent).post("/api/plans", json=BODY)
    body = r.json()

    assert r.status_code == 200
    assert body["data"]["food_today"][0]["claims"] == claims
    assert never_list_hits(body) == []
