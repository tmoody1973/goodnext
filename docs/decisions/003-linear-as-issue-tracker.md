# 003 Track work in Linear through linear-build, not in Markdown tickets

**Decision** — Linear is the single source of truth for tickets, dependencies, status, acceptance criteria, and verification evidence. The `linear-build` skill is the only thing that creates or closes issues. Matt Pocock's skills plan and build; they do not run a second tracker.

**Why this came up** — The Skills Guide, written September 8, 2026, proposed local Markdown tickets under `.scratch/`. Tarik already runs every other project in Linear with a verification-gated workflow. Two trackers would mean two places to look and two definitions of "done."

**Options**
- *Linear via linear-build.* One tracker, evidence attached to each issue, dependencies as native relations. Cost: setup needs a Linear project and every ticket passes through one more step.
- *Local Markdown under `.scratch/`.* Zero setup, works offline. Cost: no status history, no dependency graph, and a second convention for a solo developer who already uses Linear.
- *GitHub Issues.* Native to the new public repo. Cost: not where Tarik tracks work, and no verification-evidence habit there.

**What we chose and why** — Linear via linear-build. Tarik's call, Claude drafted the configuration. Decision records stay in `docs/decisions/` in the plain-English format rather than a second `docs/adr/` folder, so there is one decision log.

**What we gave up** — The guide's copyable prompts assume `.scratch/` and `docs/adr/`; they need a mental substitution when reused. Two triage roles have no Linear label and are approximated with a status plus a description line.

**How we'll know if this was right** — Every closed GoodNext issue in Linear carries a verification comment that distinguishes fixture from live evidence, and nobody creates a `.scratch/` folder by habit.

**What actually happened** —
