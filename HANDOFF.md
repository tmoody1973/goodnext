# GoodNext handoff

Written September 8, 2026, 12:45 CDT, for a fresh Claude Code session.
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
| Website (Next.js) | `apps/web/` | **Not started** |
| Directory data | `app/goodnext/fixtures/` | 93 records, see below |
| Feature spec | `docs/specs/food-today.md` | Settled |
| Decisions | `docs/decisions/001` to `006` | Plain English, blanks for Tarik |
| Research | `docs/research/` | Data access, 211 guide, drafts, call sheet |
| Evidence | `docs/evidence/` | Live responses per issue |

Tracker: **Linear**, team MOO, project "GoodNext — Agents for Humans
Hackathon". Only the `linear-build` skill creates or closes issues. Issues
MOO-770 to MOO-775, MOO-777, MOO-778 are Done with evidence comments.
**All nine Food today issues (MOO-770 to 778) are Done.**

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
  instruction, and both trace-redaction env vars. MOO-776 verified live on v3:
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
4. **211 data** needs IMPACT 211 permission (decision 005). Trial subscription
   exists; DIY verification guide at `docs/research/211-portal-verification-guide.md`.
5. **Website** does not exist. Impeccable shape pass first, then screens.

## Next steps, in order (six days to September 14, 7 p.m. Central)

1. **Website, Food today screen.** Run `impeccable` `shape` for the Food
   today journey first (PRD section 14 requires it), then
   `mattpocock-skills:grill-with-docs` → `to-spec` → `to-tickets` →
   `linear-build`. Next.js 16 static export, Tailwind 4, `apps/web/`. The
   screen calls `POST /api/plans`. It must show today expanded, days two to
   seven collapsed, the no-match state with help routes, and a delayed-status
   message after 30 s (PRD section 8) because a plan takes 60–100 s.
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
Read HANDOFF.md, then CONTEXT.md, then docs/agents/issue-tracker.md.
Do not re-read the planning docs unless a task needs them.

Next feature is the website's Food today screen. Start with the Impeccable
shape workflow for that journey, then grill-with-docs, to-spec, to-tickets,
and create the Linear issues with linear-build. Ship the scaffolding;
Socratic only at the seams. Explain in plain English. Nothing in AWS is
created or changed without my go, and deploys are commands I run myself.
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
- Use the Matt Pocock skills by plugin name (`mattpocock-skills:…`); top-level
  `code-review` is CodeRabbit.
