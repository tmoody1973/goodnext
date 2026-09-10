# 010: The finish-pass screenshots run against a fixture stub, not the deployed runtime

Date: September 8, 2026. Status: decided.

## Decision
For MOO-786, the Impeccable finish pass, the browser round renders the Food today screen against a tiny local stub that replays saved real responses (the 53206 plans from September 9 and 10 of the demo week, a no-match, and an outage), instead of calling the deployed agent runtime for every capture.

## Why this came up
The finish pass needs about a dozen renderings of the same screen at different widths, zoom levels, and states, plus a print preview. Each real plan costs a model call (a few cents) and 60 to 105 seconds of waiting. Twelve of those is fifteen to twenty minutes of dead time for pictures whose only purpose is to check layout, and the no-match and outage states are awkward to provoke on demand from the real service. Getting this wrong in one direction wastes an evening; in the other, it ships screenshots of a page that never met the real data.

## Options
1. **Real runtime for every capture.** Fully honest evidence. Cost: fifteen to twenty minutes of waiting, a dozen model calls, and no easy way to stage the outage state.
2. **A stub that replays saved real responses** (chosen). The response bodies are the exact JSON the runtime returned on earlier live runs, saved under `docs/evidence/`. Cost: the screenshots prove layout, not the live path; the request path (proxy, cookie, timing) is not exercised.
3. **Unit-test snapshots only.** No browser at all. Cost: a test renderer has no layout engine, so it cannot see overflow, contrast, focus rings, or print; the things this pass exists to check.

## What we chose and why
Option 2, for the finish pass only. The data on screen is real (saved live envelopes, not invented), the layout checks are exactly what the pass is for, and the live path gets its own dedicated proof one issue later: MOO-787 runs the whole route through the real runtime once, with cookie, console, and timing evidence. Call: Claude, disclosed to Tarik in the closing comment.

## What we gave up
The finish-pass screenshots do not prove the proxy, the session cookie, or the wait behavior. If MOO-787 finds a live-path defect, the pictures from this pass may need to be retaken.

## How we'll know if this was right
MOO-787's live screenshot at phone width matches the stub-driven `mobile.png` from this pass in every visible respect except the request id and the demo date.

## What actually happened
(Tarik fills this in.)
