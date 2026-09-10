# Generated notice letters (fictional)

These files are **fictional FoodShare letters** written for the GoodNext
"Understand my letter" demonstration and tests. They are not real letters, not
official documents, and not addressed to a real person. Every name, case
number, address, and date is invented.

Each letter has two forms:

- a `.txt` source, the human-readable text, and
- a `.pdf` built from that text by `app/goodnext/scripts/generate_notice_pdfs.py`.

The PDFs are the upload fixtures for the notice endpoint text-extraction tests
and the demo sample letters on the screen. Regenerate them after editing a
`.txt` source:

```bash
python app/goodnext/scripts/generate_notice_pdfs.py
```

## Files

| File | Class | Stands in for |
| --- | --- | --- |
| `six-month-report.txt` / `.pdf` | six-month report | A periodic report the household must return by a date |
| `proof-request.txt` / `.pdf` | proof request | A request for documents to verify the case |

The proof-request layout follows the official DMS proof-needed sample only as a
layout reference (PRD "Provenance and synthetic data"); its text is fictional
and carries no real deadline.
