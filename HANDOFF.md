# GoodNext handoff

Written September 8, 2026, 21:40 CDT, for a fresh Claude Code session.
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
| Website (Next.js 16 static export, Tailwind 4, pnpm) | `apps/web/` | Functionally complete: form, waiting states, today's cards, week tiles, no-match, summary line, help routes. 28 tests green. Finish pass (MOO-786) and closing live run (MOO-787) open |
| Directory data | `app/goodnext/fixtures/` | 93 records, see below |
| Help routes | `app/goodnext/help_routes.json` | One reviewed file; agent and API both read it (decision 009) |
| Specs | `docs/specs/food-today.md` (agent, API), `docs/specs/food-today-screen.md` (website) | Settled; grill notes beside each |
| Design context | `PRODUCT.md`, `.impeccable/surfaces/apps-web-src-app-page-tsx.md`, `.impeccable/mocks/decision/` | Shape pass done; direction is the 7-Day Forecast Strip (decision 007); **DESIGN.md does not exist yet, MOO-786 writes it** |
| Decisions | `docs/decisions/001` to `009` | Plain English; "What actually happened" blank for Tarik |
| Learning log | `docs/LEARNING-LOG.md` | One entry (dev proxy timeout) |
| Research | `docs/research/` | Data access, 211 guide, drafts, call sheet |
| Evidence | `docs/evidence/` | Live responses and screenshots per issue |

Tracker: **Linear**, team MOO, project "GoodNext — Agents for Humans
Hackathon". Only the `linear-build` skill creates, moves, or closes issues.
Food today agent issues MOO-770 to 778: Done. Screen issues MOO-779 to 785
and agent fixes 780, 781: Done, merged, with evidence comments. **Open:
MOO-786 (finish pass) and MOO-787 (live run).** 787 is blocked by 786.

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

## Next: MOO-786, the Impeccable finish pass

Read the Linear issue with `linear-build` (`get_issue MOO-786`) before starting;
it is the contract. In short: print stylesheet, keyboard and screen-reader
pass, 320 px and 200 percent zoom, contrast, reduced motion, the Impeccable
detector once, findings fixed in one batch, DESIGN.md written from the built
screen, no internal names on screen.

How Impeccable wants it run (skill `impeccable`, reference `new-work.md`
section 7 "Inspect and finish", plus `audit.md` and `polish.md`):

1. Run `node $(realpath ~/.claude/skills/impeccable/scripts)/context.mjs --target apps/web/src/app/page.tsx`
   once. The skill folder is a symlink; scripts only run through the real path.
2. Build every state locally and capture one batched round: desktop and
   mobile (320 and 390 wide), at 100 and 200 percent zoom, into
   `.impeccable/review/desktop.png`, `mobile.png`. Clip captures to the element
   (see the ego-browser pattern below); full-viewport captures from the top
   of the page have twice come out blank or wrong.
3. Run the detector once: `node $(realpath ~/.claude/skills/impeccable/scripts)/detect.mjs --json apps/web/src`.
   Fix what is mechanical in one batch.
4. The finish reviewer and documenter are shipped as Codex agent files
   (`~/.claude/skills/impeccable/agents/*.toml`), not as Claude Code agent
   types. Run them as fresh `general-purpose` Agent calls with the packet the
   reference lists, or in-thread from `reference/degraded/finish-reviewer.md`
   and `reference/degraded/documenter.md`. Say which was used.
5. DESIGN.md at the repo root, written from the built world: palette (sample
   the hex values from `apps/web/src/app/globals.css`, they are the source),
   type (system sans), spacing, the reusable pieces (time block, option card,
   day tile, summary line, help routes, pill), motion grammar (none beyond
   hover color; reduced motion honored). Update the surface brief to record
   the approved comp `.impeccable/mocks/decision/model-pick.webp`.
6. Two inspection rounds is the ceiling. Then MOO-787.

Things already noticed for the finish pass, from the live screenshots:
- The navy time block on a card stretches to the card's full height when the
  requirements text is long; it should stay compact (top-aligned or fixed).
- "2-1-1" renders as plain text in help routes because it has fewer than seven
  digits; a `tel:211` link is valid and better.
- The help-routes footer repeats the same three entries on every result; fine,
  but the footer and the delayed-status copy share one component.
- Every card says "We can't confirm they have food today." in bold; on three
  cards that is heavy. Keep the line (spec claim 6, never removed); weight is
  open.
- The "(synthetic)" label appears on the demo date. Decision for Tarik: keep
  for honesty or drop synthetic records from the demo week.
- Direction contract lives in `apps/web/src/app/layout.tsx` inside a
  `<template id="direction-contract">`; grep the built `out/index.html` for
  `a5fbc27f` to confirm it survives.

After 786: **MOO-787**, the closing live run (real 53206 through the dev
proxy on the deployed runtime, screenshot, cookie, console, request id).

## Then, in order (five days left)

1. **Latency.** Return day one first, the week second; or cache the system
   prompt. The model writes roughly 5,800 tokens for a seven-day plan, which is
   the whole wait. Measure on the real flow.
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

1. Plan latency 60 to 105 s (above).
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
  `typeText`), scroll the target into view before clicking, clip screenshots
  with `Page.captureScreenshot` and a `clip` from the element's rect, do the
  whole run in one bounded script and `completeTaskSpace` at the end. Stop the
  dev server and API before running the unit tests; they flake under load.
- Live web checks cost one model call each (cents). A no-match ZIP such as
  53001 answers in seconds and costs nothing.

## First message for the next session (paste this)

```text
We are building GoodNext in /Users/tarikmoody/Projects/foodshare-strands.
Read HANDOFF.md, then CONTEXT.md, then docs/agents/issue-tracker.md, then
docs/specs/food-today-screen.md. Do not re-read the planning docs unless a
task needs them.

Build MOO-786, the Impeccable finish pass for the Food today screen, on a
new branch off main: read the issue with linear-build, follow HANDOFF's
"Next: MOO-786" section and the impeccable skill's finish references, write
DESIGN.md, and close the issue with evidence. Then MOO-787. Explain in plain
English. Nothing in AWS is created or changed without my go; deploys, pushes,
and merges are mine.
```
