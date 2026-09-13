# Submission materials

Drafted September 13, 2026 for the Agents for Humans hackathon (deadline Monday
September 14, 2026, 7 p.m. Central). <!-- HANDOFF.md --> Everything here is a draft
for Tarik to read and edit before it goes on Devpost.

## Files

| File | What it is | Hackathon item |
| --- | --- | --- |
| `architecture.json` | The diagram spec, revised from `docs/FoodShare-Bridge-Architecture.json` to match what shipped. Same schema (archify, schema_version 1). | H07 |
| `architecture.html` | The rendered diagram, standalone, with light and dark themes. Validated 9 of 9 checks, showcase profile, 0 errors, 0 warnings. | H07 |
| `architecture.png` | Diagram-only PNG (the SVG node, light theme, 2716 by 1478 pixels, no viewer toolbar). Use this one on Devpost. | H07 |
| `architecture.visual-check.2048x1320.light.png` | Full-page screenshot at 2048 by 1320, light theme, including the three cards. Dark and 1440 by 900 variants sit beside it. | H07 |
| `architecture.visual-check.html` and `.json` | Contact sheet and containment receipt from the visual check (all four desktop sizes pass, no overflow). | evidence |
| `description.md` | The Devpost text description: what it does, who it is for, how it works, what we built with, disclosures, what it never does, pre-existing work. | H08 |
| `video-script.md` | Timed beats for the demo video, 4 minutes 30 seconds planned, 5 minutes max. Lists the demo letter files. | H09 |
| `devpost-fields.md` | Checklist of every Devpost form field, with the file that answers each. | H10 |

Note on the renderer: the original diagram was produced by the `archify` skill
(its HTML says `generator: archify 2.15.0`), not `diagram-design`. The revision was
rendered with archify's `deliver` command and its `visual-check` produced the
full-page PNGs. `architecture.png` follows the `diagram-design` export procedure
(screenshot of the SVG node through Playwright using the installed Chrome).

## What is still a placeholder

- `description.md`: "Live demo: <PUBLIC ADDRESS>" and "Video: <YOUTUBE URL>".
- `description.md`: disclosure 8 (plain-HTTP cookie note) stays; decision 012 chose
  plain HTTP for Monday. Delete it only if HTTPS is added before submission.
- `description.md`: "written during the hackathon window" needs Tarik to confirm the
  start date.
- `devpost-fields.md`: "AWS Builder ID: <TARIK FILLS IN>", track choice, team
  members, thumbnail image.
- `video-script.md`: the plan for 53206 and the letter result come from the live
  agent; read what appears on screen if it differs from the script.

## H06 check: public repo with a license

Run September 13, 2026 from the repo root.

```text
$ cat LICENSE | head -3
MIT License

Copyright (c) 2026 Tarik Moody

$ gh repo view tmoody1973/goodnext --json visibility,licenseInfo
{"licenseInfo":{"key":"mit","name":"MIT License","nickname":""},"visibility":"PUBLIC"}
```

Both pass: the LICENSE file is present at the repo root, GitHub detects it as MIT,
and the repository is public.
