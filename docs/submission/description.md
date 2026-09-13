# GoodNext: Devpost description (H08)

Draft for the Devpost "text description" field. Plain English. Every number is cited
to its source file in a trailing comment.

Live demo: <PUBLIC ADDRESS>
Video: <YOUTUBE URL>
Repository: https://github.com/tmoody1973/goodnext <!-- HANDOFF.md -->

## What it does

GoodNext is a free website for Wisconsin households on FoodShare, the state's food
benefit program. It does two things. Upload a FoodShare letter as a PDF or photo, or
answer three questions about it, and GoodNext shows what the letter says beside the
exact sentences it came from, the next supported step, the tasks and dates exactly as
printed, who to contact, and what only the agency can decide. Or skip the letter
entirely: enter a ZIP code, how much money you have, what kind of kitchen you have,
and how you travel, and GoodNext lists today's food options with their opening
window, cost, requirements, last check date, and a directions link, plus six small
tiles for the rest of the week. The promise is simple: understand what changed, take
the next supported action, and find food while you work through it. Nothing about
the resident is stored.

## Who it is for

A Milwaukee resident who just opened a confusing FoodShare notice and needs to know,
today, whether they have to do anything and where they can eat this week. Our demo
resident is "Maria Example," a fictional person in ZIP 53206 with no money, no
kitchen, and a bus pass. It is also for the people who help them: a friend, a
navigator at a community organization, or a 2-1-1 operator who wants a cited answer
instead of a guess.

## How it works

1. The resident opens one public web address. The page is a static site (plain
   files, no server rendering) served by the same container that runs the API, so
   the browser only ever talks to one host.
2. For a letter, the browser sends the file to the API. A PDF's text layer is read
   in memory. A photo goes to Amazon Textract, a service that reads printed text
   out of an image, once per image. Either way the text becomes numbered passages
   and the file is never written to disk or logged. <!-- services/api/goodnext_api/notices.py -->
3. The API invokes the agent, which runs on Amazon Bedrock AgentCore Runtime, a
   managed host for agents. The agent is built with the Strands Agents SDK and uses
   Claude Sonnet 4.6 on Bedrock as its model. <!-- HANDOFF.md -->
4. The agent calls its tools. For a letter: read the passages, look up approved
   policy passages by topic, and resolve a help route. For food: search the
   directory for the ZIP and the seven dates, then check each result against the
   resident's money, kitchen, and travel. Tools return only what the directory or
   the letter actually says.
5. After the model returns, a validator (a check written in code, not by the model)
   strips anything a tool did not support: a visit the search did not return, a date
   the letter did not print, a claim that someone is eligible. What is left comes
   back as a structured answer with every finding tied to a passage or a record id.
6. The website shows the result. For a letter, each finding sits beside the
   sentence it came from. For food, today's options come first, with "call to
   confirm" and "last checked" labels on every card and three reviewed help routes
   (2-1-1, the Hunger Task Force emergency food page, and the FoodShare member line)
   under every result.
7. If the agent cannot be reached, the API answers with a plain "temporarily
   unavailable" message that still carries the three help routes.
8. While a food plan is being built, the page shows a delayed-status message after
   about 30 seconds: checking continues, you can cancel, and the help routes are
   right there. A full plan takes 87 to 105 seconds in our measured runs; a letter
   takes 25 to 35 seconds. <!-- HANDOFF.md -->

## What we built with

- Strands Agents SDK (Python) for the agent, its tools, and structured output.
- Amazon Bedrock AgentCore Runtime to host the agent, deployed as runtime v7. <!-- HANDOFF.md -->
- Claude Sonnet 4.6 on Amazon Bedrock (model id us.anthropic.claude-sonnet-4-6, us-east-1). <!-- HANDOFF.md -->
- FastAPI (a Python web framework) for the API: sessions, validation, and the bridge
  to the agent.
- Next.js 16 static export with Tailwind 4 for the website. <!-- HANDOFF.md -->
- Amazon Textract for photo uploads.
- One container on ECS Fargate (serverless containers) behind an Application Load
  Balancer, serving the site at / and the API at /api/*.
- Test counts at submission: 57 agent tests, 25 API tests, 50 website tests, all
  green, none of which reach Bedrock. <!-- HANDOFF.md -->

## Disclosures

1. The demo letters are fictional. They were generated from official Wisconsin
   Department of Health Services sample notice templates and filled with a made-up
   resident, case number, and dates. No real resident's document was used.
2. The upload path is real. The site accepts a PDF, JPG, or PNG up to 10 MB and 6
   pages, reads it in memory, and stores nothing. <!-- services/api/goodnext_api/notices.py -->
   Real uploads from real residents await a security review before any pilot.
3. Some food directory records are synthetic. Of 93 records, 16 were reviewed by us
   against official provider pages on September 8, 2026; 68 come from the Milwaukee
   Food Environment Map; 9 are synthetic and labeled "(synthetic)" on the card. <!-- HANDOFF.md -->
4. "Questions to ask your agency" stays empty. The agent may only quote policy
   passages a human reviewer has approved. At submission, 0 of 23 passages are
   approved, so that section is empty by design, and the letter's own text is the
   only source. <!-- HANDOFF.md -->
5. The Milwaukee Food Environment Map data is dated August 27, 2024. Those records
   show "last checked 2024-08-27, call to confirm" and their hours were not verified
   by phone. <!-- README.md -->
6. The demo clock is pinned to September 10, 2026, so the directory's opening
   windows stay meaningful for judges. Outside demo mode the real Milwaukee clock is
   used. <!-- HANDOFF.md, README.md -->
7. Plans differ run to run. The validator accepts each one; none is a promise of food.
8. <IF THE PUBLIC ADDRESS IS PLAIN HTTP, KEEP THIS LINE, OTHERWISE DELETE IT> The
   public address runs without HTTPS, so the session cookie is set without the
   secure flag for the demo (decision 012).

## What GoodNext never does

- Decide eligibility. The agency decides; GoodNext says so in every letter result.
- Promise benefits or promise that a site has food in stock.
- Ask for an account, a notice, or a Social Security number before helping with food.
- Take reservations or contact anyone on the resident's behalf.
- Store anything about the resident.

## Pre-existing work and third-party material

- Code: everything in the repository, including the planning documents in `docs/`,
  was written during the hackathon window. <TARIK CONFIRMS THE START DATE>
- Milwaukee Food Environment Map (Data You Can Use / Milwaukee Food Council), public
  ArcGIS layer `EmergencyFood_MKE_2024`, 75 sites, data as of August 27, 2024. The
  layer states no license. Reuse permission has been requested from the publisher
  and had not arrived at submission; every card credits the source and its date
  (decision 006). <!-- README.md -->
- 211 National Data Platform: portal account and trial subscription only. No 211
  record appears in the repository, the demo, or any deployed environment until
  IMPACT 211 gives written permission (decision 005). <!-- README.md -->
- Wisconsin DHS sample notice templates: public documents used to generate the
  fictional demo letters (decision 011).
- Reviewed directory: 16 Milwaukee sites we checked against their official provider
  pages on September 8, 2026, with evidence notes and stated uncertainties. <!-- README.md -->
- Help routes: 2-1-1 (IMPACT 211), the Hunger Task Force emergency food page, and
  the FoodShare member line, from their public pages, checked September 8, 2026.
- Open source: MIT license in the repository. Dependencies are listed in the
  project files and carry their own open-source licenses.
