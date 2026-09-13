# GoodNext handoff

Written September 13, 2026, 12:55 CDT; updated 14:35 CDT after hosting went live.
Read this, then `CONTEXT.md`, then `DESIGN.md`, then
`docs/agents/issue-tracker.md`. Do not re-read the planning docs unless a
task needs them; the decisions are settled and the product is built.

**Deadline: Monday September 14, 2026, 7 p.m. Central.** Judging runs through
October 8. The public address is live and the submission drafts are written;
what remains is Tarik's part: merge, placeholders, video, Devpost form.

**Public address (plain HTTP, decision 012):**
`http://GoodNe-Servi-SOh7w0HGiJhV-1702778700.us-east-1.elb.amazonaws.com`

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
| Hosting (MOO-793, branch `hosting-fargate`, PR pending) | `services/api/Dockerfile`, `infra/web/` | One container (site at `/`, API at `/api/*`) on ECS Fargate behind an ALB, stack `GoodNext-web`, us-east-1. 8 jest tests; CI job. Deploy: `cd infra/web && npx cdk diff` then `npx cdk deploy` on Tarik's go. Tear down: `npx cdk destroy`. |
| Submission drafts | `docs/submission/` | H07 diagram (archify), H08 description, H09 video script, H10 Devpost fields, H06 check. Placeholders: live address, video link, Builder ID, hackathon window start date. |
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

## Next 1: hosting (done September 13)

Deployed as decision 012 describes: one ARM Fargate task (0.5 vCPU, 1 GB) in
the default VPC, an Application Load Balancer with a 300 s idle timeout, a
task role limited to `InvokeAgentRuntime` on runtime v7 plus
`textract:DetectDocumentText`, 7-day logs, ECS circuit breaker. Port 443
answers plain HTTP with a fixed 400 so https-first browsers fall back at once.
The session cookie is Secure exactly when the request arrived over HTTPS
(uvicorn trusts the balancer's `X-Forwarded-Proto`); no env switch.

Proven live on September 13: `/api/health`, the page and a static asset; a
food plan for 53206 in 91 s by request and in a real browser (ego-browser,
delayed status at 35 s, heading "Food today, Thursday, September 10", 3 options);
the six-month letter upload in 29 s (6 findings, 4 tasks). Evidence:
`docs/evidence/hosting-live-*`. Screenshots: see the learning-log entry for
2026-09-13; both on-screen browsers failed to capture that afternoon.

Cost about $1 a day. Remove after judging with `npx cdk destroy` in `infra/web`.
HTTPS later: request an ACM certificate for a hostname Tarik owns and redeploy
with `-c certificateArn=...`; the 443 stand-in listener is replaced automatically.

## Next 2: submission materials (PRD section 13) — drafted in `docs/submission/`

Read `docs/submission/README.md` first. Tarik fills in: AWS Builder ID, the
hackathon window start date, the video link, and confirms the food-site
example in the video script. Then records the video and submits.

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
3. The hosted API runs under a task role, so the expired-laptop-login 503 no
   longer applies to the public address (local runs still need `aws login`).
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
