# Building FoodShare Bridge with Matt Pocock Skills

A plain English guide to choosing skills and prompting your coding agent

September 8, 2026 | Version 1.1 | Companion to PRD 1.5

## 1 Start here

Use Matt Pocock’s skills to turn the FoodShare Bridge plan into small, working features. We already have a PRD, research, an architecture, and a selected technology stack. Start with those documents, settle the remaining questions for one feature, and build it through the website, backend, and agent together.

My recommendation is to learn six main skills: **setup-matt-pocock-skills, grill-with-docs, to-spec, to-tickets, implement, and code-review**. Install their supporting skills too. Add research when an answer needs evidence and Impeccable when you are shaping or checking the interface. Matt’s current catalog describes this main development sequence. [AI Hero skills catalog](https://www.aihero.dev/skills).

This guide explains the workflow and provides prompts you can paste into Codex. The prompts are written for FoodShare Bridge; they are not quotations from Matt. Installation, configuration, coding, and deployment have not been performed by creating this guide.

**Read Sections 2–4 once. Then use Sections 5–10 as a workbook, one prompt at a time.** Section 12 has the recommended first message to use when you are ready to start.

### The workflow in everyday language

1. Tell the coding agent where the project’s instructions and work list belong.
2. Resolve the unanswered questions for one feature.
3. Write down exactly what that feature must do.
4. Divide it into small pieces you can demonstrate.
5. Build and test one piece.
6. Check that it meets the requirements and fix the findings.
7. Save enough context for the next session.

You do not need to run every skill for every change. A small, agreed fix can go directly to implementation. A feature with several unresolved decisions needs planning first.

## 2 Understand what each tool does

A **skill** is a reusable set of instructions for the coding assistant. A **prompt** is the specific task you give it now. The skill supplies a method; your prompt supplies the project, limits, and expected result.

| Tool | Its job in this project | Example |
| --- | --- | --- |
| Codex | Reads files, writes code, runs checks, and follows the skills you select | Implements the food plan screen and its API |
| Matt Pocock skills | Guide how we plan, build, test, and review the software | Break a food planning specification into buildable tickets |
| Impeccable | Guides interface design and usability work | Make “Food today” easy to find on a small phone |
| Strands Agents | Runs the application’s agent logic using its permitted tools | Retrieve reviewed food resources and propose a seven-day plan |
| AgentCore Runtime | The selected AWS service where we will run the Strands application | Execute a resident request in the deployed agent runtime |
| Our application code | Enforces permissions, validates results, and handles records and delivery | Reject an inaccessible resource or a reminder without consent |

The last three rows summarize our selected architecture. See [AgentCore Explained](FoodShare-Bridge-AgentCore-Explained.md) and the [Tech Stack](FoodShare-Bridge-Tech-Stack.md) for the detailed design and technical sources.

Matt’s skills belong in the **development workflow**. The resident-facing prompts P01–P08 belong in the **FoodShare application**. Keep those separate: a resident asking for food should never receive a coding assistant’s tools or development instructions.

### A few terms you will encounter

| Term | Plain English meaning |
| --- | --- |
| PRD | The product’s purpose, user needs, scope, and requirements |
| Specification or spec | A precise description of the feature we have agreed to build |
| Ticket or issue | One small piece of work with a clear completion check |
| Acceptance criteria | Observable conditions that must be true before the work is complete |
| Vertical slice | A small working journey through all necessary parts of the application |
| Seam | A boundary where we can test behavior, such as an API request and its response |
| Fixture | A controlled example used for testing, such as a synthetic notice |
| ADR | A short explanation of an important architecture decision and its tradeoff |
| Commit | A saved checkpoint in Git’s history of the project |

## 3 Choose and install the skills

### The main set

| Skill | When you use it | FoodShare Bridge purpose |
| --- | --- | --- |
| `setup-matt-pocock-skills` | Once when configuring the project | Tell the skills where tickets, glossary, and decision records live |
| `grill-with-docs` | A feature still has open questions | Clarify what “verified resource” and “food covered” mean |
| `to-spec` | Decisions are settled and need to survive multiple sessions | Record the exact food planning behavior and failure cases |
| `to-tickets` | The agreed work is too large for one session | Create small journeys with explicit dependencies |
| `implement` | One ticket is ready to build | Build it with behavior tests and review |
| `code-review` | Code exists and needs checking | Check project standards and whether the agreed behavior was delivered |

These purposes follow the individual skill guides: [setup](https://www.aihero.dev/skills-setup-matt-pocock-skills), [grill with docs](https://www.aihero.dev/skills-grill-with-docs), [specification](https://www.aihero.dev/skills-to-spec), [tickets](https://www.aihero.dev/skills-to-tickets), [implementation](https://www.aihero.dev/skills-implement), and [review](https://www.aihero.dev/skills-code-review).

Also install **grilling, domain-modeling, codebase-design, and tdd**. They supply the interview, shared vocabulary, module design, and testing practices that the main workflow uses. In particular, the current `grill-with-docs` requires both `grilling` and `domain-modeling`; installing only its named entry point is insufficient. [Skill prerequisites](https://www.aihero.dev/skills-grill-with-docs).

### Useful additions

| Skill | Reach for it when | Suggested use |
| --- | --- | --- |
| `research` | A decision depends on an external fact | Verify a provider’s data access terms or an AWS integration detail |
| `prototype` | You need to try an interaction to decide whether it works | Compare ways to confirm an uncertain notice date |
| `handoff` | You are finishing a long session | Prepare the next session to continue from the actual files and checks |
| `ask-matt` | You are unsure which skill fits | Ask which step comes next given the current artifacts |
| `wait-what` | An explanation is too technical | Ask for a simpler explanation of the current decision |

The additional skill names and roles are listed in the [current catalog](https://www.aihero.dev/skills). Start with this small working set. You can install the complete collection for convenience, but you do not need to invoke all of it.

Keep `wayfinder` for work whose decisions genuinely span several planning sessions. Our existing PRD means we can usually begin with one feature. Use `diagnosing-bugs` for a reproducible failure and `improve-codebase-architecture` once real code has become difficult to change. `triage` is useful when outside feedback starts arriving; it is not an extra step required for tickets just generated by `to-tickets`. [Wayfinder](https://www.aihero.dev/skills-wayfinder), [ticket workflow](https://www.aihero.dev/skills-to-tickets).

### What is already on this computer

A targeted inspection on September 8 found local files for setup, grill-with-docs, prototype, handoff, tdd, and improve-codebase-architecture. This is not a complete installation audit. Some local text refers to older names such as `to-prd` and `to-issues`, while the current catalog uses `to-spec` and `to-tickets`.

The existing `/Users/tarikmoody/.agents/skills/code-review/SKILL.md` is **CodeRabbit’s** skill. It is not Matt’s review workflow. Before using a generic name such as `code-review`, have Codex identify the exact skill file and its source. Preserve the existing skill and explicitly select Matt’s copy for this workflow, including the review invoked by `implement`.

The project folder also does not yet have a Git repository, based on the inspection for this guide. Configure Git and create a suitable working branch before using a workflow that commits code. No GitHub repository or issue tracker should be assumed to exist.

### Installation commands for later

Run these in a terminal in the Foodshare project folder. They require Node.js and npm. The first two commands inspect what is installed and what is available:

```bash
npx skills@latest list
npx skills@latest add mattpocock/skills --list
```

Then install interactively for Codex:

```bash
npx skills@latest add mattpocock/skills -a codex
```

Select the six main skills, their four supporting skills, and whichever additions you want. Use project scope so the chosen setup can travel with FoodShare Bridge. Review any same-name replacement before proceeding. The CLI supports selecting skills and agents, and project scope is the default. These commands were checked against the CLI’s documentation through Context7. [Skills CLI documentation](https://github.com/vercel-labs/skills/blob/main/README.md), [Matt’s installation instructions](https://github.com/mattpocock/skills#installation-30-second-setup).

Record the source repository, installed revision if available, file locations, and any local modifications. Recheck those files when updating; an updated skill can change its behavior or dependencies.

### How to invoke a skill in Codex

Matt’s site writes skill names as slash commands, such as `/to-spec`. In this guide, the copyable prompts use plain language: **“Use Matt Pocock’s to-spec skill.”** Select the installed skill using the interface available in your coding agent, or provide the exact `SKILL.md` path if a name is ambiguous. A name alone is not proof that the correct skill loaded.

Do not paste the entire guide as one command. Paste the prompt for the current step, read the result, and continue when its completion conditions are met.

## 4 Give the agent the existing project context

These are the documents the skills should build from:

| Document | What it controls |
| --- | --- |
| [PRD](FoodShare-Bridge-PRD.md) | Product behavior, demo scope, accessibility, privacy, and hackathon checklist |
| [Tech Stack](FoodShare-Bridge-Tech-Stack.md) | Selected website, backend, AWS services, and development tools |
| [APIs Data and Prompts](FoodShare-Bridge-APIs-Data-and-Prompts.md) | Data contracts, integrations, resident agent prompts, and evaluation needs |
| [211 V2 Integration Plan](FoodShare-Bridge-211-Integration-Plan.md) | Owner-confirmed API access, Search and Query adapter plan, field mapping, and remaining verification |
| [AgentCore Explained](FoodShare-Bridge-AgentCore-Explained.md) | How the selected hosting and agent framework work together |
| [Research Brief](FoodShare-Bridge-Research-Brief.md) | Earlier policy and service research with sources to recheck |
| [Strands Execution Design](FoodShare-Bridge-Strands-Execution-Design.md) | Earlier detailed workflow reasoning |
| [Architecture diagram](FoodShare-Bridge-Architecture.html) | Visual explanation of the proposed logical components |

Use the current PRD and tech stack for build decisions. Earlier documents provide context; they should not silently replace the later AgentCore decision. Research dates matter: previous research is not a permanent certification of policy or service availability.

### Reusable context prompt

Paste this at the beginning of a new planning session. Later implementation sessions should also receive the specific ticket and its parent spec.

```text
We are building FoodShare Bridge in /Users/tarikmoody/Projects/Foodshare.

Read these existing documents:
- docs/FoodShare-Bridge-PRD.md
- docs/FoodShare-Bridge-Tech-Stack.md
- docs/FoodShare-Bridge-APIs-Data-and-Prompts.md
- docs/FoodShare-Bridge-AgentCore-Explained.md

Use the current PRD and selected stack as the baseline. Preserve the
responsive website, Python Strands agent on AgentCore Runtime, separate
FastAPI backend, and Impeccable UX workflow. Do not restart product discovery.

Keep the demo and live pilot boundaries explicit. Food access requires
neither an account nor a notice upload. Use synthetic sensitive documents
for the demo. Do not decide eligibility or guarantee benefits or food stock.

When technical facts affect the work, follow our Context7 instructions
and verify current official documentation. Identify unavailable integrations
and unresolved decisions instead of inventing them.

Explain decisions in plain English. Point to existing answers before asking
me questions. Tell me what this session will produce and how we will check it.
```

## 5 Configure the workflow and settle one feature

### Step A Set up the project conventions

Start with local Markdown tickets. They are ordinary files you can inspect without setting up GitHub Issues. The setup skill configures the tracker, label vocabulary, and domain documentation. It does not install AWS infrastructure or build the application. [Setup guide](https://www.aihero.dev/skills-setup-matt-pocock-skills).

```text
Use Matt Pocock's setup-matt-pocock-skills skill for FoodShare Bridge.
Read our existing project documents first and preserve all existing
instructions, including Context7 requirements.

My preferences are:
- Local Markdown tickets under .scratch/ for now.
- One project glossary in CONTEXT.md and architecture decisions in docs/adr/.
- Default triage labels unless existing project labels already apply.
- Use AGENTS.md for Codex instructions if neither instruction file exists.

Inspect before changing anything. Show the proposed configuration together
and ask only about unresolved choices. Do not create external issues or
configure cloud services as part of this setup.

Verify that the current Matt skills and their dependencies are available.
Identify any name collisions, especially the existing CodeRabbit code-review.
```

**What you should receive:** configuration in `docs/agents/` and a small instructions block in the chosen project instruction file. These are expected future outputs, not files created by this guide. Setup normally includes review of the configuration; providing your preferences up front avoids repeating settled choices. The glossary and ADRs can be created later when actual terms or decisions are resolved.

### Step B Clarify the first food journey

Use `grill-with-docs` for one bounded question: what must the first “Food today” journey do? Keep the conversation and run `to-spec` next. The glossary records vocabulary, while many feature decisions remain only in the conversation until captured in a specification. [Grill with docs guidance](https://www.aihero.dev/skills-grill-with-docs).

```text
Use Matt Pocock's grill-with-docs skill to settle the first FoodShare Bridge
feature: a resident finds a feasible food option for today.

Read the PRD and data guide. Use the documented direction as the starting
point. Ask one unresolved question at a time and recommend an answer.

Clarify ZIP area, travel limits, resource opening information, service-area
restrictions, unknown inventory, last verification, and the no-match outcome.
Define what the website is allowed to claim about each option.

Agree on observable tests at the API and agent-tool boundaries. Keep the
first feature narrow enough to demonstrate before adding notice uploads.

Put resolved vocabulary in CONTEXT.md. Record consequential architecture
tradeoffs in ADRs when appropriate. Keep a concise decision summary for the
next to-spec step, including open questions and exact acceptance conditions.
```

**What you should receive:** a clear first journey, agreed terms, named behavior checks, and a short list of remaining blockers. A useful distinction to settle is “a listed option,” “an option the resident plans to try,” and “food the resident confirms they obtained.” They must not all become “food secured.”

## 6 Research missing evidence and shape the interface

Use these steps where a specific question blocks the feature. They do not need to become a second general discovery project.

### Research the data the agent will depend on

Matt’s `research` produces a cited Markdown answer from primary sources. Its documented workflow delegates the reading, so give it one bounded question and limit further delegation. A citation is evidence to inspect, not automatic permission to publish a policy rule or reuse a provider’s data. [Research skill](https://www.aihero.dev/skills-research).

```text
Use Matt Pocock's research skill for this question only:
What dependable data can FoodShare Bridge use to show Milwaukee food
resources with opening information and service restrictions?

The owner has confirmed 211 API access. Read the 211 Integration Plan.
Prioritize Search V2 and Query V2; verify actual schemas, local scope,
and permitted reuse rather than repeating general access discovery.

Read the existing research brief and data guide to avoid duplicating work.
Use the organizations' own websites and documentation. Distinguish a public
webpage, downloadable dataset, documented API, and partner-only access.

For each source record its owner, URL, access terms, useful fields,
update frequency if stated, date checked, and remaining uncertainty.
Do not assume live stock, reservations, or unrestricted reuse.

Write docs/research/milwaukee-food-data-access.md. Mark recommendations
separately from sourced facts. Do not contact organizations or register for
services. Use at most one research subagent with no further delegation;
if unavailable, do the research in this session.
```

**What you should receive:** a source register and an answer about what can actually be used. Missing permission or unreliable freshness becomes an explicit dependency, with a manual maintained directory considered as a fallback.

For other runs, replace that question with exactly one of these:

| Research question | Evidence the answer needs |
| --- | --- |
| Which rules apply on the relevant date in Wisconsin? | Official federal and Wisconsin sources, effective dates, affected groups, and state implementation details |
| What does this supported notice class ask the resident to do? | Official examples, action and date fields, and review by someone qualified to interpret the process |
| How should FastAPI call our Strands application on AgentCore? | Current AWS and Strands documentation, authentication boundary, session handling, and a minimal integration check |
| Does the chosen speech service handle our English and Spanish tasks accurately? | A repeatable evaluation using consenting testers or synthetic samples, especially dates, amounts, and mixed-language speech |
| Can a community organization accept navigator requests? | A confirmed partner process, accepted fields, explicit consent, and a real delivery or acknowledgment mechanism |

For policy research, separate proposed changes, enacted future changes, and currently effective requirements. Route interpretation for a resident’s actual case to official staff. The research skill helps gather evidence; it does not replace that review.

### Use Impeccable to shape the user journey

Matt’s skills help define and implement the behavior. Impeccable adds the interface decisions. Our installed Impeccable offers `init`, `shape`, `critique`, `audit`, `adapt`, `clarify`, and `harden`; invoke these through the Impeccable skill, rather than assuming separate commands are installed. [Installed Impeccable instructions](/Users/tarikmoody/.agents/skills/impeccable/SKILL.md).

```text
Use Impeccable's shape workflow for the FoodShare Bridge Food today journey.
Read the PRD, agreed feature decisions, and any existing design context.
If product context is missing, derive a draft from those documents first.

Design for someone stressed, possibly hungry, and using a small phone.
Keep Food this week and Understand my notice or change equally accessible.

Specify the screens, information order, plain-language labels, English and
Spanish text needs, keyboard flow, and loading, empty, stale-data, and error
states. Show source freshness and unknown food availability clearly.

Keep voice optional with a complete text path. Use the PRD's accessibility
requirements. Produce a reviewable UX plan for this feature before coding.
```

**What you should receive:** a small set of screens and states that a developer can build and a resident can understand. Check that the first useful action is apparent without reading a long introduction.

### Prototype only when trying it will answer a question

```text
Use Matt Pocock's prototype skill to answer one interaction question:
Can a resident notice and correct an uncertain deadline before it becomes
part of their action checklist?

Use synthetic notice text. Demonstrate a readable date, an ambiguous date,
and a missing date. Make the resident's confirmed value visible.
Keep this separate from the application and use in-memory state.

Keep the runnable exploration on a separate prototype branch once Git is
set up. Record the question, what we observed, and the decision in the
implementation ticket. Do not treat this exploration as production code.
```

The current detailed prototype guide keeps the runnable evidence on a separate branch, although the catalog’s short description still mentions deleting code. Use the detailed guidance and inspect the installed version. The purpose is to resolve one design question, not to build the whole product without its checks. [Prototype guide](https://www.aihero.dev/skills-prototype).

## 7 Turn the decisions into a specification and tickets

### Step C Write a feature specification

The existing PRD stays the product reference. A feature spec adds enough detail to implement one part consistently. `to-spec` records settled decisions in the configured tracker; with our recommended setup, that means local files. [To spec guide](https://www.aihero.dev/skills-to-spec).

```text
Use Matt Pocock's to-spec skill to capture our agreed Food today feature.
Use this conversation, the PRD, the data research, and the UX plan.
Write the spec to our configured local Markdown tracker and tell me its path.

Preserve the existing PRD. Include:
- The resident's starting situation and the complete successful journey.
- The inputs, evidence required, and visible result.
- Unknown, stale, closed, out-of-area, and no-match cases.
- The boundaries among the website, FastAPI, Strands, and deterministic tools.
- Session isolation and what is allowed in logs.
- The agreed API and tool behavior we will test.
- Links to the relevant PRD requirements and research dates.
- What uses real integration, what uses a labeled fixture, and what is excluded.

Keep unanswered questions visibly unresolved. Do not invent new policy,
partner capabilities, or architecture choices to make the spec look complete.
```

**Check before proceeding:** does the spec preserve the exact decisions you made? “Show a useful plan” is too vague. “A confirmed closure removes the resource from proposed visits, and the revised plan displays any resulting gap” is testable.

### Step D Create small tickets

`to-tickets` creates small, complete paths through the necessary layers and records which tickets depend on others. For local tracking, its current source uses one file per ticket under `.scratch/<feature>/issues/`. It presents the breakdown for review before publishing it. [Ticket skill source](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-tickets/SKILL.md).

```text
Use Matt Pocock's to-tickets skill for the feature spec we just created.
Use our configured local Markdown tracker.

Draft small end-to-end tickets. Each one must deliver observable behavior,
name its real blockers, and include acceptance criteria and evidence needed.
Link each ticket to its parent spec and relevant PRD requirements.

Make the first runnable path as narrow as possible: one synthetic resident
request through the website, FastAPI, and the Strands application using a
curated resource fixture. Plan a real AgentCore integration check early.

Distinguish a local test from a deployed test. Include no-match and unavailable
service behavior. If a ticket cannot fit one session, split its behavior
further while keeping each result independently demonstrable.

Present the breakdown for review, then save the agreed tickets. Do not create
GitHub issues or begin implementation in this step.
```

**What you should receive:** a readable work list in dependency order. Avoid separate mega-tickets called “build all frontend,” “build all backend,” and “build all agents.” Those postpone proof that the parts work together.

### Suggested feature sequence for FoodShare Bridge

These are milestones to split into tickets, not promises that each fits one session. Research and actual integration results may change the order.

| Order | Demonstrable result | Main evidence |
| --- | --- | --- |
| 1 | A synthetic resident gets a food option or an honest no-match result | Website to backend to Strands path; early real AgentCore invocation; source and constraint checks |
| 2 | A seven-day plan accounts for food on hand, budget, travel, and kitchen constraints | Fixed examples show feasible suggestions and visible unmet needs |
| 3 | A reviewed closure updates two separate household plans | Shared resource change; no household data leakage; affected plans revised |
| 4 | A supported synthetic notice becomes confirmed fields and an official next action | Missing or ambiguous dates require confirmation; unsupported notices route to help |
| 5 | A resident prepares an activity summary and synthetic proof packet | Correct arithmetic; planned hours stay separate from completed hours; original evidence preserved |
| 6 | A resident uses Spanish and optional speech to complete the same journey | Transcript correction, critical-field confirmation, microphone denial, and text fallback |
| 7 | A controlled reminder or available partner request follows an explicit preview | Consent, duplicate prevention, cancellation, and truthful delivery status |
| 8 | The complete demo is understandable and reproducible | Accessibility checks, evaluation results, deployment evidence, and current hackathon checklist |

All planned demo features remain subject to the PRD. If the available time cannot support them, make an explicit scope decision and update the PRD rather than silently dropping requirements. A staged demo is not approval for a public pilot with real documents.

## 8 Implement one ticket and verify the agent behavior

### Step E Build the ticket

Matt’s documented `implement` workflow tests the agreed behavior, reviews the change, and commits to the current branch. It does not create the branch, automatically close the ticket, or necessarily resolve review findings. Establish the Git baseline first and name the ticket explicitly. [Implementation guide](https://www.aihero.dev/skills-implement).

Replace `TICKET_PATH` below with the actual path produced in Step D. It is a placeholder, not an existing file.

```text
Use Matt Pocock's implement skill for TICKET_PATH only.
Read the ticket, parent spec, relevant PRD requirements, and selected stack.

First inspect the Git state. Use a dedicated feature branch and preserve
unrelated changes. Record the starting commit for the later review. If the
project still has no Git repository, establish that local baseline first.

Build the agreed behavior through the necessary layers. Use the specified
public API and tool boundaries for tests. Run a failing behavior test first,
make it pass, then improve the implementation without changing the behavior.

For the Strands part, use the relevant project prompts from the APIs Data and
Prompts guide. Use only the tools authorized for this ticket. Validate model
results before the website or a delivery service can use them.

Keep tests repeatable with synthetic fixtures. Separately run the real
integration check required by the ticket when the authorized environment is
available. If blocked, report that check as blocked rather than passed.

Run appropriate type, behavior, and journey checks. Use Matt's review skill
from the verified installation. Fix blocking findings before marking the
ticket complete. Report what works, the evidence, and what remains unresolved.
Keep this work local unless deployment or publication is separately authorized.
```

The testing approach follows [Matt’s TDD guidance](https://www.aihero.dev/skills-tdd). Focus tests on outcomes residents and other application components depend on. A test that merely checks whether a particular internal function was called is rarely enough to prove that a food plan is feasible.

### How this applies to Strands and AgentCore

Give the coding agent a specific task for each application responsibility:

| Application responsibility | What the implementation ticket should require |
| --- | --- |
| Food resource lookup | Return structured reviewed records with provenance and freshness; preserve unknowns |
| Seven-day planning | Propose visits and meals from available evidence and resident constraints; expose gaps |
| Notice interpretation | Extract candidate fields; require confirmation for critical uncertainty; avoid inventing a deadline |
| Policy guidance | Use dated, reviewed sources and route case decisions to official staff |
| Work or activity planning | Use deterministic arithmetic; distinguish planned, reported, and supported hours |
| Proof packet | Assemble selected evidence and a summary while preserving original attachments |
| Language and voice | Let residents correct the transcript and confirm important fields before action |
| Reminders and referrals | Enforce preview, consent, and duplicate prevention outside the model |
| Community maintenance | Stage source changes for review before shared records are published |
| AgentCore integration | Prove a request reaches the deployed Strands runtime and returns a validated response under the correct permissions |

These are project implementation requirements, not features supplied automatically by Matt’s skills or AgentCore. The detailed contracts remain in the [APIs Data and Prompts guide](FoodShare-Bridge-APIs-Data-and-Prompts.md).

### A focused prompt for the seven day plan

Use this when preparing or implementing the corresponding agreed ticket:

```text
Implement the agreed seven-day planning behavior using our Strands design.
Start from the resident coordinator and food-planning prompts in the data
and prompts guide; preserve their evidence and safety requirements.

Retrieve structured resource records through the approved tool. Enforce
opening information, travel limits, service restrictions, and freshness in
deterministic code. Have the model explain a feasible proposal from those
results. Validate the proposal before presenting it.

Use fixed tests for: a resource closing today; a household without cooking
facilities; an unaffordable grocery suggestion; unknown pantry stock; a
midweek closure; and no feasible nearby option. Missing food coverage must
remain visible. Do not claim a pantry will supply particular ingredients.

Separate repeatable fixture tests from the live Bedrock and AgentCore check.
Capture sanitized evidence of tool use, output validation, latency, and
failure behavior. Do not log resident documents or sensitive input text.
```

**What you should be able to see:** the website shows where an option came from, why it fits the entered constraints, what to do next, and what is still uncertain. A successful model response alone is not proof that this happened.

## 9 Review the code and the actual resident experience

### Step F Check the change against its promises

Matt’s review separates **Standards** from **Spec**: whether the code follows project practices, and whether it implements the requested behavior. Its documented workflow uses two reviewers and requires a valid comparison point. It complements testing and domain review. [Code review guide](https://www.aihero.dev/skills-code-review).

Use the starting commit recorded during implementation as `BASE_COMMIT` and replace `SPEC_PATH` with the real spec path.

```text
Use Matt Pocock's code-review skill, not the existing CodeRabbit skill.
Read and identify the exact Matt skill file before reviewing.

Review the committed changes since BASE_COMMIT against SPEC_PATH and its
linked PRD requirements. Keep Standards and Spec findings separate.

For each finding, identify the relevant code and requirement, explain the
resident-visible consequence, and describe a concrete correction.

Pay particular attention to unsupported food or policy claims, uncertain
dates, private data in logs, cross-session access, and delivery without
consent. Explicitly list acceptance criteria that lack evidence.
Do not publish review comments or change external issues.
```

After review, use a bounded follow-up:

```text
Resolve the confirmed blocking findings from this review within the ticket's
scope. Add or adjust a behavior test where it would catch the failure.
Run the checks affected by the changes, and recheck the unresolved findings.

Update the local ticket with evidence for each acceptance criterion.
Mark it complete only when all required checks pass; identify any remaining
external dependency or live integration check as blocked or unverified.
```

### Step G Check usability with Impeccable

Use separate, focused requests so each review has a clear target:

```text
Use Impeccable's critique workflow on the implemented Food today journey.
Check whether a stressed resident can identify the next useful action,
understand uncertainty, and recover when no option fits. Review the actual
mobile and desktop screens and identify concrete problems.
```

```text
Use Impeccable's audit workflow on that journey against the PRD accessibility
requirements. Check keyboard operation, focus, labels, zoom, narrow screens,
and English and Spanish layouts. Report automated and manual evidence
separately. Do not claim a full accessibility certification from a scanner.
```

Then request `adapt`, `clarify`, or `harden` for the specific problems found. A resident or community helper should also try the journey. AI review cannot establish that real residents understand the result.

### Completion questions for every feature

- Can I demonstrate the promised result from a realistic starting screen?
- Does the failure case give a useful next action?
- Can I trace important claims to the permitted data and current reviewed rules?
- Are data ownership, permissions, and consent enforced by code?
- Do the checks cover the changed behavior, including real integration where required?
- Are the ticket and PRD honest about what is complete and what remains unavailable?

## 10 Finish a session without losing the work

Use `handoff` when the conversation contains useful state that is not already in a ticket, spec, or commit. Reference those artifacts instead of copying them into another competing plan. [Matt’s skill collection](https://github.com/mattpocock/skills).

```text
Use Matt Pocock's handoff skill for the next FoodShare Bridge session.
Focus it on continuing the current ticket or the next unblocked ticket.

Include the current branch and commit, exact ticket and spec paths, files
changed, checks completed, unresolved failures, and the next concrete action.
Reference the PRD and stack rather than repeating them.

Distinguish fixtures from verified live integrations. Include no credentials
or resident data. Save the handoff and tell me where it is.
```

If an explanation becomes difficult to follow, use this at any point:

```text
Use Matt Pocock's wait-what skill to explain the last recommendation again.
Use ordinary language and one FoodShare Bridge example. Explain the decision
I need to make, your recommendation, and its practical tradeoff.
```

If you are unsure which step is appropriate:

```text
Use Matt Pocock's ask-matt skill. We have an existing PRD and selected stack.
Inspect the current ticket, spec, and work state. Recommend the next skill
for the one unfinished task and explain why in a short paragraph.
```

## 11 Avoid the common traps

| Trap | Better instruction |
| --- | --- |
| “Build the whole PRD” | “Build this one ticket and prove these acceptance criteria” |
| Repeating discovery already captured in the PRD | “Read the current documents; ask only about unresolved choices” |
| Assuming a same-name skill is Matt’s | “Show the loaded SKILL.md path and source” |
| Treating a glossary as the complete specification | “Capture exact decisions in the feature spec before changing sessions” |
| Letting the model calculate or enforce everything | “Use deterministic validation for dates, hours, access, consent, and constraints” |
| Treating a local fixture as a live service integration | “Label the fixture and record a separate deployed verification result” |
| Assuming an available URL means an available API | “Verify access terms and supported fields before designing around it” |
| Calling an agent-written policy answer verified | “Check official sources and obtain the required domain review” |
| Assuming a review automatically fixes code or closes tickets | “Resolve findings and reconcile each acceptance criterion explicitly” |
| Starting many overlapping agents | “Use one implementation ticket at a time; bound any research or review delegation” |
| Turning a quick design experiment into the production feature | “Keep the prototype as evidence and implement from the agreed spec” |
| Submitting a feature list without demonstrable community value | “Show one reviewed closure improving two isolated household plans” |

Before submission, use the current PRD hackathon checklist and recheck the event’s official rules. Have the coding agent produce a table of requirement, artifact, verification result, and remaining gap. This guide does not change event requirements or certify submission readiness.

## 12 The first prompt I recommend using

This is a preparation task. It deliberately stops before installation or coding so you can see the specific changes the setup will require. Once the inventory is clear, proceed with the installation and Step A.

```text
Prepare FoodShare Bridge to use Matt Pocock's current skills.

Read:
- docs/FoodShare-Bridge-Matt-Pocock-Skills-Guide.md
- docs/FoodShare-Bridge-PRD.md
- docs/FoodShare-Bridge-Tech-Stack.md
- docs/FoodShare-Bridge-APIs-Data-and-Prompts.md
- docs/FoodShare-Bridge-AgentCore-Explained.md

Inventory the relevant installed skills and compare them with Matt's
current official collection. Identify missing dependencies, older names,
and collisions, especially CodeRabbit versus Matt's code-review.
Inspect Git and project instructions too.

Give me a concrete setup proposal for Codex with local Markdown tickets,
one project glossary, and the existing PRD and AgentCore stack preserved.
Explain it in plain English. Do not install, overwrite skills, or start
building during this preparation task.

End with the exact setup action to take next. Our first implementation
target after setup and feature clarification is the Food today journey.
```

## 13 Sources and maintenance

Skill names, behavior, and installation guidance were researched on September 8, 2026 using the linked AI Hero pages, Matt’s official repository, and Vercel’s Skills CLI documentation via Context7. The individual pages contain more precise behavior than some short catalog descriptions. The installed `SKILL.md` is what the coding agent will actually execute, so reconcile it with these sources before relying on a workflow.

The project examples, build order, prompts, completion checks, and local-tracker recommendation are authored recommendations for FoodShare Bridge. They do not imply that Matt reviewed this project or that its policies, architecture, or integrations have been implemented.

When the project’s PRD, installed skills, policy sources, or hosting choices change, update the affected prompts and keep this guide linked to the current documents. Preserve reviewed policy evidence in a dated source register; avoid letting old research silently become current application rules.
