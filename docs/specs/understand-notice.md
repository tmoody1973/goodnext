# Understand notice

Feature spec. September 10, 2026. Source: PRD 1.6 FR02, FR03 and FR07;
`docs/FoodShare-Bridge-APIs-Data-and-Prompts.md` sections 3, 4, 6 (P02) and 7;
`CONTEXT.md`; decision 011. Triage: ready-for-agent, ticket MOO-789.

## Problem Statement

A Milwaukee resident gets a FoodShare notice and cannot tell what it asks, when
it is due, or where to act. The letter mixes several tasks, names a person and a
program, and states a date in words. A wrong reading costs benefits. The resident
should never be told they are eligible, exempt, or safe by a website that cannot
know any of that; only official staff decide the case.

## Solution

The resident selects an authorized synthetic notice. The agent reads its finding,
retrieves approved policy for the identified topic, and resolves the official
route. It returns one prominent next action, a checklist, the deadline in the
notice's own words, the supporting evidence, an official route, and every unknown
left to confirm. Notices and people stay separate. A missing date stays unknown.
A passed date is kept, with an urgent contact step. Food planning is offered
independently and never gated behind the notice.

This feature is the notice half of the agent: prompt P02, three scoped tools, a
`NoticePlanProposal`, and a validator. It mirrors the food-today slice. The
website route and the notices API endpoint are separate tickets.

## User Stories

1. As a resident, I want the notice's request shown in plain words, so that I know what to do.
2. As a resident, I want the deadline shown in the notice's own words, so that a date is never invented for me.
3. As a resident whose notice states no clear date, I want that shown as unknown with a step to confirm it, so that I am not given a false deadline.
4. As a resident whose deadline has passed, I want it kept with an urgent contact step, so that I am not told the case cannot be repaired.
5. As a resident with two notices, I want each notice and person kept separate, so that one person's task is never applied to another.
6. As a resident aged 61, I want the work requirement explained from dated guidance, not decided by my age, so that I am not told a threshold I do not have.
7. As a resident, I want each action tied to its policy source and an official route, so that I can check it and act.
8. As a resident, I want the site to never say I am eligible, exempt, closed, or that my benefits will continue or stop, so that I am not misled about my case.
9. As a resident, I want food planning offered without the notice, so that help with food is never gated.
10. As a developer, I want an action stripped when it cites a notice, policy, or route the tools did not return, so that a fabricated citation can never reach the screen.
11. As a developer, I want a violating action stripped and the response marked partial, so that one bad action does not hide the good ones.
12. As a reviewer, I want the resident-facing wording checked against a notice never-list by a test, so that a copy change cannot reintroduce a prohibited claim.

## Implementation Decisions

- **Prompt (D-N1).** P01 stays the shared system prompt. P02 is added verbatim as the workflow instruction. The system prompt does not change.
- **One entrypoint, two workflows (D-N2).** `invoke` dispatches on the request's `workflow` field. `understand_notice` runs P01 + P02 with the three notice tools; anything else keeps the food-today path. See decision 011.
- **Tools (D-N3).** `read_notice` returns one authorized finding by id; `get_policy_evidence` returns approved dated passages for a topic; `resolve_help_route` returns the reviewed official route for a topic. Each returns the shared envelope shape and records the IDs it returned in a request-scoped ledger. No tool decides eligibility, exemption, or case status, and none submits anything.
- **Notice text is data (D-N4).** The notice passage is preserved in the finding, separate from interpretation, and arrives as a tool result. The task text carries only the notice IDs and `now_local`, delimited; no notice body is merged into the prompt.
- **Deadline handling (D-N5).** The validator sets each kept action's deadline text verbatim from the finding, and its status (upcoming, passed, unknown) from the server clock. A missing parsed date is unknown and adds a confirm step; it is never inferred. A passed date is kept and adds an urgent contact step.
- **Fabrication check (D-N6).** An action is stripped when it cites a notice, policy, or route ID the tools did not return this request. This is the notice analog of the food ledger.
- **Prohibited claims (D-N7).** `NOTICE_NEVER_LIST` in `claims.py` names the claims the agent must never make: eligibility decisions, exemption approvals, benefit continuity, and official outcomes. It is scanned by the same mechanism as the food never-list. An action, checklist item, or explanation that hits it is stripped.
- **Partial on violation (D-N8).** Any stripped action or free-text hit marks the response `partial`. No action identified at all is `needs_clarification`. A found notice with no finding, or an unknown notice id, short-circuits to `needs_clarification` with no model call.
- **Contract shape (D-N9).** The shared response envelope is unchanged. `NoticePlanProposal` carries notice IDs, actions with provenance, next step, checklist, supported dates, evidence and route IDs, confirmations and unresolved fields. Every envelope still carries the three reviewed help routes (MOO-780).

## Testing Decisions

A good test checks what a resident or a caller can observe: a returned finding,
a status, a derived date, a stripped action, a prohibited claim kept out. It
does not check how the ledger is stored.

Two seams:

1. **Tool and validator functions with the notice fixtures.** read_notice returns a finding and records it; an unknown id is no_match; missing date and missing pages are flagged; get_policy_evidence and resolve_help_route match on topic. The validator keeps a cited action and derives its deadline from the finding; strips an action citing an unreturned notice, policy, or route; strips a prohibited claim; keeps a passed date with an urgent step; does not infer a missing date; strips a prohibited claim from checklist and explanation; the never-list scan over a success envelope is empty.
2. **Entrypoint wiring with the faked-model fixture.** `tests/conftest.py` refuses to build either agent in a fixture test. A not-found notice short-circuits without the model. A fake structured model proves dispatch, validation, and envelope wiring. `invoke` dispatches `understand_notice`, needs clarification on a bad payload, and carries the three help routes.

The one live check for this feature (one real request through the deployed API
and AgentCore Runtime) is deferred to the deploy, since food-today owns the only
live-run harness today.

## Out of Scope

- The notices API endpoint (`POST /api/notices`) and the notice web route (separate tickets).
- Real resident uploads, OCR, and manual free-text notice entry; only authorized synthetic fixtures are read.
- Proof packet, work-hours calculator, reminders, speech, and plan revision (later features and their prompts).
- Any eligibility, exemption, or case-status decision; those remain with official staff.

## Further Notes

Only synthetic notice fixtures are used, labeled synthetic in the file. The
policy passages are reviewer-approved dated records checked against public DHS
pages on 2026-09-08, not live policy. This ships as runtime v6 on the next
AgentCore deploy; the entrypoint and `agentcore.json` do not change, so no other
AWS change is needed.
