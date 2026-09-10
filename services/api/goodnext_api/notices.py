"""Letter intake for Understand my letter (MOO-790, decision 011).

A letter arrives as a PDF or a photo. Its text is pulled out in memory into
numbered passages the agent reads as data. Nothing is written to disk and no
letter text is logged. Photos go through Amazon Textract, one call per image.
"""

import io
import os
import re
from dataclasses import dataclass

from pypdf import PdfReader

MAX_BYTES = 10 * 1024 * 1024
MAX_PAGES = 6
MAX_PASSAGE_CHARS = 600
LIMITS_TEXT = "PDF, JPG, or PNG up to 10 MB and 6 pages"
MAGIC = {"pdf": (b"%PDF",), "png": (b"\x89PNG",), "jpg": (b"\xff\xd8",)}
LETTER_KINDS = ("sanction", "time_limited_warning", "six_month_report", "unknown")
_SENTENCE_END = re.compile(r"[.!?:]$")


class NoticeIntakeError(ValueError):
    """A recoverable problem with the upload; the message names the limit."""


@dataclass(frozen=True)
class Passage:
    id: str
    page: int
    text: str

    def as_dict(self) -> dict:
        return {"id": self.id, "page": self.page, "text": self.text}


def sniff(data: bytes, filename: str, content_type: str | None) -> str:
    """Decide the file kind from its first bytes; the name and header only corroborate."""
    for kind, magics in MAGIC.items():
        if any(data.startswith(m) for m in magics):
            return kind
    raise NoticeIntakeError(f"We can read a {LIMITS_TEXT}. This file does not look like one.")


def check_size(data: bytes) -> None:
    if len(data) > MAX_BYTES:
        raise NoticeIntakeError(f"That file is larger than 10 MB. We can read a {LIMITS_TEXT}.")
    if not data:
        raise NoticeIntakeError(f"The file was empty. We can read a {LIMITS_TEXT}.")


def lines_to_passages(page: int, lines: list[str]) -> list[Passage]:
    """Group consecutive lines into passages. A passage closes after a line that ends
    a sentence, or when it grows past MAX_PASSAGE_CHARS. ponytail: a title with no
    period joins the paragraph under it; citations stay correct, just a little coarse."""
    passages, buffer = [], []

    def flush() -> None:
        if buffer:
            text = " ".join(buffer).strip()
            if text:
                passages.append(Passage(id=f"p{page}-{len(passages) + 1}", page=page, text=text))
            buffer.clear()

    for raw in lines:
        line = " ".join(raw.split())
        if not line:
            flush()
            continue
        buffer.append(line)
        if _SENTENCE_END.search(line) or sum(len(b) for b in buffer) > MAX_PASSAGE_CHARS:
            flush()
    flush()
    return passages


def passages_from_pdf(data: bytes) -> list[Passage]:
    try:
        reader = PdfReader(io.BytesIO(data))
        count = len(reader.pages)
    except Exception as exc:  # noqa: BLE001 - any unreadable PDF reads the same to a resident
        raise NoticeIntakeError(f"We could not read that PDF. We can read a {LIMITS_TEXT}.") from exc
    if count > MAX_PAGES:
        raise NoticeIntakeError(f"That PDF has {count} pages. We can read up to 6 pages.")
    passages: list[Passage] = []
    for number, page in enumerate(reader.pages, start=1):
        passages.extend(lines_to_passages(number, (page.extract_text() or "").splitlines()))
    if not passages:
        raise NoticeIntakeError("That PDF has no readable text. Try a photo of the letter, or answer the three questions instead.")
    return passages


def textract_lines(data: bytes) -> list[dict]:
    """One Amazon Textract call: the LINE blocks of one image, top to bottom, with their
    position (fraction of page height) so paragraphs can be told apart."""
    import boto3  # imported here so PDF-only deployments need no Textract client

    client = boto3.client("textract", region_name=os.environ.get("GOODNEXT_TEXTRACT_REGION", os.environ.get("GOODNEXT_BEDROCK_REGION", "us-east-1")))
    response = client.detect_document_text(Document={"Bytes": data})
    lines = []
    for block in response.get("Blocks", []):
        if block.get("BlockType") == "LINE":
            box = block.get("Geometry", {}).get("BoundingBox", {})
            lines.append({"text": block.get("Text", ""), "top": box.get("Top", 0.0), "height": box.get("Height", 0.02)})
    return sorted(lines, key=lambda l: l["top"])


def passages_from_image(data: bytes) -> list[Passage]:
    try:
        lines = textract_lines(data)
    except Exception as exc:  # noqa: BLE001 - a Textract outage or a bad image read the same to a resident
        raise NoticeIntakeError("We could not read that photo right now. Try a PDF, or answer the three questions instead.") from exc
    # A gap taller than 1.5 lines starts a new paragraph; the line grouping does the rest.
    grouped: list[str] = []
    previous_bottom = None
    for line in lines:
        if previous_bottom is not None and line["top"] - previous_bottom > 1.5 * max(line["height"], 0.01):
            grouped.append("")
        grouped.append(line["text"])
        previous_bottom = line["top"] + line["height"]
    passages = lines_to_passages(1, grouped)
    if not passages:
        raise NoticeIntakeError("We could not find text in that photo. Try a clearer photo, a PDF, or the three questions.")
    return passages


def passages_from_upload(data: bytes, filename: str, content_type: str | None) -> list[Passage]:
    check_size(data)
    kind = sniff(data, filename, content_type)
    return passages_from_pdf(data) if kind == "pdf" else passages_from_image(data)


def manual_notice(letter_kind: str | None, date_text: str | None, asks_text: str | None) -> dict:
    if letter_kind not in LETTER_KINDS:
        raise NoticeIntakeError("Pick the kind of letter from the list, or upload the letter.")
    return {"letter_kind": letter_kind, "date_text": (date_text or "").strip()[:200], "asks_text": (asks_text or "").strip()[:1000]}
