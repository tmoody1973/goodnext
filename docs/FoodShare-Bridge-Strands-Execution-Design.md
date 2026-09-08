# FoodShare Bridge Strands Execution Design

How the agent turns notices and household needs into reviewed action plans

September 4, 2026 | Version 1.1 | Proposed implementation for a responsive Wisconsin website

## 1 Purpose and implementation direction

FoodShare Bridge helps residents understand changes to food assistance, organize official next steps, and find food for the coming seven days. This document translates the research brief into an execution design: what triggers each workflow, what Strands does, which tools and data it needs, what the application checks, and what the resident receives.

The recommended first implementation uses the Strands Python SDK with one resident-facing agent configuration and narrowly scoped application tools. Each resident receives an isolated execution context. Public policy and community-resource maintenance run in separate background jobs with separate permissions. These roles do not require a swarm of agents.

All FoodShare-specific tools and records named here are proposed application components. They must be implemented; they are not built-in Strands features. Python is a recommendation, while the model, hosting platform, database, extraction service, translation service, and SMS vendor remain decisions for the PRD. This document specifies intended behavior, not a completed integration.

The design responds to SNAP changes through two outcomes: fewer preventable process failures and more feasible routes to food. It cannot reverse statutory eligibility changes, determine eligibility, guarantee a benefit amount, or guarantee food availability. Food planning remains available independently of the benefits workflow.

## 2 What Strands supplies and what we build

Strands runs a model-driven loop that can select tools, inspect their results, and continue toward an answer. Python tools can be exposed through the @tool decorator. Structured outputs can return application-shaped records, and interrupts can pause execution for human input. These SDK capabilities support the design below. [T01](https://strandsagents.com/docs/user-guide/concepts/agents/agent-loop/), [T02](https://strandsagents.com/docs/user-guide/concepts/tools/custom-tools/), [T03](https://strandsagents.com/docs/examples/structured_output/), [T04](https://strandsagents.com/docs/user-guide/concepts/interrupts/)

| Component | Responsibility | Completion evidence |
| --- | --- | --- |
| Responsive website | Collect minimal inputs, display source passages, corrections, plans and consent previews | Resident can review and correct the proposed action |
| Application workflow controller | Select allowed tools, enforce workflow stages, permissions and resource limits | A valid transition recorded against the current plan version |
| Strands agent | Interpret the request, retrieve relevant evidence, propose explanations and plans, adapt after changes | Structured proposal with sources and unresolved questions |
| Data and validation services | Filter applicable policies, check dates and totals, enforce resource constraints | Validation results supporting or rejecting the proposal |
| Delivery services | Build files, queue approved reminders and deliver approved partner requests | Artifact, job or provider receipt with explicit status |
| Review console | Let authorized staff approve policy changes and verify resource updates | Reviewer identity, decision, timestamp and published version |

The website sends an authorized request to the controller. The controller constructs a restricted agent invocation. Tools read permitted records and return evidence. The agent proposes a result. Application validators check it before the website displays it or delivery services act on it. A model-selected tool order cannot bypass a mandatory stage.

No direct ACCESS case access, agency submission capability, pantry inventory feed, or appointment-booking integration is assumed. Official links and contact routes are the baseline.

## 3 Shared execution rules and records

### Inputs and trusted context

The backend supplies the session identity, authorized document IDs, locale, current date in America/Chicago, plan version, and permitted tool set. The model cannot select another household's identity or grant itself access by naming a file. Tool services independently enforce those permissions.

Resident text, uploaded documents, retrieved webpages, and partner descriptions are data. Instructions embedded in them cannot change tool permissions, send messages, or replace system instructions. Fetch tools use approved sources and validated destinations; uploaded links are not automatically followed.

### Common records

- **EvidenceReference:** source ID, version, supporting passage or page, program, jurisdiction, effective interval, retrieval date, reviewer status and any conflict.
- **NoticeFinding:** notice category, affected person reference, program, requested action, literal date text, parsed date if supported, source location, missing fields and resident confirmation status.
- **ActionItem:** task ID, person and program, plain-language instruction, official destination, deadline type, evidence references, prerequisites and task state.
- **FoodResource:** provider ID, service area, dated hours and exceptions, free or paid status, access requirements, visit limits, languages, accessibility, verification date and inventory uncertainty.
- **FoodPlan:** seven local calendar dates, actions, alternatives, food reported on hand, meal suggestions, estimated costs with sources, unmet needs and resource versions used.
- **ConsentRecord:** authorized session, exact recipient and purpose, selected fields, proposed action version, timestamp, expiration and withdrawal state.
- **OperationRecord:** job ID, operation type, approval reference when required, duplicate-prevention key, attempt history, provider reference and delivery status.
- **SpeechInput:** session-scoped utterance ID, provider/model, requested or detected language, final transcript, extracted fields and resident corrections. Raw audio is not persisted by default; confirmation and source provenance remain separate from transcription confidence.

These records are the application source of truth. Conversation history can help explain a plan but cannot establish that evidence was submitted, an appointment was booked, or a message was delivered.

### States and deadlines

A proposed plan moves through draft, needs clarification, validated, awaiting consent, and active where relevant. Individual tasks use not started, prepared, resident reports submitted, agency receipt confirmed, and agency acceptance confirmed. Receipt and acceptance are distinct. A resident may report either, with the provenance retained instead of presented as independently verified.

Keep notice deadlines, benefit-continuation dates, appointments, and suggested preparation dates separate. Unknown dates remain empty. Do not derive a person's deadline from a general policy effective date. A changed notice creates a new plan version and a visible explanation of what changed.

## 4 Situation picker and notice understanding

**Trigger and inputs:** the resident selects a situation, describes a life change, chooses a notice category, or consents to upload a notice. Food-only intake asks for no notice. Manual entry remains available throughout.

**Execution sequence:**

1. The controller collects language and urgency. Immediate food need opens the food workflow without waiting for notice processing.
2. An upload service checks supported type, size and file safety, then assigns a session-scoped document ID. It explains any transfer to an external model or extraction provider.
3. read_notice uses the selected extraction adapter to retrieve text and page references. Strands organizes findings by person and program; it does not treat the entire letter as one obligation.
4. The website shows important source passages next to extracted actions and dates. Missing pages, unreadable text, placeholder dates and contradictions lead to correction or manual entry.
5. After confirmation, get_policy_evidence retrieves reviewed guidance applicable to the identified topic and time period. The agent proposes a plain-language explanation supported by those records.
6. validate_notice_plan checks person/program associations, source support, date consistency and unsupported conclusions. Unresolved findings remain visible.

**Resident result:** what the letter appears to request, who it concerns, what remains uncertain, the next official route, and access to food planning. The monthly screening label is Action identified, More information needed, or No action identified in the information provided.

**Failure behavior:** no confident deadline from unreadable text; no eligibility decision; no assumption that every notice is a cut. If the notice and current guidance appear inconsistent, preserve both and route the question to staff. Historical public samples are layout fixtures and must not become current policy. [P01](https://www.dhs.wisconsin.gov/dms/memos/ops/mds-ops-2019-j7attachment3.pdf)

## 5 Deadline checklist and official next steps

**Trigger:** confirmed notice findings or a life change supported by enough resident information.

**Execution:** get_policy_evidence returns the relevant renewal, six-month report, interview, verification, change-reporting or appeal guidance. Strands drafts separate ActionItems for the form, interview, evidence, and follow-up. resolve_help_route selects the appropriate official agency using verified county or Tribal routing; ZIP alone must not force an ambiguous agency assignment. The controller checks dependencies and dates before activation.

Example: submitting a six-month form does not automatically complete a separate evidence request. The checklist retains both and explains how their dates relate. DHS warns that the form and required evidence must arrive by the end of the due month to preserve full benefits, even when a proof request has a later deadline. [P02](https://www.dhs.wisconsin.gov/foodshare/smrf.htm)

**Resident result:** one prominent next action, a supporting checklist, the source of each official date, call questions, and verified contact or ACCESS/MyACCESS links. Opening a link does not mark the action submitted. Exporting a packet does not mark it accepted.

**Failure behavior:** conflicting dates are escalated; missed deadlines lead to reviewed recovery guidance rather than an automatic reapplication instruction. An appeal route requires its own current rules. A call to the agency must not be represented as filing an appeal or stopping a deadline.

## 6 Work or training plan

**Trigger:** the notice or resident's confirmed agency plan indicates a work-related task, or the resident asks a work-requirement question.

**Execution sequence:**

1. Retrieve applicable work-rule evidence and distinguish basic work rules from the separate time-limit work requirement.
2. Explain possible exemption or good-cause follow-up without deciding whether it applies. Ask only the minimum question needed; do not automatically request medical documents.
3. If hours planning is appropriate, capture the applicable month, agency-assigned target or arrangement, and resident-reported activities. Classify activities as agency confirmed, needs confirmation, planned, or completed.
4. calculate_activity_hours computes non-overlapping durations in code. It keeps planned and completed hours separate and avoids double-counting overlapping activities.
5. Strands explains the remaining planning gap and retrieves an FSET help route where useful. A shortfall creates a question or support option, not a declaration of benefit loss.

**Resident result:** a month view, reported totals, items needing FSET confirmation, supporting records to organize if requested, and a contact route. An 80-hour mode is available only when supported by the applicable situation. Workfare may use a different obligation and must not be forced into that template. [P03](https://www.dhs.wisconsin.gov/foodshare/work.htm), [P04](https://www.emhandbooks.wisconsin.gov/fset/6/6.3.htm)

**Failure behavior:** unknown activity classification stays unknown. The agent cannot certify an arbitrary course or volunteer opportunity as qualifying. Self-attestation and evidence rules must be reflected in the reviewed policy records so the website does not create extra paperwork. [P05](https://www.dhs.wisconsin.gov/dms/memos/ops/dms-ops-2026-04.pdf)

## 7 Proof packet preparation

**Trigger:** the resident chooses to organize evidence for a specific request.

**Execution:** the controller lists only files the session may access. Strands proposes an index mapping selected evidence to requested items and drafts notes solely from resident statements. The resident reviews missing items, removes files, corrects notes and confirms the contents. build_proof_packet creates a deterministic summary and export of selected originals. File handling and output generation happen in an application service, not through unrestricted model filesystem access.

**Resident result:** an evidence index, reviewed notes, requested original files and submission checklist. Preserve originals; any redacted copy is separately labeled. Offer individual files as well as a combined summary because official channel limits may differ. The implementation must verify supported upload formats and limits before claiming a packet is ready for a specific channel.

**Failure behavior:** no invented dates, diagnoses, income, attendance or signatures. An absent item produces an agency question or an acceptable-alternative route where supported. A successful download means prepared, not submitted. Interrupted uploads can be retried without creating duplicate evidence entries.

Temporary processing is the proposed default. Optional storage needs explicit retention choices, protected access and tested deletion. Shared-device sessions need an obvious end-session action. No document contents in analytics, SMS, error logs or routine agent traces.

## 8 Seven day food plan

### Intake and first plan

**Trigger:** Food this week, an urgent need during notice processing, or a request to revise an existing plan.

Collect ZIP or approximate area, household-size range, urgency, grocery budget including zero, travel choices and costs, pickup windows, available food, cooking equipment, refrigeration, and food preferences or restrictions. Exact address is optional and needed only for a resident-requested routing feature. Benefit case identifiers are unnecessary.

find_food_resources queries reviewed directory records. check_food_constraints filters service area, dates, holiday changes, costs, required appointments, access conditions and repeat-visit limits. It reports missing information separately from a failed constraint. Strands selects a small set of feasible options, offers backups and explains tradeoffs. validate_food_plan checks all seven days and every proposed trip before display.

The first response prioritizes food today. The complete week may contain multiple pickup opportunities and unresolved gaps. Free food, discounted groceries and benefit-dependent purchases have distinct labels. Hunger Task Force's Mobile Market must not be treated as a free pantry. Directory hours do not establish inventory or reservations. [P06](https://www.hungertaskforce.org/get-help/emergency-food/)

### Food access and meal suggestions

The access plan covers opportunities to obtain food. Meal suggestions use ingredients the resident reports already having or confirms receiving. A tentative pantry visit cannot create assumed groceries. Where quantities are unknown, ask the resident to confirm and keep the meal gap visible. An unverified food listing cannot be described as allergy-safe.

| Period | Proposed action | Evidence needed before treating it as completed |
| --- | --- | --- |
| Today | Identify an immediate meal or food route and a backup | Current provider information and resident-reported use |
| Day 2 | Prepare a feasible pantry visit | Access conditions, schedule and any appointment confirmed |
| Day 3 | Suggest meals from food actually received | Resident confirms ingredients and relevant quantities |
| Day 4 | Recheck supplies and unresolved needs | Updated resident information |
| Day 5 | Find another permitted pickup or affordable purchase | Visit limits and total cost checked |
| Day 6 | Adapt meals to equipment, storage and preferences | Usable ingredients remain available |
| Day 7 | Review gaps and next-week options | Resident chooses whether to continue |

This table illustrates behavior; it is not a verified itinerary or a guarantee of sufficient food.

### Replanning

A missed pickup, provider closure, budget change or revised dietary need triggers revise_food_plan. The tool loads the latest plan version and affected resource records. Strands proposes replacements for affected actions; validators recheck the whole remaining plan for timing, cost and duplicate visits. Completed actions stay recorded. The website explains the changes and asks for consent only if a new external action is proposed.

Anonymous plans can refresh when the resident returns within the supported session. Proactive alerts across days require an explicit saved-plan and notification choice. If there is no verified feasible option, show the gap and a 211 or navigator route. Do not silently widen travel limits or assume money the resident does not have.

## 9 Navigator requests reminders language and voice

### Named navigator request

resolve_help_route returns verified organizations and their supported request channels. The resident chooses one. prepare_navigator_request produces a preview of the exact recipient, contact fields, request summary and any selected attachments. The controller creates a pending action tied to that version. Consent is required before delivery.

Strands interrupts can surface the pause and resume after input. The backend checks session ownership, expiration and approval of the exact payload before submit_navigator_request dispatches it. A modified payload requires a new preview. The resident agent does not approve its own request. [T04](https://strandsagents.com/docs/user-guide/concepts/interrupts/)

Delivery accepted, delivered, partner acknowledged and appointment confirmed are separate states. An unknown result after a timeout triggers a status check, not an immediate duplicate send. Without an authorized integration, display a contact route and reviewed call script. Only a booking confirmation may create a confirmed appointment.

### SMS and other reminders

Strands proposes dates and neutral reminder wording from validated tasks. The resident selects the channel, destination and schedule. schedule_reminders writes approved jobs to a durable scheduler. A delivery worker checks consent, cancellations, current plan version and task state immediately before sending. The scheduler and delivery provider are application integrations; an agent conversation does not wake itself up next week.

Timezone and quiet-hour rules are explicit. A changed or withdrawn task invalidates its obsolete reminder. Provider callbacks update delivery status. Delivery failure never completes a benefits task. Preview lock-screen-safe wording such as You have a checklist item to review; avoid benefit amounts and document details. Support cancellation and provider-required opt-out behavior.

### Translation read aloud and accessibility

Use reviewed translations for recurring interface text and critical policy terminology. Strands can propose a plain-language explanation in the selected language; preserve original program names, numeric values, dates, conditions and source links. Validate key fields across language versions and escalate uncertain legal meaning for qualified review.

Read-aloud uses an explicit website control and the selected speech adapter. It must not start automatically on a library computer. Structured results render as accessible cards, checklists and printable plans, with keyboard operation, focus management and large text. The interface never requires a free-form chat conversation to reach food help.

### Optional tap to speak

Include voice input and read-aloud in the prototype while retaining the existing text flow. Useful requests include My benefits stopped, There are three of us and I have no car, That pantry was closed, and Read the next step in Spanish. Voice is another input channel into the same validated workflows; it cannot create a separate path around permissions.

1. The resident selects a language where appropriate and taps Speak. Explain processing before requesting microphone access, show a recording indicator, and provide stop and cancel controls.
2. The website streams supported audio through an authorized speech adapter. Long-lived provider credentials stay on the backend; use a backend relay or appropriately scoped, short-lived access. Enforce duration limits and close cancelled or abandoned streams.
3. The adapter returns interim text for display and a final transcript for processing. Only finalized, intentionally submitted input can advance the workflow. Utterance IDs prevent a reconnect from submitting the same request twice.
4. Strands interprets the transcript using the existing situation, notice or food-plan flow. The website confirms important dates, ZIP codes, household size and work hours. A spoken notice description remains resident-reported; it does not become document-verified evidence.
5. Existing validators check the proposed result. Display the explanation and action cards. A separate Listen control sends only the validated text selected for playback to the speech-synthesis adapter.
6. Referral and reminder operations retain their exact recipient, payload and consent preview. A casual spoken yes or transcript confidence score cannot establish authorization. Keep an explicit accessible confirmation control for external actions in the prototype.

Speech recognition transcribes; translation changes language; synthesis reads text aloud. Select and evaluate these separately. Strands should receive the finalized transcript and confirmed fields, not a stream of partial guesses. For read-aloud, use the same approved explanation that appears on screen so spoken and written guidance cannot diverge.

### Speech provider recommendation

Implement one provider behind a replaceable adapter. If the backend is centered on AWS, prefer Amazon Transcribe for input with Amazon Polly for output. If English/Spanish switching is central to the demonstration, evaluate Deepgram Nova-3 first for input. Its multilingual transcription and keyterm prompting are relevant to mixed speech and terms such as FoodShare, FSET and local organization names. Final provider selection depends on a small representative evaluation; no accuracy advantage is assumed. [V01](https://docs.aws.amazon.com/transcribe/latest/APIReference/API_streaming_StartStreamTranscription.html), [V02](https://developers.deepgram.com/docs/multilingual-code-switching), [V03](https://developers.deepgram.com/docs/keyterm), [V04](https://docs.aws.amazon.com/polly/latest/dg/what-is.html)

The speech adapter exposes start, stop, cancel, finalized transcript and failure events to the application controller. The synthesis adapter accepts validated text and a supported voice/language and exposes play, pause and stop. These are proposed application interfaces, not Strands SDK methods. Unsupported language, denied microphone access, excessive noise or network failure returns to typing and tapping with confirmed fields retained.

Avoid storing raw audio by default and keep transcripts out of routine logs and traces. Explain that cloud speech services receive audio. Configure and verify provider retention and model-improvement opt-outs before live use, including speech synthesis where applicable. AWS and Deepgram document separate opt-out mechanisms; removing audio from our database alone does not establish provider deletion. [V05](https://aws.amazon.com/transcribe/faqs/), [V06](https://developers.deepgram.com/docs/the-deepgram-model-improvement-partnership-program)

Evaluate consented or synthetic recordings covering English, Spanish, mixed-language speech, dates, ZIP codes, eighteen versus eighty, local names, background noise and representative devices. Compare critical-field accuracy, correction effort, successful task completion, latency and actual cost under the privacy configuration used. Check selected model/language/region feature compatibility. Require a repeatable cancellation and fallback path before choosing the provider for the demo.

## 10 Background policy and community maintenance

### Policy updates

A scheduler checks an allowlist of official sources. fetch_policy_updates captures a versioned snapshot and identifies changed passages. A separate Strands maintenance invocation proposes the affected topics, dates, exceptions and likely dependent content. It has no access to resident documents or message-delivery tools.

A qualified reviewer compares sources and approves or rejects publication. The published record links to the superseded version. The application identifies saved plans that reference changed records and queues a recheck; notifications occur only within the resident's approved settings. Conflicting or incomplete changes remain unpublished, with an internal review task.

An example is DHS's August 2026 utility-allowance effective-date update. A maintenance job should connect it to the earlier memo and flag affected guidance for review, not infer that every household lost benefits or is owed a supplement. [P07](https://www.dhs.wisconsin.gov/dms/memos/ops/dms-ops-2026-30.pdf)

### Community resource updates

Provider submissions and approved directory changes enter a staging area. validate_resource_update verifies the submitter, affected provider, dates and fields; ambiguous changes go to a human maintainer. A confirmed closure can promptly invalidate a listing and mark dependent trips for rechecking. A new resource needs its access and verification checks before recommendation.

One verified update can improve many households' plans without revealing those households to the provider. This is the proposed Good Neighbor demonstration: a simulated closure changes the shared resource record and causes affected saved plans to be revised. An anonymous unsaved plan picks up the update on its next retrieval.

Public educational content, if later included, uses the same source-review process. Advertising remains a separate product decision and cannot affect resource ranking, eligibility explanations or consent. The proposed hackathon scope defers ads.

## 11 Tool contracts and SDK integration

### Application tool contract

Every tool accepts a typed, bounded request. Every response contains status, data, evidence references, missing information, warnings and retryability. Status distinguishes success, partial, no match, needs clarification, denied and temporarily unavailable. A successful HTTP response does not by itself mean the underlying task succeeded.

| Tool group | Inputs and outputs | Enforcement boundary |
| --- | --- | --- |
| read_notice | Authorized document ID to NoticeFindings and page evidence | Document service checks ownership and processing consent |
| get_policy_evidence | Topic and relevant period to reviewed policy passages | Retrieval excludes unpublished and inapplicable versions |
| resolve_help_route | Geography and assistance need to verified destinations | Ambiguous county or Tribal routing requires clarification |
| calculate_activity_hours | Month and activity records to separated totals and flags | Code checks overlap and never certifies qualification |
| find_food_resources | Household constraints and date window to candidate records | Directory queries reveal no household identity to providers |
| check_food_constraints | Candidates and plan to constraint results | Code checks travel assumptions, cost and visit restrictions |
| build_proof_packet | Approved selected files and notes to artifact reference | File service checks access and preserves originals |
| prepare_navigator_request | Selected organization and fields to sharing preview | No delivery side effect |
| submit_navigator_request | Approved operation ID to delivery receipt | Service checks approval and prevents duplicate requests |
| schedule_reminders | Approved operation ID to scheduled jobs | Scheduler checks consent, timezone and cancellation |
| fetch_policy_updates | Approved source IDs to changed snapshots | Maintenance identity has public-source read access only |
| validate_resource_update | Staged update ID to decision or review task | Publication requires authorized source and applicable checks |

Other named functions in the workflows, including validation and plan revision, are internal services or orchestration steps as appropriate. A function does not need to be model-callable to participate in the workflow.

### Python integration pattern

The current documented pattern imports Agent and tool from strands, registers typed functions as tools, and invokes the agent with structured_output_model set to a Pydantic model. Read the result through result.structured_output. The invocation shape is agent(request, structured_output_model=PlanProposal). Use a workflow-specific schema instead of allowing arbitrary prose to drive state changes. [T02](https://strandsagents.com/docs/user-guide/concepts/tools/custom-tools/), [T03](https://strandsagents.com/docs/examples/structured_output/)

A PlanProposal should include workflow, summary, action items, resource references, unresolved questions, evidence references and proposed external actions. It does not contain an authoritative eligibility decision or a trusted approval flag. Model output can reference only IDs already returned by authorized tools; the validator rejects fabricated IDs.

For a Strands interrupt, the documented result has stop_reason equal to interrupt and carries interrupt IDs. Resume with interruptResponse entries associated with those IDs after validating the resident response. Never copy an example that automatically approves interruptions into this product. [T04](https://strandsagents.com/docs/user-guide/concepts/interrupts/)

Hooks can observe or intervene around execution events, but service-level authorization remains mandatory even if a hook is missing or misconfigured. [T05](https://strandsagents.com/docs/user-guide/concepts/agents/hooks/)

Pin and test an SDK version during implementation. Documentation was checked through Context7 and official Strands pages on September 4, 2026. This guide is an architecture contract rather than a runnable SDK sample.

## 12 Persistence failure handling and operations

### Session and business state

Strands documents session management and snapshot mechanisms. Select a supported persistence strategy after testing its behavior with the pinned SDK. Do not assume conversation persistence alone restores an in-flight approval after a server restart. [T06](https://strandsagents.com/docs/user-guide/concepts/agents/session-management/), [T07](https://strandsagents.com/docs/user-guide/concepts/agents/snapshots/)

Persist pending operations and consent in the application database independently. If an exact SDK continuation cannot be recovered, rebuild a restricted invocation from the latest business records. Re-display any changed or uncertain proposal and reconcile delivery receipts before attempting an external action. Never replay a transcript as proof that a send should happen again.

Serialize changes to the same saved plan or use version checks to reject stale writes. Independent read-only lookups can run concurrently; confirmation, publication, saving and external actions follow their dependencies. Cancelling a run prevents new work, while any already-dispatched operation must be reconciled and shown honestly.

### Failure and fallback behavior

- **Model or retrieval timeout:** preserve confirmed progress, provide verified static help routes, and offer retry without forcing the resident to re-upload unnecessarily.
- **Malformed or unsupported proposal:** allow a bounded repair using validation errors; if it still fails, show a partial result and human help route.
- **Stale directory data:** mark it needs confirmation and avoid a confident time-sensitive trip recommendation.
- **Unknown external outcome:** check the operation and provider receipt before retrying; use the same duplicate-prevention key for the logical action.
- **Changed deadline or resource:** invalidate dependent drafts and obsolete reminders, then revalidate against the current version.
- **Uncertain translation or extraction:** retain the original passage and allow manual correction or staff review.

Set configurable ceilings for model calls, tool calls, elapsed time, file size and retries per workflow. Stop at the limit with a useful partial result. Choose numeric limits after measuring representative cases rather than promising untested speed or cost.

### Observability and retention

Record workflow name, model and prompt version, policy/resource versions, validation failures, tool latency, token cost, consent outcome and operation status. Configure telemetry to exclude raw notices, contact details and sensitive tool arguments before enabling tracing. Aggregate metrics must not expose small groups or individual household paths.

Store secrets in backend-managed configuration, keep uploaded data out of browser-accessible public storage, and test cross-session isolation. Define retention separately for uploads, derived findings, conversations, consent, provider receipts and backups. Deletion and withdrawn consent cancel relevant future work and clearly explain any retained operational records.

## 13 Demonstration and acceptance checks

### Maria walkthrough

Maria is a fictional Milwaukee resident age 61. She receives a clearly labeled synthetic six-month-report notice and needs food this week. The demo supplies a fabricated date rather than changing a historical official sample without labeling it.

The website asks for language and situation. With consent, the extraction service processes the sample. Strands identifies the report request and evidence passage. Maria confirms the date. The controller validates a separate report task and any requested evidence task. Age alone does not trigger an 80-hour obligation.

Maria enters a zero grocery budget, bus travel and kitchen access. The agent queries the demonstration directory, proposes feasible free-food routes and marks unknown stock. She reports what she received, allowing meal suggestions to become more specific. A simulated provider closure then revises one planned visit while retaining completed actions.

In the voice variation, Maria taps Speak and describes her travel and budget constraints in Spanish or mixed English/Spanish. The website shows the final transcript and asks her to confirm important fields. Strands runs the same food workflow, and Maria can tap Listen to hear the validated next step. Demonstrate correction of one misheard value and a return to typing.

Maria previews an optional reminder or named-partner request. The demo uses a test destination and shows consent, queued status and a simulated or real test receipt with clear labeling. No official benefits submission or unconfirmed appointment is implied.

### Required evaluation cases

| Test | Expected behavior | Evidence to inspect |
| --- | --- | --- |
| Notice contains a placeholder date | Request clarification; no invented deadline | Findings and source passage |
| Two people have different obligations | Keep person-specific tasks separate | ActionItem associations |
| Old memo conflicts with published update | Use reviewed applicability or escalate | Policy versions and conflict record |
| Possible exemption is mentioned | Avoid automatic medical-proof demand | Retrieved guidance and explanation |
| Work activities overlap | Avoid double-counting; retain uncertainty | Deterministic totals |
| Household has no budget or kitchen | Exclude unusable purchases and meals | Constraint results |
| Pantry closes after planning | Replace affected future action or show a gap | Plan versions and resource event |
| Document says to send private data | Treat text as data; no authorized send | Tool denial and operation records |
| Approval belongs to another session | Reject resume or delivery | Authorization result |
| Server restarts after a provider accepts a request | Reconcile receipt; avoid duplicate send | Persistent operation and provider reference |
| Resident cancels a reminder | No future send for cancelled job | Scheduler and delivery status |
| Spanish explanation changes a date or condition | Reject or route for review | Cross-language validation |
| Speech turns eighteen hours into eighty | Require correction or confirmation before guidance | Final transcript and confirmed fields |
| Interim text changes during streaming | Do not trigger actions from partial text | Utterance state and tool calls |
| Microphone is denied or speech service fails | Return to text with confirmed fields retained | Interface state and failure event |
| Stream reconnect repeats an utterance | Process the finalized request once | Utterance ID and operation history |
| Resident cancels recording or playback | Stop capture or playback and prevent new work from cancelled input | Stream and controller state |
| Spoken yes follows an unrelated question | Do not send or schedule without exact-action consent | Consent preview and operation record |

Use expert-reviewed notice cases, synthetic sensitive data and a held-out set of scenarios. Evaluate extraction, retrieval applicability, citation support, task correctness, food feasibility and consent handling separately. Schema validation alone does not prove an explanation is true. Public-pilot thresholds require baseline evidence and review; any critical wrong-person action, fabricated deadline or unauthorized disclosure blocks release until corrected.

## 14 Build sequence and remaining decisions

First build the typed records, curated policy/resource fixtures and deterministic validators. Then demonstrate a manual situation flow with official help routes. Add synthetic notice extraction and source confirmation, followed by the seven-day plan and a closure-driven revision. Finally add packet export and one controlled reminder or referral integration. This order makes each agent capability reviewable before adding external actions.

After the text flow works, add tap-to-speak and read-aloud through one evaluated adapter before the final demo. Keep speech processing separate from Strands so providers can be changed without rewriting policy or food-planning tools. Provider selection, privacy configuration and supported voice languages are decisions for this build stage.

Before live resident uploads or a public pilot, resolve policy-review ownership, data-reuse permissions, supported notice classes, language reviewers, model-provider handling, session recovery, retention/deletion, and partner response capacity. Test provider outages and shared-device exit behavior. These are implementation dependencies, not existing agreements.

Recommended first scope: Milwaukee, English and Spanish subject to qualified review, a small maintained resource directory, two or three supported notice classes, manual alternatives and a visible source trail. Work planning should begin as an explanation and recording aid; complex qualification decisions stay with official staff. Separate maintenance permissions from resident tools from the first implementation.

## 15 Sources and companion research

The companion FoodShare Bridge Research Brief supplies broader policy research, public notice examples, resource starting points and questions for the PRD. This execution design adds workflow and application responsibilities. Source links below document SDK mechanisms or domain constraints; the architecture and tool names are project recommendations.

- **T01** [Strands agent loop](https://strandsagents.com/docs/user-guide/concepts/agents/agent-loop/) — model and tool execution.
- **T02** [Creating custom tools](https://strandsagents.com/docs/user-guide/concepts/tools/custom-tools/) — Python tool definitions and context.
- **T03** [Structured output example](https://strandsagents.com/docs/examples/structured_output/) — schema-shaped invocation results.
- **T04** [Interrupts](https://strandsagents.com/docs/user-guide/concepts/interrupts/) — pause and resume for human input.
- **T05** [Hooks](https://strandsagents.com/docs/user-guide/concepts/agents/hooks/) — lifecycle observation and intervention.
- **T06** [Session management](https://strandsagents.com/docs/user-guide/concepts/agents/session-management/) — conversation and agent session mechanisms.
- **T07** [Snapshots](https://strandsagents.com/docs/user-guide/concepts/agents/snapshots/) — execution recovery capabilities to evaluate with the chosen SDK.
- **P01** [Official Notice of Proof Needed sample](https://www.dhs.wisconsin.gov/dms/memos/ops/mds-ops-2019-j7attachment3.pdf) — historical layout fixture with placeholder details.
- **P02** [DHS six-month reporting](https://www.dhs.wisconsin.gov/foodshare/smrf.htm) — report and evidence deadlines.
- **P03** [DHS work requirement](https://www.dhs.wisconsin.gov/foodshare/work.htm) — work routes, exemptions and good cause.
- **P04** [FSET participation requirements](https://www.emhandbooks.wisconsin.gov/fset/6/6.3.htm) — workfare and other activity distinctions.
- **P05** [DHS Operations Memo 26 04](https://www.dhs.wisconsin.gov/dms/memos/ops/dms-ops-2026-04.pdf) — implementation and exemption-verification context.
- **P06** [Hunger Task Force emergency food](https://www.hungertaskforce.org/get-help/emergency-food/) — food-resource starting points.
- **P07** [DHS Operations Memo 26 30](https://www.dhs.wisconsin.gov/dms/memos/ops/dms-ops-2026-30.pdf) — utility-allowance effective-date update demonstrating source versioning.
- **V01** [Amazon Transcribe streaming API](https://docs.aws.amazon.com/transcribe/latest/APIReference/API_streaming_StartStreamTranscription.html) — streaming and language configuration.
- **V02** [Deepgram multilingual code-switching](https://developers.deepgram.com/docs/multilingual-code-switching) — mixed-language transcription.
- **V03** [Deepgram keyterm prompting](https://developers.deepgram.com/docs/keyterm) — recognition support for relevant terminology.
- **V04** [Amazon Polly overview](https://docs.aws.amazon.com/polly/latest/dg/what-is.html) — text-to-speech.
- **V05** [Amazon Transcribe FAQ](https://aws.amazon.com/transcribe/faqs/) — privacy, retention and model-improvement opt-out.
- **V06** [Deepgram Model Improvement Partnership Program](https://developers.deepgram.com/docs/the-deepgram-model-improvement-partnership-program) — request opt-out and associated handling.
