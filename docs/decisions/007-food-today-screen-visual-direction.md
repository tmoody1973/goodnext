# 007: The Food today screen looks like a 7-day forecast, not a receipt or a portal

Date: September 8, 2026. Status: decided.

## Decision
The website's Food today screen uses the "7-Day Forecast Strip" visual direction: today is the big panel with a date and a count, one card per option with a time block, and six small day tiles for the rest of the Bridge Plan.

## Why this came up
The PRD (section 14) requires the Impeccable design workflow before any screen is built. Impeccable rolls dice over a ranked list of visual worlds so the site does not land on the default look every AI-built civic site lands on. The roll assigned "The Checkout Receipt" (a library due-date slip). The screen is the first thing a judge and a resident see, and it has to be scannable by an anxious person on a phone in under a minute.

## Options
1. **The Checkout Receipt** (assigned by the roll). A thermal-paper column, monospace type, a rubber date stamp on every entry, a highlighter band across each opening window, and a real "print and carry" moment. Most distinctive. Cost: dense entries need strict ruling or become a wall; monospace on off-white can read as a gimmick.
2. **The 7-Day Forecast Strip** (Impeccable's pick, Claude's top-ranked candidate). Today big, six tiles below, the exact shape of the Bridge Plan. Cost: it is the familiar answer; it can read as a weather app, and it is where most runs land.
3. **Warm consumer app or the plain civic standard** (challengers). Clear and safe. Cost: indistinguishable from a benefits portal, the thing the site must not be mistaken for.

## What we chose and why
Tarik chose option 2 after seeing all four as phone mockups (generated on his OpenAI key, saved under `.impeccable/mocks/decision/`). The shape maps one-to-one onto the product: one big "today", six small "later" tiles that are visibly not promises. Scanability beat distinctiveness for a task screen. Call: Tarik.

## What we gave up
The receipt's stronger identity and its print-and-carry moment. Two of its disciplines are kept in the brief anyway: state is always a word, never only a color; days two to seven unfold one at a time.

## How we'll know if this was right
A first-time viewer, shown the screen for ten seconds, can say which places are open today and that the rest of the week is not promised. If judges or residents describe it as "a weather app for food" that is fine; if they describe it as "the county site" the direction failed.

## What actually happened
(Tarik fills this in.)
