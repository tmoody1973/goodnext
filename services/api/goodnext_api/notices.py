"""Read a FoodShare letter and match it to reviewed policy passages.

The 'Understand my letter' flow keeps two provenances apart. What the letter
appears to say is resident-supplied document text, pulled out here with no model
in the path. A passage is reviewed guidance, read from the same reviewed file the
maintainer edits. The endpoint shows them side by side; it never paraphrases the
letter or writes guidance of its own (PRD FR02).

Text extraction is by file kind: a PDF is read with pypdf; a scanned image goes
to Amazon Textract behind a boundary, so an AWS failure surfaces as the same
honest 503 the plan endpoint returns, never a made-up reading.
"""

import io
import json
import logging
import os
import re
from functools import lru_cache
from pathlib import Path

log = logging.getLogger(__name__)

DEFAULT_PASSAGES_PATH = Path(__file__).resolve().parents[3] / "app" / "goodnext" / "policy_passages.json"

# Fields a resident may see. triggers and notice_classes stay internal.
_RESIDENT_FIELDS = (
    "passage_id", "topic", "passage", "action_for_resident", "program", "jurisdiction",
    "source_url", "source_retrieved_on", "effective_dates", "version", "review_status",
    "review_owner", "uncertainties",
)

# Literal date phrases a resident should confirm, e.g. "September 30, 2026" or
# "9/30/2026". Reported as found text, never turned into a deadline.
_DATE_RE = re.compile(
    r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}\b"
    r"|\b\d{1,2}/\d{1,2}/\d{2,4}\b"
)


class ExtractionUnavailable(Exception):
    """Raised when a letter cannot be read for a reason that is not the resident's:
    an unreadable file, or Textract/AWS being unreachable. The endpoint answers 503."""


def _passages_path() -> Path:
    return Path(os.environ.get("GOODNEXT_POLICY_PASSAGES_FILE", DEFAULT_PASSAGES_PATH))


@lru_cache(maxsize=4)
def _load(path: str) -> tuple[dict, ...]:
    try:
        doc = json.loads(Path(path).read_text(encoding="utf-8"))
        return tuple(doc.get("passages", []))
    except OSError as exc:
        log.warning("policy passages file unreadable at %s (%s); matching none", path, exc.__class__.__name__)
        return ()


def _passages() -> tuple[dict, ...]:
    return _load(str(_passages_path()))


def extract_text_from_pdf(data: bytes) -> str:
    from pypdf import PdfReader
    from pypdf.errors import PdfReadError

    try:
        reader = PdfReader(io.BytesIO(data))
        return "\n".join(page.extract_text() or "" for page in reader.pages).strip()
    except (PdfReadError, ValueError, OSError) as exc:
        raise ExtractionUnavailable(f"pdf unreadable: {exc.__class__.__name__}") from exc


def extract_text_from_image(data: bytes) -> str:
    """Read a scanned letter with Amazon Textract. Any AWS failure raises
    ExtractionUnavailable so the endpoint answers a truthful 503."""
    try:
        import boto3

        client = boto3.client("textract", region_name=os.environ.get("GOODNEXT_BEDROCK_REGION", "us-east-1"))
        response = client.detect_document_text(Document={"Bytes": data})
        lines = [b["Text"] for b in response.get("Blocks", []) if b.get("BlockType") == "LINE"]
        return "\n".join(lines).strip()
    except Exception as exc:  # noqa: BLE001 - boundary: SDK missing, no AWS session, or Textract failure all read the same
        raise ExtractionUnavailable(f"textract unavailable: {exc.__class__.__name__}") from exc


def extract_text(data: bytes, content_type: str) -> str:
    if content_type == "application/pdf":
        return extract_text_from_pdf(data)
    if content_type in ("image/png", "image/jpeg"):
        return extract_text_from_image(data)
    raise ExtractionUnavailable(f"unsupported content type: {content_type}")


def analyze(text: str) -> tuple[list[dict], str | None]:
    """One pass over the reviewed passages: the passages whose triggers the letter
    matches (resident-facing fields only), and the letter's class. A passage that
    names exactly one class votes for it; the class with the most votes wins, or
    None when nothing matched."""
    text_lower = text.lower()
    matched: list[dict] = []
    class_counts: dict[str, int] = {}
    for passage in _passages():
        if not any(t in text_lower for t in passage.get("triggers", [])):
            continue
        matched.append({k: passage[k] for k in _RESIDENT_FIELDS if k in passage})
        classes = passage.get("notice_classes", [])
        if len(classes) == 1:
            class_counts[classes[0]] = class_counts.get(classes[0], 0) + 1
    notice_class = max(class_counts, key=lambda c: class_counts[c]) if class_counts else None
    return matched, notice_class


def found_dates(text: str) -> list[str]:
    seen: list[str] = []
    for m in _DATE_RE.findall(text):
        if m not in seen:
            seen.append(m)
    return seen
