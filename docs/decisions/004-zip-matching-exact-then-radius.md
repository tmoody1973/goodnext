# 004 Match a resident's ZIP exactly now; add radius search with the 211 adapter

**Decision** — In the first Food today feature, a food resource is shown only if the resident's ZIP is in the resource's served-ZIP list. Distance-based or neighboring-ZIP search is deferred to the 211 adapter feature, where the 211 Search API's own distance parameter is tried first and Census ZIP-area centroids are the fallback.

**Why this came up** — A resident one ZIP over from a pantry sees nothing under exact matching. Tarik asked what data could fix that before deciding. A bounded research pass on September 8, 2026 found the sources.

**Options**
- *Exact list now, radius later with 211.* No new data or code this week. Cost: a nearby pantry can be invisible in the demo.
- *Vendor the Census Gazetteer centroid file now.* A 1 MB public-domain file (a centroid is the center point of a ZIP area) and straight-line distance math. Cost: Census ZIP areas approximate postal ZIPs, so a few Milwaukee codes have no entry, and "straight line, not a route" copy has to be right before it is honest.
- *True border adjacency from Census shapefiles.* Most correct. Cost: a mapping-library step and the most testing, against a six-record fixture.

**What we chose and why** — Exact now, radius with 211. Tarik's call on Claude's recommendation. The 211 API the product already depends on publicly advertises distance search, which would make local data unnecessary, and the fixture is too small to test neighbor logic meaningfully.

**What we gave up** — Demo realism at ZIP edges. The parameter details of the 211 distance search are unverified until someone logs in with the credentials.

**How we'll know if this was right** — When the 211 adapter lands, either its distance parameter works and no local dataset was ever needed, or the Gazetteer fallback takes under a day to add.

**What actually happened** —
