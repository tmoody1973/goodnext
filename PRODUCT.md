# Product
<!-- impeccable:product-schema 1 -->

## Platform
web

## Users
A Milwaukee resident who is short on food today. Often on a phone, sometimes at a shared library computer, frequently anxious, short on time, possibly with no money, no kitchen, and only a bus. The job: find a place that is open today, free or affordable, that serves their area, and know what to bring. A second confirmed audience is a navigator at a table with a resident, using the same screen with no login.

## Product Purpose
GoodNext is a free website that helps a Wisconsin household find food today and prepare an official next step after a FoodShare notice. The first shipped feature is Food today: enter ZIP, money, kitchen, and travel; get today's listed options with opening window, cost, requirements, last-checked date, and a directions link. Success is a resident reaching a real open door today without being misled about stock, eligibility, or distance.

## Positioning
Every option on screen traces to a directory record with a named verifier and a check date, and the site renders only eight permitted statements from record fields, never free text from the model. It never asks for an account, a notice, or a benefits question before helping with food. Official tools ask residents to prove something first; GoodNext does not.

## Operating Context
- Hackathon entry, "Agents for Humans", deadline September 14, 2026, 7 p.m. Central; judging through October 8. Judges will run the site and read the repo.
- Backend: a Strands agent on Amazon Bedrock AgentCore behind a FastAPI service exposing `POST /api/plans`. A plan currently takes 60 to 105 seconds; a first-day-only response is a planned follow-up.
- Directory data: 16 records reviewed by Tarik Moody on 2026-09-08 (verified tier), 68 from the Milwaukee Food Environment Map (data as of 2024-08-27, source line required on every card), and 9 labeled synthetic records.
- Demo clock: the API pins "today" only when the environment is marked demo. Fixture windows cover 2026-09-08 to 2026-09-21.
- Tracker is Linear (team MOO); specs and decisions live in this repo under `docs/`.

## Capabilities and Constraints
- The screen calls `POST /api/plans` with `{ workflow: "food_today", constraints: {...} }` and receives the shared envelope: `status` (success, partial, needs_clarification, no_match, denied, temporarily_unavailable), `data`, `evidence`, `missing`, `warnings`, `retryable`, `request_id`, `help_routes`.
- `data.food_today` and `data.days[0].visits` carry each visit's `claims` object: `open_today_text`, `cost_label`, `requirements_text`, `appointment_text`, `freshness_text`, `inventory_text`, `service_area_text`, `travel_text`, `directions_url`, `travel_echo`, `source_text`. The screen renders these fields and nothing the model wrote.
- Days two to seven exist in the response; shown collapsed and never presented as promised.
- Confirmed for this first screen (Tarik, 2026-09-08): the form asks four things only: ZIP, money to spend (zero valid), kitchen (full, microwave only, none), travel modes plus optional minutes. Other constraint fields take API defaults.
- Confirmed: English only on this screen; Spanish is a separate ticket. Layout must survive Spanish text expansion.
- Confirmed: build path is code-first.
- Terminology is fixed in `CONTEXT.md`: Food today, Bridge Plan, opening window, next open, service area, verified, call to confirm, unconfirmed, directions link, listed option, help route, no-match. Each term has an avoid-list.
- Never-list, enforced by test: the site never says food is secured, reserved, available, confirmed, sorted, handled, booked, or obtained. It never decides eligibility or promises stock.
- No account, no cookies beyond the API's own session cookie, no personal identifiers requested. Nothing about the resident is stored by the site.
- Static export: the site is plain files served from a CDN; all API calls happen from the browser.
- Undecided: public hosting for the API and site; the latency fix; Spanish.

## Brand Commitments
- Name on screen: GoodNext. Docs still say "FoodShare Bridge"; the screen never does.
- No logo or wordmark asset exists. Text wordmark only until one is made.
- Voice: calm, respectful, concrete action labels, visible source dates. Plain English. The site must read as distinct from an official government service and say so.

## Evidence on Hand
- Live response samples: `docs/evidence/moo-777-live-53206-2026-09-09-demo.json`, `docs/evidence/moo-778-live-53206-2026-09-10-demo.json`.
- Directory fixtures: `app/goodnext/fixtures/`.
- Feature spec for the agent and API: `docs/specs/food-today.md`; grill notes D1 to D12 alongside it.
- PRD: `docs/FoodShare-Bridge-PRD.md`, sections 4, 5 (FR04), 7, 8, 14 (UX01 to UX08).
- No testimonials, no usage numbers, no partner logos. Do not fabricate any.

## Product Principles
1. A listing is never a promise. Every card says food on hand is not confirmed.
2. Show the check date, the verifier tier, and the source on every option.
3. Help before proof: no account, notice, or eligibility question stands between a resident and today's options.
4. When the site cannot help, hand off to a human route, never to a dead end.
5. The resident judges the trip; the site gives an opening window and a directions link, never a travel time.

## Accessibility & Inclusion
PRD NFR03 and UX06: keyboard order, visible focus, screen-reader labels and announcements, contrast, reflow at 320 CSS pixels, 200 percent text zoom, reduced-motion respected, status conveyed in text as well as color. Must work on a shared library computer and a low-end phone.
