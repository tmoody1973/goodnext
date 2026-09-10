import type { NoticeData, NoticePassage } from "@/lib/api";
import { copy, fill } from "@/lib/copy";
import { telHref } from "@/lib/phone";
import { primaryActionClass, secondaryActionClass, textLinkClass } from "@/lib/styles";
import { useFocusOnMount } from "@/lib/useFocusOnMount";

const r = copy.notice.result;

// A passage from the letter, shown beside the finding it supports (PRD FR02).
function Passages({ ids, byId }: { ids: string[]; byId: Map<string, NoticePassage> }) {
  const passages = ids.map((id) => byId.get(id)).filter((p): p is NoticePassage => Boolean(p));
  if (passages.length === 0) return null;
  return (
    <div className="flex flex-col gap-2">
      {passages.map((p) => (
        <blockquote key={p.id} className="rounded-2xl bg-navy-soft px-4 py-3 text-sm print:border print:border-ink">
          <p>{p.text}</p>
          <footer className="mt-1 text-xs text-ink-soft">
            <span>{r.fromLetter}</span>, <span>{fill(r.page, { n: String(p.page) })}</span>
          </footer>
        </blockquote>
      ))}
    </div>
  );
}

// Spec: the screen renders only the validated proposal fields and the passages.
export function NoticeResult({ data, onFindFood, onAnother }: { data: NoticeData; onFindFood: () => void; onAnother: () => void }) {
  const headingRef = useFocusOnMount<HTMLHeadingElement>();
  const byId = new Map(data.passages.map((p) => [p.id, p]));
  const hasTasks = data.tasks.length > 0;
  return (
    <div className="flex flex-col gap-4">
      <div className="rounded-2xl bg-navy px-5 py-6 text-paper sm:px-7 sm:py-8 print:border print:border-ink">
        <h1 ref={headingRef} tabIndex={-1} className="text-2xl font-bold text-balance break-words outline-none sm:text-4xl sm:tracking-[-0.02em]">
          {r.kinds[data.letter_kind]}
        </h1>
        <p className="mt-2 text-xl font-semibold">{r.screening[data.screening]}</p>
        {data.explanation && <p className="mt-3 text-navy-soft">{data.explanation}</p>}
      </div>

      {data.findings.length > 0 && (
        <section aria-labelledby="says-heading" className="flex flex-col gap-3">
          <h2 id="says-heading" className="text-lg font-semibold">{r.says}</h2>
          {data.findings.map((f, i) => (
            <article key={i} className="flex flex-col gap-3 rounded-2xl bg-paper p-4 shadow-[0_2px_10px_rgba(11,42,74,0.12)]">
              <h3 className="font-semibold">{f.label}</h3>
              <p>{f.text}</p>
              <Passages ids={f.passage_ids} byId={byId} />
            </article>
          ))}
        </section>
      )}

      {data.next_step && (
        <section aria-labelledby="next-heading" className="flex flex-col gap-3 rounded-2xl border border-line px-4 py-4">
          <h2 id="next-heading" className="text-lg font-semibold">{r.nextStep}</h2>
          <p className="font-medium">{data.next_step.text}</p>
          <Passages ids={data.next_step.passage_ids} byId={byId} />
        </section>
      )}

      {hasTasks && (
        <section aria-labelledby="tasks-heading" className="flex flex-col gap-3">
          <h2 id="tasks-heading" className="text-lg font-semibold">{r.tasks}</h2>
          <ul aria-label={r.tasks} className="flex flex-col gap-3">
            {data.tasks.map((t, i) => (
              <li key={i} className="flex flex-col gap-1 rounded-2xl bg-paper p-4 shadow-[0_2px_10px_rgba(11,42,74,0.12)]">
                <p className="font-medium">{t.text}</p>
                <p className="text-sm">
                  {t.date_text === "not stated" ? r.dateNotStated : (
                    <>
                      <span className="font-semibold">{t.date_text}</span>
                      {r.dateKinds[t.date_kind] && <span className="text-ink-soft"> ({r.dateKinds[t.date_kind]})</span>}
                    </>
                  )}
                </p>
                <p className="text-xs text-ink-soft">
                  {r.fromLetter}, {[...new Set(t.passage_ids.map((id) => byId.get(id)?.page).filter(Boolean))].map((n) => fill(r.page, { n: String(n) })).join(", ").toLowerCase()}
                </p>
              </li>
            ))}
          </ul>
        </section>
      )}

      {data.questions_to_ask.length > 0 && (
        <section aria-labelledby="questions-heading" className="flex flex-col gap-2 rounded-2xl border border-line px-4 py-4">
          <h2 id="questions-heading" className="text-lg font-semibold">{r.questions}</h2>
          <ul className="flex list-disc flex-col gap-1 pl-5">
            {data.questions_to_ask.map((q, i) => <li key={i}>{q.text}</li>)}
          </ul>
        </section>
      )}

      {data.routes.length > 0 && (
        <section aria-labelledby="contacts-heading" className="flex flex-col gap-2 rounded-2xl border border-line px-4 py-4">
          <h2 id="contacts-heading" className="text-lg font-semibold">{r.contacts}</h2>
          <ul className="flex flex-col gap-2">
            {data.routes.map((route) => {
              const tel = route.phone ? telHref(route.phone) : null;
              return (
                <li key={route.name} className="flex flex-col gap-0.5">
                  <p className="font-semibold">{route.name}</p>
                  <p className="flex flex-wrap gap-x-4">
                    {route.phone && (tel ? (
                      <a href={tel} aria-label={fill(copy.card.callLabel, { phone: route.phone, provider: route.name })} className={textLinkClass}>{fill(copy.card.call, { phone: route.phone })}</a>
                    ) : (
                      <span className="font-medium">{route.phone}</span>
                    ))}
                    {route.url && (
                      <a href={route.url} target="_blank" rel="noopener noreferrer" className={`${textLinkClass} [overflow-wrap:anywhere]`}>{new URL(route.url).hostname}</a>
                    )}
                  </p>
                  <p className="text-xs text-ink-soft">{route.source}</p>
                </li>
              );
            })}
          </ul>
        </section>
      )}

      {data.unknowns.length > 0 && (
        <section aria-labelledby="unknowns-heading" className="flex flex-col gap-2 rounded-2xl border border-line px-4 py-4">
          <h2 id="unknowns-heading" className="text-lg font-semibold">{r.unknowns}</h2>
          <ul className="flex list-disc flex-col gap-1 pl-5">
            {data.unknowns.map((u, i) => <li key={i}>{u}</li>)}
          </ul>
        </section>
      )}

      <p className="text-sm text-ink-soft">{r.notGovernment}</p>

      <div className="flex flex-wrap gap-3">
        <button type="button" onClick={onFindFood} className={primaryActionClass}>{r.findFood}</button>
        <button type="button" onClick={onAnother} className={secondaryActionClass}>{r.another}</button>
      </div>
    </div>
  );
}
