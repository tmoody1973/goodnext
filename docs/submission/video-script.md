# GoodNext demo video script (H09)

Target length: 4 minutes 20 seconds. Hard limit: 5 minutes.
Record on the public address with the demo clock (September 10, 2026). <!-- HANDOFF.md -->
One take per flow is fine; the letter result and the food plan both come from the
live agent, so what appears may differ slightly from the lines below. Read what is on
screen, not the script, if they disagree.

## Demo letter files (docs/research/notices/generated/)

- six-month-report-conversion-maria-example.pdf (use this one in the video)
- six-month-report-conversion-maria-example.html
- notice-of-sanction-maria-example.pdf
- notice-of-sanction-maria-example.html
- notice-of-sanction-maria-example-page1.png (photo path, goes through Textract)
- time-limited-benefits-warning-maria-example.pdf
- time-limited-benefits-warning-maria-example.html
- values.json (the fictional values used to fill the templates)

## Beats

| Time | On screen | Said |
| --- | --- | --- |
| 0:00 to 0:30 | Title card "GoodNext", then the six-month letter PDF page 1, slowly scrolling. Footer line "Fictional demonstration letter" visible. | "A FoodShare letter arrives. Three pages. Some of it is about you, some of it is boilerplate, and one line changes what you have to do. Most people cannot tell which line. Meanwhile, the question that actually matters today is where dinner is coming from. GoodNext is a free website that does two things: it reads the letter and shows you the next supported step beside the sentence it came from, and it finds food this week without asking for an account or a notice first." |
| 0:30 to 0:45 | Browser on the public address. The two tabs: "Find food today" first, "Understand my letter" second. Click "Understand my letter". | "This is the live site. Two entry points. Let us start with the letter. Our resident is Maria Example. She is fictional; the letter was generated from an official Wisconsin DHS sample template." |
| 0:45 to 1:00 | Choose file, pick six-month-report-conversion-maria-example.pdf, submit. Processing sentence appears. | "Maria uploads the PDF. The file is read in memory, turned into numbered passages, and never stored. A photo would go through Amazon Textract instead." |
| 1:00 to 1:30 | Waiting state, then the result lands (25 to 35 seconds in measured runs). <!-- HANDOFF.md --> Keep the camera on the page. | "The agent runs on Amazon Bedrock AgentCore, built with Strands, using Claude Sonnet 4.6. It reads the passages, looks up approved policy passages by topic, and resolves a help route. Then a validator written in code removes anything the letter did not actually say." |
| 1:30 to 1:50 | Result. Point at the finding "No action needed right now" and the quoted sentence beside it: "You do not need to take any action at this time." | "First finding: no action needed right now. And here is the sentence it came from. Every finding is shown beside its source." |
| 1:50 to 2:05 | Scroll to the task with date "March 2027" and its quoted sentence about the first six-month report form. | "Second: the first six-month report is due in March 2027. The date is copied exactly as printed. GoodNext never counts days or guesses a deadline." |
| 2:05 to 2:20 | Scroll to the fair-hearing task and the quoted fair-hearing page (deadline "November 17, 2026"). Then the "what only the agency decides" and the empty "questions to ask your agency" section. | "Third: she has the right to a fair hearing, with the deadline the letter prints. Notice the empty section: questions to ask your agency stays empty until a human approves the policy passages. The agent may not quote policy nobody has checked." |
| 2:20 to 2:35 | Click "Find food today". Form: ZIP 53206, money 0, kitchen "none", travel "bus". Submit. | "Now the other half. No letter needed. Maria is in 53206, has zero dollars, no kitchen, and a bus pass." |
| 2:35 to 3:10 | Waiting. At about 30 seconds the delayed-status message appears: checking continues, a cancel button, and the three help routes. Hold on it for a few seconds. | "A full seven-day plan takes about a minute and a half. We do not hide that. After thirty seconds the page says checking continues, offers a cancel, and shows three reviewed ways to reach a human: 2-1-1, the Hunger Task Force emergency food page, and the FoodShare member line. If the agent ever goes down, those same three routes are the answer." |
| 3:10 to 3:15 | Jump cut. On-screen caption: "Cut for time. A plan took 87 to 105 seconds in our measured runs." <!-- HANDOFF.md --> | (no narration, or: "We cut the wait.") |
| 3:15 to 3:45 | The plan. Today's options first: for example a free breakfast at The Gathering at Running Rebels, 8:30 to 9:30 AM, "Last checked 2026-09-08", directions link. Then a "call to confirm, checked 2024-08-27" card. <!-- docs/evidence/food-live-53206-v7.json --> | "Today's options come first: opening window, cost, requirements, when we last checked, and a directions link that opens her own map app. Every card says where the data came from and how old it is. A verified card was checked against the provider's official page this month. A call-to-confirm card comes from the 2024 Milwaukee Food Environment Map, so the phone number is right there." |
| 3:45 to 4:00 | Scroll to the six day tiles. Open one. Show the "unmet needs" or warnings line if present (for example, quantity per visit is unknown). | "Six small tiles cover the rest of the week. Listed, never promised. The plan says out loud what it could not cover." |
| 4:00 to 4:20 | Disclosure card, full screen, read aloud. | "Four disclosures. The demo letters are fictional, generated from official Wisconsin DHS sample templates. The upload path is real and nothing is stored. Some directory records are synthetic and labeled; the map records are from August 2024 and say call to confirm. And the questions-to-ask section stays empty until policy passages are approved. The demo clock is pinned to September 10, 2026." |
| 4:20 to 4:30 | Closing card: "GoodNext. Understand what changed. Take the next supported action. Find food while you work through it." Repo URL and live address on screen. | "GoodNext never decides eligibility, never promises benefits or food, and never asks for an account before helping with food. Understand what changed, take the next supported action, and find food while you work through it." |

## Recording notes

- Total planned: 4:30, leaving 30 seconds of slack for a slower letter result.
- If the letter result takes longer than 35 seconds, keep narrating the agent
  explanation; do not cut. If it takes longer than 60 seconds, stop, reload, and
  retake the beat.
- Start the food request only after the letter beats are recorded. Do not run both at
  once; the delayed-status message is part of the story and should be seen.
- If the plan for 53206 differs from the example above, read the cards that appear.
  The validator accepts several valid plans; the script must not promise a specific
  site.
- Record in a normal desktop window. Show one phone-width shot (390 px) of the letter
  result if there is time, since letter results are long on a phone.
- Upload to YouTube as public or unlisted (the rules say public). Put the same link in
  description.md and devpost-fields.md.
