"use client";

import { useId, useState } from "react";
import type { DayPlan, PlannedVisit } from "@/lib/api";
import { copy, fill } from "@/lib/copy";
import { formatTileDate } from "@/lib/format";
import { telHref } from "@/lib/phone";

// CONTEXT.md "Later this week": days two to seven of the Bridge Plan, shown as
// tiles that unfold one at a time. Listed, never promised. Later-day entries use
// the record's own schedule_text; the per-day claim text is not trustworthy for
// future days until MOO-781 lands, and the inventory line belongs to today only.
export function WeekTiles({ days }: { days: DayPlan[] }) {
  const [open, setOpen] = useState<string | null>(null);
  const panelId = useId();
  if (days.length === 0) return null;
  const openDay = days.find((d) => d.date === open);
  return (
    <section aria-labelledby="week-heading" className="flex flex-col gap-3">
      <h2 id="week-heading" className="text-lg font-semibold">{copy.week.heading}</h2>
      <ul className="grid grid-cols-3 gap-2 sm:grid-cols-6">
        {days.map((day) => {
          const n = day.visits.length;
          const { weekday, day: dayLabel } = formatTileDate(day.date);
          const isOpen = open === day.date;
          const count = n === 0 ? copy.week.nothing : n === 1 ? copy.week.oneListed : fill(copy.week.listed, { n: String(n) });
          const cls = `flex w-full flex-col items-center rounded-xl border px-2 py-2 text-center [overflow-wrap:anywhere] ${
            isOpen ? "border-navy bg-navy text-paper" : "border-line bg-paper text-ink"
          }`;
          return (
            <li key={day.date}>
              {n === 0 ? (
                <div className={`${cls} text-ink-soft`}>
                  <span className="text-xs font-semibold uppercase">{weekday}</span>
                  <span className="text-sm">{dayLabel}</span>
                  <span className="mt-1 text-xs">{count}</span>
                </div>
              ) : (
                <button
                  type="button"
                  aria-expanded={isOpen}
                  aria-controls={panelId}
                  onClick={() => setOpen(isOpen ? null : day.date)}
                  className={cls}
                >
                  <span className="text-xs font-semibold uppercase">{weekday}</span>
                  <span className="text-sm">{dayLabel}</span>
                  <span className={`mt-1 text-xs font-medium ${isOpen ? "text-navy-soft" : "text-amber-deep"}`}>{count}</span>
                </button>
              )}
            </li>
          );
        })}
      </ul>
      <div id={panelId} hidden={!openDay}>
        {openDay && (
          <ul className="flex flex-col gap-3">
            {openDay.visits.map((v) => (
              <li key={v.resource_id}>
                <DayEntry visit={v} />
              </li>
            ))}
          </ul>
        )}
      </div>
    </section>
  );
}

function DayEntry({ visit }: { visit: PlannedVisit }) {
  const c = visit.claims;
  const tel = visit.contact ? telHref(visit.contact) : null;
  return (
    <article className="flex flex-col gap-1 rounded-2xl bg-paper p-4 shadow-[0_2px_10px_rgba(11,42,74,0.12)]">
      <h3 className="font-semibold text-balance">{visit.provider}</h3>
      <p className="font-medium">{visit.schedule_text}</p>
      {c && <p>{c.cost_label}</p>}
      {c && <p>{c.freshness_text}</p>}
      <p className="flex flex-wrap gap-x-4 gap-y-1">
        {c?.directions_url && (
          <a href={c.directions_url} target="_blank" rel="noopener noreferrer" aria-label={fill(copy.card.directionsLabel, { provider: visit.provider })} className="font-medium text-navy underline underline-offset-4">
            {copy.card.directions}
          </a>
        )}
        {tel ? (
          <a href={tel} aria-label={fill(copy.card.callLabel, { phone: visit.contact, provider: visit.provider })} className="font-medium text-navy underline underline-offset-4">{fill(copy.card.call, { phone: visit.contact })}</a>
        ) : (
          visit.contact && <span className="text-ink-soft">{visit.contact}</span>
        )}
      </p>
    </article>
  );
}
