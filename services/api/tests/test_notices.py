import sys
from pathlib import Path

from fastapi.testclient import TestClient

from goodnext_api import notices
from goodnext_api.main import app

# MOO-775: reuse the agent package's never-list scanner (pydantic-only module).
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "app" / "goodnext"))
from claims import never_list_hits  # noqa: E402

GENERATED = Path(__file__).resolve().parents[3] / "docs" / "research" / "notices" / "generated"


def client() -> TestClient:
    return TestClient(app)


def upload(name: str, content_type: str = "application/pdf"):
    data = (GENERATED / name).read_bytes()
    return client().post("/api/notices", files={"file": (name, data, content_type)})


def test_six_month_report_matches_reviewed_passages():
    r = upload("six-month-report.pdf")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "success"
    assert body["data"]["notice_class"] == "six_month_report"
    assert "September 30, 2026" in body["data"]["found_dates"]
    ids = [p["passage_id"] for p in body["data"]["passages"]]
    assert "fs-six-month-report-basics" in ids
    assert body["evidence"] == ids
    # Reviewed guidance is shown, but the internal trigger keywords are not.
    assert all("triggers" not in p for p in body["data"]["passages"])
    assert r.headers["cache-control"] == "no-store"
    assert "gn_session" in r.cookies
    assert never_list_hits(body) == []


def test_proof_request_is_classified_and_dated():
    r = upload("proof-request.pdf")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "success"
    assert body["data"]["notice_class"] == "proof_request"
    assert "September 22, 2026" in body["data"]["found_dates"]
    assert body["data"]["extracted_text"].startswith("FICTIONAL SAMPLE")


def test_unsupported_file_type_is_denied_with_help_routes():
    r = client().post("/api/notices", files={"file": ("note.txt", b"hello", "text/plain")})
    assert r.status_code == 415
    body = r.json()
    assert body["status"] == "denied"
    assert len(body["help_routes"]) == 3
    assert r.headers["cache-control"] == "no-store"


def test_file_too_large_is_denied(monkeypatch):
    monkeypatch.setattr("goodnext_api.main.MAX_NOTICE_BYTES", 8)
    r = client().post("/api/notices", files={"file": ("big.pdf", b"x" * 64, "application/pdf")})
    assert r.status_code == 413
    assert r.json()["missing"] == ["file_too_large"]


def test_unreadable_letter_is_a_truthful_503(monkeypatch):
    """A scanned image whose text extraction fails (Textract or AWS unreachable)
    is the same honest 503 the plan endpoint returns, with the help routes."""
    def boom(data, content_type):
        raise notices.ExtractionUnavailable("textract unavailable: EndpointConnectionError")

    monkeypatch.setattr(notices, "extract_text", boom)
    r = client().post("/api/notices", files={"file": ("scan.png", b"\x89PNG", "image/png")})
    assert r.status_code == 503
    body = r.json()
    assert body["status"] == "temporarily_unavailable" and body["retryable"] is True
    assert len(body["help_routes"]) == 3
    assert body["warnings"][0].startswith("could not read the letter")
    assert r.headers["cache-control"] == "no-store"


def test_image_path_uses_the_reader_when_it_returns_text(monkeypatch):
    monkeypatch.setattr(notices, "extract_text", lambda data, ct: "Six-month report due September 30, 2026")
    r = client().post("/api/notices", files={"file": ("scan.png", b"\x89PNG", "image/png")})
    body = r.json()
    assert r.status_code == 200 and body["status"] == "success"
    assert body["data"]["notice_class"] == "six_month_report"


def test_readable_letter_with_no_reviewed_match_is_no_match(monkeypatch):
    monkeypatch.setattr(notices, "extract_text", lambda data, ct: "A postcard about a neighborhood picnic.")
    r = client().post("/api/notices", files={"file": ("card.pdf", b"%PDF", "application/pdf")})
    body = r.json()
    assert r.status_code == 200 and body["status"] == "no_match"
    assert body["data"]["passages"] == []
    assert body["data"]["extracted_text"].startswith("A postcard")
    assert len(body["help_routes"]) == 3
