# FoodShare Bridge 211 Integration Plan

Using the National Data Platform V2 APIs for food and nearby help

September 8, 2026 | Version 1.0 | Integration addendum to PRD 1.5

## 1 Confirmed access and the decision

The project owner confirms access to the 211 API and supplied the portal descriptions for Search V2, Query V2, Suggest V2, and Export V2. This replaces the earlier assumption that obtaining developer access was still a prerequisite. We have not yet exercised the account or inspected its operation schemas, product entitlements, Wisconsin data coverage, quotas, or reuse terms.

Use **Search V2 plus Query V2 as the first live directory integration** for FoodShare Bridge. Add Suggest V2 when it improves the interface. Consider Export V2 for a maintained local directory after confirming storage and redistribution rights. The supplied catalog labels the V1 products deprecated; do not start a new integration on V1.

211 supplies community resource information. Wisconsin DHS remains the source for official FoodShare policy and case contact routes. API access does not provide ACCESS case information, pantry inventory, appointment booking, or automatic navigator acceptance.

This is a proposed integration design, not a claim that any endpoint has been called successfully. The product descriptions below come from the catalog supplied by the project owner. Public portal retrieval exposed only the page shell, and Context7 returned no relevant 211 documentation. Exact HTTP operations, parameters, authentication headers, and response properties must come from the account's documentation or an OpenAPI definition before implementation.

## 2 How each API helps a resident

| API product | Description supplied by the owner | Recommended FoodShare Bridge use |
| --- | --- | --- |
| [Search V2](https://apiportal.211.org/api-details#api=SearchV2) | Searches service-at-location records and returns values for filtering | Find candidate food pantries, meal sites, and other local help using documented geographic and service filters |
| [Query V2](https://apiportal.211.org/api-details#api=QueryV2) | Returns service, location, and service-at-location details | Read the details of shortlisted results before recommending a visit; request linked records where the schema requires them |
| [Suggest V2](https://apiportal.211.org/api-details#api=SuggestV2) | Suggests taxonomy terms, locations, services, and organizations from at least four characters | Optional type-ahead for a search box; help residents find the terminology the directory recognizes |
| [Export V2](https://apiportal.211.org/api-details#api=ExportV2) | Moves bulk resource data from the National Data Platform to an external application | Optional background import for a local directory, quality review, and shared resource updates |

These are API product names and documentation links, not callable HTTP endpoint paths. Do not copy parameters from the deprecated export product into V2 without checking the V2 specification.

The initial situation picker does not need type-ahead. A structured choice such as “Food today” can map to reviewed search terms or taxonomy identifiers. Obtain real taxonomy identifiers from supported documentation or responses; do not have the model invent codes.

## 3 How Strands and AgentCore use the data

The planned request flow is:

1. The resident enters minimal food and travel constraints on the website.
2. FastAPI validates the request and invokes the Strands application on AgentCore Runtime.
3. Strands calls our bounded resource lookup tool with an area and a service need.
4. Our backend 211 adapter calls Search V2 using the configured account and permitted filters.
5. The adapter retrieves relevant details through Query V2, normalizes the records, and preserves missing fields.
6. Application validators check dates, service restrictions, cost, travel assumptions, and freshness. Incomplete records remain conditional candidates, rather than confirmed visits.
7. Strands proposes a seven-day plan from usable evidence, with alternatives and visible gaps.
8. The backend validates the proposal again and sends structured results to the website.

**Strands chooses and explains useful actions. The adapter retrieves records. Ordinary code checks whether the proposed actions are supported.** AgentCore hosts the Strands application; it does not automatically connect or authorize the 211 products.

Recommended credential boundary: keep the 211 credential in the backend service's secret configuration and grant access only to the adapter's workload. The AgentCore tool calls that backend through an authenticated, constrained internal interface. The browser and model receive neither the key nor an unrestricted API proxy. This is a project design choice; the exact internal transport will be specified during implementation.

Do not send a resident's notice, name, case details, voice transcript, or entire conversation to the directory search. Derive only the minimum search intent and geography required by the documented operation. Avoid including sensitive details in free-text search or telemetry.

## 4 Tools we will build

These are proposed FoodShare Bridge tools, not tools that 211 or Strands supplies automatically. Tool arguments and output schemas must be validated by the application.

| Internal tool or service | Inputs we intend to support | Output and limits |
| --- | --- | --- |
| `find_food_resources` | Area, requested date range, food-service category, bounded result limit | Normalized candidates from Search V2 and selected Query V2 details; service restrictions and unknown fields remain explicit |
| `get_resource_details` | An opaque resource reference returned by our search | Current permitted details and provenance; validate reference type and account scope before retrieval |
| `check_food_constraints` | Candidate records and confirmed resident constraints | Supported, conditional, or unsuitable options with reasons; does not determine public-benefit eligibility |
| `resolve_help_route` | Help category and confirmed jurisdiction | Directory candidates plus maintained official routes; an organization listing is not a verified referral partner |
| Suggestion service | Search text of at least four characters, if supported by the actual operation | Bounded suggestions; debounce and cancel obsolete requests; normal form entry remains available |
| Export import job | Server-configured permitted dataset scope | Staged records and a change report for review; runs separately from resident requests |

Do not give the model a tool that accepts an arbitrary URL, credential, export scope, or unrestricted query body. The adapter owns provider URLs, supported filters, pagination limits, and response size limits.

## 5 The record mapping we need

Start with this target schema, then map each field to the actual API response. These are our desired fields, not a claim that 211 returns all of them.

| Information needed | Handling rule |
| --- | --- |
| Organization, service, location, and service-at-location identifiers | Preserve typed source IDs and relationships; do not collapse different services at one address |
| Data owner and permitted source scope | Preserve provenance and enforce the account's authorized access |
| Service name, category, and description | Map taxonomy through a reviewed vocabulary; treat descriptions as data, never agent instructions |
| Address or service delivery area | Distinguish a physical location from the area it serves, virtual service, or mobile service |
| Schedule, dated events, exceptions, and timezone | Retain original values; only normalize dates and hours with sufficient evidence; use unknown when incomplete |
| Cost and access rules | Distinguish free meals, paid markets, appointment requirements, documents, and visit limits |
| Contact and provider URL | Preserve approved attribution and verify usable contact routes |
| Languages and accessibility | Report only documented capabilities; no inference from neighborhood or organization name |
| Source update time | Record it only if supplied and understood; it may describe a record edit rather than verified hours |
| Retrieval time and local review time | Store separately; fetching a record today does not prove the provider verified it today |
| Missing fields and evidence status | Keep explicit gaps; show “call to confirm” when relevant instead of inventing certainty |

If the same service appears in 211 and HTF data, match cautiously using identifiers and reviewed evidence. Do not deduplicate solely by organization name or address. A provider may operate different programs with different schedules and rules.

## 6 What changes in the seven day plan

For an illustrative household needing food today, Search V2 might return nearby candidates. Query V2 supplies whatever details are available for the selected records. The plan can then distinguish:

- A listed meal service whose documented schedule and restrictions fit the resident's request.
- A pantry that might help later in the week but requires a call because its hours or access requirements are uncertain.
- A paid option that fits only if the resident confirms enough available money.
- An unmet need when no supported option is feasible.

These are examples of how we will process results, not actual API results or claims about particular organizations. A pantry listing cannot establish the amount or type of food a household will receive. Meal suggestions must still use known food on hand or clearly conditional ingredients.

### Addition to the food planning prompt

```text
Use find_food_resources to obtain directory candidates and the detail evidence
returned by our adapter. A search result or rank is not proof that a service
is open, suitable, or stocked. Use the returned resource references; do not
invent provider IDs, taxonomy codes, schedules, restrictions, or contact data.

Check candidates against the resident's constraints and the requested dates.
Preserve missing fields and distinguish conditional options from supported
visits. Show sources and the available freshness information accurately.

If a detail lookup fails, explain that limitation. If the directory is
unavailable, use only an authorized, still-valid fallback or a maintained
help route. Never interpret an API outage as proof that no services exist.

A resource listing is not a booking, food reservation, referral acceptance,
or eligibility decision. Do not claim food coverage from unknown stock.
```

## 7 Live search first and export later

Start by proving Search V2 and Query V2 against a small Milwaukee evaluation set. This establishes the actual schemas, identifiers, available filters, and record completeness before building an import pipeline. Live retrieval still requires source freshness checks and any applicable permission to display returned data.

Export V2 becomes useful if the permitted scope and storage terms support a local directory. Schedule it as a background job, stage the result, and compare it with the last accepted dataset. Determine whether V2 supports full snapshots, incremental changes, deletions, and resumable pagination before designing synchronization. Do not assume these capabilities from the V1 description.

A missing record in one failed or partial import is not evidence that a provider closed. An accepted material change should update the shared resource version and trigger rechecks of affected future plan actions. Keep the existing review process for conflicting schedules and closure reports.

For the community demo, a reviewed resource update can revise two isolated synthetic household plans. Do not claim that 211 provides push notifications or real-time closure events unless its documented account capabilities establish that.

## 8 Verification before implementation depends on the API

The next useful artifacts are the V2 OpenAPI definitions or operation documentation, a sanitized Search V2 response, a linked Query V2 response, and the account's usage terms. Share no API keys in chat or source control; configure them through the application's secret mechanism when integration work begins.

| Verify | Why it affects the build |
| --- | --- |
| Enabled products, authentication method, and data authorization requirements | General portal access may differ from permission to call each product or dataset |
| Wisconsin and Milwaukee owners and coverage | National platform access does not by itself establish local completeness |
| Exact operations, response schemas, filter syntax, and identifier relationships | Needed to implement and test a correct adapter without guessing |
| Taxonomy and geography behavior | Needed for useful searches; distance and service-area eligibility are different |
| Rate limits, pagination, result caps, timeouts, and retry guidance | Needed for predictable latency and controlled upstream use |
| Attribution, display, retention, caching, export, and redistribution terms | Determines which records may be shown, stored, and included in public demo assets |
| Meaning of update timestamps and known data refresh process | Determines which freshness claims the website may make |
| Export deletion and incremental-update semantics | Prevents corrupting the local directory or falsely reporting closures |

Acceptance checks for the first adapter ticket:

1. One authorized Search V2 call returns permitted local results, and a linked Query V2 request resolves the intended record.
2. Actual records map to the internal schema without silently filling unknown fields.
3. Empty results, denied access, rate limiting, provider outage, malformed payloads, and missing details produce distinct, truthful states.
4. Pagination and detail calls are bounded; obsolete UI suggestions cannot replace newer input.
5. Credentials and sensitive resident text never appear in browser responses, model context, test fixtures, or logs.
6. Fixed synthetic or permitted sanitized fixtures cover schedule uncertainty, duplicate services, paid options, service boundaries, and a conflicting closure.
7. Record-derived instructions cannot change the tool permissions or prompt policy.
8. A real integration check is reported separately from tests that use fixtures, with sanitized evidence and the tested account scope.

Do not publish raw 211 payloads in the hackathon's public repository unless the applicable terms allow it. Synthetic schema-compatible fixtures can demonstrate the contract while the deployed integration uses authorized data.

## 9 Updated prompt for the Matt Pocock workflow

Use this in the next bounded research session before creating the adapter specification. It replaces the question of whether the owner has any 211 access.

```text
Use Matt Pocock's research skill to prepare the 211 V2 adapter for
FoodShare Bridge. The project owner has confirmed API access.

Read docs/FoodShare-Bridge-211-Integration-Plan.md and the existing API guide.
Inspect the available account documentation or supplied OpenAPI definitions.
Prioritize Search V2 and Query V2. Do not use deprecated V1 products.

Document exact operations, authentication configuration without secrets,
taxonomy and geography filters, identifier relationships, pagination,
response fields, limits, attribution, and permitted storage. Identify which
products and Wisconsin datasets the account actually authorizes.

Produce a source-linked field mapping and a short implementation-readiness
report. Label missing documentation as unresolved; invent no endpoint paths
or response properties. Use at most one research subagent and no further
delegation. Do not bulk export records or contact providers in this task.
```

Then use `grill-with-docs` for remaining design decisions, `to-spec` for the adapter contract and failure behavior, `to-tickets` for bounded end-to-end work, and `implement` for one agreed ticket. The first live food journey should now exercise this integration once its documented contract and permissions are established.
