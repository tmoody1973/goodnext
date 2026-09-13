# Devpost submission fields (H10)

Source of the field list: the event page https://agentsforhumans.devpost.com/ and its
rules page https://agentsforhumans.devpost.com/rules, both fetched September 13, 2026.
Fields marked "standard Devpost" were not visible in the fetched text but appear on
every Devpost submission form; confirm them on the live form.

Deadline from the event page: Monday, September 14, 2026, 5:00 pm Pacific, which is
7:00 pm Central. <!-- HANDOFF.md agrees: 7 p.m. Central -->

Judging criteria, equally weighted: technical implementation, design, potential
impact, creativity and originality, presentation.

Tracks: Everyday, Professional, Good Neighbor. GoodNext fits Good Neighbor (helping
groups and community organizations). <!-- docs/FoodShare-Bridge-PRD.md section 13 -->

## Checklist

| # | Field | Required | Answer or source file | Status |
| --- | --- | --- | --- | --- |
| 1 | AWS Builder ID | Yes (event page) | AWS Builder ID: <TARIK FILLS IN> | Placeholder |
| 2 | Project name | Standard Devpost | GoodNext | Ready |
| 3 | Tagline (one line) | Standard Devpost | "Understand what changed, take the next supported action, and find food while you work through it." (description.md) | Ready |
| 4 | Text description: what it does, who it is for, how it works | Yes (event page) | description.md, sections "What it does", "Who it is for", "How it works" | Ready |
| 5 | Public code repository URL (GitHub, GitLab, or Bitbucket) with source, assets, and setup instructions | Yes (rules) | https://github.com/tmoody1973/goodnext, visibility PUBLIC (README.md in this folder, H06 check) | Ready |
| 6 | Open source license file, visible in the repo About section | Yes (rules) | MIT, LICENSE at repo root; GitHub detects "MIT License" (README.md in this folder) | Ready |
| 7 | README in the repo | Yes (rules) | Repo README.md (setup, run, data sources, demo boundaries) | Ready |
| 8 | Architecture diagram | Yes (rules) | architecture.html and the PNG next to it (see README.md in this folder for the exact file names) | Ready |
| 9 | Demo video URL, YouTube or Vimeo, public, 5 minutes max, shows the working project and pitches problem, audience, and why it matters | Yes (rules) | video-script.md; final link goes in description.md "Video:" line | Placeholder |
| 10 | Testing access: link to a website, functioning demo, or test build that works through the end of judging (October 8, 2026) | Yes (rules) | description.md "Live demo:" line, the public address | Placeholder |
| 11 | Live demo link (scores higher on technical implementation) | Optional (event page) | Same as 10 | Placeholder |
| 12 | Built with (technology tags) | Standard Devpost | Strands Agents SDK, Amazon Bedrock AgentCore, Amazon Bedrock, Claude Sonnet 4.6, Amazon Textract, FastAPI, Python, Next.js, Tailwind, ECS Fargate, Application Load Balancer (description.md "What we built with") | Ready |
| 13 | Track selection | Likely on the form | Good Neighbor | Confirm on form |
| 14 | Pre-existing work and third-party material disclosure | Yes (rules: incorporated pre-existing work must be disclosed; third-party code, APIs, and data need authorized use) | description.md "Pre-existing work and third-party material" and "Disclosures" | Ready, one line needs Tarik's start-date confirmation |
| 15 | Thumbnail image | Standard Devpost | Not made. Suggest a clipped screenshot of the letter result from docs/evidence/notice-live-six-month-390.png or the food plan from docs/evidence/food-live-53206-v7-390.png | Placeholder |
| 16 | Image gallery (screenshots) | Standard Devpost, optional | docs/evidence/ screenshots (food-live-53206-v7-390.png, notice-live-six-month-390.png, moo-783-live-delayed-status.png) | Optional |
| 17 | Team members | Standard Devpost | Tarik Moody (solo) | Confirm on form |
| 18 | builder.aws.com blog post | Optional bonus (event page) | Not written | Optional |

## Before pressing submit

- Open the public address in a private browser window and run both flows.
- Check the video is public and under five minutes.
- Check the GitHub About panel shows "MIT License".
- Paste the same live address and video link into description.md, then paste
  description.md into the Devpost description field.
