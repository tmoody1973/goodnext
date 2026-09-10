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
    delayed: "Still checking. You can wait, or use one of these help routes.",
    cancel: "Cancel",
  },
  actions: {
    retry: "Try again",
    change: "Change my answers",
  },
  help: {
    heading: "Need more help?",
    checked: "Checked {date}",
  },
  noMatch: {
    statement: "Nothing is listed for {zip} today.",
    tryAnother: "Try another ZIP",
  },
  week: {
    heading: "Later this week",
    listed: "{n} listed",
    oneListed: "1 listed",
    nothing: "Nothing listed",
  },
  summary: {
    change: "Change",
    money: "${money}",
    minutes: "up to {n} min",
    label: "Your answers",
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
    // The count is the panel's focal number; the label sits beside it.
    listedToday: "listed today",
    noneListedToday: "Nothing listed for today.",
  },
  card: {
    directions: "Directions",
    call: "Call {phone}",
    // Read out of context by a screen reader, so each link also names its
    // provider. The visible text stays the start of the label.
    directionsLabel: "Directions to {provider}",
    callLabel: "Call {phone}, {provider}",
  },
  print: {
    action: "Print this list",
  },
  unconfirmed: {
    heading: "Not checked recently. Call before you go.",
  },
  entry: {
    label: "What do you need?",
    food: "Find food today",
    letter: "Understand my letter",
  },
  notice: {
    heading: "Understand my letter",
    fileLabel: "Your letter (PDF or photo)",
    limits: "PDF, JPG, or PNG up to 10 MB and 6 pages.",
    consent: "Your letter is read once to find what it asks and is not stored.",
    submit: "Read my letter",
    manualLink: "No file? Answer three questions instead",
    uploadLink: "Upload the letter instead",
    kindLabel: "What kind of letter is it?",
    kinds: {
      sanction: "Notice of Sanction",
      time_limited_warning: "Time-limited benefits letter",
      six_month_report: "Six-month report letter",
      unknown: "Not sure",
    },
    dateLabel: "What date does it show, if any? (optional)",
    asksLabel: "What does it seem to ask you to do? (optional)",
    manualSubmit: "Read my answers",
    checking: "Reading your letter.",
    estimate: "This usually takes under a minute.",
    fileMissing: "Choose a file first, or answer the three questions.",
    result: {
      kinds: {
        sanction: "Notice of Sanction",
        time_limited_warning: "Time-limited benefits letter",
        six_month_report: "Six-month report letter",
        unknown: "We could not tell what this letter is",
      },
      screening: {
        action_identified: "Something to do",
        more_information_needed: "More information needed",
        no_action_identified: "No action identified in this letter",
      },
      says: "What your letter says",
      fromLetter: "From your letter",
      page: "Page {n}",
      nextStep: "Your next step",
      tasks: "Tasks",
      dateNotStated: "Date not stated in the letter",
      dateKinds: {
        official: "Official date",
        continuity: "Date that affects your benefits",
        suggested: "Suggested date",
        unknown: "",
      },
      questions: "Questions to ask your agency",
      contacts: "Who to contact",
      unknowns: "What we can't tell from this letter",
      findFood: "Find food today",
      another: "Check another letter",
      notGovernment: "GoodNext is not your agency. Only your agency decides your case.",
    },
  },
} as const;

export function fill(template: string, values: Record<string, string>): string {
  return template.replace(/\{(\w+)\}/g, (_, key: string) => values[key] ?? "");
}
