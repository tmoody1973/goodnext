---
name: GoodNext
description: A Milwaukee food-finder that reads as a forecast strip, not a benefits portal.
colors:
  paper: "#ffffff"
  ink: "#141414"
  ink-soft: "#3d4653"
  navy: "#0b2a4a"
  navy-soft: "#dbe6f2"
  amber: "#ffb703"
  amber-deep: "#8a5a00"
  alert: "#a4211f"
  line: "#cfd6df"
typography:
  display:
    fontFamily: "ui-sans-serif, system-ui, -apple-system, \"Segoe UI\", Roboto, sans-serif"
    fontSize: "3rem"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "-0.02em"
  headline:
    fontFamily: "ui-sans-serif, system-ui, -apple-system, \"Segoe UI\", Roboto, sans-serif"
    fontSize: "clamp(1.5rem, 4vw, 2.25rem)"
    fontWeight: 700
    letterSpacing: "-0.02em"
  title:
    fontFamily: "ui-sans-serif, system-ui, -apple-system, \"Segoe UI\", Roboto, sans-serif"
    fontSize: "1.125rem"
    fontWeight: 600
  body:
    fontFamily: "ui-sans-serif, system-ui, -apple-system, \"Segoe UI\", Roboto, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    fontFeature: "tnum"
  label:
    fontFamily: "ui-sans-serif, system-ui, -apple-system, \"Segoe UI\", Roboto, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 500
rounded:
  xl: "12px"
  "2xl": "16px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "32px"
components:
  button-primary:
    backgroundColor: "{colors.amber}"
    textColor: "{colors.ink}"
    rounded: "{rounded.xl}"
    padding: "10px 20px"
  button-primary-hover:
    backgroundColor: "{colors.amber-deep}"
    textColor: "{colors.paper}"
    rounded: "{rounded.xl}"
    padding: "10px 20px"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.navy}"
    rounded: "{rounded.xl}"
    padding: "10px 20px"
  button-secondary-hover:
    backgroundColor: "{colors.navy-soft}"
    textColor: "{colors.navy}"
    rounded: "{rounded.xl}"
    padding: "10px 20px"
  input:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.xl}"
    padding: "12px 16px"
  pill-default:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.xl}"
    padding: "12px 16px"
  pill-selected:
    backgroundColor: "{colors.navy}"
    textColor: "{colors.paper}"
    rounded: "{rounded.xl}"
    padding: "12px 16px"
  day-tile-default:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.xl}"
    padding: "8px 8px"
  day-tile-selected:
    backgroundColor: "{colors.navy}"
    textColor: "{colors.paper}"
    rounded: "{rounded.xl}"
    padding: "8px 8px"
  time-block:
    backgroundColor: "{colors.navy}"
    textColor: "{colors.paper}"
    rounded: "{rounded.xl}"
    padding: "8px 16px"
---

# Design System: GoodNext

## Overview

**Creative North Star: "The Forecast, Not the Form"**

GoodNext borrows a shape people already read correctly — today big, the rest of the week small — and refuses to look like the thing it must not be mistaken for: a benefits portal's list of identical rows. Decision 007 turned down a Checkout Receipt world specifically because it carried more identity than a scannable task screen needs. What shipped instead spends almost the whole page on structure and words, and saves color for two jobs only: something a resident can press, and something they can count.

The result reads as calm rather than unfinished. One typeface carries a giant amber count numeral, a navy header field, and an eight-word source line at the same weight of restraint. Nothing on the screen competes with the number the whole page exists to answer.

Two confirmed rejections shape everything below: no dark theme (the use scene is a daylight phone or a library terminal, never a dim room), and no device the system doesn't already use natively — no hard-offset shadow, no icon glyph, no second typeface waiting to become "the brand font."

**Key Characteristics:**
- One accent color, rationed to pressable and countable things only.
- A single navy field carries almost all of the screen's visual weight; everything else is paper, ink, or a thin line.
- One typeface, one tabular-numeral rule, no display face.
- Two radii, two shadows, and a hard rule that a shadow and a border never share an element.
- Status is always a sentence first, a color second.

## Colors

The palette is nearly monochrome on purpose: one structural color (navy), one accent (amber) rationed to two jobs, and paper/ink/line carrying everything else.

### Primary
- **Listing Amber** (#ffb703): the one color reserved for anything a resident can press or count — Directions, Try another ZIP, Retry, Change my answers, the form's own submit, and the day's count numeral. It never appears as decoration or structure.
- **Amber Deep** (#8a5a00): the same accent stepped down for contrast. It's the day tile's own listed-count color on white, and it's also where every primary amber action lands on hover and press, with its label flipping to paper so contrast holds.

### Secondary
- **Field Navy** (#0b2a4a): the header field and the result panel, every text link, the global focus ring, and the selected state on pills and day tiles. This is the identity color; it carries the "not a portal" weight amber can't.
- **Navy Soft** (#dbe6f2): secondary text sitting on the navy panel (the "nothing listed" line, an open day-tile's own count), and the pale wash behind the folded answer summary.

### Neutral
- **Paper** (#ffffff): page and card background.
- **Ink** (#141414): primary body text, and the text color on amber buttons.
- **Ink Soft** (#3d4653): secondary text — helper copy, source lines — and the input field's own border, chosen because it clears 3:1 against paper where the lighter `line` token would not.
- **Line** (#cfd6df): decorative section borders only — help routes, the unconfirmed list, a closed day tile. It never carries text and never appears on the same element as a shadow.
- **Alert Red** (#a4211f): validation and failure text only — the ZIP error, the temporarily-unavailable message.

### Named Rules
**The One Pressable Color Rule.** Amber appears only on something a resident can press or something they can count. Everything else on screen is navy, paper, ink, or line.
**The Word-First Status Rule.** Every state — submitting, delayed, partial, no-match, unavailable — is a sentence before it is a color. Color is a second signal, never the only one.
**The State-Is-A-Color-Step Rule.** Every hover or active state is a deeper or softer step of the same palette — amber to amber-deep, a navy outline filling with navy-soft, a thin underline thickening — never a new hue and never a shadow. `transition-colors` carries the change and `prefers-reduced-motion` removes it cleanly.

## Typography

**Body Font:** the system sans stack (`ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`), with no separate display face.

**Character:** one typeface carries every role, from the four-digit count down to the source-date caption. Numerals are tabular throughout the body copy, so a changing count never reflows its neighbors.

### Hierarchy
- **Display** (bold, 700, 3rem / `text-5xl`, leading-none, -0.02em): the day's listed-option count. The single largest thing on the screen, in amber, inside the navy panel.
- **Headline** (bold, 700, 1.5rem scaling to 2.25rem at 640px, -0.02em): the result heading ("Food today, [date]") and the site's own wordmark share this class, so the name and the answer read as one voice.
- **Title** (semibold, 600, 1.125rem, up to 1.25rem for the form's own heading): section and card headings — a provider's name, "Later this week," "Need more help?"
- **Body** (regular, 400, 1rem): claim text on every card — cost, requirements, freshness, inventory caveats.
- **Label** (medium, 500, 0.875rem down to 0.75rem for captions): helper text under form fields, the tagline, the day tile's uppercase weekday abbreviation, and the smallest source/checked-date line.

### Named Rules
**The One Typeface Rule.** The system sans stack is the whole hierarchy, from the count to the caption. No serif, no display face, no icon font. This is a deliberate OWN-WORLD choice, not a placeholder waiting for a brand font.

## Layout

Single column to 640px (`max-w-2xl`, centered, 16px side padding); page sections stack with 32px of rhythm between them, and items within a section keep 16px. At 640px and up, the option card's time block breaks out to a fixed 128px left column and the card itself turns row-direction; the six day tiles move from a 3-column grid to one row of six. Every text-bearing element defends against overflow — balanced wrapping, `break-words`, or `overflow-wrap: anywhere` on URLs and long strings — so a long provider name or a 30%-longer Spanish string never breaks the grid.

Print is its own layout, not an afterthought: the form, every button, and the day-tile strip disappear; everything renders flat black on white; the result panel, the option cards, and the help-routes section keep a 1px black rule so their shape survives on paper.

## Elevation & Depth

The system is mostly flat. The two shadows that exist are both soft and diffuse, never a hard offset. A card gets a shadow to read as an object resting on the page; a pressable amber action gets a slightly stronger version of the same shadow to read as raised. Nothing else casts one — a section that isn't a card (help routes, the unconfirmed list) gets a 1px line border instead, and a shadow and a border never appear on the same element.

### Shadow Vocabulary
- **Card** (`box-shadow: 0 2px 10px rgba(11,42,74,0.12)`): the option card and an unfolded day-tile entry.
- **Action** (`box-shadow: 0 2px 8px rgba(11,42,74,0.18)`): every amber pressable — Directions, the form's submit, Try another ZIP, Retry.

### Named Rules
**The Shadow-Or-Border Rule.** An element gets a soft shadow or a 1px line border, never both.

## Shapes

Two radii carry the whole system. Cards, the result panel, and the bordered sections (help routes, the unconfirmed list) use a generous 16px corner that reads as a resting object. Everything a resident touches or types into — buttons, pills, inputs, day tiles, the time block — uses a tighter 12px corner, so touch targets read as one family distinct from the cards that hold them. No sharp corners, and no fully-rounded pill-shaped control anywhere.

### Named Rules
**The Two-Radius Rule.** 16px for anything you rest on; 12px for anything you press or type into. No third radius.

## Components

### Buttons
- **Shape:** 12px corner.
- **Primary:** amber background, ink text, semibold, `10px 20px` padding and the Action shadow — the form's own submit is larger (`12px 24px`, 18px text) but otherwise identical. Disabled state (submit only) drops to 60% opacity; the shadow stays.
- **Secondary:** transparent background, 1px navy border, navy text, same padding, no shadow. Used beside a primary action for a lower-stakes choice — Cancel, Print this list.
- **Hover / Active:** primary deepens to amber-deep with paper text; secondary fills with navy-soft, keeping its navy border and text. Both run on `transition-colors`, stripped by `prefers-reduced-motion`.
- **Focus:** every button takes the global 3px navy outline at a 2px offset.

### Text Links
- **Style:** navy, medium weight, underlined at a 4px offset.
- **Hover:** the underline thickens from 1px to 2px; color and weight don't change.

### Pills (radio and checkbox choices)
- **Style:** 12px corner, 1px border. Unselected: line border, paper background, ink text, shifting to a navy border on hover. Selected: navy background and border, paper text.
- **Behavior:** the native input sits visually hidden inside the styled label, so keyboard and screen-reader semantics stay with the browser's own control.

### Cards
- **Corner:** 16px.
- **Background:** paper.
- **Shadow:** the Card shadow; no border.
- **Internal padding:** 16px, with a 12–20px gap between the time block and the claims column depending on viewport.

### Time Block
- **Style:** navy background, paper text, 12px corner; stacked (open time, "to," close time) at 640px and up, inline on mobile. A record whose text doesn't parse into an open/close pair falls back to a single centered sentence in the same chip.

### Day Tile
- **Style:** 12px corner, 1px border, vertically centered. The count is the tile's dominant line (1rem, semibold); the weekday and day number above it are secondary, smaller text. A zero-listing day renders as a static `ink-soft` block with a smaller count label, not a button; a day with listings is a real button that toggles open or closed, one at a time, with its count switching from amber-deep on white to paper on the open navy tile.
- **Hover / Active:** a closed tile takes a navy border on hover and fills with navy-soft on press.

### Inputs / Fields
- **Style:** paper background, 1px `ink-soft` border, 12px corner, 18px text sized for a phone.
- **Focus:** the global 3px navy outline at a 2px offset — no separate glow or border-color change.
- **Error:** the field's own alert-red text appears beneath it in a live-announced line; the border does not change color.

### Result Panel
- **Style:** navy background, paper text, 16px corner, `20px/24px` padding at rest and `28px/32px` at 640px and up. Carries the date headline and the amber count as one unit; this is the screen's one deliberately oversized surface.
- **Focus:** the heading takes programmatic focus on every result, so a keyboard or screen-reader user lands on the answer, but the visible ring is suppressed there since it isn't a real interactive target.

## Do's and Don'ts

### Do:
- **Do** keep amber to things a resident can press or count. Nothing else earns it.
- **Do** pair every status with a sentence, not just a color change.
- **Do** use the Card shadow and the 1px line border as alternatives, never together.
- **Do** carry the 12px/16px corner split into any new control or container.
- **Do** trust the palette's own contrast — every shipped text/background pair already clears 5.9:1; don't dial back to a lighter tint for "softness."
- **Do** respect `prefers-reduced-motion`: the global rule strips every transition and animation, including the day tile's expand/collapse and every hover/active color shift, with no fallback state to design around.
- **Do** carry the browser-chrome theming — amber-on-ink text selection, navy-on-navy-soft scrollbar, tabular numerals — into any new page; it's a sitewide rule, not a one-off.

### Don't:
- **Don't** add a second typeface, a display serif, or an icon set. The system sans and text alone carry the whole hierarchy.
- **Don't** give any hover or active state a new hue, a shadow, or a size change — the vocabulary is a deeper/softer step of the existing palette, or a thicker underline, nothing else.
- **Don't** use `line` (#cfd6df) for anything but a decorative section border; it is not a text or icon color.
- **Don't** reach for a hard-offset or neobrutalist shadow. Both shadows in this system are soft and diffuse.
