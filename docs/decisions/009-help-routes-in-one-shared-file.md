# 009: The three help routes live in one JSON file that both services read

Date: September 8, 2026. Status: decided.

## Decision
The three reviewed help routes (2-1-1, Hunger Task Force emergency food, the FoodShare member line) live in `app/goodnext/help_routes.json`. The agent reads that file and attaches the routes to every answer it gives, whatever the status. The API reads the same file for the one answer it writes itself, the "temporarily unavailable" reply it sends when it cannot reach the agent at all.

## Why this came up
The Food today screen shows the help routes under every result and inside the 30-second delayed status, so a human is always one tap away. The agent used to send them only when nothing was found. The API, a separate service, had no copy at all, so its own outage reply could not include them. The grill had already ruled out the website keeping its own copy: reviewed facts should have one home.

## Options
1. **One shared JSON file, read by both** (chosen). No copies, one place to edit, a test in each service that reads it. Cost: when the API gets its own container for hosting, that file must be copied into the container and the path set by an environment variable; a test guards the read.
2. **The API remembers the last routes it saw from the agent.** No file coupling. Cost: after a restart, if the agent is down on the very first request, the reply has no routes, which is the exact moment they matter.
3. **The API's outage reply carries no routes.** Simplest. Cost: the resident who most needs a phone number gets none.

## What we chose and why
Option 1. Tarik's call during the MOO-780 build, on Claude's recommendation. The reviewed facts stay in one file; the two services stay honest about where they got them.

## What we gave up
Some deployment freedom. The API is no longer self-contained; hosting has to ship one small file from the agent folder alongside it. A missing file logs a warning and serves no routes rather than crashing.

## How we'll know if this was right
The first hosted API "temporarily unavailable" reply, captured during the live run, carries three routes. If hosting forgets the file, the API test that reads it will not catch that, but the live run will.

## What actually happened
(Tarik fills this in.)
