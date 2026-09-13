"""Hosting (decision 008 and 012): one container serves the static site at / and the API at /api/*."""

import pathlib

from fastapi import FastAPI
from fastapi.testclient import TestClient

from goodnext_api.main import app, get_agent_client, mount_site
from test_plans import BODY, FakeAgent


def test_root_serves_index_html_from_static_dir(tmp_path):
    (tmp_path / "index.html").write_text("<h1>GoodNext</h1>", encoding="utf-8")
    site = FastAPI()
    mount_site(site, tmp_path)
    r = TestClient(site).get("/")
    assert r.status_code == 200 and "<h1>GoodNext</h1>" in r.text


def test_api_routes_win_over_the_static_mount(tmp_path):
    (tmp_path / "index.html").write_text("site", encoding="utf-8")
    site = FastAPI()

    @site.get("/api/health")
    def health():
        return {"ok": True}

    mount_site(site, tmp_path)
    r = TestClient(site).get("/api/health")
    assert r.status_code == 200 and r.json() == {"ok": True}


def test_cookie_is_secure_only_when_the_request_arrived_over_https():
    app.dependency_overrides[get_agent_client] = lambda: FakeAgent()
    over_http = TestClient(app).post("/api/plans", json=BODY)
    over_https = TestClient(app, base_url="https://testserver").post("/api/plans", json=BODY)
    assert "gn_session" in over_http.cookies and "secure" not in over_http.headers["set-cookie"].lower()
    assert "secure" in over_https.headers["set-cookie"].lower()


def test_help_routes_path_never_walks_above_the_filesystem_root(monkeypatch):
    """In the image the package lives at /srv/goodnext_api (two levels below /); the loader
    must resolve its default lazily and survive a shallow location."""
    import goodnext_api.help_routes as hr
    monkeypatch.setattr(hr, "__file__", "/srv/goodnext_api/help_routes.py")
    monkeypatch.setenv("GOODNEXT_HELP_ROUTES_FILE", "/srv/data/help_routes.json")
    assert str(hr._path()) == "/srv/data/help_routes.json"
    monkeypatch.delenv("GOODNEXT_HELP_ROUTES_FILE")
    assert hr._path().name == "help_routes.json"  # no IndexError
