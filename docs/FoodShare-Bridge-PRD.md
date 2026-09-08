# FoodShare Bridge Product Requirements

Product requirements for the responsive website and community support workflows

September 8, 2026 | Version 1.6 | Draft for product and engineering review

This Markdown file is the current PRD. Version 1.6 records owner-confirmed 211 API access and adds the proposed AgentPhone evaluation for two-way SMS and telephone access. The earlier Word export remains version 1.5.

**Product name:** this product is now called **GoodNext** (decided September 8, 2026). "FoodShare Bridge" in this and companion documents is the working title. See docs/decisions/002.

## 1 Product decision and purpose

Build a free, responsive website that helps Wisconsin households turn a confusing FoodShare notice or life change into a clear official next step and a practical plan for food this week. The recommended first release is a Milwaukee demonstration with English and Spanish experiences, optional voice interaction, and explicitly synthetic benefits documents. A public pilot follows only after the operational requirements in this document are met.

The website has two equal entry points: **Food this week** and **Understand my notice or change**. Food access never requires a notice upload, an account, or completion of benefits questions. The product supports understanding, preparation and connection to help; official staff remain responsible for case decisions.

This PRD translates the existing research brief, Strands execution design and architecture into testable product behavior. It defines the proposed build baseline, rather than claiming implementation, partner commitments or validated demand. Requirement IDs are stable so design, engineering and evaluation can refer to the same behavior. Detailed SDK integration remains in the execution design.

### Confirmed direction and working assumptions

Confirmed user direction includes a responsive website, seven-day food planning, notice literacy, deadline checklists, a work or training planner, optional uploads and proof packets, official help routes, multilingual access, optional speech and reminders, privacy, and a community benefit beyond one household.

The working assumptions are a Milwaukee starting directory, English and Spanish first, two supported notice classes, synthetic documents in the demonstration, and advertising deferred. These are recommendations for this draft. Team capacity, implementation budget, named reviewers, partner availability and final vendors remain unconfirmed. A requirement marked prototype is a scope proposal, not evidence that its dependency is already available.

## 2 Problem and intended outcomes

SNAP changes are the motivation for FoodShare Bridge. The tractable product problem is the confusion and practical disruption surrounding changed rules, reporting obligations, deadlines and access to food. The product cannot undo statutory cuts. It can help residents understand an identified task, prepare for an official interaction and find feasible food options while the case is unresolved.

Wisconsin DHS describes an expansion of the FoodShare work requirement following the federal law signed in July 2025. Work routes, exemptions, good cause and case-specific applicability must be distinguished. Its current member news also describes reporting changes for some adults aged 60 through 64. This makes a personal notice and its dates more useful than a blanket message that everyone in an age group has the same obligation. [DHS work requirement](https://www.dhs.wisconsin.gov/foodshare/work.htm), [DHS member news](https://www.dhs.wisconsin.gov/foodshare/news.htm).

These two pages were rechecked on September 8, 2026. The broader research register was compiled September 4 and is not a fresh policy certification. No policy constants in this PRD should become unreviewed application rules. Proposed legislation, enacted future provisions, and rules currently applicable to a resident must remain distinct in the content model.

The intended resident outcome is the ability to identify what to do next, where to do it, which dates are known, and what remains unresolved. The food outcome is a feasible access plan with visible gaps. The community outcome is that one verified resource update can improve several household plans without revealing household information to the provider. Benefit retention and reduced food insecurity are longer-term research outcomes, not claims supported by the demonstration.

### Users and needs to validate

| Actor | Primary need | Product responsibility |
| --- | --- | --- |
| Resident with a notice or life change | Understand the next action without unnecessary paperwork | Explain evidence, uncertainty, dates and official routes |
| Resident needing food now | Find usable options within money, travel and kitchen constraints | Prioritize food today and preserve access without benefits screening |
| Resident using voice or another language | Complete the same tasks without relying on complex English text | Offer equivalent controls, correction and readable results |
| Navigator or library helper | Help a resident understand and prepare | Support resident-controlled sessions and printable plans |
| Resource maintainer or policy reviewer | Keep shared guidance accurate | Review provenance and publish accountable updates |

These are audience hypotheses. The project has not yet established resident interviews or agreements with any named organization.

## 3 Release scope and exclusions

Prototype means a working demonstration using real agent execution, synthetic sensitive inputs and clearly labeled test integrations. Pilot means limited live resident use after review, security and operational gates. Later means retained product direction outside the initial delivery commitment.

| Capability | Prototype baseline | Pilot or later boundary |
| --- | --- | --- |
| Entry and official routes | Anonymous food and notice entry; maintained help links | Expand geography only with an accountable directory owner |
| Notice and checklist | Synthetic six-month report and proof-request cases; manual alternative | Live uploads only after document and policy review gates |
| Seven-day bridge plan | Curated Milwaukee resources, food today, gaps, meal suggestions and revision | Broader coverage and richer routing as verified data allows |
| Work or training plan | Manual activity log, conditional 80-hour mode and FSET route | Complex activity and workfare support after expert validation |
| Proof packet | Export a summary and selected synthetic evidence | Live evidence handling after retention and security decisions |
| Language and voice | English and Spanish text; one evaluated STT adapter and optional read-aloud | Additional languages require separate review and evaluation |
| Community maintenance | Review an update and revise two isolated synthetic household plans | Scheduled monitoring and sustained review coverage |
| Reminders and referrals | One controlled reminder demonstration; named partner route if verified | Real SMS and referrals require consent and operational readiness |
| Saved plans | Anonymous active session; controlled test records for demo reminders | Cross-device recovery and long-term storage require a separate decision |

Excluded from this release are eligibility or benefit-amount decisions, exemption certification, automatic benefits submissions, ACCESS credential collection, pantry reservations, assumed live inventory, unverified appointment booking, a native mobile application, advertising, payment collection and automated immigration-status screening. Community education remains a later possibility; assistance rankings and consent flows must remain independent of sponsors.

The demonstration must invoke Strands on AgentCore Runtime to interpret inputs, use scoped tools and propose or revise a plan. A mock model response must not be presented as agent execution. External delivery may use a test adapter if clearly labeled. Section 16 defines the selected hosting and recommended supporting stack.

## 4 Experience and primary journeys

### Screen structure

The initial screen offers language selection and the two entry points. Subsequent screens cover the situation or food intake, optional notice input, review of extracted information, My Next Step, Food This Week, My Work or Training Plan, My Proof Packet, and Help and Reminders. Speak, Listen, Help and End Session are available where relevant. A separate restricted review screen supports policy and resource maintenance.

The primary action screen shows one prominent next action, its destination, a deadline or an explicit unknown state, supporting evidence and related checklist items. The food screen starts with today's need and lets the resident expand the following six local calendar days. Neither screen requires a conversational chat exchange to proceed.

### Journey A from notice to plan

Maria, a fictional Milwaukee resident aged 61, chooses Understand my notice or change and selects a synthetic six-month report notice. She sees the request and source passage side by side, confirms its date, and gets separate report and requested-evidence tasks. Her age alone does not create an 80-hour obligation. She then selects Food this week, enters a zero budget and bus travel, and receives feasible free-food routes and any unresolved gaps.

Maria can prepare a packet, open an official route, or set a controlled test reminder. Each result accurately distinguishes preparation, attempted delivery and confirmed outcomes. A later synthetic proof request adds a task without erasing completed work.

### Journey B from immediate food need to revision

A resident enters through Food this week, provides approximate location and practical constraints, and chooses a suitable option. The website explains access requirements, unknown availability and a backup. After the resident reports what food they actually received, meal suggestions become more specific. If a pickup fails, the plan revises remaining days and keeps the missing food visible.

### Journey C one community update helps several households

A maintainer reviews a simulated closure of a resource used in two separate synthetic household plans. Publishing the verified update invalidates the affected future visits. The agent proposes alternatives for each household's constraints. A household with no alternative sees a gap and a help route. The maintainer sees the shared resource update, not residents' documents or contact details.

### Journey D voice with correction

Maria taps Speak and describes her needs in Spanish or mixed English and Spanish. She reviews the final transcript and confirms important values. The demo includes one misheard number and its correction. She taps Listen to hear the same validated next step shown on screen, then returns to typing without losing confirmed inputs.

## 5 Functional requirements

### FR01 Entry and situation selection

**Story:** As a resident, I want to choose the help I need so that I can act without first understanding benefits terminology.

**Acceptance criteria:**

- Both entry points work without registration. Food planning asks no case number, Social Security number, immigration information or benefits documents.
- The situation picker includes benefits reduced, benefits stopped, unfamiliar letter, missed deadline, work question, life change, QUEST card problem, and not sure. Card problems route to official card help rather than an inferred eligibility problem.
- Unknown answers are allowed. Requests outside supported geography or notice scope produce an honest limitation and an official or 211 route, with confirmed inputs retained.
- A resident can change entry paths without restarting. Editing an input marks dependent results for rechecking before reuse.

### FR02 Optional notice input and confirmation

**Story:** As a resident, I want the website to show what my notice appears to request so that I can check it before relying on a plan.

**Acceptance criteria:**

- Manual notice description and sample selection remain available beside upload. The prototype accepts only supplied synthetic fixtures; live resident upload is disabled until pilot gates pass.
- Before processing an allowed upload, the website states what will be processed and where. Unsupported type, excessive size, unreadable content or missing pages lead to a recoverable error and manual alternative. Actual format and size limits are set before implementation release and displayed in the interface.
- Findings separate notice type, program, affected person, action, date text and source location. The website displays important fields beside the passage or page that supports them.
- A placeholder, blurred date or conflict remains unresolved. Resident corrections retain their resident-reported provenance; they do not silently become verified document evidence.
- Multi-person and multi-program fixtures cannot transfer one person's obligation to another or apply FoodShare logic to another program. Embedded document instructions cannot authorize tool actions or sharing.

### FR03 Next step and deadline checklist

**Story:** As a resident, I want a clear next action and separate deadlines so that completing one task does not hide another unfinished step.

**Acceptance criteria:**

- Monthly screening uses Action identified, More information needed, or No action identified in the information provided. It never states that the official case was checked or that the resident is eligible.
- Each action shows the relevant person and program, plain-language instruction, destination, source, date type, prerequisites and status. Unknown dates are visibly unknown.
- Renewals, six-month reports, interviews, requested proof and follow-up are separate linked tasks. Official due dates, dates relevant to benefit continuity and suggested preparation dates are labeled separately.
- A missed deadline or disputed action produces reviewed recovery information and the appropriate official route. A general phone call is not labeled as a filed appeal or a deadline extension.
- Opening ACCESS, downloading a packet or reporting a submission cannot mark agency acceptance confirmed. A new notice creates a visible plan revision and preserves completed work.

### FR04 Seven day food access plan

**Story:** As a household, we want a plan we can actually use this week so that limited money, time or transportation does not make the recommendations unusable.

**Acceptance criteria:**

- Intake collects ZIP or approximate area, household-size range, urgency, budget including zero, travel options and limits, pickup availability, food on hand, cooking and refrigeration access, and food preferences or restrictions. Ask follow-ups only where they change the plan.
- Results contain seven dated local days, beginning with food today. Each proposed visit shows provider, service type, cost, schedule, requirements, last verification, contact or directions, uncertainty and a backup where available.
- Recommendations satisfy known service-area, opening, holiday, appointment, visit-limit, budget and travel constraints. Unknown constraints are flagged for confirmation; they are not treated as satisfied.
- Free food and paid or discounted groceries have distinct labels. A zero-budget plan cannot rely on a purchase. Travel costs count toward stated limits; missing routing data cannot generate invented times or fares.
- Meal and grocery suggestions use reported available or received food and practical household quantities. Tentative pickups cannot establish ingredients or adequate food for the week. Unverified offerings cannot be labeled allergy-safe.
- No suitable resource produces a visible food gap and maintained human-help route. Changes in pickups, supplies or constraints trigger revision of affected future actions while preserving completed actions.

### FR05 Work or training plan

**Story:** As a resident with a work-related task, I want to organize activities and questions so that I can discuss my actual obligation with official staff.

**Acceptance criteria:**

- The feature first distinguishes a work question from an established agency task. It offers reviewed information about possible exemptions and good cause without deciding applicability or automatically demanding medical evidence.
- An 80-hour mode appears only when supported by the resident's relevant situation. A recorded agency-assigned arrangement can use a different target; workfare is not forced into the 80-hour template.
- Entries capture month, date, duration, activity, planned or completed state, and whether qualification is agency-confirmed or unresolved. Totals are calculated consistently and overlapping time is not counted twice.
- A shortfall is described as a planning gap, with an FSET or official follow-up route. Arbitrary courses, volunteering and job-search time are not automatically certified as qualifying.

### FR06 Proof packet preparation

**Story:** As a resident, I want to organize selected evidence and my own notes so that I can submit them through an official channel or bring them to an appointment.

**Acceptance criteria:**

- Packet contents are tied to an identified request. A preview lists selected files, requested items, missing information and draft notes. Residents can remove files and edit notes before export.
- Notes contain only resident-provided facts. The agent cannot invent attendance, income, diagnoses, signatures, dates or a good-cause event.
- Export provides an index, reviewed notes and selected originals, with individual files available where needed. Any modified or redacted derivative is separately labeled.
- The result says Prepared for your review. Compatibility with an official upload channel is claimed only after that channel's file restrictions are verified. Downloading is not submission.
- Missing evidence offers an agency question or a reviewed acceptable-alternative route. It does not block food planning. The demonstration uses synthetic evidence throughout.

### FR07 Official help and navigator requests

**Story:** As a resident, I want to reach the right organization and control what is shared so that seeking help does not expose unnecessary information.

**Acceptance criteria:**

- Help cards distinguish official case services, food providers, FSET, advocates and 211. They show a direct source and verification date. County or Tribal routing ambiguity requires clarification rather than a ZIP-only assumption.
- ACCESS and MyACCESS are official destination routes. The product does not ask for their passwords or claim a case connection, partnership or booked appointment that does not exist.
- A request button appears only for an active verified partner with an agreed receiving channel. Otherwise the card offers contact information and questions to ask.
- Before sending, the resident sees the named recipient, purpose, exact contact fields and any selected attachments, then explicitly approves that version. Editing the payload requires another preview.
- A request displays pending, sent, failed or acknowledged as supported by evidence. Only actual confirmation may show an appointment as booked. Unknown outcomes are reconciled before retrying.

### FR08 Reminders

**Story:** As a resident, I want optional reminders for known tasks so that I can remember preparation without sharing benefits details on my lock screen.

**Acceptance criteria:**

- A reminder requires a confirmed task, chosen channel, destination and schedule, a neutral message preview, and explicit consent. Consent to upload is not consent to receive messages.
- The resident can review and cancel future reminders. Delivery respects America/Chicago time and an agreed quiet-hours policy. Exact channel limits and schedule defaults are release decisions.
- A changed deadline, completed task or withdrawn consent cancels obsolete future reminders. A delivery worker rechecks current state before dispatch.
- A timeout or retry cannot create duplicate logical sends. Failed delivery is visible and does not complete a benefits task. The prototype uses a test destination or labeled simulation.
- Two-way SMS and telephone access follow Section 17. AgentPhone is the preferred candidate to evaluate, not an already configured service. Scheduling, consent and cancellation remain application responsibilities regardless of delivery provider.

### FR09 Language and voice access

**Story:** As a resident, I want to speak or read in a supported language while retaining control over important details.

**Acceptance criteria:**

- English and Spanish cover the complete prototype journey, including errors, consent, uncertainty and cancellation. Critical policy terminology and reusable interface translations require qualified review before pilot use.
- Speak requires explicit microphone activation, a recording indicator, and stop and cancel controls. Partial transcripts may be displayed but do not trigger actions. Only intentionally submitted final input advances the workflow.
- Dates, ZIP codes, household size and work hours require correction or confirmation before use. Speech confidence is not proof of correctness or authorization. Duplicate utterances on reconnect are processed once.
- Listen reads the selected validated text already shown on screen, with pause and stop controls. It never starts automatically. Translation preserves official names, dates, quantities, conditions, uncertainty and source links.
- Denied microphone access, unsupported speech language, cancellation or provider failure restores typing and tapping without losing confirmed fields. A casual spoken yes cannot authorize a referral or reminder.

The recommendation retained from the plan is one replaceable speech adapter: prefer Amazon Transcribe with Polly if the backend is centered on AWS; evaluate Deepgram Nova-3 first if mixed English and Spanish speech is central to the demo. This is an evaluation direction, not a provider selection or accuracy claim. Compare important-field accuracy, correction effort, task completion, latency, cost and privacy configuration before choosing. Provider capabilities must be rechecked during implementation.

### FR10 Shared policy and resource maintenance

**Story:** As a community maintainer, I want one verified update to improve all affected plans without receiving household information.

**Acceptance criteria:**

- A maintenance job examines approved official sources or authenticated provider updates and records a proposed change with provenance, dates and affected records. It has no resident-document or message-delivery permissions.
- Qualified reviewers approve substantive policy changes before publication. Resource changes require an authorized source and validation; ambiguous reports remain unpublished pending review.
- Publication creates a version linked to the earlier record. Plans referencing a changed record are marked for recheck. Existing saved plans are revised within their authorized persistence scope; anonymous plans pick up changes on subsequent retrieval.
- Conflicting policy sources cannot silently replace one another. A suspect resource can be withdrawn from recommendation while review proceeds. Reviewers can retire an incorrect version and trigger dependent-plan rechecks.
- The prototype demonstrates one shared closure affecting two isolated households with different constraints. Proactive resident notification remains subject to separate consent.

## 6 Data quality and agent responsibilities

The model may interpret, retrieve, explain and propose. Application services enforce access, calculate totals, validate sources and constraints, persist state, build files and execute authorized deliveries. An agent-selected tool order cannot bypass a mandatory confirmation or validation step. One resident agent configuration runs with isolated context; background maintenance uses separate permissions.

| Record | Minimum information | Publication or use rule |
| --- | --- | --- |
| Policy evidence | Source, passage, program, jurisdiction, publication and effective dates, version, review owner and status | Only reviewed guidance applicable to the request period supports instructions |
| Resource | Provider, source, service area, dates and hours, cost, access rules, contact, languages, verification and review owner | Stale or unknown fields remain visible and cannot support a confident trip promise |
| Notice finding | Person, program, requested action, literal date, source location, missing fields and confirmation | Preserve document-derived and resident-reported provenance |
| Plan action | Action, date type, prerequisites, destination, evidence, version and state | Changed inputs invalidate dependent drafts; completion requires appropriate evidence |
| Consent and operation | Exact purpose, recipient, fields, approved version, time, expiry or withdrawal, delivery receipt | Recheck authorization before dispatch and prevent duplicate operations |

No open-web result becomes a live policy instruction or a food listing without the relevant review. Data ingestion must record reuse permissions and an update owner. Model output must reference records actually returned by authorized tools. A valid response format alone does not establish factual correctness.

For the prototype, the curated directory includes examples that exercise free food, paid options, opening restrictions, transportation limits and a closure. Its fixtures distinguish genuine published facts from simulated changes. Before pilot use, every displayed record must meet a freshness rule agreed with its owner. The exact review interval is an open operational decision; missed review deadlines make records stale rather than silently current.

Historical official notices remain unchanged as research fixtures. Synthetic derivatives are clearly fictional. The [official proof-needed sample](https://www.dhs.wisconsin.gov/dms/memos/ops/mds-ops-2019-j7attachment3.pdf) is a layout reference, not current policy or a real resident deadline. Full source and sample context remains in the research brief.

## 7 Privacy persistence and accessibility

### NFR01 Minimal data and resident control

The anonymous Bridge Plan collects no name, exact birth date, Social Security number, case number, immigration status or medical documentation. Optional free-text restrictions may themselves be sensitive and receive the same protection as other session inputs. A phone number is collected only for a chosen contact action. Exact location is optional and requested only when the resident chooses a routing feature that needs it.

Upload processing, persistent saving, recording, SMS and partner sharing have separate explanations and controls. Provider processing locations, retention and model-improvement settings must be documented and verified before live data is enabled. Raw audio is not retained by default, and deleting a local copy cannot be described as deleting a provider copy.

### NFR02 Session and file handling

Anonymous sessions do not promise recovery across devices or after session expiry. The interface states this and offers print or download where appropriate. End Session clears accessible session content and invalidates access to temporary artifacts; cached pages must not reveal it through back navigation. Exact inactivity timeout and deletion periods are release-blocking decisions for a live pilot.

Any approved saved-plan mode must explain retention, recovery, deletion and notifications. Consent and operation state must survive the supported retry or restart behavior independently of a model conversation. Uploaded and exported files require access checks, protected transfer and storage, tested deletion, and prevention of cross-session access. The prototype does not require real resident uploads to demonstrate these controls.

Routine logs, analytics and agent traces exclude raw documents, audio, transcripts, contact details and sensitive tool arguments. Operational measurement uses minimal event metadata. Third-party tracking and ads are excluded from assistance flows.

### NFR03 Accessibility and responsive behavior

Proposed pilot target: WCAG 2.2 AA, with manual review of core journeys as well as automated checks. The site must be usable by keyboard, provide visible focus, accessible names and errors, announce processing states appropriately, preserve a logical reading order, and avoid color-only meaning. Text resizing and narrow layouts must not hide actions or require horizontal scrolling for ordinary forms and cards. [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/).

Test the complete flow at a 320 CSS-pixel viewport, at 200 percent text zoom, on a representative phone browser, and with desktop and mobile screen readers. Voice is optional and does not replace accessible forms. Printed plans retain action text, dates, uncertainty and source contacts without requiring interactive controls.

## 8 States failure handling and performance

Plans move through Draft, Needs clarification and Validated; proposed external actions then move to Awaiting consent and the relevant delivery state. An edited validated plan becomes a new draft version until rechecked. Task states distinguish Not started, Prepared, Resident reports submitted, Agency receipt confirmed and Agency acceptance confirmed. A resident's own report of agency confirmation must retain that attribution.

On missing evidence or model failure, the website preserves confirmed progress, identifies unresolved items and offers a maintained official or local route. It must not fill gaps with confident guesses. A partial food plan remains useful if its missing days are explicit. Retrying cannot repeat an already accepted external action.

Proposed prototype performance targets, to be measured rather than advertised: show visible feedback within one second of submission; target a first validated action within 20 seconds for a typical test case; after 30 seconds, provide explicit delayed status and cancellation or fallback. Final numeric upload limits, timeouts, retry counts and per-session cost limits must be set in the implementation specification. Cost exhaustion returns a useful partial result rather than an uncontrolled retry loop.

## 9 Evaluation and acceptance gates

Every functional requirement must have at least one passing happy-path test and its listed failure-path tests. Record fixture version, expected behavior and observed result. Synthetic tests establish controlled behavior; they do not demonstrate real-world efficacy or compliance by themselves.

| Measure | Proposed prototype gate | Evidence |
| --- | --- | --- |
| Critical unsupported claims | Zero fabricated official dates, eligibility decisions or confirmed inventory claims in the release suite | Annotated notice and food cases with reviewer comparison |
| Action evidence | Every displayed official date and policy instruction has valid supporting evidence or explicit unresolved status | Action-to-source audit |
| Food feasibility | Every recommended visit satisfies all known hard constraints; every unknown is labeled | Zero-budget, no-kitchen, closure and restricted-hours fixtures |
| Consent and isolation | All denied, cancelled, cross-session and duplicate-send cases pass | Operation records and attempted unauthorized access tests |
| Language and speech | All critical number, date, condition and confirmation cases pass for each supported demo language | English, Spanish, mixed speech, noise and eighteen-versus-eighty cases |
| Community benefit | One reviewed change revises two isolated plans appropriately and preserves completed tasks | Before-and-after plans and resource version record |
| Usability | Proposed research target: at least four of five formative participants identify the next action, destination and known deadline without prompting | Consented sessions; report the small sample and failures |

The release suite must additionally cover missing pages, historical notices, multiple household members, conflicting policy versions, a possible exemption, overlapping work hours, a failed pickup, microphone denial, cancellation, provider outage, expired sessions, changed reminder dates and restart after a delivery provider accepts a request. A critical failure blocks the affected live feature until corrected; a demonstration must disclose any disabled capability.

Measure time to a useful next step, correction effort, successful task completion, food-plan gaps, provider latency, cost per completed journey and review workload. Do not use transcript contents or detailed household histories as analytics. Do not optimize solely for fewer human referrals: escalation can be the correct outcome.

## 10 Delivery plan and demonstration

The published hackathon deadline is September 14, 2026 at 5 p.m. Pacific, or 7 p.m. Central. The schedule below is a proposed sequence from September 8, not a team-capacity estimate. The final submission checklist must be rechecked against the event rules. [Agents for Humans rules](https://agentsforhumans.devpost.com/rules).

| Stage | Deliverable | Exit condition |
| --- | --- | --- |
| 1 Scope and fixtures | Confirm the prototype baseline, two notice classes, reviewed directory fixtures and explicit simulations | Every demo claim has an evidence or simulation label |
| 2 Resident text journey | Entry, notice confirmation, checklist, food plan and official routes | FR01 through FR04 pass their core cases |
| 3 Preparation and adaptation | Basic hours log, synthetic packet and shared closure revision | FR05, FR06 and FR10 demonstrate observable results |
| 4 Voice and controlled delivery | Evaluated speech adapter, read-aloud and one test reminder | FR08 and FR09 pass cancellation, correction and failure cases |
| 5 Review and submission | Regression evidence, accessible demo, setup instructions, architecture and recorded walkthrough | Critical gates pass and limitations are accurately disclosed |

If capacity is constrained, reduce fixture breadth and additional integrations first. Preserve the two entry paths, source confirmation, food-plan revision, isolation and consent. Any removal of the recommended voice demonstration is a visible scope decision, not an undisclosed omission. Live partner referrals are not required to prove the product's core value.

The recommended demonstration follows Maria's synthetic notice, confirmed checklist and food plan; shows a speech correction and optional read-aloud; introduces a shared closure affecting a second household; and ends with a reviewed packet or a controlled reminder receipt. The audience should see tools doing work and plans adapting to evidence. Simulations, unselected vendors and absent official integrations remain clearly labeled.

## 11 Pilot readiness and open decisions

Live use requires named owners for policy and translation review, resource maintenance, security, partner operations and incident handling. No owner is assumed assigned by this PRD. Reviewers need a way to withdraw bad guidance promptly, retire obsolete records, find dependent plans and explain corrections. The team needs a route for residents or helpers to report inaccurate guidance without posting sensitive documents publicly.

| Decision | Proposed direction | Resolve before |
| --- | --- | --- |
| Geography and supported notices | Milwaukee; six-month report and proof request first | Prototype fixture freeze |
| Team capacity and spend | Set explicit build and per-session operating budgets | Implementation commitments |
| Speech, model and hosting | Follow the execution design; compare speech using representative samples | Voice integration and infrastructure setup |
| Language reviewers | English and Spanish with qualified review of critical content | Live guidance |
| Policy owner and precedence | Named qualified reviewer, versioned records and conflict escalation | Live guidance and scheduled publication |
| Directory rights and freshness | Direct sources, permission review and accountable update intervals | Public resource recommendations |
| Real uploads and retention | Temporary processing by default; explicit provider and deletion controls | Any live resident document processing |
| Saved-plan identity | Anonymous session first; separately scoped secure recovery | Cross-session persistence |
| SMS and partner channel | Test reminder first; real referrals only with active agreement and response expectations | External resident delivery |
| Accessibility and support | Manual core-journey review and named incident owner | Public pilot |

Priority discovery work is to review the two notice classes with benefits staff; test next-step comprehension with residents; verify local food records and travel assumptions; compare voice correction effort; and walk through a referral with an interested partner. These activities must establish constraints without requiring unnecessary personal case details. If no partner can receive requests reliably, retain contact routes and defer sending.

Later research may expand to additional notice classes, appeals, disaster food replacement, other household circumstances and additional languages. Each extension needs its own source, applicability, review and usability work. It must not be activated merely because a model can discuss it.

## 12 Supporting artifacts and requirement traceability

The [Research Brief](FoodShare-Bridge-Research-Brief.md) supplies FoodShare process research, sample notices, local source starting points and research questions. The [Strands Execution Design](FoodShare-Bridge-Strands-Execution-Design.md) supplies workflow responsibilities, tool contracts and failure boundaries. The [interactive architecture](FoodShare-Bridge-Architecture.html) shows the proposed components; it is not evidence of a deployed system. These companions were version 1.1 or the September 4 diagram when this PRD was authored.

| PRD area | Companion evidence | Development handoff |
| --- | --- | --- |
| FR01 through FR03 | Research sections 4, 6 and 7; execution sections 4 and 5 | Supported notice fixtures and action-screen design |
| FR04 and FR10 | Research sections 8 and 11; execution sections 8 and 10 | Directory records, constraint checks and revision scenarios |
| FR05 and FR06 | Research sections 5 and 7; execution sections 6 and 7 | Activity classification, totals and packet preview |
| FR07 through FR09 | Research sections 10 and 11; execution section 9 | Consent previews, delivery states and speech evaluation |
| Data and nonfunctional requirements | Research sections 9, 10 and 13; execution sections 3, 11 and 12 | Access, retention, recovery and operational decisions |
| Evaluation and rollout | Research sections 12 and 13; execution sections 13 and 14 | Release fixtures, review evidence and pilot readiness |

Use this PRD to derive screen designs, implementation tasks and an evaluation backlog. Resolve open decisions explicitly and record later scope changes by requirement ID. Refresh policy and resource evidence before enabling live guidance; the PRD governs product behavior, while reviewed source records govern case-relevant content.

## 13 Hackathon requirements and technology constraints

This section corrects incomplete hackathon coverage in version 1.0. Rules and the event overview were rechecked September 8, 2026. The requirements below govern submission readiness in addition to the product acceptance gates; this document does not establish entrant eligibility or a completed submission.

### Required technology and optional choices

| Item | Event status | FoodShare Bridge requirement |
| --- | --- | --- |
| Strands Agents SDK | Required | H01 Use Strands for observable tool execution and plan revision |
| AWS account | Required setup in the entry instructions | H02 Confirm account access and an operating budget |
| AWS Builder ID | Required submission field | H03 Have the entrant provide their Builder ID |
| Amazon Bedrock AgentCore | Optional and favorable for technical scoring | H04 Selected for our project; deploy Strands on AgentCore Runtime |
| Frontend, database, speech and model provider | No particular selection mandated in the reviewed project requirements | H05 Document selected vendors and authorized use |

The event calls for a new working agent that completes useful tasks. Incorporated pre-existing work must be disclosed; third-party code, APIs and data require authorized use. Judges need free access to a functioning website, demo or test build through the end of judging, October 8, 2026. [Official rules](https://agentsforhumans.devpost.com/rules).

Our recommended implementation direction remains the Strands Python SDK, a responsive web interface, application validators, reviewed policy and resource records, and separate maintenance permissions. Python is our recommendation. Speech remains a choice between evaluated adapters; AWS Transcribe, Polly and Deepgram are not mandated by the event. A specific frontend framework, database and model remain engineering decisions. An AWS account requirement does not establish that every component must run on AWS.

### Required submission evidence

The following checklist comes from the [event submission overview](https://agentsforhumans.devpost.com/). Each item needs an actual artifact or confirmation before submission.

- **H06 Public repository:** Source, necessary assets, setup instructions, README and a detectable MIT or Apache license file.
- **H07 Architecture:** Include a diagram matching the delivered implementation; revise the current proposed architecture where needed.
- **H08 Description:** Explain the product, intended audience and functionality.
- **H09 Video:** Publish a working demonstration on YouTube or Vimeo, no longer than five minutes. Explain the problem, audience and why it matters.
- **H10 Entry:** Include the AWS Builder ID and complete required submission fields by the deadline in Section 10.

A live demo link is optional but helps technical scoring. A public builder.aws.com build article is an optional bonus contribution. Good Neighbor Agents focuses on helping groups and community organizations. The planned two-household closure scenario makes that benefit visible. [Event overview](https://agentsforhumans.devpost.com/).

### Judging alignment and final verification

The five equally weighted criteria are technical implementation, design, potential impact, creativity and originality, and presentation. [Official rules](https://agentsforhumans.devpost.com/rules).

Our evidence plan maps technical implementation to real tool calls and a reproducible build; design to a complete accessible journey; impact to a specific household problem and credible resource constraints; originality to reviewed shared updates that adapt multiple plans; and presentation to a clear end-to-end walkthrough. These mappings are project recommendations, not additional contest rules.

Before submission, run the documented setup from a clean environment, test judge access, confirm the repository license, verify video visibility and duration, disclose simulations and prior work, and compare claims with delivered behavior. The demo may use synthetic residents while the agent and showcased features actually work. A simulated external service must not be advertised as a completed live integration. H01 through H10 are submission acceptance items, not claims already satisfied.

## 14 Impeccable UX design workflow

**UX01 Design tooling:** Use the Impeccable skill to shape, review and refine the responsive website experience. This is a user-selected project requirement, not a hackathon rule or a runtime dependency. Strands executes agent workflows; Impeccable guides how residents understand and interact with their results. This section incorporates the installed Impeccable version 4.1.2 workflow; it does not claim that screen designs or UX reviews are complete.

### Design intent and scope

Design for a resident who may be anxious, short on time, using a phone or sharing a library computer. The resident task screens use Impeccable's **Operate** mode, which prioritizes task completion and scanability. Explanatory help uses **Read** mode, which prioritizes comprehension. Choose visual direction during design discovery; the architecture diagram is a technical reference, not an approved resident interface.

Preserve the two entry points in Section 1. Within each task, make the next action clear and reveal additional detail when useful. Residents must be able to use structured controls without knowing how to prompt an agent. Use calm, respectful language, concrete action labels and visible source dates. The interface must distinguish FoodShare Bridge from an official government service and avoid promising food availability, benefit outcomes or completed submissions.

### Design sequence and deliverables

| Step | Impeccable workflow | Required project output |
| --- | --- | --- |
| Establish context | init and shape | Use the PRD as settled product context; resolve material gaps, create PRODUCT.md and confirm a brief covering users, tasks, states and constraints |
| Choose the interface direction | New work process following shape | Define the visual direction and core flow concepts; record DESIGN.md and surface briefs when proceeding to implementation |
| Make reusable interface patterns | extract when patterns exist | Shared typography, spacing, colors, focus styles, forms, action cards, evidence labels and status components |
| Review clarity and behavior | critique and clarify | Review the complete resident journey, hierarchy, cognitive load, action labels and uncertainty wording against the PRD |
| Address device and content variation | adapt and harden | Responsive layouts, translation expansion, errors, interrupted sessions, permissions and realistic content extremes |
| Verify the implementation | audit and scoped polish | Accessibility, responsive and performance findings with corrections and a final handoff linked to requirements |

Begin this work during Stage 1 in Section 10, establish core text-flow designs before Stage 2 implementation, and review delivered journeys in Stage 5. Do not repeat settled discovery questions. The first design outputs are a journey map and core screen concepts; the implementation handoff adds responsive screen specifications, reusable patterns, interaction states and requirement references. PRODUCT.md and DESIGN.md are planned artifacts, not files created by this PRD update.

### Required screen and interaction coverage

- **UX02 Entry and notice flow:** Cover FR01 through FR03 with two independent entry paths, optional synthetic notice selection, extracted-field confirmation, and an action checklist showing the known deadline, official destination and unresolved questions. Place source details near the guidance they support.
- **UX03 Food access flow:** Cover FR04 and FR10 with distinct food-today and later-this-week views, travel and household constraints, preparation checklists, visible unmet needs and a clear change summary after a verified closure. Never visually imply that seven days of food are secured when gaps remain.
- **UX04 Preparation and help:** Cover FR05 through FR08 with understandable hours totals, possible exemption or good-cause follow-up, packet preview, official contact routes and separate consent previews for reminders or navigator sharing. Use the precise preparation and delivery states defined in Section 8.
- **UX05 Language and voice:** Cover FR09 with a persistent language control, optional microphone activation, visible listening and processing states, editable transcription, read-aloud controls and an obvious return to text. Require confirmation of critical dates, hours, names and consent choices before dependent actions. Never make speech the only way to complete a task.

### Acceptance evidence and handoff

**UX06 Responsive and inclusive behavior:** Review mobile and desktop layouts, keyboard order, visible focus, screen-reader labels and announcements, contrast, 320 CSS pixel reflow and 200 percent text zoom against NFR03. Use actual English and Spanish sample content, long resource names, long translations and large text. Check that zoom, the mobile keyboard and reading controls do not hide the next action. Respect reduced-motion preferences and communicate status using text as well as color.

**UX07 Failure and uncertainty states:** The design handoff must cover loading, empty results, unreadable or incomplete notices, conflicting dates, stale sources, no feasible food option, provider outages, microphone denial, speech correction, cancellation, expired sessions and failed delivery. Explain what happened and provide a useful recovery or official help route. Preserve confirmed work where the privacy and session rules permit it.

**UX08 Review completion:** Map screens and findings to FR01 through FR10 and the relevant nonfunctional requirements. Conduct one batched mobile and desktop inspection, fix the findings together, and use at most one confirmation pass per design cycle as the skill directs. Record unresolved issues and apply the release gates in Section 9; bounded polishing does not waive an acceptance failure. Automated checks and visual review must be supplemented by manual accessibility checks and resident comprehension research. Do not describe the experience as validated until that evidence exists.

The handoff should identify each screen's primary action, required data, known and uncertain states, source display, consent boundary, localization behavior and acceptance evidence. Keep Strands tool names, infrastructure choices and internal agent traces out of resident screens unless they help the resident make a meaningful decision.

## 15 API data and prompt implementation requirements

The [APIs Data and Agent Prompts companion](FoodShare-Bridge-APIs-Data-and-Prompts.md) adds the integration inventory, source acquisition requirements, proposed application endpoints and starter prompt templates needed to implement this PRD. It supplements the Strands Execution Design. The services, prompts and application routes are specifications, not evidence of connected systems.

### Core data and service dependencies

The agent needs a selected model, pinned Strands SDK, reviewed policy and food records, session isolation, application tools and output validators. Policy records need dated applicability and approved passages. Food records need schedules, costs, access restrictions and verification dates. Plans must use household budget, food on hand, transport and preparation constraints; unknown pantry quantities cannot establish seven days of food coverage.

The project owner confirms 211 API access. Prioritize Search V2 for discovery and Query V2 for resource details; Suggest V2 is optional type-ahead and Export V2 is a conditional background import. Use no deprecated V1 products for new work. Exact schemas, enabled products, Wisconsin coverage, quotas, attribution, caching and redistribution rights still require verification; no account call has been tested. See the [211 Integration Plan](FoodShare-Bridge-211-Integration-Plan.md). HTF pages are source starting points; this research did not establish a supported inventory or appointment API. The baseline for ACCESS, MyACCESS, MilES and FSET remains verified official contact and resident submission routes. Do not collect ACCESS credentials or claim live case access. [211 developer onboarding](https://apiportal.211.org/get-started-overview), [211 data authorization](https://register.211.org/Home/LogIntoApiPortal), [HTF emergency food](https://www.hungertaskforce.org/get-help/emergency-food/), [MilES](https://www.dhs.wisconsin.gov/dms/miles.htm).

Evaluate OCR, speech, travel, messaging and navigator integrations separately. Verify access, coverage, quotas, privacy, retention and failure behavior before activation. The companion lists candidates and fallbacks. Vendor selection, maintainers, reuse rights and partner agreements remain open.

### Strands prompt requirements

Use a shared resident system prompt, a controller-selected workflow instruction, server-owned context, separated resident data and a typed output schema. Strands supports system prompts, custom Python tools and structured output; it does not provide the project's FoodShare policy or workflow prompts. SDK documentation was checked through Context7 and official pages on September 8, 2026. [Strands prompts](https://strandsagents.com/docs/user-guide/concepts/agents/prompts/), [custom tools](https://strandsagents.com/docs/user-guide/concepts/tools/custom-tools/), [structured output](https://strandsagents.com/docs/examples/structured_output/).

The companion provides eight starting templates for resident behavior, notices, food plans, activity and packets, revisions, language and speech, delivery previews and separate maintenance. Evaluate these project-authored prompts before use. Keep policy constants in reviewed records. Tool descriptions must state limitations and side effects. Model output cannot authorize sending or establish eligibility, stock, bookings or submission success.

### Implementation acceptance

- **I01 Model and runtime:** Configured access, pinned versions, observed tool calls and structured output under a defined budget.
- **I02 Reviewed data:** Supported notice fixtures, local resource records and policy passages with owners, reuse status and review deadlines.
- **I03 Tools and validators:** Typed requests, bounded errors, evidence and constraint checks, session isolation and safe partial results.
- **I04 Prompt evaluation:** Versioned templates, schemas, tools and tests for missing dates, applicability uncertainty, closures, speech correction and prompt injection.
- **I05 Optional integrations:** Feature-specific quality, privacy, consent and failure checks before OCR, speech, travel or delivery is enabled.
- **I06 Operational readiness:** Source correction, retention, deletion, incident ownership and required partner agreements verified before live use.

Track I01 through I06 alongside the product, UX and hackathon gates. A valid output schema is not proof of factual accuracy, and a good prompt is not an authorization control. Do not describe any integration or review as complete until the implementation supplies the relevant evidence.

## 16 Full technology stack baseline

The [Full Technology Stack companion](FoodShare-Bridge-Tech-Stack.md) supplies the recommended implementation choices for every product layer. This section supersedes earlier statements that the frontend, model, database, hosting and preferred speech provider are unspecified. These are project recommendations requiring configuration and evaluation, not completed integrations or additional hackathon requirements. The synthetic-data and public-pilot gates remain in force.

### Application and data stack

| Layer | Recommended technology | Purpose |
| --- | --- | --- |
| Website | Next.js 16 App Router, React 19 and TypeScript | Responsive website with static screen shells and interactive client components |
| Styling and UX | Tailwind CSS 4, shared CSS tokens and Impeccable | Accessible components, layouts and resident journeys |
| Localization | Reviewed English and Spanish JSON catalogs and browser Intl | UI language, dates and numbers; reviewed glossary for generated explanations |
| Application API | Python 3.12, FastAPI, Uvicorn and Pydantic 2 | Sessions, typed contracts, validation, consent and job status |
| Agent | Strands Agents Python SDK | Scoped tools and versioned workflow prompts |
| Model | Claude Sonnet 4.6 through Amazon Bedrock | Notice interpretation, explanations and plan proposals |
| Database | Amazon DynamoDB on-demand | Policy, resource, plan, session, job and operation records |
| Files | Separate private Amazon S3 buckets with KMS encryption for resident documents | Source snapshots, synthetic fixtures and authorized temporary exports |
| Document processing | Amazon Textract, ReportLab and pypdf | OCR, packet index and preserved original attachments |
| Source ingestion | HTTPX, Beautiful Soup and pypdf | Allowlisted public sources into a reviewed publication process |
| Resource directory API | 211 Search V2 and Query V2 through a bounded backend adapter | Owner-confirmed access; retrieve candidates and details, preserve unknowns and verify local scope |
| Speech | Amazon Transcribe and Amazon Polly | Optional speech input and read-aloud; Deepgram is an evaluated replacement |
| Identity | Anonymous secure session cookies; Amazon Cognito with MFA for reviewers | No resident account required; restricted review and publication |

### Deployment delivery and quality stack

| Layer | Recommended technology | Purpose |
| --- | --- | --- |
| Website delivery | Private S3 assets bucket and CloudFront | Static exported website with protected origin access |
| Application hosting | ECS Fargate, Application Load Balancer and ECR | FastAPI, HTTPS and speech gateway |
| Agent hosting | Amazon Bedrock AgentCore Runtime | Required project choice for resident and separately permissioned maintenance Strands execution |
| Scheduling and jobs | EventBridge Scheduler, SQS and dead-letter queues | Durable reminders, retries and processing jobs |
| Workers | Lambda for short delivery jobs; Fargate for longer work | Consent-checked dispatch, retries and separate maintenance permissions |
| SMS and telephone provider | AgentPhone preferred evaluation candidate; AWS End User Messaging SMS retained as the SMS fallback candidate | Two-way text first, inbound calls later; activation requires Section 17 checks |
| Domain and protection | Route 53, ACM, WAF, IAM, KMS and Secrets Manager | TLS, access boundaries, encryption and protected credentials |
| Infrastructure and CI | AWS CDK with TypeScript; GitHub Actions with AWS OIDC | Repeatable environments, tests and deployment without stored AWS access keys |
| Monitoring and spend | CloudWatch, sanitized OpenTelemetry and AWS Budgets | Errors, latency, usage and spend alerts; application enforces usage ceilings |
| Frontend tests | TypeScript, ESLint, Vitest and React Testing Library | Form, state and localization checks |
| Journey and accessibility tests | Playwright, axe-core and manual review | Mobile/desktop flows and assistive-technology behavior |
| Backend evaluation | pytest, Hypothesis and versioned agent fixtures | Constraints, evidence, authorization and prompt regressions |
| Local development | Supported Node LTS, npm lockfile, Python uv, Docker Compose and DynamoDB Local | Reproducible builds with synthetic fixtures |

CloudFront serves the static website and forwards uncached API and speech traffic to FastAPI. FastAPI invokes Strands on AgentCore using server-side IAM permissions and validates the result. [Next.js static exports](https://nextjs.org/docs/app/guides/static-exports), [Strands AgentCore deployment](https://strandsagents.com/docs/user-guide/deploy/deploy_to_bedrock_agentcore/python/).

Verify the model identifier, US region and data routing; pin dependencies and deployment versions. Speech and SMS retain their evaluation, privacy, registration and consent gates. Keep resident files private. Service selection does not establish case access, inventory or booking.

AgentCore Runtime is required for this project. Strands organizes agent work, Claude generates proposals and AgentCore runs the code. FastAPI enforces permissions and validation. See the [plain-English walkthrough](FoodShare-Bridge-AgentCore-Explained.md).

## 17 SMS and telephone access through AgentPhone

### Product decision and scope

Evaluate AgentPhone at agentphone.ai as the communications provider for FoodShare Bridge. Its documented capabilities include phone numbers, messaging and calls. In webhook voice mode, it sends transcribed input to our backend and receives the response to speak. This fits the existing Strands and AgentCore architecture. This is an evaluation decision, not a completed purchase, integration or production approval. [AgentPhone overview](https://docs.agentphone.ai/welcome), [voice modes](https://docs.agentphone.ai/documentation/guides/agents).

The responsive website remains the primary experience. First prove two-way SMS with controlled test participants, then evaluate inbound telephone assistance. Inbound calls are an extension unless explicitly added to the committed demo scope. Automated outbound calls to residents, agencies or food providers are outside this phase. Telephone access is separate from the website's Transcribe and Polly speech controls.

| Phase | Resident experience | Completion evidence |
| --- | --- | --- |
| SMS demonstration | Text a request for food, provide minimal constraints, receive supported options and an optional website link | Real controlled inbound and outbound messages; validated resource references; consent and failure checks |
| Reminder integration | Receive an explicitly requested neutral reminder and cancel future reminders | Scheduler, consent, opt-out, cancellation and duplicate-prevention evidence |
| Inbound phone evaluation | Call the service, hear a clear AI introduction, discuss nearby food help, and optionally request a text summary | English and Spanish task checks, correction flow, acceptable turn latency and a consented summary |
| Public pilot | Use an enabled channel under the same reviewed guidance and privacy rules as the website | Provider readiness, retention, security, operational ownership and applicable pilot gates |

These phases refine FR08 and FR09; they do not add hackathon technology requirements. If AgentPhone does not pass evaluation, retain the website and evaluate the existing AWS SMS option. Do not automatically send through a second provider after an uncertain delivery outcome.

### End to end architecture

```text
Resident SMS or telephone call
          ↓
AgentPhone receives the message or transcribes the spoken turn
          ↓
FastAPI verifies the provider event and binds the conversation scope
          ↓
Strands on AgentCore uses bounded tools and reviewed evidence
          ↓
211 Search V2 and Query V2 plus maintained official guidance
          ↓
Application validates the proposed answer and any requested action
          ↓
AgentPhone delivers the text or speaks the validated response
```

Use AgentPhone's webhook mode for the proposed phone integration so the FoodShare response remains under our agent workflow. Keep provider secrets server-side and expose only constrained application operations. Verify webhook signatures, reject replayed or duplicate events, bound message sizes, and rate-limit abuse. A sender's phone number alone must not grant access to an existing private website plan or proof packet.

Phone responses need a distinct latency budget. AgentPhone documents streamed voice webhook responses and a configurable response timeout. Test the actual FastAPI, AgentCore, model and 211 path together. A neutral progress message may acknowledge a lookup, but it must not imply results have been found. [AgentPhone webhook documentation](https://docs.agentphone.ai/documentation/guides/webhooks).

### Communication requirements

- **COM01 Minimal intake:** SMS can ask for ZIP area, immediate food need and constraints that change the result. It does not require a benefits notice or an account. Offer one manageable question at a time and a clear way to end the conversation.
- **COM02 Same evidence rules:** Messages and spoken answers use the same reviewed sources and validators as the website. Unknown opening information, access restrictions and pantry stock remain explicit. API failure is not a no-services result.
- **COM03 Separate permission:** A request for food information does not authorize ongoing reminders or partner sharing. Apply FR08's preview and explicit consent before recurring or scheduled messages. Confirm the destination before sending a caller's optional text summary.
- **COM04 Opt out and cancellation:** Implement and test applicable provider opt-out handling, including STOP and HELP behavior, before enabling public SMS. Enforce the latest consent state again at dispatch. Re-enrollment must be explicit; never bypass a provider suppression through another channel or number.
- **COM05 Truthful delivery:** Track requested, queued, provider-accepted, delivered when supported, failed and unknown states. Provider acceptance is not proof the resident read the message. Duplicate webhooks and retries cannot create duplicate logical replies or reminders.
- **COM06 Sensitive information:** Keep reminder text neutral for lock screens. Do not request SSNs, case numbers or benefit documents by SMS. Unexpected attachments must not enter the notice pipeline automatically. Private website links require appropriate authorization and must not expose sensitive data in their URLs.
- **COM07 Phone clarity:** Introduce the service as an AI assistant, explain its limits, and confirm important dates, ZIP codes and quantities. A contextual yes does not authorize an unrelated action. Offer correction, repetition and an appropriate verified human contact route.
- **COM08 Language and fallback:** Evaluate complete English and Spanish tasks, including interruptions, unclear speech, low-quality audio, provider timeouts and correction. Offer a text or website alternative when the channel cannot complete the task. Do not claim an unsupported language works.
- **COM09 Retention:** Verify message, transcript, recording, deletion and subprocessor settings before live resident use. Leave optional call recording disabled for the initial evaluation. Disabling recording alone does not establish that transcripts or other provider records are not stored. AgentPhone states that existing recordings are preserved when its recording add-on is disabled. [Call documentation](https://docs.agentphone.ai/documentation/guides/calls).

### Provider selection gate

Record the tested phone number capabilities, US outbound registration status, actual delivery channels, per-message and per-minute cost, spending limits, webhook behavior, retention settings and deletion evidence. AgentPhone's messaging documentation requires 10DLC registration for outbound SMS on its US numbers; do not equate number provisioning with messaging readiness. Its automatic channel behavior also needs review so the application accurately represents how messages are sent. [Messaging documentation](https://docs.agentphone.ai/documentation/guides/messages).

Require a controlled live round trip separately from fixture tests. Exercise duplicate delivery events, withdrawal of consent before dispatch, an ambiguous deadline, a shared phone, a provider outage and an unavailable resource. Confirm that no credentials or sensitive resident payloads appear in logs. An unresolved critical issue disables the affected channel rather than weakening the website's privacy or evidence requirements.

### Development workflow

Use the [Matt Pocock Skills Guide](FoodShare-Bridge-Matt-Pocock-Skills-Guide.md) to turn this section into bounded work: verify the provider contract, resolve remaining behavior decisions, write a feature specification, and create one end-to-end ticket at a time. Start with controlled SMS food-resource lookup. Keep phone calling, document processing and general outreach out of that first ticket.

This section supersedes the technology companion's AWS-only messaging recommendation for evaluation priority. AgentPhone remains a candidate until the selection gate passes; the earlier stack and execution documents do not establish a working communications integration.
