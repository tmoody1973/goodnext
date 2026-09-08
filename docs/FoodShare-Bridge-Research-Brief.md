# FoodShare Bridge Research Brief

Research foundation for product discovery and PRD development

Research date: September 4, 2026 | Version 1.1 | Geography: Wisconsin, with a proposed Milwaukee pilot

## 1 Purpose and main findings

FoodShare Bridge is a proposed free, responsive, multilingual website that helps Wisconsin households understand a benefits notice or life change, organize their next official steps, and find food for the next seven days. This brief brings together policy research, product direction, agent workflows, unresolved questions, and a source register for further investigation and a later product requirements document.

The central product opportunity is continuity across separate tasks. Submitting an application or renewal does not necessarily finish the process: an interview, requested evidence, or agency review can remain outstanding. A useful website makes those dependencies visible while helping the household access food immediately.

The research supports five design priorities:

- Identify the notice, affected household member, and requested action before offering guidance.
- Track different deadlines separately and retain the source for each date.
- Build food plans around real constraints and verified resource records, with explicit gaps and alternatives.
- Use Strands to retrieve information, organize tasks, explain choices, and revise plans; enforce calculations and permissions in application code.
- Keep public policy and resource monitoring separate from optional storage of personal information.

No resident interviews, partner commitments, production integrations, or measured impact results are established in this brief. Those are research tasks. Policy findings describe sources checked on the research date and require rechecking before use in a public service.

### How to read the evidence

**Verified finding** means a cited primary source supports the statement. **User direction** records the requested product concept or constraint. **Recommendation** is a proposed design choice. **Open question** identifies something that must be investigated or decided. Illustrative scenarios are examples for design and testing, not actual case determinations or verified food availability.

## 2 Product direction and scope

### User direction

The product is a responsive website usable on phones, tablets, library computers, and desktops. A separate mobile application is unnecessary. The intended audience includes residents whose FoodShare benefits were reduced, interrupted, or put at risk by notices, deadlines, reporting, or work requirements.

Two entry points should remain visible: **Food this week** and **Understand my notice or change**. Residents should be able to find food without uploading a notice or completing benefits screening.

The requested capability set includes:

- A situation picker for reduced or stopped benefits, an unfamiliar letter, a missed deadline, work questions, and other life changes.
- A seven-day food-access plan with optional meal and grocery suggestions.
- Plain-language notice explanations and a screening flow about whether action may be needed this month.
- A checklist covering renewals, six-month reports, interviews, requested proof, and agency follow-up.
- A monthly work or training planner, including an 80-hour planning mode when appropriate.
- Optional notice uploads and a proof packet containing resident-selected evidence and reviewed notes.
- Official case-help routes, local food resources, and optional requests to a named verified navigator.
- Language selection, readable text, optional tap-to-speak input and read-aloud explanations, printable plans, and optional SMS reminders.

### Boundaries

The website does not decide eligibility, guarantee benefits, certify an exemption, attest that activity hours qualify, or submit benefits paperwork. Residents retain control over official submissions and sharing. Food access is available regardless of whether someone completes the benefits workflow.

The initial concept excluded documents; the user subsequently added notice uploads and proof packets. The current direction includes these as optional paths, with a manual alternative. This materially increases privacy and security requirements.

The original concept included a separate educational Community Updates screen with a clearly labeled native ad, while keeping assistance and consent flows ad-free. The recommendation is to defer advertising for the hackathon and pilot. That is a proposed scope decision, not a confirmed removal from the long-term concept.

### Audience hypotheses to validate

Primary users may include a working parent with limited pickup time, an older adult receiving a new reporting notice, a resident without a kitchen or transportation, and someone seeking help after a deadline. Secondary users may include FoodShare advocates, pantry staff, librarians, school staff, and community navigators. These are research hypotheses rather than validated personas.

## 3 Hackathon context

The Agents for Humans hackathon requires a new project using Strands Agents. The Good Neighbor category includes groups such as neighborhoods, nonprofits, food banks, schools, and libraries. The event emphasizes agents doing useful work, including recurring work that can happen in the background. A household-facing workflow becomes a stronger category story when a shared partner update improves guidance for multiple households. [S01](https://agentsforhumans.devpost.com/)

The published deadline is September 14, 2026 at 5 p.m. Pacific, or 7 p.m. Central. Submission requirements include a public repository with an MIT or Apache license, README, setup materials, architecture diagram, AWS Builder ID, description, and a working demonstration video no longer than five minutes. A live demo and AgentCore deployment can strengthen technical scoring; AgentCore is optional. New-project and prior-work disclosure rules apply. Recheck rules and announcements before submission. [S02](https://agentsforhumans.devpost.com/rules)

Recommended demonstration focus: show the resident receiving a useful plan, then introduce a new proof request or a simulated pantry closure and show the agent revising only affected tasks. Clearly label simulated documents, partner updates, and integrations.

## 4 Wisconsin FoodShare process

### Applying and expedited service

Residents can apply through ACCESS, by phone, in person, or with a paper form. A county or Tribal agency handles the case; Milwaukee County uses Milwaukee Enrollment Services, or MilES. An application requires an interview. [S03](https://www.dhs.wisconsin.gov/foodshare/eligibility.htm)

Normal application processing is within 30 days of filing. Some missing-action cases can be completed within 60 days without a new application, with consequences for the benefit start date. These are case-specific recovery paths; the product should route residents to the agency instead of automatically directing every denied applicant to reapply. [S04](https://www.emhandbooks.wisconsin.gov/fsh/policy_files/2/21/2.1.2.htm)

Applications and qualifying late renewals are screened for expedited service. Eligible households generally receive benefits within seven days, with required interview and verification rules and special rules when expedited eligibility is discovered later. The product can help residents ask about this option without promising approval or a payment date. [S05](https://www.emhandbooks.wisconsin.gov/fsh/policy_files/2/21/2.1.4.htm)

### Interview and requested evidence

Interviews normally happen by telephone; residents may request an in-person interview. An interview may also be required at renewal. Suggested evidence can include income records and shelter or utility expenses, depending on the case. A suggested example must not become a universal document requirement in the website. [S06](https://www.dhs.wisconsin.gov/foodshare/interviews.htm)

A Notice of Proof Needed identifies required information and a deadline. The handbook generally allows at least 20 days for verification, with exceptions. Agencies must avoid excessive verification and should accept different adequate evidence types. The product should follow the actual request and offer help obtaining evidence, rather than invent an exhaustive paperwork list. [S07](https://www.emhandbooks.wisconsin.gov/fsh/policy_files/1/12/1.2.1.htm)

### Decision and access to benefits

The agency determines eligibility and issues notices. Benefits are used through the Wisconsin QUEST card. Card failure, loss, or damage has a separate support route from case eligibility; temporary cards may be available through the agency in qualifying circumstances. Add a distinct card-problem route to the situation picker. [S08](https://www.dhs.wisconsin.gov/foodshare/ebt.htm)

ACCESS is the official website for applying and managing case tasks. MyACCESS provides functions including document uploads and status information. The proposed website prepares residents for those official channels; a file prepared in FoodShare Bridge is not an official submission or acceptance receipt. [S09](https://www.dhs.wisconsin.gov/forwardhealth/myaccess.htm)

### Renewals

Most households renew yearly, although other certification periods apply. DHS sends a renewal notice identifying steps and timing. Completing a renewal may involve updated information, an interview, and evidence. DHS advises finishing all required steps by the last business day of the renewal month to preserve full benefits for the following month. A renewal may generally be completed up to one month late without reapplying, but a gap or reduced benefits can result. [S10](https://www.dhs.wisconsin.gov/foodshare/renewals.htm)

### Six month reports

Some households must complete an interim report and requested supporting documents. DHS says both must be received by the end of the due month to preserve full benefits. A later date on a proof-request letter may not preserve the full amount. Being more than a month late can require reapplication. Treat the report and its evidence as linked but separate tasks. [S11](https://www.dhs.wisconsin.gov/foodshare/smrf.htm)

### Reporting changes between reviews

Simplified reporting includes certain income increases, work hours falling below 80 for affected members, and substantial lottery or gambling winnings. Applicable reports are generally due by the 10th of the following month. The income reporting threshold is distinct from eligibility, and exceptions and case context matter. Do not turn any life change into an automatic immediate-reporting instruction. [S12](https://www.emhandbooks.wisconsin.gov/fsh/policy_files/6/61/6.1.1.htm)

### Benefit interruptions and appeals

The appropriate route depends on whether the issue concerns missing evidence, a late review, work requirements, a card, or a disputed decision. DHS describes ways to regain benefits after work-requirement interruptions, which can involve meeting requirements, exemptions, or good cause; reapplication may be needed. [S13](https://www.dhs.wisconsin.gov/foodshare/work.htm)

Residents may request a fair hearing about agency action. The handbook generally specifies 90 days from when the action affected benefits, with a separate rule allowing challenges to the current amount during a certification period. Any earlier deadline relevant to continued benefits must be handled separately and verified with current official guidance. Do not imply that an ordinary call to the agency files an appeal or pauses a deadline. [S14](https://www.emhandbooks.wisconsin.gov/fsh/policy_files/6/64/6.4.1.htm)

## 5 Policy changes and interpretation risks

### Work requirements and implementation dates

Wisconsin distinguishes FoodShare basic work rules from the separate FoodShare work requirement. Current public guidance describes the latter as potentially applying to members ages 18 through 64 without a child age 13 or younger in the home. Exemptions and good cause may apply. A resident's age alone does not establish their current obligation. [S13](https://www.dhs.wisconsin.gov/foodshare/work.htm)

Operations Memo 26-04 explains federal changes and Wisconsin implementation, including changes to prior exemptions and staged treatment at applications or renewals. The product needs both the policy effective date and the resident's relevant notice or review date. A news announcement cannot establish a personal deadline. [S15](https://www.dhs.wisconsin.gov/dms/memos/ops/dms-ops-2026-04.pdf)

The same memo says agencies generally accept self-attestation of an exemption unless the information is questionable. Therefore, a possible exemption should first lead to a reviewed explanation or agency conversation. Do not automatically demand medical records or a proof packet from everyone who raises an exemption. [S15](https://www.dhs.wisconsin.gov/dms/memos/ops/dms-ops-2026-04.pdf)

### August change affecting some older adults

Effective August 8, 2026, changes to 36-month certification periods affected certain members ages 60 through 64 without a disability. Affected existing households retain their current renewal date while gaining six-month reporting and next-renewal interview obligations. The agency sends a letter specifying the first report due date. This is particularly relevant to the proposed Maria scenario. [S16](https://www.dhs.wisconsin.gov/dms/memos/ops/dms-ops-2026-28.pdf)

### Workfare and hours planning

An 80-hour tracker does not cover every permitted arrangement. FSET distinguishes workfare from Work Activity and other activities. Workfare can use an hours obligation calculated from the household allotment and applicable minimum wage. The website should record an agency-assigned plan and flag uncertainty about whether activities count. Suggested public name: **My Work or Training Plan**. [S17](https://www.emhandbooks.wisconsin.gov/fset/6/6.3.htm)

FSET also distinguishes qualifying and non-qualifying activities. The agent must not certify an arbitrary class, volunteer placement, or job-search activity as qualifying merely because it occupies time. Validate integration requirements and activity classifications with FSET staff. [S18](https://www.emhandbooks.wisconsin.gov/fset/1/1.4.htm)

### Policy source governance

Recommendation: maintain reviewed policy records containing program, jurisdiction, publication date, effective date, source URL, affected population, conditions, superseded version, review status, and review owner. A scheduled Strands workflow can detect changes and draft comparisons. A qualified reviewer approves substantive changes before resident-facing instructions change.

Separate proposed rules, enacted future changes, and current rules. Keep SNAP and Medicaid logic separate even when a notice mentions multiple programs. Broader changes such as noncitizen eligibility, benefit calculations, and future legislation need dedicated research before inclusion; immigration-status collection is outside the requested initial data set.

When an older sample, public webpage, and newer memo conflict, record the conflict and seek review. Do not silently apply whichever source was retrieved first.

## 6 Public sample notices

### Notice of Proof Needed

The official ten-page example is a useful starting fixture. Pages 1 and 2 show the affected programs, agency contact, deadline field, person, and requested self-employment information. Later pages contain forms and instructions. It uses fictional details and date placeholders. The extraction system should report that no real deadline is present. [S19](https://www.dhs.wisconsin.gov/dms/memos/ops/mds-ops-2019-j7attachment3.pdf)

Proposed explanation: the agency needs additional information about the listed person's business income and expenses. The resident can organize the evidence requested, identify unanswered questions, and contact the agency for help. This supports the first notice-to-checklist demonstration.

### Work rules and requirement information

The official twelve-page sample lists different statuses for different household members on page 2. Later sections cover rules, exemptions, good cause, FSET, and hearing information. It contains historical policy wording and dates, including an older age range and time-limit period. Use it to study layout and person-specific extraction, not as the live policy authority. [S20](https://www.dhs.wisconsin.gov/foodshare/workinfo-letter.pdf)

### Additional research fixtures

The time-limited-benefits warning sample and DEAR renewal example provide additional formats to investigate. Treat both as historical sample material requiring content review; DEAR is a specialized renewal context, not a universal renewal template. Their layouts can broaden testing after the first two examples work reliably. [S21](https://www.dhs.wisconsin.gov/foodshare/3tlb-warning-letter-sample.pdf), [S22](https://www.dhs.wisconsin.gov/foodshare/dear-renewal.pdf)

Fixture policy: retain original samples unchanged; label their historical status. Any derivative demonstration document must be conspicuously fictional, use fabricated personal details, and avoid implying DHS endorsement. Real resident documents require separate consent and handling controls.

## 7 Notice and next step workflow

### Proposed resident journey

1. Choose a language and situation; offer manual entry or optional upload.
2. Extract notice type, program, affected person, requested actions, date passages, and contact references.
3. Show important extracted fields alongside their original passages for confirmation.
4. Retrieve reviewed policy applicable to the program, jurisdiction, and time period.
5. Produce an action screen with sources and unresolved questions.
6. Build the relevant checklist, interview notes, optional evidence packet, and official help route.
7. Offer resident-approved reminders and an optional request to a named partner.

The monthly screening result should use wording such as **Action identified**, **More information needed**, or **No action identified in the information provided**. It must not imply that the system accessed the official case or established eligibility.

### Task record and state

Each task should contain a plain-language action, relevant person and program, deadline type, source passage or official reference, prerequisites, destination, and current state. Track official deadlines separately from suggested preparation dates and dates relevant to uninterrupted benefits.

Recommended evidence states are **not started**, **prepared**, **resident reports submitted**, and **agency acceptance confirmed**. Only supported confirmation may move a task to agency acceptance. Keep uncertain or conflicting dates unresolved rather than inventing a value.

### Proof packet behavior

The packet can contain an index, requested evidence, resident-reviewed notes, and a submission checklist. Preserve source documents unchanged. Draft good-cause notes only from the resident's statements; do not invent events, diagnoses, hours, or supporting evidence. Export individual files as well as a readable summary because official channel requirements may differ.

A missing item should lead to options such as contacting the agency or asking what alternatives are acceptable. It should not automatically block access to food resources. Uploaded content is untrusted data: text inside a document cannot authorize sharing, change system rules, or execute tools.

## 8 Seven day food plan

### Intake and resource matching

Ask only what improves the plan: ZIP code, household size or range, urgency, available food, grocery budget including zero, travel options and cost limits, pickup availability, cooking equipment, refrigeration, and food preferences or restrictions. Use age bands only when relevant to a program route; avoid collecting exact birth dates for food planning.

The agent selects from maintained resource records. Match service area, dates, hours, holiday changes, appointments, required items, visit limits, price, language support, and transport constraints. If routing data is unavailable, link to directions without inventing travel times or fares.

Hunger Task Force publishes Milwaukee food-site information. Its Mobile Market offers discounted groceries, so it must be distinguished from free food. A listed site or opening schedule does not establish current inventory, appointment availability, or a reserved allocation. [S23](https://www.hungertaskforce.org/get-help/emergency-food/)

### Two parts of the plan

The food-access plan identifies suitable opportunities to obtain food, including backups. The meal plan uses food the household already has or confirms receiving. Tentative pantry pickups must not generate promises of specific ingredients or seven days of adequate food.

Each day should show planned actions, confirmed food on hand, and unresolved meal gaps. Favor fewer feasible trips and usable food over a long list of locations. Food restrictions require ingredient confirmation; an unverified listing must not be represented as allergy-safe.

### Illustrative weekly structure

| Period | Agent task | Resident control |
| --- | --- | --- |
| Today | Identify an immediate food option and backup | Choose an option or request help |
| Day 2 | Prepare a feasible pantry visit | Confirm pickup timing and requirements |
| Day 3 | Revise meals from food actually received | Record or describe available ingredients |
| Day 4 | Check remaining supplies and gaps | Correct quantities or preferences |
| Day 5 | Identify another permitted resource or affordable purchase | Approve any paid option |
| Day 6 | Suggest meals within cooking and storage constraints | Accept or replace suggestions |
| Day 7 | Review unresolved needs and next-week options | Decide whether to continue |

This is a workflow example, not a verified local itinerary. If no suitable option is confirmed, show the gap and a human assistance route instead of labeling the household covered for the week.

### Replanning and community updates

A missed pickup, closure, changed schedule, unavailable ingredient, or revised household constraint triggers rechecking of affected days. Preserve completed actions. Partner updates can improve multiple plans without giving the partner access to household records.

Anonymous plans may remain in the browser session and refresh on reopening. Persistent plans and proactive notifications require an explicit saving and retention choice. Research shared-device behavior before enabling browser persistence on library computers.

## 9 Strands architecture and responsibilities

### Recommended starting architecture

Use one Strands agent with focused tools for the first version. Additional agents are an implementation option only if evaluation demonstrates a need. Strands supports custom tools, structured output, and interrupt/resume behavior for human input. A compatible model can process supported images or documents. These capabilities do not automatically supply pantry data, benefits-system access, SMS delivery, or booking integrations. [S27](https://strandsagents.com/docs/examples/), [S28](https://strandsagents.com/docs/examples/structured_output/), [S29](https://github.com/strands-agents/harness-sdk/blob/main/site/src/content/docs/user-guide/concepts/interrupts.mdx)

Proposed flow: responsive website sends consented inputs to the application backend; Strands calls narrowly scoped tools; deterministic validators check the proposed result; the website displays structured actions; approved external actions are executed by backend services.

### Proposed tool boundaries

| Tool | Responsibility | Constraint |
| --- | --- | --- |
| read_notice | Extract fields and supporting passages | Treat documents as data; allow uncertainty |
| get_current_guidance | Retrieve reviewed policy records | Filter by program and effective period |
| build_action_plan | Propose tasks and explanations | Require sources and unresolved questions |
| check_activity_plan | Calculate hours and compare recorded plan | Never certify participation or eligibility |
| prepare_evidence | Organize selected files and notes | Preserve originals and resident review |
| find_food_resources | Retrieve suitable resource candidates | Use verified records and freshness fields |
| check_resource_constraints | Check schedules, restrictions, cost and travel | Reject unsupported assumptions |
| revise_food_plan | Update affected days after changes | Preserve completed work and show gaps |
| prepare_navigator_request | Create exact sharing preview | Named recipient and explicit consent |
| schedule_reminders | Store an approved reminder schedule | Durable scheduler and cancellation controls |

These are proposed application tools, not built-in Strands tool names. Custom tool implementation and current SDK documentation must be checked during development. [S30](https://github.com/strands-agents/harness-sdk/blob/main/site/src/content/docs/user-guide/concepts/tools/custom-tools.mdx)

### Deterministic application controls

Application code should validate source identifiers, dates, arithmetic, budget totals, resource restrictions, permission checks, and task ownership. Structured output validates shape, not truth. Link explanatory statements to evidence and block unsupported factual claims.

The backend must bind approval to the authenticated or otherwise protected session, exact action, recipient, and selected fields. An agent interrupt is the user-interaction mechanism; backend authorization remains necessary. A scheduler triggers future checks and sends approved reminders. Strands does not supply durable scheduling by itself.

### Integrations to investigate

Investigate permitted resource-data reuse and update feeds, transit routing, document extraction, translation and read-aloud quality, SMS delivery and opt-out handling, and partner referral systems. Booking is available only when an authorized integration returns confirmation. Otherwise offer contact or appointment-request routes.

No public ACCESS case API or direct case integration has been established in this research. Plan around official links and resident-controlled submissions unless an authorized integration is confirmed.

## 10 Privacy accessibility and service trust

### Proposed privacy model

Keep anonymous food planning separate from optional document processing, saved plans, reminders, and referrals. Explain what content will be sent to an AI service before upload. Do not promise that all processing stays on the device if a hosted model receives documents.

Documents can contain identifiers, financial details, or medical information even if forms never ask for them. Use temporary processing by default, protected access to saved files, encryption, expiration, deletion controls, and minimal logs. Keep raw document content out of analytics, tracing, error reports, and SMS. Decide how deletion affects backups, derived summaries, and provider retention before a live pilot.

Do not collect Social Security numbers, case numbers, immigration details, or medical details for the basic food plan. Keep contact details separate from the planning model when possible. A referral shares only reviewed fields with a named verified organization, and only after consent.

### Language and accessibility

Recommendation: start with English and Spanish, subject to community research and qualified review; evaluate Hmong, Karen, and other languages with local partners. Preserve names, dates, numbers, official program names, and conditional wording in translations. Machine translation quality is not established by fluent-looking output.

Use responsive layouts, keyboard support, screen-reader labels, large text, clear focus states, readable contrast, and printable plans. Read-aloud must be optional, particularly on shared devices. Test low-bandwidth use, interrupted uploads, manual alternatives, and leaving a library computer safely. Select measurable accessibility criteria during PRD development and verify current standards then.

### Voice interaction in the prototype

Include optional Tap to speak and Listen to this explanation controls in the prototype. Residents can describe a situation, answer food-intake questions, revise a plan, and hear the next step while retaining visible forms and checklists. Typing and tapping remain available. Speaking a description of a notice does not establish what the notice actually says.

The proposed flow is microphone input, speech-to-text, confirmation of important details, the existing Strands workflow, validated on-screen results, and optional text-to-speech. Confirm dates, ZIP codes, household size and work hours before they drive guidance. Interim transcripts cannot trigger actions; hearing a general yes does not authorize sharing or reminders without the existing exact-action consent flow.

Use a replaceable speech adapter and implement one provider first. Prefer Amazon Transcribe with Amazon Polly if the backend is centered on AWS; evaluate Deepgram Nova-3 first if English/Spanish code-switching is a central demo feature. The provider remains unselected until a small evaluation compares accuracy, task completion, latency and cost. Transcribe provides streaming transcription; Deepgram documents multilingual code-switching and keyterm prompting; Polly provides speech synthesis. Check each chosen model's language support separately from translation support. [S34](https://docs.aws.amazon.com/transcribe/latest/APIReference/API_streaming_StartStreamTranscription.html), [S35](https://developers.deepgram.com/docs/multilingual-code-switching), [S36](https://developers.deepgram.com/docs/keyterm), [S37](https://docs.aws.amazon.com/polly/latest/dg/what-is.html)

Recording requires an explicit control, a visible indicator and a stop/cancel option. Avoid retaining raw audio by default; explain cloud processing and verify provider retention and model-improvement opt-outs before resident use. Exclude audio and transcripts from routine logs. Permission denial, unsupported language or connection failure returns to text without losing confirmed information. Read-aloud remains optional on shared devices. Both providers document model-improvement opt-out mechanisms. [S38](https://aws.amazon.com/transcribe/faqs/), [S39](https://developers.deepgram.com/docs/the-deepgram-model-improvement-partnership-program)

### External actions and advertising

Separate consent for document processing, saving, SMS, and partner sharing. Provide cancellation and a way to review scheduled reminders. Use neutral message text that avoids disclosing benefit or health details on a lock screen.

Defer advertising for the pilot. Any later sponsorship model needs its own research into tracking, referral incentives, editorial independence, and trust. Rankings of food or help options should follow resident needs and verified suitability.

## 11 Milwaukee resource starting points

The records below were checked on September 4, 2026. Reconfirm before publishing contact cards or planning travel. Inclusion is not a partnership, API agreement, or endorsement.

| Organization or service | Role | Starting contact |
| --- | --- | --- |
| Milwaukee Enrollment Services | Official case questions, interviews and proof | 888-947-6583; 6055 N 64th St and UMOS at 2701 S Chase Ave |
| Hunger Task Force advocates | Free FoodShare navigation | 414-988-6501 at 4144 N 56th St; 414-238-6484 at 802 W Historic Mitchell St |
| FSET | Employment and training support | Use the official program route and regional provider information |
| 211 Wisconsin | Food and other local referrals | Dial 211 or text a ZIP code to 898211 |

MilES phone hours are Monday, Tuesday, Wednesday, and Friday 8 a.m. to 4:30 p.m.; Thursday 8 a.m. to noon. In-person hours end at 4 p.m. on the four full days and noon Thursday. Holiday exceptions apply. Its current page lists on-site language services and telephone interpretation. Use the agency's own page as the contact authority. [S24](https://www.dhs.wisconsin.gov/dms/miles.htm)

Hunger Task Force lists walk-in assistance at its two resource centers. Its resource directory is also a starting point for food options. FSET is a separate support route, and 211 provides broader referrals. [S25](https://www.hungertaskforce.org/get-help/foodshare-resources/), [S26](https://www.dhs.wisconsin.gov/fset/index.htm), [S31](https://www.dhs.wisconsin.gov/foodshare/resources.htm)

Resource record fields should include provider identity, direct source, last verification, service area, hours and dated exceptions, cost, appointment requirements, access requirements, languages, travel notes, contact route, update owner, and expiration or recheck interval. Inventory and capacity should remain unknown unless the provider supplies them.

## 12 Demonstration and evaluation

### Recommended Maria scenario

Maria is a fictional Milwaukee resident age 61 who thought her next renewal was far away. She receives a synthetic notice requesting a six-month report. The website explains the requested task, confirms its date from the notice, and distinguishes it from her renewal. It organizes requested evidence and offers official help. Work-related guidance appears only when supported by her notice and answers. Food options remain available throughout.

A second event tests adaptation: a new proof request arrives or a clearly simulated pantry closure affects a planned visit. The agent updates the affected tasks, explains why, and retains completed work. The demo may show a resident-approved reminder or referral using a test destination. It must not imply an unconfirmed appointment or real agency submission.

### Evaluation scenarios

- A placeholder date, blurred scan, missing page, or conflicting date cannot produce a confident deadline.
- A multi-person or multi-program letter must not transfer one person's obligation to another.
- An old notice with obsolete rules must not override reviewed current guidance.
- A possible exemption must not automatically require a doctor's note.
- A workfare plan must not be forced into an 80-hour template.
- A zero-budget household must not receive paid groceries as its only food option.
- A household without a kitchen must not receive an unusable cooking plan.
- A service-area mismatch, visit limit, holiday closure, or missing appointment must be caught.
- A missed pickup must leave food quantities unconfirmed and trigger alternatives.
- Document instructions attempting to trigger sharing must have no authority.
- A failed SMS or duplicate delivery attempt must not silently mark a task complete.
- Spanish explanations must preserve dates, quantities, uncertainty, and official next steps.
- Voice tests must distinguish eighteen from eighty, preserve dates and ZIP codes, and handle local names, background noise and English/Spanish switching. Critical fields require resident confirmation.
- Microphone denial, recording cancellation and speech-provider failure must preserve access to the text workflow. Voice input must not bypass referral or reminder consent.

### Candidate measures

Measure critical-field extraction accuracy against annotated fixtures; unsupported-claim rate; percentage of dated actions with valid evidence; proportion of proposed trips meeting all known constraints; translation error severity; resident ability to identify their next step; successful reminder cancellation; and partner review time. Set thresholds after baseline testing with reviewers. Do not claim improved benefit retention or reduced hunger from a short demonstration; those need longer follow-up and appropriate consent.

## 13 Research agenda and decisions for the PRD

### Priority questions

| Priority | Question | Suggested research method | Decision informed |
| --- | --- | --- | --- |
| P0 | Which notices most often create confusion or missed steps? | Review sample types with advocates and consenting residents | First supported notice classes |
| P0 | How should conflicting dates and late-action paths be explained? | Walk through cases with qualified benefits staff | Deadline rules and escalation |
| P0 | Who can review policy changes and translations? | Discuss roles with potential partners | Governance and supported languages |
| P0 | Can local resource data be reused and kept current? | Confirm permissions and maintenance with providers | Directory and update design |
| P0 | What retention and model-provider settings are acceptable? | Security and privacy review of candidate architecture | Upload and saved-plan scope |
| P0 | Can a navigator accept referrals and respond reliably? | Partner workflow and capacity interviews | Live referrals versus contact links |
| P1 | Which foods, pickup times, and travel constraints matter most? | Resident interviews and plan walkthroughs | Food intake and ranking |
| P1 | How do FSET staff verify activities and handle workfare? | Review example employment plans | Hours-planning boundaries |
| P1 | Which channels and languages do residents trust? | Community usability sessions | SMS and translation roadmap |
| P1 | Which speech provider captures important information most reliably? | Compare consented or synthetic recordings containing dates, numbers, local names, noise and mixed-language speech; measure correction effort, latency and cost | Speech provider and supported voice modes |
| P1 | How does a shared-computer session end safely? | Library-based usability and accessibility review | Persistence and exit behavior |
| P1 | What do reminders add beyond official tools? | Compare resident workflows with ACCESS and MyACCESS | Differentiation and notifications |
| P2 | What operating costs and funding models are sustainable? | Estimate usage and interview potential funders | Hosting budget and sponsorship |

Suggested interview prompts: describe the last confusing notice; identify what happened after submitting a form; explain what prevented a pantry trip; show how an agency confirms receipt; describe acceptable sharing; and identify a translation that would need staff review. Avoid requesting identifying case details when a hypothetical or redacted example will answer the question.

### Decisions still open

Confirm pilot geography, notice types, language set, upload and audio retention, identity method for saved plans, resource update ownership, SMS and speech providers, model and hosting configuration, partner response expectations, appointment scope, work-plan complexity, accessibility criteria, and whether advertising remains deferred. No partner or technology vendor is selected by this brief.

### Candidate delivery stages

For the hackathon, prioritize a responsive English and Spanish flow, synthetic notice demonstrations, a structured checklist, a small verified Milwaukee directory, food-plan revision, and a downloadable demonstration packet. Add optional tap-to-speak and read-aloud through one evaluated speech adapter, preserving the text flow. Use one controlled reminder or referral demonstration if feasible. These are recommendations for scope, not a delivery commitment.

Before a public pilot, complete policy review, translation validation, document security and deletion testing, accessibility testing, provider permissions, failure handling, and partner operating agreements. Expand geography, languages, persistent storage, and integrations only when their maintenance responsibilities are clear.

### PRD preparation map

Use Sections 1 and 2 for the problem and audience; Sections 4 through 6 for evidence and domain constraints; Sections 7 and 8 for user journeys; Section 9 for system responsibilities; Section 10 for privacy and accessibility requirements; Section 11 for integrations; Section 12 for acceptance scenarios; and this section for unresolved decisions.

The PRD should specify actors, entry conditions, happy paths, failure paths, data collected, permissions, completion evidence, measurable acceptance criteria, dependencies, and explicit exclusions for each feature. Convert recommendations to requirements only after the associated decision is made.

## 14 Source register

All sources below were consulted during the research on September 4, 2026. A current URL or recent crawl does not guarantee that every paragraph is current. Check document dates, effective dates, and superseding guidance. Sample notices are marked separately from policy authorities.

- **S01** [Agents for Humans overview](https://agentsforhumans.devpost.com/) — category, theme, judging and submission overview.
- **S02** [Agents for Humans rules](https://agentsforhumans.devpost.com/rules) — deadline, licensing, new-work and submission conditions.
- **S03** [DHS How to Apply](https://www.dhs.wisconsin.gov/foodshare/eligibility.htm) — application channels and agency route.
- **S04** [FoodShare Handbook application processing](https://www.emhandbooks.wisconsin.gov/fsh/policy_files/2/21/2.1.2.htm) — processing and incomplete-application recovery.
- **S05** [FoodShare Handbook expedited service](https://www.emhandbooks.wisconsin.gov/fsh/policy_files/2/21/2.1.4.htm) — priority screening and issuance rules.
- **S06** [DHS Interviews](https://www.dhs.wisconsin.gov/foodshare/interviews.htm) — interview process and evidence examples.
- **S07** [FoodShare Handbook verification](https://www.emhandbooks.wisconsin.gov/fsh/policy_files/1/12/1.2.1.htm) — acceptable evidence and verification responsibilities.
- **S08** [DHS Wisconsin QUEST Card](https://www.dhs.wisconsin.gov/foodshare/ebt.htm) — card support and temporary-card route.
- **S09** [DHS MyACCESS](https://www.dhs.wisconsin.gov/forwardhealth/myaccess.htm) — official document upload and status features.
- **S10** [DHS Renewals](https://www.dhs.wisconsin.gov/foodshare/renewals.htm) — renewal steps and late completion.
- **S11** [DHS Six Month Reporting](https://www.dhs.wisconsin.gov/foodshare/smrf.htm) — report and evidence timing; check older population descriptions against S16.
- **S12** [FoodShare Handbook change reporting](https://www.emhandbooks.wisconsin.gov/fsh/policy_files/6/61/6.1.1.htm) — between-review reporting rules.
- **S13** [DHS Work Requirement](https://www.dhs.wisconsin.gov/foodshare/work.htm) — current public overview, exemptions, good cause and restarting benefits.
- **S14** [FoodShare Handbook fair hearings](https://www.emhandbooks.wisconsin.gov/fsh/policy_files/6/64/6.4.1.htm) — hearing rights and timing.
- **S15** [DHS Operations Memo 26 04](https://www.dhs.wisconsin.gov/dms/memos/ops/dms-ops-2026-04.pdf) — February 6, 2026 memo, effective March 1; staged work-rule changes and self-attestation. Certification-period wording must be checked against S16.
- **S16** [DHS Operations Memo 26 28](https://www.dhs.wisconsin.gov/dms/memos/ops/dms-ops-2026-28.pdf) — July 31, 2026 memo, effective August 8; certification-period changes for affected adults aged 60 through 64.
- **S17** [FSET participation requirements](https://www.emhandbooks.wisconsin.gov/fset/6/6.3.htm) — workfare and activity-hour distinctions.
- **S18** [FSET component activities](https://www.emhandbooks.wisconsin.gov/fset/1/1.4.htm) — activity classifications and program structure.
- **S19** [Official Notice of Proof Needed sample](https://www.dhs.wisconsin.gov/dms/memos/ops/mds-ops-2019-j7attachment3.pdf) — historical ten-page fixture with placeholder details.
- **S20** [Official work information letter sample](https://www.dhs.wisconsin.gov/foodshare/workinfo-letter.pdf) — historical twelve-page fixture with person-specific statuses and obsolete policy text.
- **S21** [Time limited benefits warning sample](https://www.dhs.wisconsin.gov/foodshare/3tlb-warning-letter-sample.pdf) — historical sample for additional layout research.
- **S22** [DEAR renewal sample](https://www.dhs.wisconsin.gov/foodshare/dear-renewal.pdf) — specialized sample; not a universal renewal flow.
- **S23** [Hunger Task Force Emergency Food](https://www.hungertaskforce.org/get-help/emergency-food/) — food-site map, emergency referral and resource types.
- **S24** [DHS Milwaukee Enrollment Services](https://www.dhs.wisconsin.gov/dms/miles.htm) — current agency contacts, locations, hours and language services.
- **S25** [Hunger Task Force FoodShare Resources](https://www.hungertaskforce.org/get-help/foodshare-resources/) — advocate assistance and resource-center contacts.
- **S26** [DHS FSET](https://www.dhs.wisconsin.gov/fset/index.htm) — program information and assistance route.
- **S27** [Strands examples](https://strandsagents.com/docs/examples/) — workflow, knowledge retrieval, multimodal and deployment examples.
- **S28** [Strands structured output](https://strandsagents.com/docs/examples/structured_output/) — typed output for application rendering.
- **S29** [Strands interrupts](https://github.com/strands-agents/harness-sdk/blob/main/site/src/content/docs/user-guide/concepts/interrupts.mdx) — pausing and resuming for resident input.
- **S30** [Strands custom tools](https://github.com/strands-agents/harness-sdk/blob/main/site/src/content/docs/user-guide/concepts/tools/custom-tools.mdx) — implementation of bounded application tools.
- **S31** [DHS Food Support Resources](https://www.dhs.wisconsin.gov/foodshare/resources.htm) — local food and 211 routes.
- **S32** [DHS News for Members](https://www.dhs.wisconsin.gov/foodshare/news.htm) — monitoring starting point for member-facing updates.
- **S33** [FoodShare Handbook six month reporting](https://www.emhandbooks.wisconsin.gov/fsh/policy_files/6/61/6.1.2.htm) — detailed report-processing and reopening policy for follow-up research.

- **S34** [Amazon Transcribe streaming API](https://docs.aws.amazon.com/transcribe/latest/APIReference/API_streaming_StartStreamTranscription.html) — streaming and language configuration; validate compatible options during implementation.
- **S35** [Deepgram multilingual code-switching](https://developers.deepgram.com/docs/multilingual-code-switching) — mixed-language transcription capabilities by model.
- **S36** [Deepgram keyterm prompting](https://developers.deepgram.com/docs/keyterm) — recognition support for domain terms and local names.
- **S37** [Amazon Polly overview](https://docs.aws.amazon.com/polly/latest/dg/what-is.html) — text-to-speech service.
- **S38** [Amazon Transcribe FAQ](https://aws.amazon.com/transcribe/faqs/) — privacy, retention and model-improvement opt-out considerations.
- **S39** [Deepgram Model Improvement Partnership Program](https://developers.deepgram.com/docs/the-deepgram-model-improvement-partnership-program) — request opt-out and associated handling.

## 15 Glossary

- **ACCESS** — Wisconsin's official website for applying for and managing benefits.
- **MyACCESS** — The state's companion mobile application; residents can use it even though FoodShare Bridge itself is a website.
- **FoodShare** — Wisconsin's name for the Supplemental Nutrition Assistance Program, or SNAP.
- **QUEST** — The card used to access FoodShare benefits.
- **MilES** — Milwaukee Enrollment Services, the official case-management agency for Milwaukee County.
- **FSET** — FoodShare Employment and Training.
- **SMRF** — Six-Month Report Form, an interim reporting task required for some households.
- **Certification period** — The period of approved benefits before a required renewal, subject to program rules and changes.
- **Verification** — Evidence or an acceptable third-party contact used to confirm information.
- **Exemption** — A reason a particular requirement may not apply; the agency determines its application to the case.
- **Good cause** — Circumstances that may excuse failure to meet a requirement, subject to agency review.
- **ABAWD** — The policy term able-bodied adult without dependents; its program definition should not be inferred from everyday meanings.
- **Workfare** — A specific program arrangement with distinct participation rules, not a synonym for any volunteering.
- **Structured output** — Agent results returned in an application-defined data format; valid format does not establish factual accuracy.
