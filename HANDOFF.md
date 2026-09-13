# GoodNext handoff

Written September 13, 2026, 12:55 CDT, for a fresh Claude Code session.
Read this, then `CONTEXT.md`, then `DESIGN.md`, then
`docs/agents/issue-tracker.md`. Do not re-read the planning docs unless a
task needs them; the decisions are settled and the product is built.

**Deadline: Monday September 14, 2026, 7 p.m. Central.** Judging runs through
October 8. What is missing is not code: it is a public address a judge can
open, and the submission materials.

## What GoodNext is

A free website with two entry points. **Find food today**: enter ZIP, money,
kitchen, travel; get today's listed options with opening window, cost,
requirements, check date, and a directions link, plus six small tiles for the
rest of the week. **Understand my letter**: upload a FoodShare letter as a PDF
or photo, or answer three questions; see what the letter says beside the
sentences it came from, the next step, tasks with dates exactly as printed,
who to contact, and what only the agency can decide. Nothing about the
resident is stored. Hackathon entry, "Agents for Humans". Product name
GoodNext; older docs say "FoodShare Bridge".

Never: decide eligibility, promise benefits or food stock, ask for an account
or a notice before helping with food, or use real residents' documents. The
demo letters are fictional ("Maria Example"), generated from official DHS
sample templates (decision 011).

## State on main (all merged, nothing pending)

| Piece | Path | State |
| --- | --- | --- |
| Strands agent (Python 3.12) | `app/goodnext/` | 57 tests green. Two workflows: `food_today` and `understand_notice`. Deployed runtime **v7** (2026-09-10 15:35 CDT), both verified live. |
| FastAPI backend | `services/api/` | 25 tests green. `POST /api/plans`, `POST /api/notices` (multipart: PDF text layer via pypdf, photos via Amazon Textract, or three form fields). Truthful 503 with help routes on any agent failure. |
| AgentCore CLI config + CDK | `agentcore/` | Stack `AgentCore-goodnext-default`, us-east-1. Deploy: `agentcore deploy --target default --diff` (expect only the code bundle), then `--yes`. |
| Website (Next.js 16 static export, Tailwind 4, pnpm) | `apps/web/` | 50 tests green (axe and never-list included). Two tabs, Find food today first. Impeccable finish passes done on both screens (MOO-786, MOO-792). |
| Directory data | `app/goodnext/fixtures/` | 93 records: 16 reviewed by Tarik (wins), 68 from the Milwaukee Food Environment Map (2024-08-27, source line on every card), 9 synthetic labeled "(synthetic)". |
| Help routes | `app/goodnext/help_routes.json` | One reviewed file; the agent and the API both read it (decision 009). |
| Policy passages | `app/goodnext/policy_passages.json` | 23 entries, **zero approved**. The tool loads only `review_status: approved` (test-enforced). Review checklist: `docs/research/notices/policy-passages-review.md`. |
| Demo letters | `docs/research/notices/generated/` | Three fictional letters (sanction, time-limited warning, six-month report) as HTML, PDF with text layer, PNG of page 1, and `values.json`. |
| Design | `DESIGN.md`, `.impeccable/design.json`, `PRODUCT.md` | Read `DESIGN.md` before touching any web UI. |
| Specs and decisions | `docs/specs/*.md`, `docs/decisions/001` to `011` | Plain English; "What actually happened" fields blank for Tarik. |
| Evidence | `docs/evidence/` | Per-issue live envelopes and screenshots; latest are `notice-live-*-v7.json` and `food-live-53206-v7.json`. |

Tracker: **Linear**, team MOO, project "GoodNext — Agents for Humans
Hackathon"; only the `linear-build` skill creates, moves, or closes issues.
MOO-770 to 792 are Done except **MOO-788** (In Progress: letters done,
passage approval waits on Tarik). GitHub: https://github.com/tmoody1973/goodnext,
PRs #4 to #19 merged, none open. CI (agent, API, `agentcore validate`, web) on
every PR; branch protection on main. Claude works on branches and opens PRs;
Tarik merges, and says "push" before any push.

**A PostHog "self-driving" bot opens PRs from Linear issues** (PRs #12, #16,
#17, all stale, all closed). Before creating any new issue, find the switch
that turns that agent off, or expect another one.

## The deployed runtime

- ARN: `arn:aws:bedrock-agentcore:us-east-1:953791390715:runtime/goodnext_goodnext-j7ndOFF7b3`
- Model: `us.anthropic.claude-sonnet-4-6`, us-east-1 (`app/goodnext/model/load.py`).
- Run the API against it:
  `cd services/api && GOODNEXT_ENV=demo GOODNEXT_DEMO_NOW=2026-09-10T09:00:00-05:00 GOODNEXT_AGENT_RUNTIME_ARN='<ARN>' AWS_REGION=us-east-1 uv run uvicorn goodnext_api.main:app --port 8000`
- Run the site: `cd apps/web && pnpm dev` (port 3000, proxies `/api/*` to 8000 with a 180 s timeout).
- Run the agent locally instead: `agentcore dev` from the repo root (serves on **8082**); pass `GOODNEXT_AGENT_LOCAL_URL=http://127.0.0.1:8082` to the API and drop the ARN.
- Timings, measured: a food plan 87 to 105 s (delayed status at 31 s); a letter 25 to 35 s; no-match under 10 s with no model call.
- Demo clock: `GOODNEXT_ENV=demo` plus `GOODNEXT_DEMO_NOW` pins "today"; fixture windows cover 2026-09-08 to 2026-09-21. Judges will see September 10; the README setup note says so.
- AWS login today is the account **root** user via `aws login` (`! aws login` in the session); it expires after hours (the API then answers 503). Hosting must run under an IAM role.

## Next 1: hosting (the one thing that makes the entry judgeable)

Decision 008: one hostname for site and API. Nothing below exists yet;
every resource is created only on Tarik's go, one named resource at a time.

Recommended shape, smallest that fits the timings (a food plan takes up to
105 s, which rules out anything with a 30 or 60 second cap such as API
Gateway or CloudFront's default origin timeout):

1. **One container** from `services/api/`: FastAPI serves `/api/*` and also
   serves the static export from `apps/web/out` (add a StaticFiles mount for
   `/`; ~5 lines). Copy `app/goodnext/help_routes.json` into the image
   (decision 009) or set `GOODNEXT_HELP_ROUTES_FILE`.
2. **ECR repository** for the image.
3. **ECS Fargate service** (one task, 0.5 vCPU, 1 GB) in the default VPC, with
   a **task role** allowing `bedrock-agentcore:InvokeAgentRuntime` on the ARN
   above and `textract:DetectDocumentText`.
4. **Application Load Balancer**, idle timeout **300 s**, target group health
   check `GET /api/health`.
5. **HTTPS**: an ACM certificate on a hostname Tarik owns (Route 53 or an
   external DNS CNAME to the ALB). Without HTTPS the session cookie is not set
   (`secure=not DEV`); if no domain is available by Monday, run with
   `GOODNEXT_ENV=demo` and add an env switch for `secure=False`, and say so in
   the write-up.
6. Env on the task: `GOODNEXT_ENV=demo`, `GOODNEXT_DEMO_NOW=2026-09-10T09:00:00-05:00`,
   `GOODNEXT_AGENT_RUNTIME_ARN`, `AWS_REGION=us-east-1`.
7. Prove it: open the hostname in a real browser, run 53206 and upload the
   six-month letter, save the evidence as MOO-776/787 did. Write decision 012
   (hosting shape) in plain English.

Alternative if Fargate setup drags: App Runner (120 s request cap; a food
plan at 99 to 105 s is too close). Lambda function URLs allow 15 minutes but
need response streaming and a different packaging; not for Monday.

## Next 2: submission materials (PRD section 13)

- **H07 architecture diagram** matching what shipped: browser → static site
  and `/api/*` on one host → FastAPI → AgentCore Runtime (Strands, Bedrock) →
  tools (fixture directory, help routes, policy passages, letter passages);
  Textract for photos; validators after every model return.
- **H08 description**: the promise is "understand what changed, take the next
  supported action, and find food while you work through it." Disclose:
  fictional demo letters, real upload path, nothing stored, synthetic
  directory records labeled, policy questions empty until passages are approved.
- **H09 video** under five minutes: Maria uploads the six-month letter (no
  action now, March 2027 due date, fair-hearing right), then finds food for
  today with zero dollars and a bus.
- **H10** Builder ID and the form fields; **H06** repo public with license.

## Next 3: approve policy passages (MOO-788)

Tarik ticks `docs/research/notices/policy-passages-review.md`. Claude sets
`review_status: approved` on those ids in `app/goodnext/policy_passages.json`,
runs the agent tests, deploys v8 (diff first), and re-runs one letter to show
"questions to ask your agency" populated. Fair hearing has no DHS page; the
letters' own fair-hearing page is quoted instead.

## Known problems

1. Plan latency 87 to 105 s; plans differ run to run (the validator accepts
   each). Latency work (day one first) is deferred past the deadline.
2. Letter results are long on a phone (six findings, ten to thirteen quotes);
   v7 caps them; folding quotes behind "show more" was not done.
3. The API's `/api/plans` on the deployed runtime answers 503 when the local
   AWS session has expired; hosting under a role removes that.
4. Older runtime log events hold synthetic test prompts; set CloudWatch
   retention on the log group.
5. Impeccable 4.1.2 installed (4.2.2 available); do not update mid-session.

## Working agreements

- Plain English; define terms inline. Tarik is not a traditional engineer.
- Nothing in AWS is created or changed without Tarik's go; run the CDK diff
  before every `agentcore deploy`. Deploys, pushes, and merges are his calls.
- Every non-trivial decision gets `docs/decisions/NNN` with "What actually
  happened" left blank.
- Fixture tests never reach Bedrock (`tests/conftest.py`).
- Per ticket: branch off main, tests first, one bounded live run with clipped
  screenshots, PR, CI green, `linear-build` closes with evidence, Tarik merges.
- Browser checks run through `ego-browser`: set the viewport override after
  the tab exists; real typing, then read the field value back before
  submitting; scroll targets into view; scope submit clicks to the panel
  (`#panel-food button[type="submit"]`); clip captures to `main` and keep them
  under 6000 px tall; log the h1 before every capture; capture on the
  production build (`pnpm build`, then a small static server) so no dev badge
  covers content; `completeTaskSpace` at the end. Stop servers before unit tests.
- Impeccable reviewer and documenter run as fresh `general-purpose` Agent
  calls from `reference/degraded/*.md`; let the documenter wait for the
  reviewer's verdict.
- Live checks cost one model call each (cents); Textract cents per page.

## First message for the next session (paste this)

```text
We are building GoodNext in /Users/tarikmoody/Projects/foodshare-strands.
Read HANDOFF.md, then CONTEXT.md, then DESIGN.md, then
docs/agents/issue-tracker.md. Do not re-read the planning docs unless a task
needs them.

Deadline is Monday September 14, 7 p.m. Central. Do "Next 1: hosting" from
HANDOFF.md: present the resource list for my go, create only what I approve,
prove the public address in a real browser with both flows, write decision
012, then draft the submission materials in Next 2. Explain in plain English.
Nothing in AWS is created or changed without my go; deploys, pushes, and
merges are mine.
```
