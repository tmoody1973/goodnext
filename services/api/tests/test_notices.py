"""POST /api/notices (MOO-790): upload or three answers, extraction in memory, agent invoke."""

import io
import logging
from pathlib import Path

import httpx
from fastapi.testclient import TestClient
from pypdf import PdfWriter

import goodnext_api.notices as notices
from goodnext_api.main import app, get_agent_client

GENERATED = Path(__file__).resolve().parents[3] / "docs" / "research" / "notices" / "generated"
LETTERS = {
    "notice-of-sanction-maria-example.pdf": (2, "Notice of Sanction"),
    "time-limited-benefits-warning-maria-example.pdf": (3, "Time-Limited"),
    "six-month-report-conversion-maria-example.pdf": (3, "Six-Month Report"),
}


class FakeAgent:
    def __init__(self, fail=False):
        self.calls, self.fail = [], fail

    def invoke(self, payload, runtime_session_id):
        self.calls.append((payload, runtime_session_id))
        if self.fail:
            raise httpx.ConnectError("refused")
        return {"status": "success", "data": {"letter_kind": "sanction", "passages": payload.get("passages", [])}, "evidence": [], "missing": [], "warnings": [], "retryable": False, "request_id": payload["request_id"]}


def client_with(agent):
    app.dependency_overrides[get_agent_client] = lambda: agent
    return TestClient(app)


def upload(client, name, data, content_type):
    return client.post("/api/notices", files={"file": (name, io.BytesIO(data), content_type)})


def test_rejects_unsupported_type_before_agent():
    agent = FakeAgent()
    r = upload(client_with(agent), "letter.txt", b"hello", "text/plain")
    assert r.status_code == 400 and agent.calls == []
    body = r.json()
    assert body["status"] == "needs_clarification"
    assert any("PDF" in m for m in body["missing"]) and len(body["help_routes"]) == 3


def test_rejects_oversized_file_before_agent():
    agent = FakeAgent()
    big = b"%PDF-1.4" + b"0" * (notices.MAX_BYTES + 1)
    r = upload(client_with(agent), "big.pdf", big, "application/pdf")
    assert r.status_code == 400 and agent.calls == []
    assert any("10 MB" in m for m in r.json()["missing"])


def test_rejects_too_many_pages():
    w = PdfWriter()
    for _ in range(notices.MAX_PAGES + 1):
        w.add_blank_page(width=612, height=792)
    buf = io.BytesIO()
    w.write(buf)
    agent = FakeAgent()
    r = upload(client_with(agent), "long.pdf", buf.getvalue(), "application/pdf")
    assert r.status_code == 400 and agent.calls == []
    assert any("6 pages" in m for m in r.json()["missing"])


def test_pdf_letters_become_passages_and_reach_the_agent():
    for name, (pages, title) in LETTERS.items():
        agent = FakeAgent()
        r = upload(client_with(agent), name, (GENERATED / name).read_bytes(), "application/pdf")
        assert r.status_code == 200, name
        payload, sid = agent.calls[0]
        assert payload["workflow"] == "understand_notice" and len(sid) >= 33
        assert sorted({p["page"] for p in payload["passages"]}) == list(range(1, pages + 1)), name
        assert any(title in p["text"] for p in payload["passages"] if p["page"] == 1), name
        assert all(p["id"].startswith(f"p{p['page']}-") for p in payload["passages"]), name
        assert "gn_session" in r.cookies and r.headers["cache-control"] == "no-store"
        assert r.json()["request_id"] == payload["request_id"]


def test_client_cannot_forge_request_id_or_passages():
    agent = FakeAgent()
    client = client_with(agent)
    client.post("/api/notices", files={"file": ("x.pdf", io.BytesIO((GENERATED / "notice-of-sanction-maria-example.pdf").read_bytes()), "application/pdf")}, data={"request_id": "forged"})
    payload, _ = agent.calls[0]
    assert payload["request_id"] != "forged"


def test_manual_answers_forwarded_without_a_file():
    agent = FakeAgent()
    r = client_with(agent).post("/api/notices", data={"letter_kind": "six_month_report", "date_text": "March 2027", "asks_text": "Fill out a six-month report form"})
    assert r.status_code == 200
    payload, _ = agent.calls[0]
    assert payload["workflow"] == "understand_notice" and "passages" not in payload
    assert payload["manual"] == {"letter_kind": "six_month_report", "date_text": "March 2027", "asks_text": "Fill out a six-month report form"}


def test_manual_requires_a_known_letter_kind():
    agent = FakeAgent()
    r = client_with(agent).post("/api/notices", data={"letter_kind": "parking ticket"})
    assert r.status_code == 400 and agent.calls == []


def test_nothing_at_all_is_a_recoverable_error():
    agent = FakeAgent()
    r = client_with(agent).post("/api/notices", data={})
    assert r.status_code == 400 and agent.calls == [] and r.json()["status"] == "needs_clarification"


def test_image_goes_through_textract_lines(monkeypatch):
    seen = {}

    def fake_lines(data: bytes) -> list[dict]:
        seen["bytes"] = len(data)
        return [
            {"text": "FoodShare Notice of Sanction", "top": 0.10, "height": 0.02},
            {"text": "This letter is to notify you that you have voluntarily quit a job without good cause.", "top": 0.13, "height": 0.02},
            {"text": "Work Registration", "top": 0.40, "height": 0.02},
        ]

    monkeypatch.setattr(notices, "textract_lines", fake_lines)
    png = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100
    agent = FakeAgent()
    r = upload(client_with(agent), "photo.png", png, "image/png")
    assert r.status_code == 200 and seen["bytes"] == len(png)
    passages = agent.calls[0][0]["passages"]
    assert [p["page"] for p in passages] == [1, 1]
    assert "Notice of Sanction" in passages[0]["text"] and "good cause" in passages[0]["text"]
    assert passages[1]["text"] == "Work Registration"


def test_image_with_wrong_magic_bytes_is_rejected():
    agent = FakeAgent()
    r = upload(client_with(agent), "photo.png", b"not really a png", "image/png")
    assert r.status_code == 400 and agent.calls == []


def test_agent_outage_is_truthful_503():
    r = upload(client_with(FakeAgent(fail=True)), "l.pdf", (GENERATED / "notice-of-sanction-maria-example.pdf").read_bytes(), "application/pdf")
    assert r.status_code == 503 and r.json()["status"] == "temporarily_unavailable" and len(r.json()["help_routes"]) == 3


def test_letter_text_never_reaches_the_log(caplog):
    caplog.set_level(logging.DEBUG)
    upload(client_with(FakeAgent()), "l.pdf", (GENERATED / "notice-of-sanction-maria-example.pdf").read_bytes(), "application/pdf")
    assert "Maria" not in caplog.text and "Example" not in caplog.text
    assert "passages" in caplog.text
