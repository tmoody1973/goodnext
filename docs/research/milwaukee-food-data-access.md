# Milwaukee Food Data Access — Research Findings

Research date: September 8, 2026 | Time-boxed research task, public web sources only

## One-paragraph answer

No source found today gives FoodShare Bridge a public, self-serve feed of Milwaukee food resources with structured opening windows and service restrictions. The 211 National Data Platform (Search V2 / Query V2) is the most promising candidate because the owner already has account access, but its actual response fields, Wisconsin coverage, and reuse terms sit entirely behind login — nothing about them is publicly visible on the API portal, so every field in the integration plan's target schema remains unconfirmed until someone signs in and inspects the account. Hunger Task Force publishes a curated, human-reviewed interactive map (opening days/times, program type) for Milwaukee County but offers no API or download. Feeding America Eastern Wisconsin has a pantry locator with no visible data terms. No Milwaukee or Milwaukee County open-data portal listing, and no Wisconsin DHS page, currently offers a food-pantry-with-hours dataset — DHS's "FoodShare: Wisconsin Data" page is caseload statistics, not a resource directory. Until the 211 account is inspected, the most dependable near-term source of real opening-hours and restriction data is Hunger Task Force's map, read manually or by future permission-gated scraping, not an API.

## Source table

| # | Source | Owner | Access type | Public fields confirmed | Terms confirmed |
|---|--------|-------|-------------|--------------------------|------------------|
| 1 | National Data Platform Search V2 / Query V2 / Suggest V2 / Export V2 | United Way Worldwide (UWW), data owned by local 211s | Documented, partner-only (account required) | None — portal shell only | Local 211 retains data ownership; no cost for internal use; 5% revenue share if monetized; redistribution/attribution/caching terms not found |
| 2 | Hunger Task Force emergency food map | Hunger Task Force | Public webpage (interactive map, no API) | Days/times, program type, location | None stated |
| 3 | Hunger Task Force Mobile Market | Hunger Task Force | Public webpage, no published schedule | Route runs Mon–Fri; no schedule table on page | None stated |
| 4 | Feeding America Eastern Wisconsin pantry locator | Feeding America Eastern WI | Public webpage (search widget) | ZIP/radius/category search only; per-site fields not visible in page shell | None stated |
| 5 | IMPACT 211 / IMPACT Connect | IMPACT, Inc. | Public info page; IMPACT Connect is partner-only | ~1,500 agencies / 4,800 services (aggregate stat only) | Not found |
| 6 | City of Milwaukee Open Data Portal | City of Milwaukee | Public, downloadable | No food/pantry dataset found | General portal terms allow reuse |
| 7 | Milwaukee County Open Data Portal | Milwaukee County | Public, downloadable | Search did not surface a food dataset (inconclusive — see below) | General portal terms allow reuse |
| 8 | Wisconsin DHS FoodShare Data page | Wisconsin DHS | Public, downloadable | Caseload/benefit statistics only, no resource list | N/A |
| 9 | Wisconsin DPI Summer Meals Site Finder | WI DPI, powered by USDA fns.usda.gov/meals4kids | Public map | Site listing during summer only; fields not itemized on the WI page | Not stated on WI page; likely USDA's |

## Per-source detail

**1. 211 National Data Platform (Search V2, Query V2, Suggest V2, Export V2)**
apiportal.211.org is a Microsoft Azure API Management developer portal. The unauthenticated page is only navigation chrome — no product descriptions, response schemas, or terms render without registering and subscribing. register.211.org's FAQ confirms: individual 211 agencies keep ownership of their data; United Way Worldwide cannot sell it; there is no cost to use the platform internally; a 5% revenue-share fee applies only if the data is monetized; and external partner access requires an "API Request Form" that creates a scoped product subscription. A 2016 platform overview PDF (register.211.org/files/211 NDP Snapshot.pdf) confirms the same ownership/control model but predates V2 and says nothing about V2's actual fields. One web search summarized a claim that the platform uses a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 license; the primary FAQ page fetched directly does **not** contain that language, so this is unconfirmed and possibly wrong — do not rely on it. Wisconsin/Milwaukee coverage is not mentioned anywhere public. **Everything the integration plan needs — opening hours field, service-area field, eligibility, cost, languages, last-updated, attribution/display/caching/redistribution terms, rate limits — is unverified and requires signing into the account.**

**2. Hunger Task Force — Emergency Food map**
hungertaskforce.org/get-help/emergency-food/ hosts "an interactive map" the page describes as listing "public senior Stockbox sites, school meal sites and emergency food sites in Milwaukee County." Clicking a site shows "days and times of service, type of program." The organization states it has "created a list of confirmed, trusted sites" — meaning the listings are human-curated, which fits the project's "verified" vocabulary well. No API, CSV, embed code, or reuse terms were found. Fields shown per site: opening window (days/times) and program type; no explicit service-area, cost, or language fields were described.

**3. Hunger Task Force — Mobile Market**
hungertaskforce.org/what-we-do/mobile-market/ states routes run Monday–Friday but does not publish the schedule on the page; it directs schedule requests to a named staff contact. This is a paid/discounted grocery service, not free food — matches the plan's note to distinguish it clearly. No structured data found.

**4. Feeding America Eastern Wisconsin — Find a Pantry**
feedingamericawi.org/find-a-pantry/ is a search widget (ZIP or address, radius 1–300 miles, category: shelter/meal program/soup kitchen/pantry) covering their 35-county service area, which includes Milwaukee. The rendered page shell did not expose per-location fields (hours, eligibility, phone) or any underlying vendor/API name; a live interactive check (not done here) would be needed to see per-result data. No reuse terms found.

**5. IMPACT 211**
IMPACT, Inc. is the designated 211 provider for nine southeastern Wisconsin counties, including Milwaukee, and answers 64% of the state's 211 call volume. It separately runs IMPACT Connect (built with NowPow), a shared multi-sector directory (~1,500 agencies, 4,800 services) for partner organizations in healthcare, food, housing, and other sectors — this is partner-gated, not a public API, and there is no confirmed statement that IMPACT 211's data is the same data exposed through the National Data Platform V2 products the owner has access to. That link needs confirmation with the 211 account.

**6 & 7. Milwaukee city and county open data portals**
Both portals are real, general-purpose open-data catalogs with standard reuse terms (download as CSV/GeoJSON/etc., free to use). Searching the city portal for "food" returned only unrelated matches (property assessments, financial reports) among 186 total datasets — no confirmed absence, since only a partial browse was done. The county portal's search page did not render a results list in this pass; this is inconclusive, not a confirmed negative, and deserves a direct catalog browse rather than a query-string search.

**8. Wisconsin DHS FoodShare Data page**
dhs.wisconsin.gov/foodshare/rsdata.htm provides only program statistics (monthly caseload, benefit amounts, recipient counts, 2011–2026, downloadable by county/tribe) — useful for policy context, not a resource directory.

**9. Wisconsin DPI Summer Meals Site Finder**
A map tool for the USDA Summer Food Service Program, powered by USDA's fns.usda.gov/meals4kids infrastructure, updated weekly starting in May. Only relevant during summer months and only for child meal sites; not a year-round FoodShare-relevant source.

## Recommendations (not facts — proposed judgment calls)

- Treat the Hunger Task Force map as the nearest thing to a dependable, human-verified Milwaukee source today, but note it has no API — any use requires either manual curation into the project's own directory or a scraping/reuse conversation with Hunger Task Force first.
- Do not build against assumed 211 V2 response fields. The integration plan's target schema (Section 5) is well-designed but every field needs confirmation against the real account before an adapter is written.
- Contact IMPACT 211 directly to ask whether its data is the same data reachable through the owner's National Data Platform V2 subscription — this determines whether "211 coverage of Milwaukee" is actually confirmed or just plausible.
- Re-run the Milwaukee County open-data portal search manually (browser, not just a scripted fetch) before concluding no food dataset exists there.
- Revisit Feeding America Eastern Wisconsin's locator with an interactive browser check to see actual per-pantry fields before deciding whether it can supplement 211.

## Verify with credentials — 211 API checklist

- [ ] Which products (Search V2, Query V2, Suggest V2, Export V2) are actually enabled on the owner's subscription
- [ ] Exact response fields for opening hours, service area, eligibility, cost, languages, last-updated
- [ ] Whether Milwaukee/Wisconsin/IMPACT 211 records are included and how complete they are
- [ ] Authentication method and rate limits, pagination, result caps
- [x] Terms read 2026-09-08: data owned by local 211 centers; any production, operational, commercial, or external use needs each center's prior permission. No CC license language; the CC BY-NC-SA claim is refuted for the API terms. Excerpt in 211-samples/terms-of-use-2026-09-08.md.
- [ ] Meaning of any "last updated" timestamp — record edit vs. verified-in-person
- [ ] Export V2 semantics: full snapshot vs. incremental, deletions, resumable pagination

## URLs fetched

- https://apiportal.211.org/api-details#api=SearchV2
- https://apiportal.211.org/get-started-overview
- https://apiportal.211.org/apis
- https://register.211.org/Home/FAQs
- https://register.211.org/files/211%20NDP%20Snapshot.pdf
- https://www.hungertaskforce.org/get-help/emergency-food/
- https://www.hungertaskforce.org/what-we-do/mobile-market/
- https://www.feedingamericawi.org/find-food (404)
- https://feedingamericawi.org/find-a-pantry/
- https://data.milwaukee.gov/dataset?q=food
- https://data.milwaukee.gov/dataset
- https://data.county.milwaukee.gov/search?q=food
- https://dpi.wi.gov/community-nutrition/sfsp/find-summer-meals-site
- https://www.dhs.wisconsin.gov/foodshare/rsdata.htm
- Web searches: 211 NDP terms of use; Milwaukee County open data food pantry; IMPACT 211 southeastern Wisconsin; Wisconsin DHS summer meal sites; Feeding America Eastern Wisconsin locator


## Addendum (2026-09-08, after the report): Milwaukee Food Environment map layer

Found via a separate search Tarik ran; verified by Claude with direct read-only
requests to the public service, no login.

- **Source:** Milwaukee Food Council emergency food layer, published on ArcGIS
  Online as a public Feature Service (a queryable map data table):
  https://services5.arcgis.com/3kr3fkJcIf6EOY6g/ArcGIS/rest/services/EmergencyFood_MKE/FeatureServer
  Public viewer: https://experience.arcgis.com/experience/4883a0957d124294aa236d9e9cc696a5
- **Owner:** Milwaukee Food Council with Data You Can Use (service description
  credits the Food Council and SafeGraph).
- **Access type:** public, queryable, downloadable via the standard ArcGIS
  query endpoint. No terms text on the service; reuse permission not stated.
- **Confirmed fields:** business name, address, city, ZIP, phone, type (for
  example "Food Pantry"), notes (hours as free text, e.g. "Tuesdays 4pm - 6pm"),
  website, service area (a comma-separated ZIP list).
- **Record count:** 75. **Last edited:** 2024-08-27 per the layer's own
  metadata, so more than a year stale as of this note.
- **Useful for:** a realistic, non-synthetic fixture for evaluation and the
  closure scenario; a bootstrap list for a hand-reviewed directory.
- **Not useful for:** live opening windows or freshness claims. Hours are
  free text and over a year old; every record would be "unconfirmed" under
  our tiers.
- **Remaining uncertainty:** reuse and redistribution rights; whether the
  Food Council maintains a newer version elsewhere.

**Recommendation (not a fact):** ask Data You Can Use / Milwaukee Food Council
for reuse permission before any record from this layer appears in the public
repo or demo. Until then, use it only to sanity-check the fixture's shape.

**Item record check (2026-09-08, ArcGIS Online):** feature layer item
`EmergencyFood_MKE_2024`, owner `amanda_dycu` (Data You Can Use), access
public, license field empty, credits field empty, item modified 2025-07-09,
data last edited 2024-08-27. The viewer app "Milwaukee Food Environment Map"
has the same owner, no license, modified 2026-04-13. The layer description
says the data came from the Milwaukee Food Council and SafeGraph. SafeGraph is
a commercial data vendor whose terms normally restrict redistribution, so
some records may carry a third-party restriction the publisher cannot waive.
No license means all rights reserved by default. Conclusion: usable to look
at and to shape our own data model; not usable in the public repo or demo
until Data You Can Use grants permission in writing and confirms the SafeGraph
portion is clear.
