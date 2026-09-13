"""Hosting boundary (MOO-793): the site and the API share one address, and the
session cookie's Secure flag is split from the demo clock so plain HTTP works."""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from goodnext_api.main import app, cookie_secure, get_agent_client, mount_web


def test_missing_web_root_does_not_mount(tmp_path):
    assert mount_web(FastAPI(), str(tmp_path / "nope")) is False


def test_static_site_served_at_root_beside_api(tmp_path):
    (tmp_path / "index.html").write_text("<h1>GoodNext</h1>", encoding="utf-8")

    site = FastAPI()

    @site.get("/api/health")
    def health() -> dict:
        return {"ok": True}

    assert mount_web(site, str(tmp_path)) is True
    client = TestClient(site)
    assert client.get("/api/health").json() == {"ok": True}
    assert "GoodNext" in client.get("/").text


def test_cookie_secure_off_in_dev(monkeypatch):
    monkeypatch.delenv("GOODNEXT_COOKIE_SECURE", raising=False)
    monkeypatch.setenv("GOODNEXT_ENV", "dev")
    assert cookie_secure() is False


def test_cookie_secure_on_in_demo_by_default(monkeypatch):
    monkeypatch.delenv("GOODNEXT_COOKIE_SECURE", raising=False)
    monkeypatch.setenv("GOODNEXT_ENV", "demo")
    assert cookie_secure() is True


def test_cookie_secure_override_lets_demo_run_on_plain_http(monkeypatch):
    monkeypatch.setenv("GOODNEXT_ENV", "demo")
    monkeypatch.setenv("GOODNEXT_COOKIE_SECURE", "false")
    assert cookie_secure() is False


def test_demo_on_plain_http_still_sets_the_session_cookie(monkeypatch):
    """The reported symptom: GOODNEXT_ENV=demo turned Secure on, so a browser on
    plain HTTP dropped the cookie and every request looked like a stranger."""
    monkeypatch.setenv("GOODNEXT_ENV", "demo")
    monkeypatch.setenv("GOODNEXT_DEMO_NOW", "2026-09-10T09:00:00-05:00")
    monkeypatch.setenv("GOODNEXT_COOKIE_SECURE", "false")

    class FakeAgent:
        def invoke(self, payload, runtime_session_id):
            return {"status": "no_match", "data": None, "evidence": [], "missing": ["none"],
                    "warnings": [], "retryable": False, "request_id": payload["request_id"]}

    app.dependency_overrides[get_agent_client] = lambda: FakeAgent()
    try:
        client = TestClient(app)
        r = client.post("/api/plans", json={"constraints": {"zip_code": "53206", "budget_usd": 0}})
        assert r.status_code == 200
        assert "gn_session" in r.cookies
    finally:
        app.dependency_overrides.clear()
