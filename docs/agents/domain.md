# Domain Docs

How the engineering skills consume this repo's domain documentation when
exploring the codebase.

## Before exploring, read these

- **`CONTEXT.md`** at the repo root: the single project glossary. It does not
  exist yet. `mattpocock-skills:domain-modeling` (reached through
  `grill-with-docs`) creates it the first time a term is resolved.
- **`docs/decisions/`**: decision records, numbered `NNN-short-slug.md`. Read
  the ones that touch the area you are about to work in.

If a file does not exist, proceed silently. Do not suggest creating it upfront.

## Decision record format

This repo uses `docs/decisions/` in place of `docs/adr/`. Records follow the
plain-English format already used by 001 and 002: Decision, Why this came up,
Options, What we chose and why, What we gave up, How we'll know, and a
"What actually happened" field left blank for the owner to fill in later.
Skills that would write an ADR write in this format and this folder instead.
Define any technical term inline on first use.

## File structure

Single-context repo:

```
/
├── CONTEXT.md            (created lazily)
├── docs/decisions/
│   ├── 001-agentcore-cli-deploy-path.md
│   └── 002-goodnext-name-and-doc-filenames.md
└── app/, services/, agentcore/
```

## Use the glossary's vocabulary

When output names a domain concept (issue title, test name, refactor
proposal), use the term as defined in `CONTEXT.md`. Terms the PRD already
fixes, such as Prototype, Pilot, Later, Bridge Plan, and the plan and task
states in PRD section 8, are the starting vocabulary.

## Flag decision conflicts

If output contradicts an existing decision record, say so explicitly rather
than silently overriding: "Contradicts decision 001, but worth reopening
because…".
