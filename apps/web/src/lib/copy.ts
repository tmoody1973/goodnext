// Every resident-facing string lives here so the never-list test can scan it
// and so Spanish can follow as one file. Use CONTEXT.md terms; avoid the
// avoid-lists. Keep sentences short.

export const copy = {
  site: {
    name: "GoodNext",
    tagline: "Not a government service",
    description: "Find food today in Milwaukee. No account, no notice, no benefits question.",
  },
  form: {
    heading: "Find food today",
    zipLabel: "ZIP code",
    zipHelp: "Five digits, like 53206.",
    zipInvalid: "Enter a five-digit ZIP code.",
    moneyLabel: "Money you can spend on food this week",
    moneyHelp: "Zero is fine.",
    kitchenLabel: "Your kitchen",
    kitchen: {
      full: "Full kitchen",
      microwave_only: "Microwave only",
      none: "No kitchen",
    },
    travelLabel: "How you get around",
    travelHelp: "Pick every way that works for you.",
    travel: { walk: "Walk", bus: "Bus", car: "Car", ride: "Ride" },
    travelInvalid: "Pick at least one way you get around.",
    minutesLabel: "Up to how many minutes each way (optional)",
    submit: "Show food today",
  },
  wait: {
    checking: "Checking today's listings for {zip}.",
    estimate: "This usually takes one to two minutes.",
  },
  result: {
    heading: "Food today, {date}",
    status: {
      success: "Listed options found.",
      partial: "Some suggestions were left out because they did not pass our checks.",
      no_match: "Nothing is listed for this ZIP today.",
      needs_clarification: "We could not build a list for that answer.",
      denied: "We could not build a list for that answer.",
      temporarily_unavailable: "Temporarily unavailable. Try again in a moment.",
    },
    unreachable: "We could not reach the service. Try again in a moment.",
    listedToday: "{n} listed today",
    oneListedToday: "1 listed today",
    noneListedToday: "Nothing listed for today.",
  },
  card: {
    directions: "Directions",
    call: "Call {phone}",
  },
  unconfirmed: {
    heading: "Not checked recently. Call before you go.",
  },
} as const;

export function fill(template: string, values: Record<string, string>): string {
  return template.replace(/\{(\w+)\}/g, (_, key: string) => values[key] ?? "");
}
