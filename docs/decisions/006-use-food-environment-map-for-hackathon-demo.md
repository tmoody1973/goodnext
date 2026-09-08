# 006 Use the Milwaukee Food Environment Map in the hackathon demo, with attribution, before permission arrives

**Decision** — The September 14 demo shows real Milwaukee sites from the public Milwaukee Food Environment Map (Data You Can Use / Milwaukee Food Council, data as of August 27, 2024), credited on every card and disclosed in the submission. Permission requests still go out, but the demo does not wait for them. To make that work, the freshness rule changes: a record checked more than 60 days ago is shown as "call to confirm, checked DATE" instead of being hidden; only a record with no date is unconfirmed.

**Why this came up** — Decision 005 kept the demo synthetic until 211 and the map publisher granted permission. Tarik decided the same day that a temporary hackathon project should use the public map now. Under the original 60-day rule every map record would have been hidden, so the rule had to move or the data was useless.

**Options**
- *Use the map now, credited, and loosen the 60-day rule.* Cost: a small reuse-rights risk on a public, unlicensed layer; cards show hours that are a year old, labeled as such.
- *Keep the demo synthetic and wait for permission.* Cost: a demo of made-up pantries in a product whose pitch is real help; permission may not arrive before judging.
- *Phone-verify the 9 sites in 53206 first.* Cost: an hour of calls before any real data appears; still the best upgrade and still planned.

**What we chose and why** — The first. Tarik's call, over Claude's recommendation to wait or call first. A hackathon demo is temporary, the layer is public, and every card says where the data came from and how old it is. The phone calls remain the path to "verified" records.

**Refinements made while loading the data (same day)** — Two follow-on changes, both Tarik-approved in spirit under "be pragmatic": (1) a site with no service area is shown only for the ZIP in its own address, still marked "confirm they serve your area"; the original "any ZIP" rule (D5) returned the whole county on every search once 54 real records lacked an area. (2) The model's output ceiling and both client timeouts were raised; a full plan over real records takes 60 to 90 seconds, which the website must cover with a delayed-status message per PRD section 8, and which prompt caching or a smaller plan should shorten later.

**What we gave up** — Certainty about reuse rights, and the original strictness of the freshness rule. A judge could still object to unlicensed data; the disclosure is the answer.

**How we'll know if this was right** — No objection from the publisher or judges, and the call sheet later replaces map hours with phone-confirmed hours for the demo ZIP.

**What actually happened** —
