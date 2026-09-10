# GoodNext handoff

Written September 8, 2026, 21:40 CDT; updated 23:59 CDT after MOO-786 and
MOO-787 closed. For a fresh Claude Code session.
Read this, then `CONTEXT.md`, then `docs/agents/issue-tracker.md`, then
`docs/specs/food-today-screen.md`. Do not re-read the planning docs unless a
task needs them; the decisions are settled.

## What GoodNext is

A free website that helps a Wisconsin household find food today and prepare
an official next step after a FoodShare notice. Hackathon entry ("Agents for
Humans"), deadline **September 14, 2026, 7 p.m. Central**, judging through
October 8. Product name GoodNext; older docs still say "FoodShare Bridge."

Never: decide eligibility, promise benefits or food stock, ask for an account
or a notice before helping with food, or use real residents' documents.

## Where things are

| Piece | Path | State |
| --- | --- | --- |
| Strands agent (Python 3.12) | `app/goodnext/` | 42 tests green; deployed runtime v5, verified live |
| FastAPI backend | `services/api/` | 13 tests green; truthful 503 on any agent failure (PR #13) |
| AgentCore CLI config + CDK | `agentcore/` | Deployed to us-east-1 |
| Website (Next.js 16 static export, Tailwind 4, pnpm) | `apps/web/` | Complete and finished: form, waiting states, today's cards, week tiles, no-match, summary line, help routes, print sheet, accessibility pass. 42 tests green (axe-core fixture test included). MOO-786 and MOO-787 Done on branch `tarikjmoody/moo-786-finish-pass`, **11 commits, not yet pushed** |
| Directory data | `app/goodnext/fixtures/` | 93 records, see below |
| Help routes | `app/goodnext/help_routes.json` | One reviewed file; agent and API both read it (decision 009) |
| Specs | `docs/specs/food-today.md` (agent, API), `docs/specs/food-today-screen.md` (website) | Settled; grill notes beside each |
| Design context | `PRODUCT.md`, `DESIGN.md`, `.impeccable/design.json`, `.impeccable/surfaces/apps-web-src-app-page-tsx.md`, `.impeccable/mocks/decision/`, `.impeccable/review/` (untracked captures) | Direction is the 7-Day Forecast Strip (decision 007). DESIGN.md records the built system (finish pass MOO-786). Read DESIGN.md before touching any web UI |
| Decisions | `docs/decisions/001` to `010` | Plain English; "What actually happened" blank for Tarik |
| Learning log | `docs/LEARNING-LOG.md` | Two entries (dev proxy timeout; the bot PR) |
| Research | `docs/research/` | Data access, 211 guide, drafts, call sheet |
| Evidence | `docs/evidence/` | Live responses and screenshots per issue |

Tracker: **Linear**, team MOO, project "GoodNext — Agents for Humans
Hackathon". Only the `linear-build` skill creates, moves, or closes issues.
Food today agent issues MOO-770 to 778: Done. Screen issues MOO-779 to 787
and agent fixes 780, 781: Done with evidence comments. 786 and 787 are Done
in Linear but their branch is **not merged**; see "Next" below.

GitHub: https://github.com/tmoody1973/goodnext. PRs #4 to #11 and #13 merged
2026-09-08. CI runs agent tests, API tests, `agentcore validate`, and the web
job (typecheck, tests, build) on every push and PR; branch protection on main
requires them. Claude works on branches off main and opens PRs; Tarik merges
and says "push" before any push.

## The deployed runtime

- Runtime ARN: `arn:aws:bedrock-agentcore:us-east-1:953791390715:runtime/goodnext_goodnext-j7ndOFF7b3`
- Stack `AgentCore-goodnext-default`, us-east-1.
- **v5 deployed 2026-09-08 20:57 CDT** (later-day claims name their own day,
  MOO-781). v4 19:12 CDT (help routes on every status, MOO-780). v3 12:55 CDT
  (output ceiling, brevity, trace redaction). All verified live; evidence
  under `docs/evidence/moo-776-*`, `moo-780-*`, `moo-781-*`.
- Run the API against it:
  `cd services/api && GOODNEXT_ENV=demo GOODNEXT_DEMO_NOW=2026-09-10T09:00:00-05:00 GOODNEXT_AGENT_RUNTIME_ARN='<ARN above>' AWS_REGION=us-east-1 uv run uvicorn goodnext_api.main:app --port 8000`
- Run the site: `cd apps/web && pnpm dev` (port 3000, proxies `/api/*` to 8000
  with a 180 s timeout).
- Demo clock: fixture windows cover 2026-09-08 to 2026-09-21; regenerate with
  the two scripts in `app/goodnext/scripts/` when the demo week moves.
- A plan takes 60 to 105 s. No-match returns in under 10 s without a model call.
- AWS login is the account **root** user via `aws login`; the session expires
  after some hours (the API then answers 503 with help routes). Use a role
  before judge-facing hosting. `agentcore deploy` runs from the repo root.

## Directory data, in trust order

1. **Reviewed** (`fixtures/milwaukee-food-resources-reviewed.json`, 16 sites):
   built by Tarik, each checked against the official provider page on
   2026-09-08; "verified" tier, verifier "Tarik Moody". Wins over the map.
2. **Milwaukee Food Environment Map** (75 sites, 68 after de-dup): public
   ArcGIS layer, data as of 2024-08-27, no license stated. Used per decision
   006 with a source line on every card; permission request drafted, not sent.
3. **Synthetic** (9): closed, unknown-area, paid, appointment cases. Labeled
   "(synthetic)" in the provider name, which a judge will see on the demo date.

Rules from real data (decision 006): unknown service area shows only for the
site's own ZIP; over 14 days old is "call to confirm" with the date; only a
missing date is "unconfirmed".

## Next: get the finish-pass branch onto main

Branch `tarikjmoody/moo-786-finish-pass` holds MOO-786 and MOO-787: print
sheet, accessibility pass (focus to the result heading, provider-named links,
tel:211, axe test), reflow fixes at 320 px and doubled text, the reviewer's
design fixes (amber count as the focal number, compact time row on phones,
taller today panel, Print below the cards, dominant tile count, hover and
pressed states), DESIGN.md and its sidecar, decision 010, evidence for both
issues. 42 web tests green; typecheck and build green; agent and API suites
untouched. Steps, all Tarik's:

1. **Close PR #12.** A PostHog Desktop "self-driving" bot opened it at 20:06
   CDT against a stale main with a partial version of MOO-786. Not adopted;
   its good ideas were rebuilt on this branch. Closing it also stops the Linear
   automation that flipped MOO-786 to Done with no evidence.
2. Say "push"; Claude pushes the branch and opens the PR; CI runs the four
   jobs; Tarik merges.
3. **Decide fix 5 from the finish review:** two synthetic records (St. Demo
   Hot Meal Program, Northside Community Pantry on some runs) carry 555
   numbers with no "(synthetic)" label or source line on the demo dates.
   Either give the nine synthetic fixture records a `source_text` naming them
   synthetic, or drop them from the demo week. Fixture and agent side, one
   small ticket.
4. Optional, small: show the response `request_id` as a "Reference" line on
   the result so a support call can quote it (MOO-787 noted the screen does
   not display it).

Impeccable notes for the next UI change: read `DESIGN.md` first; run
`context.mjs --target <file>` once; the reviewer and documenter run as fresh
`general-purpose` Agent calls from the `reference/degraded/*.md` role files
(the shipped `.toml` agents are Codex-only); capture on the production build
(`pnpm build` then a static server) so the dev badge never covers content;
set the viewport with `Emulation.setDeviceMetricsOverride` **after** the tab
exists, and log the heading text before every capture.

## Then, in order (five days left)

1. **Latency.** Return day one first, the week second; or cache the system
   prompt. The model writes roughly 5,800 tokens for a seven-day plan, which is
   the whole wait. Measured on the real flow tonight (MOO-787): 95.4, 89.2, and
   87.1 seconds; delayed status at about 31 seconds each time.
2. **Judge-facing hosting.** One hostname for site and API (decision 008):
   static files plus a path rule sending `/api/*` to the API with an origin
   timeout of at least 180 s; the API container must carry
   `app/goodnext/help_routes.json` (decision 009). IAM role, not root. Nothing
   in AWS is created without Tarik's go.
3. **Submission checklist** (PRD section 13): architecture diagram matching
   what shipped, description, video under five minutes, Builder ID, judge
   access through October 8.
4. **Data follow-ups.** The 211 API trial was rejected 2026-09-08; the fixture
   directory stays the source. Send the drafted IMPACT 211 request anyway; work
   the 53206 call sheet; set CloudWatch retention on the runtime log group.

## Known problems

1. Plan latency 87 to 105 s (above). Plans also differ run to run (the model
   picks different valid visits); the validator accepts each.
2. Older log events (v1, v2) hold synthetic test prompts; set retention.
3. The model sometimes places visits on days with no window; the validator
   strips them and returns `partial`. Working as designed.
4. Older Impeccable version installed (4.1.2; 4.2.2 available). Do not update
   mid-session.

## Working agreements

- Socratic at the seams only; ship the scaffolding. Cite data sources,
  disclose, move on.
- Plain English; define terms inline. Tarik is not a traditional engineer.
- Every non-trivial decision gets a `docs/decisions/NNN` file with the
  "What actually happened" field left blank for Tarik.
- Fixture tests never reach Bedrock; `tests/conftest.py` enforces it.
- The Matt Pocock skills `grill-with-docs`, `to-spec`, `to-tickets`, and
  `implement` are user-invocation only: Tarik types the slash command.
  `linear-build` and `impeccable` are callable by Claude.
- Per ticket: branch off main, tests first, one bounded live run with clipped
  screenshots, PR, CI green, `linear-build` closes with evidence, Tarik merges.
- Browser checks run through `ego-browser`. Real typing (`click` then
  `typeText`, then read the field value back before submitting; at phone
  emulation the first keystrokes sometimes miss), scroll the target into view
  before clicking, clip screenshots with `Page.captureScreenshot` and a `clip`
  from the `main` element's rect, keep captures under about 6000 px tall (taller
  ones fail), do the run in bounded scripts and `completeTaskSpace` at the end.
  Stop the dev server and API before running the unit tests; they time out
  under load (three did tonight, all green once the servers were stopped).
- Live web checks cost one model call each (cents). A no-match ZIP such as
  53001 answers in seconds and costs nothing.

## First message for the next session (paste this)

```text
We are building GoodNext in /Users/tarikmoody/Projects/foodshare-strands.
Read HANDOFF.md, then CONTEXT.md, then DESIGN.md, then
docs/agents/issue-tracker.md. Do not re-read the planning docs unless a task
needs them.

The finish-pass branch tarikjmoody/moo-786-finish-pass is merged (or: I will
merge it now). Next is latency: return Food today first and the rest of the
week second, measured on the real flow, as a Linear issue created with
linear-build. Explain in plain English. Nothing in AWS is created or changed
without my go; deploys, pushes, and merges are mine.
```
