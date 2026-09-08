# 005 Live 211 data in anything external needs IMPACT 211's permission first

**Decision** — GoodNext uses the 211 trial API only to verify schemas and build the adapter locally. No 211 record appears in the public repository, the judges' demo, or any deployed environment until the Milwaukee 211 center, IMPACT 211, gives written permission. Until then the demo runs on the synthetic fixture and says so.

**Why this came up** — On September 8, 2026 Tarik read the API portal's Terms of Use. They say every 211 record is owned by the local 211 center, and that "any use of this data for production, operational, commercial, or other external purposes requires the prior permission of each participating 211 center." A hackathon demo that judges use is an external purpose. The trial product adds "development and testing only."

**Options**
- *Fixture for the demo, 211 adapter built and tested locally, ask IMPACT 211 for permission in parallel.* Cost: the judges see synthetic pantries, clearly labeled; the adapter is proven with the trial key but not shown live.
- *Use trial data in the demo and hope "testing" covers it.* Cost: violates the terms as written, risks the subscription and the account, and puts 211 records in a public repo without permission.
- *Skip 211 entirely and hand-curate a directory from public pages.* Cost: loses the only structured, maintained source, and the Hunger Task Force and Food Council data have their own unstated reuse terms.

**What we chose and why** — The first. Tarik's call on Claude's recommendation. It respects the data owners, keeps the submission honest, and loses nothing technically: the adapter can be fully built against the trial key and switched on the day permission arrives.

**What we gave up** — Live data in the September 14 demo. The community-benefit story is told with synthetic households and a synthetic closure, which the PRD already planned.

**How we'll know if this was right** — IMPACT 211 replies to a permission request with either a yes and terms, or a process to follow. If they say yes before judging ends October 8, the live path is flipped on and the demo notes are updated.

**What actually happened** —
