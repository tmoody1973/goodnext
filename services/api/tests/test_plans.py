from datetime import date, datetime

import httpx
from fastapi.testclient import TestClient

from goodnext_api.main import LOCAL_TZ, app, get_agent_client, seven_local_dates, runtime_session_id

BODY = {"constraints": {"zip_code": "53206", "budget_usd": 0, "kitchen": "none", "travel": ["bus"]}}


class FakeAgent:
    def __init__(self, reply=None, fail=False):
        self.calls, self.reply, self.fail = [], reply, fail

    def invoke(self, payload, runtime_session_id):
        self.calls.append((payload, runtime_session_id))
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
