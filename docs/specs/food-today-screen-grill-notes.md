# Food today screen: grill notes

September 8, 2026, 14:09 to 14:15 CDT. Plan under test: the surface brief at
`.impeccable/surfaces/apps-web-src-app-page-tsx.md` (direction: decision 007).
Tested against `CONTEXT.md`, decisions 003 to 007, PRD sections 8 and 14, and
the API and agent code. Tarik took every recommendation.

## Summary for to-spec

One route, `/`, in `apps/web` (Next.js 16 static export, Tailwind 4, pnpm).
The browser calls the relative path `POST /api/plans`; site and API share one
hostname (decision 008). The screen renders only the API's `claims` fields for
today and the record's `schedule_text` for later days. Every state is covered:
idle, submitting, delayed status, success, partial, no-match, unconfirmed list,
temporarily unavailable, needs clarification or denied, bad ZIP, cancelled.
Three test seams: render tests on saved evidence responses, a never-list scan of
the copy file, one live browser run that closes the issue.

## Settled by existing documents (no question asked)

- Feature boundary, today rule, pinned date, ZIP matching, unknown service
  area, travel without routing, verification tiers, option states, permitted
  claims, no-match with three help routes: `docs/specs/food-today.md` D1 to D11.
- Direction and mode: decision 007, Operate mode, code-first.
- Form scope (four questions), English only: PRODUCT.md, confirmed by Tarik.
- Package manager pnpm 10 (installed); the heading date comes from the API's
  `start_date`, never the browser clock, so the demo clock shows correctly.

## Facts found in code that shaped the questions

- The API session cookie is SameSite=Strict and the API has no CORS setup:
  `services/api/goodnext_api/main.py`.
- For days two to seven, each visit's `claims.open_today_text` is computed
  against today's clock and is wrong for future days; `schedule_text` is right.
  Evidence: `docs/evidence/moo-777-live-53206-2026-09-09-demo.json`. Agent bug,
  own ticket.
- `help_routes` is empty on success and partial responses; only no-match fills
  it. `app/goodnext/help_routes.py` is the single reviewed source.
- `NEVER_LIST` in `app/goodnext/claims.py` has seven terms: in stock, reserved,
  available, guaranteed, confirmed for you, secured, food covered.

## Decisions

### S1 One address for site and API (Q1)
Same hostname; `/api/*` routed to the API; dev server proxies to port 8000.
No API change. Decision 008.

### S2 Help routes on every response (Q2)
Agent-side change: the envelope always carries the three help routes. Own
ticket with a fixture test. Until it ships the footer renders only when the
list is non-empty. The site never carries its own copy of the routes.

### S3 Later this week tiles (Q3)
Six tiles, weekday and date plus "N listed". Tapping unfolds that day beneath
the strip, one day at a time: provider, `schedule_text`, cost label, freshness
text, phone, directions. No inventory line, no next-open text for later days.
Term added to CONTEXT.md: Later this week.

### S4 Waiting, delayed status, cancel (Q4)
From submit: "This usually takes one to two minutes." At 30 seconds: "Still
checking. You can wait, or use one of these help routes." plus the routes and
Cancel. Cancel aborts the browser wait only; the form returns with values kept.
Term added to CONTEXT.md: Delayed status.

### S5 Source and verifier (Q5)
`source_text` shown as the last, smallest line when present. Verifier name not
shown; no API change.

### S6 Print (Q6)
"Print this list" link; print stylesheet hides form and tiles, prints today's
cards and help routes.

### S7 Unconfirmed list (Q7)
Under today's cards, heading "Not checked recently. Call before you go.", name
and phone only, never a card.

### S8 Glossary (Q8)
"Later this week" and "Delayed status" added to CONTEXT.md.

### S9 Form defaults (Q9)
ZIP five digits; money whole dollars default 0; kitchen three buttons default
full; travel four toggles, none preselected, at least one required, optional
minutes.

### S10 Card claim order (Q10)
Time block left. Right column: provider, cost, requirements, appointment (if
any), service-area caveat (if any), checked date with tier word, "We can't
confirm they have food today", travel echo small, Directions and phone, source
line last.

### S11 Partial responses (Q11)
One fixed sentence above the cards: "Some suggestions were left out because
they did not pass our checks." Warnings not shown.

### S12 Test seams (Q12)
1. Render tests with saved evidence responses as fixtures (success, no-match,
   partial, temporarily unavailable, delayed).
2. Never-list scan over the copy file: the seven NEVER_LIST terms plus the
   CONTEXT.md avoid-words.
3. One live browser run: local dev server, API pointed at the deployed runtime,
   ZIP 53206, screenshot attached to the Linear issue. Only this closes it.

## Carried to separate tickets (not the screen)

- Agent: per-day claims for days two to seven use that day's date.
- Agent: help routes on every envelope status.
- Hosting with a path rule for `/api/*` (handoff step 3).
- Spanish copy and language control (PRD UX05).
- CI: add web typecheck, test, and build to `.github/workflows/ci.yml`.

## Open questions

None.
