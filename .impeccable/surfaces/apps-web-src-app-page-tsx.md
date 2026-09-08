---
version: 1
slug: "apps-web-src-app-page-tsx"
primary_target: "apps/web/src/app/page.tsx"
related_targets: []
---

# Food today screen: surface brief

Scope: route `/` of `apps/web` (Next.js 16 static export, Tailwind 4). Visitor mode: Operate. Help-route and delay copy use Read register.

## Job and audience
A Milwaukee resident short on food today, on a phone or a shared library computer, often anxious, with no money and a bus. Second audience: a navigator using the same screen beside a resident, no login. The job: know which listed options are open today, what they cost, what to bring, how fresh the record is, and get directions in their own map app.

## Outcome and proof
Enter four things (ZIP, money, kitchen, travel plus optional minutes); get today's listed options. Each card renders the eight permitted claims from the API's `claims` object and nothing else: open-today text, cost label, requirements, appointment, freshness (check date and tier word), inventory caveat, service-area caveat, travel echo, directions link, source line. Proof is the check date and tier word on every card. Success: the resident reaches an open door today without a false promise.

## Selected direction: The 7-Day Forecast Strip
Chosen by Tarik 2026-09-08 over the rolled Checkout Receipt (seed a5fbc27f). Approved comp: `.impeccable/mocks/decision/model-pick.webp`.
- Structural thesis: today is the big panel; the next six days are small tiles. Days two to seven are collapsed by default and never presented as promised.
- Sequence: wordmark plus "Not a government service"; the four-question form (first visit) which collapses to a one-line summary with Change after a result; the today heading with the date and a count of listed options; one card per option with a time block on the left; the six-tile strip; the help-route footer.
- Focal moment: the date and count in the header ("2 listed today").
- Signature interaction: tapping a day tile expands that day inline beneath the strip; only one day open at a time; tiles say "listed", never "open" or "secured".
- Consequences: three reusable pieces (time block, option card, day tile); a restrained palette with one navy field for the header, white cards, and amber reserved for actions and the count; status always in words, color secondary.
- What must not be literalized from the comp: the footer phone numbers and URLs (they come from the API help routes), the icons, the "in Milwaukee" line, the exact per-day counts.

## Scope and boundaries
Production-ready single route with all states. Untouched: the API contract, the agent, the fixtures. Anti-goals: no map embed, no travel time or distance, no account, no cookies beyond the API session cookie, no analytics, no eligibility questions, no never-list words (secured, reserved, available, confirmed food, sorted, handled, booked, obtained), no Strands or AWS names on screen.

## States and ranges
- Idle: form only, ZIP focused, money defaults to 0, kitchen and travel as segmented choices.
- Submitting: visible feedback within one second; a plain progress line ("Checking today's listings for 53206").
- Delayed (after 30 s): "This is taking longer than usual. We are still checking." with Cancel, and the three help routes shown beneath so no one waits on a spinner.
- Success: 1 to 6 options today (fixture range); provider names up to ~60 characters; requirements up to five lines; two long uncertainty lines. Each card shows its claims verbatim.
- Partial: same as success plus the warnings list in plain words above the cards.
- No-match: the plain statement, the three help routes as cards, and a Change ZIP action that reopens the form with ZIP focused.
- Unconfirmed list: below today's cards, name and phone only, labeled unconfirmed, never a card.
- Temporarily unavailable: one sentence, Retry, help routes.
- Needs clarification or denied: treated as "we could not build a list", help routes, Change.
- Validation: ZIP must be five digits; inline message, no submit.
- Cancelled: form returns with values kept.

## Interaction and layout
Single column to 640 px; at wider widths the form becomes a row and cards keep a fixed max width. Time block left, provider and claims right, Directions as the card's one amber action, phone as a text link. Keyboard order follows reading order; visible focus rings; the today heading is a live region announcing the result count; day tiles are buttons with expanded state; reduced motion removes the expand animation. Reflows at 320 px and 200 percent zoom without hiding the next action.

## Constraints and open decisions
- Static export; API base URL from a public env var; browser calls `POST /api/plans` with credentials for the session cookie.
- English only; strings in one file so Spanish is a later ticket; layout tolerates 30 percent text expansion.
- Open for the grill: what the day tiles show; whether Print is kept from the receipt idea; where the source line sits on a card; how the summary bar reads; whether cancel aborts the request or only the wait.
