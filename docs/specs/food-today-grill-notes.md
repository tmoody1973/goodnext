# Food today — grill session notes

Working notes for the to-spec step. September 8, 2026. Settled decisions,
open questions, and acceptance conditions as they are agreed. Not the spec.

## Summary for to-spec

Feature: a resident enters a ZIP, budget, kitchen, and travel modes and sees
today's listed options or an honest no-match, with no account or notice.
Twelve decisions D1 to D12 below are settled. Vocabulary is in CONTEXT.md.
Acceptance conditions A1 to A13 and the fifteen observable tests in D12 are
the contract. The only live test (15) closes the Linear issue. Synthetic
fixture data only; no real resident data in any verification.

## Settled by existing documents (no question asked)

- PRD FR01, FR04: no account, notice, or benefits question before food help; intake fields; per-visit fields; free vs paid labeled; zero budget never relies on a purchase; unknown constraints flagged, not assumed.
- APIs doc sections 1, 3, 4: a listing is not a reservation or stock; inventory unknown is separate from opening hours; response envelope statuses; tools `find_food_resources` and `check_food_constraints`.
- Tech Stack section 5: no routing service in the first release; travel times unknown, not invented.
- 211 plan: fixture directory for the demo; live 211 adapter is a separate feature.

## Decisions

### D1 Feature boundary (Q1)
The first feature promises Food today only: today's options and the no-match outcome. The agent, API, and site keep producing and showing all seven days; days two to seven are not covered by this feature's acceptance criteria and become feature 2 (Bridge Plan).

### D2 Today after closing time (Q2)
A Food today option needs an opening window dated today that is still open or opens later, judged by the server's America/Chicago clock. A window that already closed is not Food today; the resource is shown with its next open window instead.

### D3 Pinned date for demos and tests (Q3)
The API honors an environment setting that pins "today" for demo and test runs. The fixture keeps dated windows. The setting is refused outside demo environments.

### D5 Unknown service area (Q5)
A record with no served-ZIP information is shown as conditional with "confirm they serve your area" and is never a confirmed Food today visit. Unknown is not no.

### D4 ZIP matching (Q4)
Exact served-ZIP list matching in this feature. Neighboring-ZIP or radius search is part of the 211 adapter feature: verify the 211 Search V2 "distance from location" parameter first (publicly advertised, details unverified behind portal login); fall back to Census ZCTA Gazetteer centroids (public domain, ~1 MB) with straight-line distance labeled "straight line, not a route," handling PO-box ZIPs that have no Census area. No ready-made US ZIP adjacency dataset with a clear license was found. See docs/decisions/004.

### D6 Travel without routing data (Q6)
Each option shows its address and a directions link to the resident's own map app. Travel time is "unknown, check the map." The resident's stated travel limit is echoed beside each option and never filters results. No distances, times, or fares are computed or shown.

### D7 Verification age (Q7)
Verified within 14 days: shown plainly with the date. 15 to 60 days: shown with "call to confirm, last checked DATE." Over 60 days or no date: never a Food today visit; listed as Unconfirmed with the phone number only.

### D8 Three states of an option (Q8)
Listed option: returned by the directory and passes the rules. Planned visit: a listed option the resident marked "I'll try this." Confirmed food: what the resident reports receiving after a visit. Only Confirmed food counts toward food covered. Nothing is ever shown as "food secured."

### D9 Permitted claims (Q9)
1. "Open today from H:MM to H:MM" only with a still-open window dated today.
2. Cost label from the record: Free, Paid, Sliding scale. Always shown.
3. "May require: …" listing the record's requirements verbatim.
4. "Appointment required, not booked" when the record says so.
5. "Last checked DATE" / "Call to confirm" / "Unconfirmed" per D7.
6. "We can't confirm they have food today." Always shown on every option.
7. "Confirm they serve your area" when service area is unknown (D5).
8. "Travel time unknown, check the map." Always shown (D6).
Never: in stock, reserved, available, guaranteed, confirmed for you, secured, or any item count. A test scans resident-facing strings for the never-list.

### D10 No-match presentation (Q10)
Plain statement naming the ZIP and date. Three fixed help routes: 2-1-1, Hunger Task Force emergency food page, FoodShare member line. Offer to try another ZIP. Show later-in-week windows if any exist. No apology copy.

### D11 Out-of-area options on no-match (Q11)
Not shown in this feature. Folded into the Q4 neighboring-ZIP decision.

### D12 Observable tests (Q12)
Fifteen tests adopted. Tool boundary (fixture): closed/out-of-area excluded; unserved ZIP is no_match; closed-earlier-today window not open today and next-open carried; empty service area returned conditional; freshness tiers assigned; paid unsuitable at zero budget; unreturned ID refused. Validator (fixture): fabricated ID, paid-at-zero, no-window-day stripped; unconfirmed-tier stripped from Food today. API (fixture): server dates and ignored client dates; pinned date honored in demo and refused elsewhere; no-match carries three help routes; never-list scan plus claims 6 and 8 present; agent outage is a truthful 503. Live: one real request through deployed API and AgentCore Runtime returns success for 53206 at zero budget with ledger-matching evidence, saved as issue evidence. Only the live test closes the Linear issue.

## Open questions

None for this feature. Frontier closed September 8, 2026.

## Carried to later features

- 211 adapter: confirm the Search V2 distance parameter name, units, and maximum with the real credentials; decide radius vs. exact list for live data.
- Bridge Plan (feature 2): visit limits across days, backups, coverage gaps, weekly schedules with exceptions instead of dated windows.
- Website: the Food today screen, the collapsed days two to seven, the never-list scan on rendered copy, Impeccable shape pass first.

## Acceptance conditions (draft, grows each round)

- A1 A request with a served ZIP and at least one open window today returns status `success` with one or more Food today visits.
- A2 Every Food today visit references a resource the tools returned, is free when budget is zero, and has an opening window dated today.
- A3 A window that closed before the request time is not a Food today visit; the resource appears with its next open window.
- A5 A resource with no served-ZIP data appears only as conditional, carrying a confirm-service-area instruction.
- A6 No option displays a travel time, distance, or fare; each shows an address and a directions link; the resident's travel limit is echoed verbatim.
- A7 A record verified over 60 days ago, or with no verification date, never appears as a Food today visit.
- A8 A record verified 15 to 60 days ago carries a call-to-confirm note with the verification date.
- A9 Every option's resident-facing text contains claim 6 and claim 8 and none of the never-list words.
- A10 The response distinguishes listed options from planned visits; no field or label reads "secured" or "covered" for a listed option.
- A11 A request for a ZIP no published record serves returns status `no_match`, three help routes, and no visits.
- A12 No-match never lists a resource whose service area excludes the resident's ZIP.
- A13 A resource is a listed option only if the resident's ZIP is in its served-ZIP list, or the list is empty (then conditional per A5).
- A4 With the pinned-date setting, the same request gives the same Food today result on any real date; without it, "today" is the Milwaukee date.
