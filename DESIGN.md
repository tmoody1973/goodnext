# GoodNext design

This file records the visual and interaction design of the GoodNext website. It
is the finish-pass artifact named in the root layout direction contract and in
`docs/specs/food-today-screen.md`. It describes what the code does today. The
source decision is `docs/decisions/007-food-today-screen-visual-direction.md`.

## Audience and use scene

A Milwaukee resident opens GoodNext after a FoodShare notice or a hard week.
The resident often reads the screen on a phone in daylight, or on a shared
library terminal, or on paper printed from that terminal. The design serves
that scene first. It stays scannable by an anxious person in under a minute, and
it never reads like the county benefits portal.

## Direction: the 7-Day Forecast Strip

Today is the big panel. The later days are small tiles. The shape maps one to
one onto the product: one large "Food today" and six small "later this week"
tiles that are plainly not promises.

Three rules come from the direction:

- The screen shows the date and how many places are listed today, at the top.
- Each option reads as a card, and the opening window is the biggest thing on
  the card.
- The state is always a word. Color is secondary and never carries meaning on
  its own.

## Palette

The palette is restrained and light only, because the use scene is daylight or a
library terminal. The tokens live in `apps/web/src/app/globals.css`.

| Token | Value | Use |
| --- | --- | --- |
| `paper` | `#ffffff` | page and card background |
| `ink` | `#141414` | body text |
| `ink-soft` | `#3d4653` | secondary text |
| `navy` | `#0b2a4a` | header field, time block, focus outline |
| `navy-soft` | `#dbe6f2` | text on navy, summary line background |
| `amber` | `#ffb703` | actions and the count only |
| `amber-deep` | `#8a5a00` | amber text on light when contrast needs it |
| `line` | `#cfd6df` | borders |
| `alert` | `#a4211f` | error text |

Amber marks a thing the resident can press or count. Nothing else is amber.

## Type

The type is the system sans stack. Numbers use tabular figures, so times and
dollar amounts line up.

## Reusable pieces

The screen is built from three pieces.

- **Time block.** A navy block on the left of a card. It shows the opening
  window as two large times, or a single sentence when the provider is closed or
  opens later. See `apps/web/src/components/OptionCard.tsx`.
- **Option card.** One listed option. It shows, in order, the time block, the
  provider, the cost, the requirements, an appointment note when present, a
  service-area caveat when present, the check date with a tier word, the line
  "We can't confirm they have food today", the travel echo, Directions and a
  phone link, and the source line last. The card renders only the API's
  permitted claims, never free text the model wrote.
- **Day tile.** A small tile for one later day. It shows the weekday, the date,
  and how many options are listed. The day tiles land with the "Later this week"
  work (MOO-785); this file will gain their expanded-state and motion rules when
  that work merges.

## State in words

Every state names itself in plain words.

- The success view names the date and the count.
- The partial view adds one fixed sentence above the cards.
- The no-match view states that nothing is listed for the ZIP today, and shows
  the three help routes and a way to change the ZIP.
- The waiting view says checking takes one to two minutes. After 30 seconds it
  adds a delayed status, a cancel control, and the help routes.
- The outage view says the site is temporarily unavailable and offers retry.

## Accessibility

The screen meets the audience where it is: a keyboard, a screen reader, a small
phone, or a magnified page.

- **Reading order equals keyboard order.** The markup order is the reading
  order.
- **Visible focus.** A 3px navy outline marks the focused control.
- **Announced result.** The result count is a heading, so a screen-reader user
  can reach it as a result and hear how many places are listed today. The result
  section is also a polite live region.
- **Descriptive links.** Each Directions link and each Call link names its
  provider through an accessible label, so the link still makes sense when a
  screen reader reads it out of context.
- **Reduced motion.** When the resident asks for less motion, the site removes
  transitions and animations.
- **Reflow.** The page works at 320 pixels wide and at 200 percent zoom, so the
  next action is never hidden.

## Print

A resident on a library terminal can carry today's list on paper. The screen
offers a "Print this list" control on a result. The print stylesheet prints the
result — the cards, the unconfirmed list, and the help routes — as flat black on
white, and drops the form, the buttons, and the waiting chrome the page cannot
use. The rules live in `apps/web/src/app/globals.css`.

## Privacy

The site stores nothing about the resident. It uses no analytics and no cookies
beyond the API session cookie. A resident on a shared computer leaves no trace.

## No machinery on screen

The site names no technology. The never-list test scans the copy module and
every rendered page and fails on any vendor or build name, and on any of the
certainty words the product forbids. See `apps/web/src/lib/never-list.ts`.
