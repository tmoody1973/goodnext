# FoodShare Bridge Full Technology Stack

Recommended implementation baseline for the responsive website

September 8, 2026 | Version 1.2 | Companion to PRD version 1.5

## 1 Stack decision

Use an AWS-centered architecture: Next.js and TypeScript for the website, Python and FastAPI for application services, Strands for agent execution, Claude Sonnet 4.6 through Amazon Bedrock, DynamoDB for structured records and S3 for files. Deploy the website through CloudFront, FastAPI on ECS Fargate and Strands on Amazon Bedrock AgentCore Runtime. Use AWS speech and messaging services behind replaceable adapters.

This is the build baseline, replacing the earlier documents' unspecified technology choices. It is not a claim that services are deployed, accounts are configured or vendors have passed evaluation. Strands and the event's account requirements remain the hackathon obligations in PRD Section 13; the other technologies are project choices. AgentCore Runtime is now explicitly selected by the user and required for this project, although optional under the event rules. Existing privacy, consent, synthetic-document and pilot gates still apply.

Select patched versions and commit lockfiles at implementation kickoff. The version families below guide compatibility, not a claim that a particular patch is the newest or has been security-audited. Record the actual tested SDK, model identifier, region, package versions and container digests in the release manifest.

## 2 Website and UX

| Layer | Recommended choice | Responsibility |
| --- | --- | --- |
| Web framework | Next.js 16 App Router and React 19 with TypeScript | Responsive resident screens and restricted review interface |
| Rendering | Static export with interactive client components | Prebuilt screen shells; fetch private data from the Python API at runtime |
| Styling | Tailwind CSS 4 and project CSS design tokens | Responsive layout, typography, contrast, focus and reusable UI patterns |
| UX process | Impeccable skill | Shape flows, document design decisions, critique, adapt, harden and audit |
| Forms and UI state | Semantic HTML forms, React state and a typed fetch client | Structured input, correction, loading and recoverable errors; server remains authoritative |
| Localization | Reviewed English and Spanish JSON catalogs plus browser Intl | Stable UI copy and date/number formatting; reviewed policy glossary for model text |
| Voice controls | Browser microphone APIs and explicit playback controls | Opt-in recording, transcript correction, stop/cancel and text fallback |
| Client quality | ESLint, TypeScript checks, Vitest and React Testing Library | Component behavior, forms and locale consistency |
| Journey checks | Playwright and axe-core plus manual assistive-technology review | Mobile/desktop journeys, keyboard use, contrast and screen-reader behavior |

Static export avoids needing a Node server in production. Dynamic API endpoints, sessions and consent belong in FastAPI. Do not implement this plan using Next.js Server Actions, request-time server rendering or dynamic route handlers: those require a different hosting choice. Use prebuilt screen routes and load the authorized plan from the API; do not put private notice text or access tokens into URLs. Configure static route resolution at the CDN and verify direct navigation as well as in-app links. [Next.js static exports](https://nextjs.org/docs/app/guides/static-exports).

Use self-hosted fonts and icons where needed. Keep resident documents and plan responses out of static builds, analytics and service-worker caches. No native app or offline private-document storage is required. Impeccable remains development tooling, not a service receiving resident data.

## 3 Backend and agent

| Layer | Recommended choice | Responsibility |
| --- | --- | --- |
| Language and runtime | Python 3.12 with uv and a committed lockfile | Shared API, tool, worker and validation modules |
| API server | FastAPI with Uvicorn | Session-bound endpoints, consent previews, job status and speech gateway |
| Validation and contracts | Pydantic 2 and generated OpenAPI contract | Typed requests, tool results and workflow proposals; generate frontend types from the contract |
| Agent framework | Strands Agents Python SDK | P01 through P08 prompt configurations, scoped tools and structured proposals |
| Agent host | Amazon Bedrock AgentCore Runtime and its Python SDK | Deploy and invoke the Strands application; separate resident and maintenance runtime configurations |
| Model | Anthropic Claude Sonnet 4.6 through Amazon Bedrock | Evidence-based interpretation, explanations and plan proposals |
| AWS access | Boto3 and workload IAM roles | Bedrock, DynamoDB, S3, Textract, speech and queue access without embedded AWS keys |
| Resource API adapter | HTTPX with Pydantic response validation | 211 Search V2 and Query V2 behind bounded backend tools; account access confirmed by owner, schemas and local scope still to verify |
| Source ingestion | HTTPX, Beautiful Soup and pypdf | Allowlisted public pages and PDFs into staged versioned records; optional 211 Export V2 import only under verified account terms |
| Packet generation | ReportLab and pypdf | Index and cover pages, preserved original attachments and private exports |
| Backend testing | pytest and Hypothesis | Policy/date fixtures, hours arithmetic, resource constraints, authorization and idempotency |

FastAPI supplies an OpenAPI-oriented interface with Pydantic integration. The application still needs explicit permission and business-rule checks. [FastAPI features](https://fastapi.tiangolo.com/features/).

The [211 V2 Integration Plan](FoodShare-Bridge-211-Integration-Plan.md) selects Search V2 for discovery and Query V2 for details. Keep the 211 secret in the backend adapter's secret configuration. AgentCore tools use an authenticated bounded backend interface; neither the browser nor the model receives the secret. Suggest V2 is optional UI support, and Export V2 belongs in a separate import job when permitted. Exact provider operations and schemas remain to be verified; no V1 compatibility layer is planned.

Select the Bedrock model identifier explicitly; do not rely on SDK defaults. The official documentation lists Claude Sonnet 4.6 and Strands provides a Bedrock adapter. Start with a US deployment region, proposed us-east-1, subject to account access and feature availability. Verify the chosen in-region endpoint or US inference profile and its data-routing implications; do not silently substitute a global profile. Model access, quotas, tool use, structured output, cost and English/Spanish quality must pass the fixture evaluation before release. [Bedrock Sonnet 4.6](https://docs.aws.amazon.com/en_en/bedrock/latest/userguide/model-card-anthropic-claude-sonnet-4-6.html), [Strands Bedrock provider](https://strandsagents.com/docs/user-guide/concepts/model-providers/amazon-bedrock/).

FastAPI invokes Strands on AgentCore Runtime through an IAM-authenticated server call. The backend binds the anonymous resident session to a runtime session and supplies only the permitted workflow context. Long operations use a durable application job record. Deterministic validators run in the backend after agent output and before display or execution. Public-source maintenance analysis runs in a separate AgentCore runtime configuration and role without resident-file or messaging permissions. Non-agent extraction and packet jobs may still run in ordinary workers.

## 4 Data storage and identity

| Layer | Recommended choice | Responsibility |
| --- | --- | --- |
| Structured database | Amazon DynamoDB on-demand capacity | Versioned policy/resources, plan metadata, sessions, approvals, jobs and operation receipts |
| Public evidence files | Separate private S3 bucket with versioning | Source snapshots and reviewed fixture assets; publication controlled by reviewers |
| Resident documents | Separate private S3 bucket with SSE-KMS | Authorized temporary uploads and exports, excluded from public CDN distribution |
| Encryption and secrets | AWS KMS and Secrets Manager | Encryption keys and any third-party API credentials |
| Anonymous resident identity | Opaque server-generated session with Secure HttpOnly SameSite cookie | No account for food planning; server checks ownership, expiration and CSRF protections |
| Reviewer identity | Amazon Cognito user pool with MFA and server-enforced roles | Restricted publication and resource-review functions |
| Retrieval | DynamoDB indexes and bounded retrieval of approved passages | Topic, jurisdiction, geography, effective-date and publication filters |

Keep public records and private household records in separate tables or tightly separated access domains with distinct IAM permissions. Record version IDs and use conditional updates for plan revisions and operation claims. Index food services by supported geography and service period; resolve irregular service areas and exceptions in code. Prototype coverage is small enough to avoid a vector database. Introduce embeddings only if measured retrieval failures justify the additional index and evaluation work.

Do not equate database TTL with immediate deletion. DynamoDB's documentation describes eventual expiry deletion, typically within days. Enforce expiration on every read, revoke access immediately at session end, and run explicit deletion jobs for private objects and derived artifacts according to the retention policy. Configure backups, object versions and log retention consistently with that policy. [DynamoDB TTL](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html).

Cognito is for reviewers in the baseline. Resident cross-device recovery and accounts remain a later scoped feature; a phone number used for reminders is not automatically a login identity. Private download URLs must be short-lived and generated only after ownership checks.

## 5 Speech documents and delivery

| Capability | Recommended choice | Activation condition |
| --- | --- | --- |
| Speech to text | Amazon Transcribe streaming | Supported language mode and representative correction/privacy tests pass |
| Read aloud | Amazon Polly | Supported voice and locale; approved displayed text with stop and replay controls |
| Alternate speech adapter | Deepgram Nova-3 evaluation option | Use only if the mixed-language evaluation justifies replacing Transcribe |
| Notice OCR | Amazon Textract | Synthetic demo fixtures first; actual uploads require the pilot processing controls |
| Reminder scheduling | Amazon EventBridge Scheduler | Approved destination, plan version, local timezone and cancellation logic |
| Queued work | Amazon SQS with dead-letter queues | Durable jobs with retry limits, idempotency and status reconciliation |
| Short delivery worker | AWS Lambda | Recheck consent and current task before attempting a send |
| SMS | AWS End User Messaging SMS | Authorized origination identity, registration/production access as applicable, verified test destination and opt-out handling |
| Longer processing | ECS Fargate worker using the shared Python image | Durable job record, restricted role and safe restart handling |

Transcribe and Polly are the preferred adapters for this AWS baseline; Deepgram is an evaluated replacement, not a second default provider. Streaming language identification and redaction cannot be assumed to work together. Retain the processing disclosure, minimal retention and critical-field confirmation requirements from the APIs and Prompts guide. A provider change must rerun speech tests and update the privacy description.

EventBridge Scheduler triggers durable work; the agent itself is not a reminder clock. The delivery worker reloads consent, task state and plan version before using the SMS service. Provider acceptance is distinct from delivery. Incoming opt-out events must update application consent as well as provider suppression. Store receipt events and reconcile ambiguous sends. [EventBridge Scheduler](https://docs.aws.amazon.com/scheduler/latest/UserGuide/what-is-scheduler.html), [AWS End User Messaging SMS](https://docs.aws.amazon.com/sms-voice/latest/userguide/what-is-sms-mms.html).

No live booking, pantry inventory, grocery-pricing or ACCESS integration is assumed. Use the reviewed directory and official outbound links. A map or routing API is not required for the first release; provide destination links and mark unverified travel estimates unknown. Implement navigator delivery only after the named partner's authorized channel is known.

## 6 Hosting networking and operations

| Layer | Recommended choice | Responsibility |
| --- | --- | --- |
| Static hosting | Private S3 website-assets bucket and Amazon CloudFront | Serve exported Next.js assets through origin access control |
| Application hosting | Amazon ECS Fargate with Application Load Balancer | FastAPI and speech gateway; agent execution is hosted separately |
| Agent hosting | Amazon Bedrock AgentCore Runtime | Managed execution of the resident and separately permissioned maintenance Strands applications |
| Container registry | Amazon ECR | Versioned API and worker images with recorded digests |
| Domain and certificates | Route 53 and AWS Certificate Manager | Domain resolution and TLS; domain purchase is not authorized by this document |
| Edge protection | AWS WAF plus application rate limits | Abuse controls and request-size limits without relying on IP as household identity |
| Infrastructure definition | AWS CDK in TypeScript and CloudFormation | Repeatable deployment with separate environment parameters |
| Continuous integration | GitHub Actions with AWS OIDC federation | Tests, dependency checks, builds and narrowly scoped deployment permissions |
| Monitoring | CloudWatch logs, metrics and alarms; sanitized OpenTelemetry traces | Errors, latency, tool failures and cost visibility without raw resident content |
| Spend controls | AWS Budgets, service quotas and application usage ceilings | Alerts plus enforced model-call, retry, file-size and concurrency limits |
| Local development | Node LTS supported by Next.js, npm lockfile, Python uv, Docker Compose and DynamoDB Local | Repeatable setup, synthetic fixtures and mocked external delivery |

CloudFront serves static content from the S3 REST origin using origin access control, not a publicly readable website bucket. Route /api and the speech streaming path to the load balancer; disable caching there, forward required cookies and headers, and set private responses to no-store. Verify streaming, cancellation, timeouts and cookie behavior end to end. The backend issues the session cookie under the website origin. Restrict direct origin access and allow container ingress only from the load balancer. [CloudFront S3 access control](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html), [ECS load balancing](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-load-balancing.html).

Place backend workloads in a VPC with a deliberate outbound network path. Budget for load balancers, egress, NAT or private endpoints, logs, and continuously running tasks as well as model tokens. AWS budget alerts are not hard spending caps. Keep demo and live resident environments separate; use synthetic fixtures in CI, screenshots and recordings.

The request path is browser to CloudFront to FastAPI on Fargate to AgentCore Runtime running Strands, then Bedrock and authorized data tools. Validated results return through FastAPI. Scheduled reminders follow Scheduler to SQS to Lambda to the SMS provider. Policy/resource maintenance follows a separate queue, AgentCore runtime configuration and review process; resident identity is never attached to provider directory queries.

## 7 How AgentCore works with Strands

Strands defines how our agent works with its model and tools. AgentCore Runtime is where that code runs when a resident uses the website. Claude, accessed through Bedrock, interprets the request and generates proposals; our tools provide reviewed evidence and calculations. FastAPI controls permissions and validates the result. Read the [plain-English walkthrough](FoodShare-Bridge-AgentCore-Explained.md) for Maria's full request flow. [Strands AgentCore deployment](https://strandsagents.com/docs/user-guide/deploy/deploy_to_bedrock_agentcore/python/).

Package the Strands application with the AgentCore Python entrypoint and deploy it to a versioned runtime endpoint. FastAPI uses its IAM role to invoke that endpoint; AWS credentials never reach the browser. The runtime role gets only the required model and tool-service permissions. Bind household scope in server-owned context, and have tool services validate that scope independently. A shared runtime role does not itself provide per-household database authorization.

Treat runtime state as temporary. Keep plan versions, jobs, consent and delivery receipts in application storage. On restart or session expiry, reload only records still permitted by the retention policy and reconcile operations before retrying. Configure explicit request limits, deployed versions, network access and telemetry redaction. Test concurrent households, maintenance isolation, cancellation, timeouts and restart recovery before rollout. [AgentCore runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-how-it-works.html).

The baseline does not require AgentCore Memory, a vector database, Redis, Kubernetes, a swarm, a paid map integration, a second model provider or a second speech provider. These additions need a specific measured need. The first data integrations remain curated DHS and food-resource records with provenance; a larger cloud stack cannot substitute for accurate data.

## 8 Repository and release handoff

Proposed repository layout: apps/web for Next.js; services/api for FastAPI; services/workers for background processing; packages/agent for Strands tools, prompts and schemas; data/fixtures for synthetic cases and reviewed public examples; infra for CDK; tests for cross-service fixtures; docs for research, PRD and implementation decisions. These are planned directories, not files created by this document.

Before deployment, pin dependencies and container digests; test model and regional access; run the notice, food, consent and language fixtures; exercise worker restart and duplicate delivery; inspect the Impeccable mobile/desktop designs; test judge access and rollback; and record actual costs from representative runs. Publish setup instructions and an environment-variable example with placeholder values only. GitHub CI must not expose account secrets or resident files in public build logs.

The current architecture diagram remains a proposed logical view. The AgentCore walkthrough supplies the updated deployment flow. Update the interactive diagram's deployment labels during implementation; the submission diagram must show Strands executing on AgentCore and describe the delivered system accurately.
