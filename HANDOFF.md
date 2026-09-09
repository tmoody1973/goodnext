# GoodNext handoff

Written September 8, 2026, 12:45 CDT; updated 15:10 CDT, for a fresh Claude Code session.
Read this, then `CONTEXT.md`, then `docs/agents/issue-tracker.md`. Do not
re-read the planning docs unless a task needs them; the decisions are settled.

## What GoodNext is

A free website that helps a Wisconsin household find food today and prepare
an official next step after a FoodShare notice. Hackathon entry ("Agents for
Humans"), deadline **September 14, 2026, 7 p.m. Central**, judging through
October 8. Product name GoodNext; docs still say "FoodShare Bridge."

Never: decide eligibility, promise benefits or food stock, ask for an account
or a notice before helping with food, or use real residents' documents.

## Where things are

| Piece | Path | State |
| --- | --- | --- |
| Strands agent (Python 3.12) | `app/goodnext/` | Built, 39 tests green, deployed v3 and verified live |
| FastAPI backend | `services/api/` | Built, 10 tests green |
| AgentCore CLI config + CDK | `agentcore/` | Deployed to us-east-1 |
| Website (Next.js 16 static export, Tailwind 4, pnpm) | `apps/web/` | Base, cards, waiting states, no-match and summary line (MOO-779, 782, 783, 784); 24 tests green; MOO-785 to 787 open |
| Directory data | `app/goodnext/fixtures/` | 93 records, see below |
| Feature specs | `docs/specs/food-today.md`, `docs/specs/food-today-screen.md` | Settled |
| Design context | `PRODUCT.md`, `.impeccable/surfaces/`, `.impeccable/mocks/decision/` | Shape pass done; DESIGN.md lands with MOO-786 |
| Decisions | `docs/decisions/001` to `006` | Plain English, blanks for Tarik |
| Research | `docs/research/` | Data access, 211 guide, drafts, call sheet |
| Evidence | `docs/evidence/` | Live responses per issue |

Tracker: **Linear**, team MOO, project "GoodNext — Agents for Humans
Hackathon". Only the `linear-build` skill creates or closes issues. Issues
MOO-770 to MOO-775, MOO-777, MOO-778 are Done with evidence comments.
**All nine Food today issues (MOO-770 to 778) are Done.** Screen issues
MOO-779 to MOO-787 created 2026-09-08 14:45 CDT. 779, 782, 783 Done and
merged (PRs #4, #5, #6). 780 Done and merged (PR #7), live on runtime v4. 781 unblocked. 784 and 785 unblocked.
786 waits on 784 and 785.

GitHub: https://github.com/tmoody1973/goodnext, pushed and current as of
2026-09-08 13:10 CDT. CI (`.github/workflows/ci.yml`) runs both test suites
and `agentcore validate` on every push to main and every PR; proven red on
PR #1 (closed, throwaway). Branch protection on main requires all three CI
checks and blocks force-pushes; admins can bypass in an emergency. Claude
makes changes through pull requests. Push only when Tarik says "push".

## The deployed runtime

- Runtime ARN: `arn:aws:bedrock-agentcore:us-east-1:953791390715:runtime/goodnext_goodnext-j7ndOFF7b3`
- Stack `AgentCore-goodnext-default`, us-east-1, deployed 2026-09-08 12:30 CDT, version 1.
- Version 3 deployed 2026-09-08 12:55 CDT: larger output ceiling, brevity
  instruction, and both trace-redaction env vars. **Version 4 deployed 2026-09-08 19:12 CDT** by
  Tarik: help routes on every status (MOO-780, decision 009). Verified live:
  53206 partial plan in 98 s with three routes; evidence
  `docs/evidence/moo-780-deployed-runtime-v4-*`. MOO-776 verified live on v3:
  53206 plan in 89 s, no-match in 7 s, CloudWatch shows zero resident values
  and REDACTED markers. Evidence under `docs/evidence/moo-776-*`.
- Local dev: `agentcore dev --skip-deploy -l` (port 8080) plus
  `cd services/api && uv run uvicorn goodnext_api.main:app --port 8000`.
- Point the API at the deployed runtime with env `GOODNEXT_AGENT_RUNTIME_ARN`.
- Demo clock: `GOODNEXT_ENV=demo GOODNEXT_DEMO_NOW=2026-09-10T09:00:00-05:00`
  (fixture windows cover 2026-09-08 to 2026-09-21; regenerate with the two
  scripts in `app/goodnext/scripts/` when the demo week moves).
- AWS login is the account **root** user via `aws login`. Fine for now; use a
  role before judge-facing hosting.

## Directory data, in trust order

1. **Reviewed** (`fixtures/milwaukee-food-resources-reviewed.json`, 16 sites):
   built by Tarik himself, each checked against the official provider page on
   2026-09-08; "verified" tier, verifier "Tarik Moody". Source
   file under `fixtures/reviewed/`. Wins over the map for the same site.
2. **Milwaukee Food Environment Map** (75 sites, 68 after de-dup): public
   ArcGIS layer, data as of 2024-08-27, no license stated. Used per decision
   006 with a source line on every card; permission request drafted, not sent.
3. **Synthetic** (9): closed, unknown-area, paid, appointment cases. Labeled.

Rules that came out of real data (decision 006): unknown service area shows
only for the site's own ZIP; anything checked over 14 days ago is "call to
confirm" with the date; only a missing date is "unconfirmed".

## Known problems, in priority order

1. **Plan latency 60–105 s.** Too slow for a resident. Fix direction: a
   day-one-only first response, then the week; delayed-status message per
   PRD section 8; prompt caching. Not started.
2. **Older log events (v1, v2) still hold synthetic test prompts** in the
   runtime log group; harmless (no real resident) but delete the log group or
   set retention before any real use.
3. **Model sometimes places visits on days with no window**; the validator
   strips them and returns `partial` with a warning. Working as designed;
   a nudge in the task text could reduce it.
4. **211 data** needs IMPACT 211 permission (decision 005). The 211 API trial
   request was rejected on 2026-09-08; the fixture directory (reviewed plus
   Food Environment Map, decision 006) stays the data source for the hackathon.
   DIY verification guide at `docs/research/211-portal-verification-guide.md`.
5. **Website** has only the base screen (form to first response). Cards,
   waiting states, no-match, tiles, finish, and the live run are MOO-782 to 787.
6. **Dev proxy timeout.** The Next dev proxy drops requests at 30 s by default;
   `experimental.proxyTimeout` is set to 180 s in dev. Judge-facing hosting
   needs the same patience at the edge (CloudFront origin timeout).

## Next steps, in order (six days to September 14, 7 p.m. Central)

1. **Website, Food today screen.** Shape, grill, spec, and tickets are done
   (2026-09-08). Branch `tarikjmoody/moo-779-web-app-base` is pushed as PR #4
   (https://github.com/tmoody1973/goodnext/pull/4), all five CI checks green,
   web job proven red then green. PRs #4 and #5 merged; PR #6 (MOO-783,
   waiting states) is open for merge. Then MOO-784 and 785 (parallel-safe),
   then 786, 787, each via `linear-build`, on branches off main. MOO-780
   (help routes on every status) should land before 786 so the delayed
   status and the footer actually show routes on a first visit. Spec:
   `docs/specs/food-today-screen.md`. The Matt Pocock `implement` skill is
   user-invocation only, like `grill-with-docs`, `to-spec`, `to-tickets`.
2. **Latency.** Return day one first, the week second; or cache the system
   prompt. Only after the screen exists, so the fix is measured on the real
   flow.
3. **Judge-facing hosting.** The API needs a public home (Tech Stack says
   Fargate behind CloudFront); the site is a static export. Use an IAM role,
   not root, for this. Not started.
4. **Submission checklist** (PRD section 13, H06–H10): public repo with MIT
   (done), architecture diagram matching what shipped, description, video
   under five minutes, Builder ID, judge access through October 8.
5. **Data follow-ups.** Send the three drafted permission requests; work the
   53206 call sheet; set CloudWatch log retention on the runtime log group.

## First message for the next session (paste this)

```text
We are building GoodNext in /Users/tarikmoody/Projects/foodshare-strands.
Read HANDOFF.md, then CONTEXT.md, then docs/agents/issue-tracker.md, then
docs/specs/food-today-screen.md. Do not re-read the planning docs unless a
task needs them.

PR #9 (MOO-784) may still be open; merge it. Build MOO-785 (later this week
tiles) with linear-build, tdd, and code-review, on a new branch off main; then
MOO-781 on the agent side, then 786 and 787. Read the surface brief and PRODUCT.md before
touching UI. Explain in plain English. Nothing in AWS is created or changed
without my go; deploys and pushes are mine.
```

## Working agreements

- Socratic at the seams only; ship the scaffolding. Tarik said "quit being
  strict" about data reuse for the hackathon; cite sources, disclose, move on.
- Explain in plain English; define terms inline. Tarik is not a traditional
  engineer.
- Every non-trivial decision gets a `docs/decisions/NNN` file with the
  "What actually happened" field left blank.
- Fixture tests must never reach Bedrock; `tests/conftest.py` enforces it.
  Mark a live test `@pytest.mark.live`.
- `agentcore deploy` runs from the repo root, not from `agentcore/`.
- Use the Matt Pocock skills by plugin name (`mattpocock-skills:…`); top-level
  `code-review` is CodeRabbit. `grill-with-docs`, `to-spec`, `to-tickets`, and
  `implement` are user-invocation only: Tarik types the slash command.
- Browser checks run through `ego-browser`; scroll the target into view before
  clicking (the dev-tools badge and the viewport edge swallow clicks), and use
  real typing so React sees the input. LastPass injects into inputs and trips a
  harmless hydration warning in dev.
