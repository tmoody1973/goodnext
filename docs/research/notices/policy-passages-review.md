# FoodShare Policy Passages — Review Checklist

Tarik, this is a list of exact sentences copied word-for-word from official
Wisconsin DHS FoodShare web pages. Nothing here has been reworded or summarized.
Please check each box only after you've confirmed the passage is accurate and
safe for an agent to quote to a resident. Unchecked = not yet approved to cite.

| ID | Topic | First 120 characters | Source URL | Approved |
|---|---|---|---|---|
| pol-001 | How to meet the FoodShare work requirement | There are three main ways to meet the work requirement. Working or volunteering at least 80 hours per month. Participati… | https://www.dhs.wisconsin.gov/foodshare/work.htm | [ ] |
| pol-002 | Definition of exemptions from the work requirement | Exemptions are reasons why you don’t have to meet the work requirement under federal law. At your interview, your local … | https://www.dhs.wisconsin.gov/foodshare/work.htm | [ ] |
| pol-003 | Who is exempt from the work requirement | You don't have meet the work requirement if: You are pregnant. You can't work due to your physical or mental health. Thi… | https://www.dhs.wisconsin.gov/foodshare/work.htm | [ ] |
| pol-004 | What good cause means for the work requirement | If something happens in your life that you cannot control, like you get sick or your car breaks down and you can't meet … | https://www.dhs.wisconsin.gov/foodshare/work.htm | [ ] |
| pol-005 | What a six-month report is | If you are getting FoodShare, we may ask you to update your household information every six months. You can do so by com… | https://www.dhs.wisconsin.gov/foodshare/smrf.htm | [ ] |
| pol-006 | How to complete a six-month report | We will mail you a FoodShare Six-Month Report and Instructions, F-16076 , about a month before it is due. You can comple… | https://www.dhs.wisconsin.gov/foodshare/smrf.htm | [ ] |
| pol-007 | What happens if a six-month report is late | If you don’t complete all steps by the end of the month when they’re due, federal rules require that we reduce your bene… | https://www.dhs.wisconsin.gov/foodshare/smrf.htm | [ ] |
| pol-008 | What happens if a six-month report is very late | Your benefits will end if your form and any needed documents are more than a month late. You’ll need to reapply to start… | https://www.dhs.wisconsin.gov/foodshare/smrf.htm | [ ] |
| pol-009 | What FSET is | FoodShare Employment and Training (FSET) is a free program for anyone 16 and older who gets FoodShare. FSET can help you… | https://www.dhs.wisconsin.gov/fset/index.htm | [ ] |
| pol-010 | How to enroll in FSET | Before starting FSET, you need to enroll in FoodShare. You may know it as food stamps, QUEST card, EBT, your food card, … | https://www.dhs.wisconsin.gov/fset/index.htm | [ ] |
| pol-011 | How to get started with FSET | Find your FSET agency and reach out to set up an appointment for orientation to get started. A worker from your local FS… | https://www.dhs.wisconsin.gov/fset/index.htm | [ ] |
| pol-012 | Reporting change for members 60 through 64 | Starting August 8, if you are 60–64, and aren’t blind or disabled, you no longer qualify for longer renewal periods. | https://www.dhs.wisconsin.gov/foodshare/news.htm | [ ] |
| pol-013 | What members 60 through 64 must now do | If you are a current member with a 36-month renewal period, you will keep your renewal date. But now you must complete b… | https://www.dhs.wisconsin.gov/foodshare/news.htm | [ ] |
| pol-014 | Work requirement expansion | Last year federal rules expanded the work requirement for some FoodShare members. The age range of affected members grew… | https://www.dhs.wisconsin.gov/foodshare/news.htm | [ ] |
| pol-015 | FoodShare member line phone number | Call your agency or ForwardHealth Member Services at 800-362-3002 if you think someone is trying to scam you. | https://www.dhs.wisconsin.gov/foodshare/index.htm | [ ] |
| pol-016 | How to manage FoodShare benefits online | Only use ACCESS ( ACCESS in Spanish ) to apply for and manage your benefits. You also can use MyACCESS mobile app to get… | https://www.dhs.wisconsin.gov/foodshare/index.htm | [ ] |
| pol-017 | What FoodShare is | You’ve probably heard of food stamps or SNAP (Supplemental Nutrition Assistance Program). In Wisconsin, we call the prog… | https://www.dhs.wisconsin.gov/foodshare/index.htm | [ ] |
| pol-018 | What a FoodShare sanction is | If you do not follow FoodShare basic work rules, and you do not have an exemption or a good cause reason, you will not b… | https://www.dhs.wisconsin.gov/foodshare/basic-work-rules.htm | [ ] |
| pol-019 | Quitting a job without good cause | Not quit a job of 30 or more hours per week voluntarily and without good cause (or a job with weekly earnings of $217.50… | https://www.dhs.wisconsin.gov/foodshare/basic-work-rules.htm | [ ] |
| pol-020 | How long a sanction lasts | The length of a sanction period depends on how many sanctions you have: The first sanction is for one month. A second sa… | https://www.dhs.wisconsin.gov/foodshare/basic-work-rules.htm | [ ] |
| pol-021 | How a sanction can end early | You can end a sanction period early if you have an exemption from the FoodShare basic work rules. Call your agency right… | https://www.dhs.wisconsin.gov/foodshare/basic-work-rules.htm | [ ] |
| pol-022 | Getting FoodShare again after a sanction ends | You will need to reapply for FoodShare. If you are part of a household that is already getting benefits, you will need t… | https://www.dhs.wisconsin.gov/foodshare/basic-work-rules.htm | [ ] |

## Fetch problems

These are pages the task asked for that did not load at the address given, and what happened instead.

- **FoodShare Employment and Training (FSET) page**: the address `https://www.dhs.wisconsin.gov/foodshare/fset.htm` 
  redirects (HTTP 301) to `https://www.dhs.wisconsin.gov/fset/index.htm`. That page loaded fine and pol-009
  through pol-011 come from it.
- **Fair hearing page**: `https://www.dhs.wisconsin.gov/foodshare/fairhearing.htm` returned "page not found" (HTTP 404).
  See "Topics not found" below for what was tried to find a replacement.
- **Sanctions page**: `https://www.dhs.wisconsin.gov/foodshare/sanctions.htm` also returned "page not found" (HTTP 404).
  A working replacement was found by following a link from another DHS FoodShare page:
  `https://www.dhs.wisconsin.gov/foodshare/basic-work-rules.htm`. It covers quitting a job without good cause and
  how a sanction period ends, so pol-018 through pol-022 use it instead of the address given in the task.

## Topics not found

- **How to request a fair hearing and the deadline rule** — no DHS FoodShare page with this content was found.
  What was tried, all with `curl` (no browser): the direct address named in the task (404); DHS's own site search
  at `/search` (blocked every time with "Access Denied" from the site's security filter, regardless of headers used);
  DuckDuckGo and Bing web search for `site:dhs.wisconsin.gov fair hearing FoodShare` (both returned pages that need
  a real browser to show results, so nothing could be read from them); DHS's own sitemap file (the index loaded, but
  every one of its 11 sub-pages was blocked the same way as the search page); and the FoodShare-related pages already
  fetched, checked for any outbound link mentioning "hearing" or "appeal" (none found — two promising-looking links,
  `/clientrights/index.htm` and `/your-rights.htm`, turned out to be about mental-health client rights and civil-rights
  nondiscrimination, not fair hearings). This entry is recorded as `pol-023` with `passage: null` in the JSON file.
  A person could likely find this by calling the FoodShare member line or searching the site in an actual browser.

