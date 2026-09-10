# Understand my letter

Feature spec. September 10, 2026. Source: PRD 1.6 FR02, section 5 (Journey A),
sections 8 and 14 (provenance and synthetic data), `CONTEXT.md`, decision 011,
decision 008 (site and API share one address), and the food flow this reuses
(`docs/specs/food-today.md`, `docs/specs/food-today-screen.md`).
Triage: ready-for-agent (Linear status Todo) once ticketed. Tickets: MOO-788
(letters and passages), MOO-790 (the API endpoint), MOO-791 (the screen).

## Problem Statement

A FoodShare letter is hard to read. A resident cannot always tell whether it
asks for a report, for documents, or for nothing they can act on, or by when.
Official tools ask them to log in first. The food flow answers "where can I eat
today"; nothing yet answers "what does this letter want, and what can I do".

## Solution

A second screen at `/notice`, an equal front door beside Food today. The
resident picks a fictional sample letter or opens a letter file. The API reads
the text with no model in the path, names the letter's class from reviewed
triggers, finds the literal dates the letter mentions, and matches reviewed
policy passages. The screen shows the class, the dates to check, the reviewed
passages with their source and check date, and the letter's own text to read.
When no reviewed passage fits, it says so plainly and shows the help routes. The
letter's text and the reviewed guidance stay two separate things; no sentence on
screen is written by a model. No account, no eligibility question, and the site
never decides the case.

## User Stories

1. As a resident, I want to see what my letter appears to ask for, so that I can check it before I rely on a plan.
2. As a resident, I want the letter's kind named in plain words, so that I know whether it wants a report or documents.
3. As a resident, I want the dates my letter mentions pulled out, so that I do not miss a due date.
4. As a resident, I want to be told the dates are mine to confirm, so that I do not treat the site's reading as my deadline.
5. As a resident, I want guidance that a person reviewed, with its source and check date, so that I am not reading a machine's guess.
6. As a resident, I want each passage to say what I can do, so that I have a next step, not only a description.
7. As a resident, I want to be told the guidance is a demo draft to confirm with a caseworker, so that I do not rely on it as a ruling.
8. As a resident aged 60 to 64, I want to know that age alone does not create an 80-hour obligation, so that a general message does not frighten me.
9. As a resident, I want the site never to say I am exempt, eligible, approved, or denied, so that I am not misled about my case.
10. As a resident, I want to read the text the site pulled from my letter, so that I can check it read the letter correctly.
11. As a resident whose letter matches nothing reviewed, I want a plain statement and the help routes, so that I still have somewhere to turn.
12. As a resident, I want an honest "temporarily unavailable" with a retry if the letter cannot be read, so that I am not left with a spinner.
13. As a resident, I want the wait to show the same one-to-two-minute message and delayed status as the food flow, so that a long read does not feel broken.
14. As a resident on a shared computer, I want no account and nothing stored about me, so that my letter is not kept.
15. As a resident, I want to be warned not to send a real letter in the prototype, so that I do not upload sensitive documents before the pilot gates pass.
16. As a navigator, I want the same screen with no login, so that I can use it at a table with a resident.
17. As a judge, I want to open `/notice`, pick a sample, and see a reviewed reading, so that I can evaluate the second flow without setup.
18. As a maintainer, I want the passages in one reviewed file with a named owner and check date, so that I can correct guidance at the source.
19. As a maintainer, I want the screen to render only the file's passages and the letter's own text, so that a copy change cannot introduce a model's words.
20. As a developer, I want the letter files committed as fixtures, so that the extraction tests match what a resident would send.

## Implementation Decisions

- **Two provenances (decision 011).** The letter's text is resident-supplied and
  document-derived; a passage is reviewed guidance. They are shown side by side
  and never merged into one claim. No model writes any resident-facing text.
- **Letters (MOO-788).** Two fictional letter classes, a six-month report and a
  proof request, under `docs/research/notices/generated/` as `.txt` sources and
  `.pdf` built by `app/goodnext/scripts/generate_notice_pdfs.py`. Every name,
  case number, and date is invented and labeled fictional. The same PDFs are the
  demo samples under `apps/web/public/samples/`.
- **Reviewed passages (MOO-788).** `app/goodnext/policy_passages.json`, in the
  reviewed-source shape the food directory uses: a header with purpose and use
  rules, then passages each with a program, jurisdiction, topic, the passage,
  a resident action, triggers, source URL, check date, effective dates, version,
  review owner, review status, and uncertainties. Passages are drafted for the
  demo and marked as needing benefits-staff review before pilot.
- **Endpoint (MOO-790).** `POST /api/notices` takes one uploaded file. A PDF is
  read with pypdf; a PNG or JPEG scan goes to Amazon Textract behind a boundary,
  so an AWS failure returns the same honest 503 the plan endpoint returns. The
  endpoint classifies the letter, finds its literal dates, matches passages, and
  returns the shared envelope with `data`, `evidence` (matched passage ids), and
  `help_routes`. Unsupported file type is denied; an oversized file is denied.
- **Response handling (MOO-791).** The envelope drives the screen by `status`:
  success and no_match render the reading (no_match shows the plain sentence);
  temporarily_unavailable renders retry; denied renders a plain file message.
  All states end with the help routes.
- **Shared waiting (MOO-791).** The waiting and delayed states move out of the
  food page into one `Waiting` component both screens use; the food flow's
  behavior is unchanged.
- **One address (decision 008).** The browser posts to the relative `/api/notices`
  with credentials so the session cookie round-trips. No new cross-origin setup.
- **Copy.** All resident-facing strings live in the one copy module the never-list
  test scans. No model, vendor, or build names on screen.
- **Privacy.** No analytics, no storage, no cookies beyond the API's own session
  cookie. Nothing about the letter is kept.

## Testing Decisions

A good test checks what a resident or a caller can observe: an extracted text, a
class, a matched passage id, a status, a help route, a stripped internal field.

Three seams:

1. **Extraction and matching through the API test client.** New tests: the
   six-month-report PDF is classified and its due date found; the proof-request
   PDF is classified and dated; an unsupported type is denied; an oversized file
   is denied; an unreadable scan is a truthful 503 with help routes; a readable
   letter with no reviewed match is a no-match; internal trigger keywords are not
   in the response. The 503 answer carries `Cache-Control: no-store`, the fix the
   plan endpoint also needed.
2. **Render tests with saved envelopes.** New tests: success renders the class,
   the dates, the reviewed passage with its source and check date, and the help
   routes; no-match shows the plain sentence; temporarily_unavailable shows retry
   and re-sends the file; the delayed status appears at 30 seconds. One never-list
   scan covers the notice copy and the rendered notice page.
3. **Live.** One browser run of the dev server against the deployed or local
   runtime: pick the six-month-report sample, see the reading render, the session
   cookie on the request, and no cross-origin error; a screenshot is attached to
   the screen issue. This is the only live check and the only one that closes it.

## Out of Scope

- An agent workflow that explains the letter in its own words (MOO-789).
- Live resident upload of a real letter; the prototype accepts fictional samples
  only until the PRD's document and policy review gates pass.
- Additional notice classes beyond the six-month report and the proof request.
- The checklist, work plan, proof packet, reminders, and speech (later features).
- Spanish copy and the language control.
- Analytics of any kind.
- Any use of a real resident's document or data.

## Further Notes

The reviewed passages are prepared for the demonstration and are not legal
advice or an eligibility decision. Qualified benefits staff must review them
before any pilot use; the screen shows the draft status and routes case
decisions to official staff. The proof-request letter's layout follows the
official DMS proof-needed sample only as a layout reference; its text is
fictional and carries no real deadline.
