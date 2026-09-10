// The two action treatments, shared by the form, the result, and the cards.
// Amber is for things that can be pressed; on hover and press it deepens and
// the label flips to paper so contrast holds. Transitions are removed by the
// reduced-motion rule in globals.css.
export const primaryActionClass =
  "self-start rounded-xl bg-amber px-5 py-2.5 font-semibold text-ink shadow-[0_2px_8px_rgba(11,42,74,0.18)] transition-colors hover:bg-amber-deep hover:text-paper active:bg-amber-deep active:text-paper";

export const secondaryActionClass =
  "self-start rounded-xl border border-navy px-5 py-2.5 font-semibold text-navy transition-colors hover:bg-navy-soft active:bg-navy-soft";

export const textLinkClass = "font-medium text-navy underline underline-offset-4 hover:decoration-2";
