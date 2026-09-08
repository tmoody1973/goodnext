# Food today

Feature spec. September 8, 2026. Source decisions: `food-today-grill-notes.md`
(D1 to D12), `CONTEXT.md`, PRD 1.6 FR01 and FR04, decisions 003 and 004.
Triage: ready-for-agent (Linear status Todo) once ticketed.

## Problem Statement

A Milwaukee resident is short on food today. They may have no money, no
kitchen, and only a bus. Finding a pantry or meal means reading a dozen web
pages with hours that may be wrong, calling numbers that may not answer, and
never knowing whether the place has food or serves their neighborhood. Every
official tool asks them to log in or prove something first.

## Solution

One screen. The resident enters their ZIP, how much money they can spend
(zero is fine), what kitchen they have, and how they can travel. They get
today's listed options, each with its opening window, cost, requirements,
last-checked date, a directions link, and the honest line "We can't confirm
they have food today." If nothing is listed for their ZIP today, they see that
plainly, with three help routes and a way to try another ZIP. No account, no
notice, no benefits question, no promise of stock.

Under the hood the Bridge Plan for all seven days is still produced. This
feature promises and tests only Food today; days two to seven are shown
collapsed and belong to the next feature.

## User Stories

1. As a resident with no food today, I want to enter my ZIP and get options open today, so that I can eat today.
2. As a resident with no money, I want zero budget to be accepted, so that I only see free options and am never sent to a market I cannot afford.
3. As a resident with no kitchen, I want that known, so that pantry options warn me to ask for no-cook items.
4. As a resident who travels by bus, I want my travel limit shown back to me beside each option, so that I can judge the trip myself.
5. As a resident, I want a directions link that opens my own map app, so that I am not shown invented travel times.
6. As a resident, I want to see each option's opening window for today, so that I do not arrive at a closed door.
7. As a resident asking in the afternoon, I want options that already closed today not to be offered as today, so that I do not waste a bus fare.
8. As a resident, I want a closed-for-today option to show its next open window, so that I can plan the rest of the week.
9. As a resident, I want free and paid options labeled differently, so that I know before I go.
10. As a resident, I want requirements like photo ID or proof of address listed word for word, so that I bring what is needed.
11. As a resident, I want to know when an appointment is required and that nothing was booked for me, so that I call first.
12. As a resident, I want the date each record was last checked, so that I can judge how much to trust it.
13. As a resident, I want records checked more than two weeks ago marked "call to confirm," so that I phone before traveling.
14. As a resident, I want records checked more than two months ago kept out of today's options, so that stale listings do not send me somewhere gone.
15. As a resident, I want every option to say plainly that food on hand is not confirmed, so that I am not surprised by an empty pantry.
16. As a resident, I want a record whose service area is unknown shown as "confirm they serve your area," so that I neither miss it nor count on it.
17. As a resident whose ZIP is served by nothing today, I want a plain statement and three help routes, so that I still have somewhere to turn.
18. As a resident, I want to try a different ZIP after a no-match, so that I can search near work or family.
19. As a resident, I want the option to mark "I'll try this," so that my intention is remembered without being mistaken for food secured.
20. As a resident, I want the site never to say food is secured, reserved, or available, so that I am not misled.
21. As a resident using a shared library computer, I want no account and no personal identifiers requested, so that nothing about me is stored.
22. As a resident, I want the request to keep working if the agent is slow or down, with an honest "temporarily unavailable" and a retry, so that I am not left with a spinner.
23. As a resident, I want results in under half a minute for the demo case, so that the tool is usable in the moment.
24. As a navigator helping a resident, I want the same screen with no login, so that I can use it at a table with them.
25. As a maintainer, I want every option traceable to a directory record with a verifier and date, so that I can correct bad data at the source.
26. As a maintainer, I want closed or withdrawn records excluded automatically, so that a closure never reaches a resident.
27. As a reviewer, I want the resident-facing wording checked against a never-list by a test, so that a copy change cannot reintroduce a promise.
28. As a demo presenter, I want to pin today's date so the synthetic directory still has open windows on judging day, so that the demo does not show no-match by accident.
29. As an operator, I want the pinned date refused outside demo environments, so that a resident never sees a fake today.
30. As a developer, I want the agent to reference only resource IDs the tools returned, so that a made-up pantry can never reach the screen.
31. As a developer, I want a violating visit stripped and the response marked partial, so that one bad suggestion does not hide the good ones.
32. As a developer, I want the API to own dates and request IDs, so that a browser cannot forge either.
33. As a product owner, I want Food today shipped before notice uploads, so that the community-benefit demo has a working base.

## Implementation Decisions

- **Feature boundary (D1).** The agent and API return the full Bridge Plan; acceptance covers Food today only. The website shows today expanded and days two to seven collapsed and unlabeled as promises.
- **Today (D2).** An option is Food today only if it has an opening window dated today that is still open or opens later, judged by the server's America/Chicago clock. The search tool receives the current local time along with the date range. A window that already closed yields the resource's next open window instead.
- **Pinned date (D3).** The API reads an environment setting that fixes today's date and time for demo and test runs. It is honored only when the environment is marked demo; otherwise it is ignored and the real Milwaukee clock is used.
- **ZIP matching (D4, decision 004).** Exact match against the record's served-ZIP list. No neighbor or radius logic.
- **Unknown service area (D5).** A record with no served-ZIP data is returned by the search tool marked conditional and carries the confirm-service-area instruction. It is never a confirmed Food today visit.
- **Travel (D6).** Each option carries the record's address and a directions link built from the address. No distance, time, or fare field exists in the response. The resident's stated travel modes and limit are echoed in the response so the interface can show them beside each option.
- **Verification tiers (D7).** The search tool assigns each record a freshness tier from its last-verified date relative to today: verified (0 to 14 days), call-to-confirm (15 to 60 days), unconfirmed (over 60 days or no date). The validator strips unconfirmed-tier visits from Food today; the response lists them separately as unconfirmed with a phone number.
- **Option states (D8).** The response marks each entry as a listed option. Planned visit and confirmed food are resident actions recorded by later features; this feature reserves the vocabulary and never emits "secured" or "covered."
- **Permitted claims (D9).** The eight allowed statements are rendered from record fields, never free text from the model. Claims 6 and 8 are always present. The never-list is a constant checked by a test.
- **No-match (D10, D11).** Status no_match returns three fixed help routes (2-1-1, Hunger Task Force emergency food, FoodShare member line) as structured entries, no visits, and no out-of-area records.
- **Contract shape.** The existing response envelope (status, data, evidence, missing, warnings, retryable, request ID) is unchanged. The plan's day entries gain a freshness tier and a next-open field per visit; the envelope gains a help-routes list used on no-match.
- **Ledger.** The request-scoped record of tool-returned IDs remains the fabrication check (decision from the first build session).
- **Prompts.** P01 and P03 stay verbatim from the APIs doc. The task text supplied by the server gains the current local time and the pinned-date flag; the system prompt does not change.

## Testing Decisions

A good test checks what a resident or a caller can observe: a returned record, a status, a label, a stripped visit, a help route. It does not check how the ledger is stored or which function called which.

Three seams, confirmed with Tarik:

1. **Tool and validator functions with the fixture directory.** Prior art: the eleven existing agent tests. New tests: closed-earlier-today is not open today and next-open is carried; empty service area returns conditional; freshness tiers assigned at 14 and 60 days and for a missing date; unconfirmed-tier visit stripped from Food today.
2. **API endpoint through the test client with a fake agent.** Prior art: the six existing API tests. New tests: pinned date honored in demo and refused elsewhere; no-match carries three help routes; every resident-facing string in a success and a no-match response contains claims 6 and 8 and none of the never-list words.
3. **Live.** One real request through the deployed API and AgentCore Runtime with Sonnet 4.6 for ZIP 53206 at zero budget returns success, its evidence IDs match the ledger, and the response is attached to the Linear issue as evidence. This is the only live check and the only one that closes the issue. All other tests are fixture tests and are labeled so in the issue.

Existing tests that already cover this spec are kept, not rewritten: closed and out-of-area excluded, unserved ZIP is no_match, paid unsuitable at zero budget, unreturned ID refused, fabricated ID and paid-at-zero and no-window-day stripped, server dates and ignored client fields, outage 503.

## Out of Scope

- Days two to seven of the Bridge Plan: coverage gaps, visit limits across days, backups (feature 2).
- The Food today screen itself; this spec covers the agent and API behavior. The website follows the Impeccable shape pass.
- Neighboring-ZIP or radius search (211 adapter feature, decision 004).
- Live 211 data; the fixture directory stands in.
- Notice upload, checklist, work plan, proof packet, reminders, speech.
- Planned-visit and confirmed-food recording as resident actions.
- Any use of real resident documents or data in verification.

## Further Notes

Only synthetic fixture records are used. The fixture is labeled synthetic in
the file and must stay so. The 211 distance parameter is unverified until
someone with credentials checks it; that is a task in the 211 adapter feature,
not here. The demo clock setting must be documented in the README so a judge
running setup instructions knows why the date is fixed.
