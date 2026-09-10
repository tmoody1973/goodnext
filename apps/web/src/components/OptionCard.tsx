import type { PlannedVisit } from "@/lib/api";
import { copy, fill } from "@/lib/copy";
import { telHref } from "@/lib/phone";
import { primaryActionClass, textLinkClass } from "@/lib/styles";

// "Open today from 8:30 AM to 12:00 PM" -> ["8:30 AM", "12:00 PM"]; anything
// else (closed, next open) is shown as its own sentence in the time block.
const WINDOW = /from (.+?) to (.+)$/;

// Spec S10: the card renders the API's permitted claims, in this order, and
// nothing the model wrote free-hand. Claims are built by the validator.
export function OptionCard({ visit }: { visit: PlannedVisit }) {
  const c = visit.claims;
  if (!c) return null;
  const window = WINDOW.exec(c.open_today_text);
  const tel = visit.contact ? telHref(visit.contact) : null;
  return (
    <article className="flex flex-col gap-3 rounded-2xl bg-paper p-4 shadow-[0_2px_10px_rgba(11,42,74,0.12)] sm:flex-row sm:gap-5">
      <div className="flex shrink-0 flex-wrap items-baseline gap-x-2 self-start rounded-xl bg-navy px-4 py-2 text-paper sm:w-32 sm:flex-col sm:items-stretch sm:gap-0 sm:py-3 sm:text-center print:border print:border-ink">
        {window ? (
          <>
            <span className="text-xl font-bold leading-tight">{window[1]}</span>
            <span className="text-sm text-navy-soft">to</span>
            <span className="text-xl font-bold leading-tight">{window[2]}</span>
          </>
        ) : (
          <span className="text-base font-semibold text-balance">{c.open_today_text}</span>
        )}
      </div>
      <div className="flex min-w-0 flex-1 flex-col gap-1">
        <h2 className="text-lg font-semibold text-balance break-words">{visit.provider}</h2>
        <p className="font-medium">{c.cost_label}</p>
        <p>{c.requirements_text}</p>
        {c.appointment_text && <p>{c.appointment_text}</p>}
        {c.service_area_text && <p className="font-medium">{c.service_area_text}</p>}
        <p>{c.freshness_text}</p>
        <p className="font-medium">{c.inventory_text}</p>
        <p className="text-sm text-ink-soft">{c.travel_echo}</p>
        <div className="mt-2 flex flex-wrap items-center gap-x-5 gap-y-2">
          <a
            href={c.directions_url}
            target="_blank"
            rel="noopener noreferrer"
            aria-label={fill(copy.card.directionsLabel, { provider: visit.provider })}
            className={`${primaryActionClass} print:hidden`}
          >
            {copy.card.directions}
          </a>
          {tel ? (
            <a href={tel} aria-label={fill(copy.card.callLabel, { phone: visit.contact, provider: visit.provider })} className={textLinkClass}>
              {fill(copy.card.call, { phone: visit.contact })}
            </a>
          ) : (
            visit.contact && <span className="text-ink-soft">{visit.contact}</span>
          )}
        </div>
        {c.source_text && <p className="mt-1 text-xs text-ink-soft">{c.source_text}</p>}
      </div>
    </article>
  );
}
