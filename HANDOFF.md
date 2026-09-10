# GoodNext handoff

Written September 8, 2026; updated September 10, 14:30 CDT after the notice
entry point shipped on runtime v6. For a fresh Claude Code session.
Read this, then `CONTEXT.md`, then `docs/agents/issue-tracker.md`, then
`docs/specs/food-today-screen.md`. Do not re-read the planning docs unless a
task needs them; the decisions are settled.

## What GoodNext is

A free website that helps a Wisconsin household find food today and
understand a FoodShare letter (sanction, time-limited benefits warning,
six-month report), with the next supported step and the official routes. Hackathon entry ("Agents for
Humans"), deadline **September 14, 2026, 7 p.m. Central**, judging through
October 8. Product name GoodNext; older docs still say "FoodShare Bridge."

Never: decide eligibility, promise benefits or food stock, ask for an account
or a notice before helping with food, or use real residents' documents.

## Where things are

| Piece | Path | State |
| --- | --- | --- |
| Strands agent (Python 3.12) | `app/goodnext/` | 57 tests green; two workflows, `food_today` and `understand_notice`; deployed runtime **v6** (2026-09-10 14:06 CDT), verified live; v7 pending (notice task-text caps and never-list hedge fix are on the branch, not deployed) |
| FastAPI backend | `services/api/` | 25 tests green; `POST /api/plans` and `POST /api/notices` (PDF text layer, Textract for photos, three answers); truthful 503 |
| AgentCore CLI config + CDK | `agentcore/` | Deployed to us-east-1 |
| Website (Next.js 16 static export, Tailwind 4, pnpm) | `apps/web/` | Two entry tabs: Find food today (finished, MOO-786/787 merged in PR #15) and Understand my letter (upload or three questions, result beside quoted passages; MOO-791). 50 tests green. Notice work on branch `tarikjmoody/notice-entry-point`, **not yet pushed** |
| Directory data | `app/goodnext/fixtures/` | 93 records, see below |
| Help routes | `app/goodnext/help_routes.json` | One reviewed file; agent and API both read it (decision 009) |
| Specs | `docs/specs/food-today.md`, `docs/specs/food-today-screen.md`, `docs/specs/understand-notice.md` | Settled; the notice spec was written from an approved plan, not a grill |
| Demo letters | `docs/research/notices/generated/` | Three fictional FoodShare letters for "Maria Example" from DHS templates (HTML, PDF with text layer, PNG of page 1, `values.json`); MilES phone verified against DHS |
| Policy passages | `app/goodnext/policy_passages.json` (23 draft), review checklist `docs/research/notices/policy-passages-review.md` | **Zero approved.** The agent cites only approved entries; "questions to ask your agency" stays empty until Tarik ticks the checklist and the status flips to `approved` |
| Design context | `PRODUCT.md`, `DESIGN.md`, `.impeccable/design.json`, `.impeccable/surfaces/apps-web-src-app-page-tsx.md`, `.impeccable/mocks/decision/`, `.impeccable/review/` (untracked captures) | Direction is the 7-Day Forecast Strip (decision 007). DESIGN.md records the built system (finish pass MOO-786). Read DESIGN.md before touching any web UI |
| Decisions | `docs/decisions/001` to `011` | Plain English; "What actually happened" blank for Tarik. 011: real upload in the demo, fed with fictional letters |
| Learning log | `docs/LEARNING-LOG.md` | Two entries (dev proxy timeout; the bot PR) |
| Research | `docs/research/` | Data access, 211 guide, drafts, call sheet |
| Evidence | `docs/evidence/` | Live responses and screenshots per issue |

Tracker: **Linear**, team MOO, project "GoodNext — Agents for Humans
Hackathon". Only the `linear-build` skill creates, moves, or closes issues.
Food today MOO-770 to 787: Done and merged. Notice entry point MOO-788 to
792: 789, 790, 791 Done with evidence; 788 In Progress (letters done,
passage approval waits on Tarik); 792 closes after the finish review verdict.
Branch `tarikjmoody/notice-entry-point` is **not pushed**.

**A PostHog "self-driving" bot opens PRs on this repo from Linear issues**
(PR #12 on 2026-09-08, PR #16 on 2026-09-10, both stale and unadopted).
Close them; find the switch that turns it off.

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

## Next: land the notice branch, deploy v7, approve passages

1. Tarik: `push`, PR, merge (CI runs agent, API, AgentCore validate, web).
2. Tarik: review `docs/research/notices/policy-passages-review.md`; tick the
   passages the agent may cite. Claude then sets `review_status: approved` on
   those entries in `app/goodnext/policy_passages.json` (a test enforces that
   only approved, official-URL entries load).
3. Deploy **v7** on Tarik's go: `agentcore deploy --target default --diff`
   (expect only the code bundle), then `--yes`. v7 carries the finding and
   citation caps and the never-list hedge fix; without it, results run long
   and a next step can be stripped.
4. Re-run the four live uploads (script pattern in the MOO-792 evidence) and
   refresh `docs/evidence/notice-live-*`.
5. Hosting: the API's role needs `textract:DetectDocumentText` for photo
   uploads; `/api/notices` is multipart up to 10 MB.

Running the notice path locally: `agentcore dev` (serves on **8082**, not
8080; pass `GOODNEXT_AGENT_LOCAL_URL=http://127.0.0.1:8082` to the API), then
the API and `pnpm dev`. A letter answer takes 25 to 35 s. Photo uploads call
Textract under the local AWS session.

## Then, in order (four days left)

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
