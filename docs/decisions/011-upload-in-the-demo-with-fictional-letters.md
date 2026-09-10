# 011: The demo accepts a real upload, fed with fictional letters

Date: September 10, 2026. Status: decided.

## Decision
The "Understand my letter" entry point accepts a PDF or photo of a FoodShare letter and reads it, in the hackathon demo, using fictional letters generated from official Wisconsin DHS sample templates. The PRD had kept live upload behind pilot gates and offered a sample picker for the prototype.

## Why this came up
Tarik will not submit without the notice entry point, and a judge picking a sample from a menu does not show an agent reading a document. The submission is judged on technical implementation and impact; a menu hides both. Getting this wrong one way ships a demo that looks like a slideshow; the other way ships a path that could mishandle a real person's letter.

## Options
1. **Sample picker, no upload.** Honest and cheap; fits the PRD's prototype line. Cost: judges never see the agent read anything; the entry looks staged.
2. **Real upload with fictional letters** (chosen). The upload path is real: type and size checks, in-memory text extraction, a stated processing sentence, nothing stored. The demo material is fictional. Cost: half a day more, an OCR service call for photos (Amazon Textract, cents per page), and the pilot gates (consent, retention, security review) are satisfied only in their minimal form: nothing is retained and the site says so.
3. **Static explanations per letter, no agent.** Cheapest. Cost: the event requires the agent to do the work; the entry would be weaker on its strongest criterion.

## What we chose and why
Option 2. The value of the product is an agent reading a document and returning a checked, cited answer; a demo should show exactly that. Fictional letters keep the standing rule that no real resident's document is used in verification. Call: Tarik, with Claude recommending the picker and being overruled.

## What we gave up
The pilot gates are met minimally, not fully: there is no retention policy to enforce because nothing is retained, but there is also no security review, no document-classification of what a judge might upload, and no handling of a multi-person letter beyond the validator's separation rules. The write-up must say the demo is for fictional letters and real uploads await review.

## How we'll know if this was right
A judge uploads a provided letter and gets a cited, honest result in under 30 seconds, and the write-up's disclosure reads as deliberate rather than as a gap.

## What actually happened
(Tarik fills this in.)
