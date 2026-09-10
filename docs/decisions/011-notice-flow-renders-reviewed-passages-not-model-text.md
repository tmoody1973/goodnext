# 011: Understand my letter shows reviewed policy passages, matched deterministically, never model free text

Date: September 10, 2026. Status: decided.

## Decision
The "Understand my letter" flow reads a FoodShare letter, pulls its text with no
model in the path, and shows what the letter appears to ask for beside reviewed
policy passages it matches. The passages come from one reviewed file,
`app/goodnext/policy_passages.json`. A passage is matched by plain-text triggers,
not written or paraphrased by a model. The letter's own text and the reviewed
guidance stay two separate things on screen.

## Why this came up
FR02 promises a resident can check what a notice appears to request before
relying on a plan. The food flow already earns trust by rendering only permitted
statements from reviewed records, never the model's own words (decisions 007 and
009, the never-list test). The notice flow needed the same rule, and it had to
ship for the September 14 demo without a live LLM notice workflow in place
(MOO-789 is a separate ticket).

## Options
1. **Send the letter to the agent for a plain-language explanation.** Warmest
   reading, but the words on screen are the model's, which the whole product
   avoids; and it depends on MOO-789, which is not built. Cost: a trust rule
   broken and a dependency not yet available.
2. **Deterministic passage matching** (chosen). The letter's text is matched
   against reviewed passages by trigger phrases; the screen shows those passages
   with their source, check date, and review status. Cost: guidance is only as
   broad as the reviewed file; a letter it does not cover gets an honest
   no-match and the help routes.
3. **No guidance, only the extracted text.** Honest but thin; the resident is
   left to read the letter alone, which is the problem FR02 set out to fix.

## What we chose and why
Option 2. It keeps the product's core rule — reviewed records, never model free
text — for the second flow, it needs no AWS session or model call to be correct,
and it is testable end to end with committed fixtures. It also matches the PRD's
data rule that only reviewed guidance applicable to the request supports
instructions.

## What we gave up
No warm paraphrase of the letter. A letter outside the reviewed set gets a
no-match, not a best guess. The policy passages are drafted for the demo and
still need qualified benefits-staff review before any pilot use; the screen shows
that status and routes the case decision to official staff.

## How we'll know if this was right
A judge opens `/notice`, picks the six-month-report sample, and sees the letter's
due date beside the reviewed six-month-report and how-to-respond passages, each
with its source and check date, and no sentence written by a model.

## What actually happened
(Tarik fills this in.)
