# 008: The website and the API share one address

Date: September 8, 2026. Status: decided.

## Decision
The static website and the API are served from the same hostname. Pages come from the static files; anything under `/api/` is routed to the FastAPI service. The browser calls the relative path `/api/plans`.

## Why this came up
The Food today screen is the first thing that calls the API from a browser. The API keeps a short session cookie (a small token the browser sends back so the agent can keep context across requests) marked "strict same-site", meaning the browser only sends it to the same site that set it. If the site and the API lived at two different addresses, the cookie would be dropped silently and every request would look like a stranger. The API also has no cross-origin allowance (the header a browser needs before it will talk to a different address).

## Options
1. **One address** (chosen). Routing rule at the edge sends `/api/*` to the API. In local dev, the Next dev server proxies `/api/*` to port 8000. No API change. Cost: hosting must put both behind one hostname, which constrains the hosting choice in step 3 of the handoff.
2. **Two addresses with cross-origin allowance.** The API adds an allowed-origins list and loosens the cookie to "none" plus secure. Cost: two things to configure and keep in step, a weaker cookie, and an API change before the screen can be tested end to end.
3. **No cookie at all.** Drop sessions; every request is independent. Cost: the agent runtime requires a session id, and later features (planned visits) need continuity.

## What we chose and why
Option 1, joint call by Tarik and Claude during the grill on 2026-09-08. Fewest moving parts, no API change, and the cookie keeps its strongest setting.

## What we gave up
Freedom to host the site and API on unrelated services with no shared front door. Judge-facing hosting must include a path-based routing rule.

## How we'll know if this was right
The first live browser run of the Food today screen against the deployed API shows the same session id on two consecutive requests, with no cross-origin errors in the console.

## What actually happened
(Tarik fills this in.)
