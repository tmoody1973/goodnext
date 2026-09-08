# Food today screen

Feature spec. September 8, 2026. Source decisions:
`food-today-screen-grill-notes.md` (S1 to S12), the surface brief at
`.impeccable/surfaces/apps-web-src-app-page-tsx.md`, `CONTEXT.md`, decisions
007 and 008, `docs/specs/food-today.md` (agent and API behavior), PRD 1.6
FR04, UX01 to UX03, UX06, UX07, section 8.
Triage: ready-for-agent (Linear status Todo) once ticketed.

## Problem Statement

The GoodNext agent and API already answer "where can I get food today in my
ZIP" with honest, dated listings, but nothing a resident can open exists. A
Milwaukee resident on a phone or a library computer has no screen to type a
ZIP into, and a judge has nothing to click. The answer also takes one to two
minutes to arrive, which on a bare page feels like the site is broken.

## Solution

One screen at the site's front door. The resident answers four questions:
ZIP, money they can spend (zero is fine), what kitchen they have, how they
travel. The screen says plainly that checking takes one to two minutes, and
after 30 seconds adds a delayed status with a cancel and the three help routes.
When the plan arrives, Food today is the big panel: one card per listed
option, its opening window in a time block, its cost, requirements, check date
and tier word, the line "We can't confirm they have food today", a directions
link that opens the resident's own map app, and the phone number. Later this
week is six small tiles that say how many options are listed each day and
unfold one at a time. If nothing is listed for the ZIP today, the screen says
so and shows the three help routes and a way to change ZIP. No account, no
notice, no eligibility question, no promise of stock.

## User Stories

1. As a resident, I want to type my ZIP and answer three quick questions, so that I get today's options without reading a manual.
2. As a resident with no money, I want zero to be the default money answer, so that I only see free options.
3. As a resident, I want kitchen offered as three plain buttons, so that I do not have to describe my situation in words.
4. As a resident, I want to pick one or more ways I travel, so that the travel echo beside each option matches how I actually get around.
5. As a resident, I want to be told if I forgot to pick how I travel, so that a silent default does not shape my plan.
6. As a resident, I want a wrong ZIP caught before anything is sent, so that I do not wait two minutes for an error.
7. As a resident, I want the screen to react within one second of pressing the button, so that I know it heard me.
8. As a resident, I want to be told up front that checking takes one to two minutes, so that I do not assume the site is stuck.
9. As a resident, I want a delayed status after 30 seconds with the help routes beside it, so that I always have somewhere to turn while waiting.
10. As a resident, I want to cancel the wait and get my answers back in the form, so that I can change something without retyping.
11. As a resident, I want today's date and the number of listed options at the top, so that I know at a glance whether today has anything.
12. As a resident, I want each option's opening window as the biggest thing on its card, so that I can judge whether I can make it.
13. As a resident, I want free and paid labeled differently, so that I know before I go.
14. As a resident, I want requirements like photo ID listed word for word, so that I bring what is needed.
15. As a resident, I want to be told when an appointment is required and that nothing was booked, so that I call first.
16. As a resident, I want to see "confirm they serve your area" when the site is not sure, so that I neither miss the option nor count on it.
17. As a resident, I want the check date and a tier word on every card, so that I can judge how much to trust it.
18. As a resident, I want "call to confirm" shown with the phone number when a record is older than two weeks, so that I phone before traveling.
19. As a resident, I want every card to say food on hand is not confirmed, so that an empty pantry does not surprise me.
20. As a resident, I want my travel choices echoed beside each option, so that I can judge the trip myself.
21. As a resident, I want a directions link that opens my own map app, so that I am not shown invented travel times.
22. As a resident, I want the phone number on the card as something I can tap, so that I can call from the same screen.
23. As a resident, I want to see where a record's information came from, so that I know it is not the site's own guess.
24. As a resident, I want records not checked in over two months listed by name and phone only, under a plain heading, so that stale listings do not send me somewhere gone.
25. As a resident, I want later days shown as small tiles with a count, so that I can see the week without it competing with today.
26. As a resident, I want a tile to unfold and show that day's places with their hours, so that I can plan a bus trip for later in the week.
27. As a resident, I want later days worded as "listed", so that I never mistake a listing for a promise.
28. As a resident, I want only one later day open at a time, so that the screen stays short on a phone.
29. As a resident whose ZIP has nothing today, I want a plain statement and three help routes, so that I still have somewhere to turn.
30. As a resident, I want to change my ZIP after a no-match and try again, so that I can search near work or family.
31. As a resident, I want the help routes at the bottom of every result, so that a human is always one tap away.
32. As a resident, I want an honest "temporarily unavailable" with a retry if the agent is down, so that I am not left with a spinner.
33. As a resident, I want a plain sentence when some suggestions were left out, so that I am not shown developer messages.
34. As a resident, I want to print today's list, so that I can carry it from a library computer.
35. As a resident, I want the site to say it is not a government service, so that I do not confuse it with my FoodShare case.
36. As a resident, I want the site never to say food is secured, reserved, or available, so that I am not misled.
37. As a resident using a shared computer, I want no account and nothing asked about me, so that nothing about me is stored.
38. As a resident on a small phone, I want the page to work at 320 pixels wide and at 200 percent zoom, so that the next action is never hidden.
39. As a resident who uses a keyboard or a screen reader, I want a sensible order, visible focus, and the result count announced, so that I can use the screen without a mouse.
40. As a resident who prefers less motion, I want the unfold to happen without animation, so that the screen respects my setting.
41. As a navigator, I want the same screen with no login, so that I can use it at a table with a resident.
42. As a demo presenter, I want the heading date to come from the API, so that the pinned demo date shows correctly.
43. As a maintainer, I want the screen to render only the API's permitted claims, so that a copy change cannot reintroduce a promise.
44. As a maintainer, I want every resident-facing string in one file, so that the never-list test can scan it and Spanish can follow.
45. As a maintainer, I want the site and the API on one address, so that the session cookie works without cross-origin setup.
46. As a developer, I want the dev server to proxy the API, so that the screen runs locally against the local or deployed runtime.
47. As a developer, I want render tests driven by real saved responses, so that the tests match what the agent actually sends.
48. As a developer, I want the web typecheck, tests, and build in CI, so that a broken screen cannot reach main.
49. As a judge, I want to open the site, type 53206, and see a real plan, so that I can evaluate the entry without setup.
50. As a product owner, I want later-week fixes and Spanish kept out of this slice, so that the screen ships before the deadline.

## Implementation Decisions

- **Placement (S1, decision 008).** A Next.js 16 application in the web app directory, built as a static export with Tailwind 4, managed with pnpm. One route at the root. The browser calls the relative path `/api/plans`; the site and the API share one hostname. In development the Next dev server proxies `/api/*` to the FastAPI service on port 8000.
- **Request.** The form posts `{ workflow: "food_today", constraints }` with `zip_code`, `budget_usd`, `kitchen`, `travel`, and `max_travel_minutes` when given. All other constraint fields take the API defaults. The request carries credentials so the API session cookie round-trips.
- **Response handling.** The shared envelope drives the screen by `status`: success and partial render the plan; no_match renders the no-match state with `help_routes`; temporarily_unavailable renders retry; needs_clarification and denied render "we could not build a list" with help routes and Change. The heading date is `data.start_date`.
- **Today's cards (S10).** Each visit in the first day renders only its `claims` object plus `contact`: time block from `open_today_text`, then provider, `cost_label`, `requirements_text`, `appointment_text` if non-empty, `service_area_text` if non-empty, `freshness_text`, `inventory_text`, `travel_echo` small, Directions from `directions_url`, phone as a tel link, `source_text` last and smallest when non-empty.
- **Later this week (S3).** Days two to seven render as six tiles: weekday, date, "N listed". One tile unfolds at a time; the unfolded day renders each visit's provider, `schedule_text`, cost label, `freshness_text`, phone, and directions. No `open_today_text`, no inventory line, no next-open text for later days.
- **Unconfirmed list (S7).** `data.unconfirmed` renders under today's cards with the heading "Not checked recently. Call before you go.", name and phone only.
- **Partial (S11).** One fixed sentence above the cards; `warnings` are not shown.
- **Waiting and delayed status (S4).** From submit the screen shows "This usually takes one to two minutes." At 30 seconds it adds the delayed status: "Still checking. You can wait, or use one of these help routes.", the three help routes, and Cancel. Cancel aborts the browser request only and returns the form with values kept.
- **Help routes (S2).** Rendered from `help_routes` whenever the list is non-empty. A separate agent ticket makes the envelope carry the three routes on every status; until then the footer appears only on no-match.
- **Form (S9).** ZIP five digits, validated before send. Money whole dollars, default 0. Kitchen three buttons, default full. Travel four toggles, none preselected, at least one required, optional minutes. After a result the form collapses to a summary line with Change; Change reopens the form with values kept.
- **Print (S6).** A "Print this list" link that prints today's cards and help routes; the print stylesheet hides the form and the tiles.
- **Copy.** All resident-facing strings live in one copy module. No Strands, AWS, or internal names on screen. The wordmark and "Not a government service" appear at the top of every state.
- **Visual direction (decision 007).** The 7-Day Forecast Strip: restrained palette, one navy header field, white cards, amber only for actions and the count, status always in words. Three reusable pieces: time block, option card, day tile. The direction contract lives in the root layout as a comment; DESIGN.md is written when the build finishes.
- **Accessibility.** Reading order equals keyboard order; visible focus; the result heading is a live region; tiles are buttons with expanded state; reduced motion removes the unfold animation; reflow at 320 pixels and 200 percent zoom.
- **Privacy.** No analytics, no storage, no cookies beyond the API's own session cookie.
- **CI.** The existing workflow gains a web job: install, typecheck, test, build.

## Testing Decisions

A good test checks what a resident sees for a given API response: a heading,
a card line, a tile count, a help route, a message. It does not check component
internals, class names, or which hook fired.

Three seams, confirmed with Tarik in the grill (S12):

1. **Render tests with saved responses.** The live evidence files already in the
   repo are the fixtures; a small set of hand-written envelopes covers no-match,
   partial, temporarily unavailable, and a delayed wait with a faked clock. Prior
   art: the fixture-only agent tests, which never reach Bedrock. New tests: success
   renders one card per today visit with the claims in order; a later-day tile
   shows the listed count and unfolds to `schedule_text`; no-match shows the
   statement, three help routes, and Change ZIP; partial shows the fixed sentence
   and no warnings; temporarily unavailable shows Retry; the delayed status
   appears at 30 seconds with Cancel; Cancel returns the form with values kept;
   the form refuses a four-digit ZIP and an empty travel choice.
2. **Never-list scan.** One test reads the copy module and every fixture-rendered
   page and fails on any of the seven NEVER_LIST terms or the CONTEXT.md
   avoid-words. Prior art: the agent's never-list test.
3. **Live.** One browser run of the dev server with the API pointed at the
   deployed runtime, ZIP 53206 at zero budget: the plan renders, the console
   shows no cross-origin errors, the session cookie is present on the request,
   and a screenshot is attached to the Linear issue. This is the only live check
   and the only one that closes the screen issue.

## Out of Scope

- Fixing the agent's per-day claims for days two to seven (own ticket).
- Making the API return help routes on every status (own ticket).
- Judge-facing hosting and the `/api/*` routing rule (handoff step 3).
- Latency work: day-one-first responses, prompt caching.
- Spanish copy and the language control.
- Planned-visit and confirmed-food actions; notice upload; anything after Food today.
- Analytics of any kind.
- Any use of real resident data in verification.

## Further Notes

The four direction mockups under `.impeccable/mocks/decision/` are direction
tests, not copy: their footer phone numbers and web addresses were invented by
the image model. The real help routes come only from the API.

The demo clock is set on the API, not the site; the README's setup note for
judges covers it.
