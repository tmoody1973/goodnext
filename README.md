# GoodNext

A free, responsive website that helps Wisconsin households turn a confusing
FoodShare notice or life change into a clear official next step and a practical
plan for food this week. Milwaukee demonstration first; English and Spanish.

GoodNext is the product name. The planning documents in `docs/` still use the
working title "FoodShare Bridge"; PRD 1.6 is the current baseline.

**What GoodNext does not do:** decide eligibility, promise benefits, promise
food stock, or ask for an account, a notice, or a Social Security number before
helping someone find food.

## Layout

| Path | What it is |
| --- | --- |
| `app/goodnext/` | Strands agent, deployed to Amazon Bedrock AgentCore Runtime |
| `agentcore/` | AgentCore CLI config and CDK stack (`agentcore deploy`) |
| `services/api/` | FastAPI backend: sessions, validation, bridge to the agent |
| `apps/web/` | Next.js static site (not started; Impeccable shape pass first) |
| `docs/` | PRD, research, tech stack, prompts, decisions |

## Run the first slice locally

```bash
# agent, terminal 1 (needs AWS credentials with Bedrock access)
agentcore dev

# API, terminal 2
cd services/api && uv run uvicorn goodnext_api.main:app --port 8000

# ask for food today with zero budget and no kitchen
curl -s localhost:8000/api/plans -H 'content-type: application/json' \
  -d '{"constraints":{"zip_code":"53206","budget_usd":0,"kitchen":"none","travel":["bus"]}}'
```

Offline tests (no AWS): `cd app/goodnext && uv run pytest` and
`cd services/api && uv run pytest`.

## Demo boundaries

The demo runs the real agent on AgentCore with a **synthetic** Milwaukee food
directory (`app/goodnext/fixtures/`), synthetic notices, and labeled test
delivery. A public pilot needs the gates in PRD section 11. Every integration
that is not wired yet is listed in `docs/decisions/`.

Hackathon: Agents for Humans, deadline September 14, 2026, 7 p.m. Central.
