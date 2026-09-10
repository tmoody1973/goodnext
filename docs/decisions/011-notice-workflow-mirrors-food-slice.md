# 011: The notice workflow mirrors the food slice inside one agent entrypoint

Date: September 10, 2026. Status: decided.

## Decision
The understand-notice workflow (MOO-789) is built as a mirror of the food-today
slice, inside the same agent package and the same AgentCore entrypoint. `invoke`
in `app/goodnext/main.py` dispatches on the request's `workflow` field: an
`understand_notice` request runs P01 + P02 with the three notice tools
(`read_notice`, `get_policy_evidence`, `resolve_help_route`); every other request
keeps the food-today path. The notice validator reuses two food-slice patterns
unchanged: a request-scoped ledger of tool-returned IDs as the fabrication check,
and the never-list scan mechanism in `claims.py`, applied to a second reviewed
constant, `NOTICE_NEVER_LIST`.

## Why this came up
The product promises two entry points (PRD FR02, FR03, FR07), but only food-today
existed in the repo. The notice half needed P02, three tools, a
`NoticePlanProposal`, and a validator. The question was whether to grow a second
agent configuration and service, or to fold the workflow into the one entrypoint
the food slice already deploys.

## Options
1. **One entrypoint, dispatch on workflow** (chosen). One runtime, one system prompt, workflow instruction selected per request, tools scoped per workflow. Cost: `invoke` gains a branch, and two request models share the file.
2. **A second agent and a second runtime.** Clean separation. Cost: a second deploy, a second cold start, and duplicated help-route and envelope wiring, for a demo that runs one runtime.
3. **Reuse the food request model and add notice fields.** Fewest new types. Cost: one model with two shapes and optional fields that only make sense for one workflow; the validator would have to guess the workflow.

## What we chose and why
Option 1. The APIs doc already describes one resident agent configuration with a
controller-selected workflow instruction and an explicit per-invocation tool set
(section 5). Dispatching in the entrypoint matches that, keeps one deploy, and
lets the notice slice reuse the ledger and never-list mechanisms rather than copy
them. The two request models stay separate and typed, so each workflow validates
its own shape.

## What we gave up
A hard process boundary between the two workflows. They share a runtime and a
system prompt, so a change to P01 affects both. The tool sets are still scoped per
workflow, so neither workflow can call the other's tools.

## How we'll know if this was right
The notice slice ships as runtime v6 with no `agentcore.json` change and no second
AWS resource. The one live notice request returns a `success` envelope whose
evidence IDs all trace to the request ledger, and its resident-facing text carries
no `NOTICE_NEVER_LIST` word.

## What actually happened
(Tarik fills this in.)
