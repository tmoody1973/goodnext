"""Build the fictional notice PDFs from their .txt sources.

One text PDF per letter under docs/research/notices/generated/, laid out as a
single page of Helvetica lines. The output is deterministic so the committed
PDF only changes when the source text does. Pure standard library: the API
reads these with pypdf, but making them needs no third-party package.

Run from the repo root:

    python app/goodnext/scripts/generate_notice_pdfs.py
"""

from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
GENERATED = REPO / "docs" / "research" / "notices" / "generated"
# The screen offers the same letters as demo samples, so the browser needs them
# under the web app's static files too (MOO-791).
WEB_SAMPLES = REPO / "apps" / "web" / "public" / "samples"
LETTERS = ["six-month-report", "proof-request"]

FONT_SIZE = 11
LEADING = 15
TOP = 740
LEFT = 72


def _escape(text: str) -> str:
    return text.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")


def _content_stream(lines: list[str]) -> bytes:
    body = [f"BT /F1 {FONT_SIZE} Tf {LEFT} {TOP} Td {LEADING} TL"]
    for line in lines:
        body.append(f"({_escape(line)}) Tj T*")
    body.append("ET")
    return "\n".join(body).encode("latin-1", "replace")


def build_pdf(lines: list[str]) -> bytes:
    content = _content_stream(lines)
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length %d >>\nstream\n%s\nendstream" % (len(content), content),
    ]

    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for i, obj in enumerate(objects, start=1):
        offsets.append(len(out))
        out += b"%d 0 obj\n%s\nendobj\n" % (i, obj)

    xref_pos = len(out)
    out += b"xref\n0 %d\n" % (len(objects) + 1)
    out += b"0000000000 65535 f \n"
    for offset in offsets:
        out += b"%010d 00000 n \n" % offset
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\n" % (len(objects) + 1)
    out += b"startxref\n%d\n%%%%EOF\n" % xref_pos
    return bytes(out)


def main() -> None:
    WEB_SAMPLES.mkdir(parents=True, exist_ok=True)
    for name in LETTERS:
        source = GENERATED / f"{name}.txt"
        lines = source.read_text(encoding="utf-8").splitlines()
        pdf = build_pdf(lines)
        (GENERATED / f"{name}.pdf").write_bytes(pdf)
        (WEB_SAMPLES / f"{name}.pdf").write_bytes(pdf)
        print(f"wrote {name}.pdf ({len(lines)} lines)")


if __name__ == "__main__":
    main()
