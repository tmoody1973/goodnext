# Issue tracker: Linear via linear-build

Issues for this repo live in **Linear**: workspace Moodyco, team **MOO**, project
**GoodNext — Agents for Humans Hackathon**. The project does not exist yet; the
`linear-build` kickoff creates it. Do not create a second project.

The PRD, research, and specs stay in this repository under `docs/`. Linear
holds the execution contracts. There are no Markdown tickets.

## Who does what

| Step | Skill | Output |
| --- | --- | --- |
| Settle decisions and vocabulary | `mattpocock-skills:grill-with-docs` | `CONTEXT.md` terms, `docs/decisions/` records |
| Write the feature spec | `mattpocock-skills:to-spec` | `docs/specs/<feature>.md` in this repo |
| Cut the spec into small end-to-end tickets | `mattpocock-skills:to-tickets` | A ticket list with blocking edges, presented for review |
| Create, move, and close issues | `linear-build` | Linear issues and verification comments |
| Build one issue | `mattpocock-skills:implement` with `mattpocock-skills:tdd` and `mattpocock-skills:code-review` | Code, tests, review findings |

`to-tickets` never calls the Linear tools. Its reviewed ticket list is handed to
`linear-build`, which creates one issue per ticket in dependency order.

## Issue shape (the contract)

Every issue body has these sections, in this order:

```markdown
## Intent
## Acceptance criteria
## Verification checklist
## Out of scope
## Links
```

- **Verification checklist** items are each tagged `[fixture]` or `[live]`.
  `[fixture]` runs against synthetic data in the repo. `[live]` runs against a
  real deployed service, real API, or real browser.
- **Links** names the PRD requirement IDs (for example FR04, I03), the spec
  file, and any decision record the issue depends on.
- **Blocked by** uses Linear's native blocking relation, set by `linear-build`.

## Status meanings

| Linear status | Meaning here |
| --- | --- |
| Backlog | Not yet triaged, or waiting on information |
| Todo | Fully specified and ready to build |
| In Progress | `linear-build` is building it |
| In Review | Built; verification checklist running |
| Done | Every checklist item passed, evidence posted as a comment |
| Canceled | Will not be done; reason in a comment |

## Done gate

`linear-build` moves an issue to Done only when its verification checklist
passes. `[fixture]` items alone do not satisfy an issue that has `[live]` items.
The closing comment states which items were fixture and which were live, with
the evidence (test output, request and response, screenshot, or identifier).

## Standing restriction

Verification never uses a real resident's documents, notices, contact details,
or account data. Synthetic fixtures only, per PRD section 3. An issue whose
checklist would require real resident data is blocked, not verified.

## When a skill says "publish to the issue tracker"

Hand the ticket to `linear-build` ("turn this into a Linear issue"). It drafts
the body in the shape above, shows it, and creates it on a yes.

## When a skill says "fetch the relevant ticket"

`linear-build` reads it with `get_issue` by identifier, for example `MOO-123`.

## Tool namespace note

`linear-build`'s text refers to `mcp__linear-server__*`. In Claude Code these
tools load as `mcp__plugin_linear-build_linear-server__*`. Same tools, longer
names.

## Wayfinding operations

`wayfinder` is not in use for this project. If it is adopted later, the map is
a Linear parent issue and children are sub-issues with native blocking.
