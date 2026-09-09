"use client";

import { useEffect, useRef, useState } from "react";
import { ConstraintForm, toConstraints, type FormValues } from "@/components/ConstraintForm";
import { HelpRoutes } from "@/components/HelpRoutes";
import { OptionCard } from "@/components/OptionCard";
import { SummaryLine } from "@/components/SummaryLine";
import { WeekTiles } from "@/components/WeekTiles";
import { postPlan, type Envelope, type HelpRoute, type PlanData } from "@/lib/api";
import { copy, fill } from "@/lib/copy";
import { formatPlanDate } from "@/lib/format";
import { telHref } from "@/lib/phone";

// PRD section 8: after 30 s of waiting, show explicit delayed status.
export const DELAYED_AFTER_MS = 30_000;

type State =
  | { kind: "idle" }
  | { kind: "submitting"; zip: string; delayed: boolean }
  | { kind: "done"; envelope: Envelope };

// A network failure looks like the API's own 503 to the resident.
function unreachableEnvelope(): Envelope {
  return { status: "temporarily_unavailable", data: null, evidence: [], missing: [], warnings: ["unreachable"], retryable: true, request_id: "local" };
}

// The form folds away when a result lands, which would drop keyboard focus on
// the body. Move it to the result heading so a keyboard or screen-reader user
// starts reading at the answer.
function useFocusOnMount<T extends HTMLElement>() {
  const ref = useRef<T>(null);
  useEffect(() => {
    ref.current?.focus();
  }, []);
  return ref;
}

function focusZip() {
  const zip = document.getElementById("zip");
  zip?.scrollIntoView?.({ block: "center" });
  zip?.focus();
}

export default function FoodTodayPage() {
  const [state, setState] = useState<State>({ kind: "idle" });
  // The last help routes any response carried; shown while waiting and on failures.
  const [routes, setRoutes] = useState<HelpRoute[]>([]);
  // The answers behind the current result; the form folds into a summary of them.
  const [submitted, setSubmitted] = useState<FormValues | null>(null);
  const [editing, setEditing] = useState(true);
  const lastValues = useRef<FormValues | null>(null);
  const controller = useRef<AbortController | null>(null);

  useEffect(() => {
    if (state.kind !== "submitting" || state.delayed) return;
    const timer = setTimeout(() => setState((s) => (s.kind === "submitting" ? { ...s, delayed: true } : s)), DELAYED_AFTER_MS);
    return () => clearTimeout(timer);
  }, [state]);

  async function submit(next: FormValues) {
    lastValues.current = next;
    setSubmitted(next);
    setEditing(false);
    controller.current?.abort();
    const ac = new AbortController();
    controller.current = ac;
    setState({ kind: "submitting", zip: next.zip, delayed: false });
    try {
      const envelope = await postPlan(toConstraints(next), ac.signal);
      if (ac.signal.aborted) return;
      if (envelope.help_routes?.length) setRoutes(envelope.help_routes);
      setState({ kind: "done", envelope });
    } catch (error) {
      if (ac.signal.aborted || (error instanceof DOMException && error.name === "AbortError")) return;
      setState({ kind: "done", envelope: unreachableEnvelope() });
    }
  }

  function cancel() {
    controller.current?.abort();
    setState({ kind: "idle" });
    reopen();
  }

  // Show the form again with its values intact (it never unmounts) and put the
  // cursor in the ZIP field.
  function reopen() {
    setEditing(true);
    setTimeout(focusZip, 0);
  }

  function retry() {
    if (lastValues.current) void submit(lastValues.current);
  }

  const busy = state.kind === "submitting";

  return (
    <main className="mx-auto flex w-full max-w-2xl flex-col gap-8 px-4 py-6">
      <header className="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1">
        <p className="text-2xl font-bold tracking-[-0.02em] text-navy">{copy.site.name}</p>
        <p className="text-sm text-ink-soft">{copy.site.tagline}</p>
      </header>

      {!editing && submitted && <SummaryLine values={submitted} onChange={reopen} />}
      <div hidden={!editing}>
        <ConstraintForm busy={busy} onSubmit={submit} />
      </div>

      <section aria-live="polite" className="flex flex-col gap-4">
        {state.kind === "submitting" && (
          <div className="flex flex-col gap-2">
            <p className="font-medium">{fill(copy.wait.checking, { zip: state.zip })}</p>
            <p className="text-ink-soft">{copy.wait.estimate}</p>
            {state.delayed && (
              <>
                <p role="status" className="font-medium">{copy.wait.delayed}</p>
                <button type="button" onClick={cancel} className={secondaryActionClass}>
                  {copy.wait.cancel}
                </button>
                <HelpRoutes routes={routes} />
              </>
            )}
          </div>
        )}
        {state.kind === "done" && (
          <Result
            envelope={state.envelope}
            zip={submitted?.zip ?? ""}
            routes={state.envelope.help_routes?.length ? state.envelope.help_routes : routes}
            onRetry={retry}
            onChange={reopen}
          />
        )}
      </section>
    </main>
  );
}

// Spec: today's visits are the plan's first day. food_today mirrors it.
function todayVisits(data: PlanData) {
  return data.days.find((d) => d.date === data.start_date)?.visits ?? data.food_today;
}

// Later this week: every day after the start date, in order.
function laterDays(data: PlanData) {
  return data.days.filter((d) => d.date > data.start_date).slice(0, 6);
}

function countLine(n: number) {
  if (n === 0) return copy.result.noneListedToday;
  if (n === 1) return copy.result.oneListedToday;
  return fill(copy.result.listedToday, { n: String(n) });
}

type ResultProps = { envelope: Envelope; zip: string; routes: HelpRoute[]; onRetry: () => void; onChange: () => void };

const actionClass = "self-start rounded-xl bg-amber px-5 py-2.5 font-semibold text-ink shadow-[0_2px_8px_rgba(11,42,74,0.18)]";
const secondaryActionClass = "self-start rounded-xl border border-navy px-5 py-2.5 font-semibold text-navy";

function Result({ envelope, zip, routes, onRetry, onChange }: ResultProps) {
  const headingRef = useFocusOnMount<HTMLHeadingElement>();
  const data = envelope.data;
  const hasPlan = (envelope.status === "success" || envelope.status === "partial") && data !== null;
  const visits = hasPlan ? todayVisits(data) : [];
  if (envelope.status === "no_match") {
    return (
      <div className="flex flex-col gap-4">
        <div className="rounded-2xl bg-navy px-5 py-4 text-paper">
          <h1 ref={headingRef} tabIndex={-1} className="text-2xl font-bold text-balance outline-none">{fill(copy.noMatch.statement, { zip })}</h1>
        </div>
        <HelpRoutes routes={routes} />
        <button type="button" onClick={onChange} className={actionClass}>{copy.noMatch.tryAnother}</button>
      </div>
    );
  }
  if (envelope.status === "temporarily_unavailable") {
    return (
      <div className="flex flex-col gap-4">
        <p role="alert" className="font-medium text-alert">{copy.result.status.temporarily_unavailable}</p>
        <button type="button" onClick={onRetry} className={actionClass}>{copy.actions.retry}</button>
        <HelpRoutes routes={routes} />
      </div>
    );
  }
  if (envelope.status === "needs_clarification" || envelope.status === "denied") {
    return (
      <div className="flex flex-col gap-4">
        <p role="alert" className="font-medium">{copy.result.status[envelope.status]}</p>
        <button type="button" onClick={onChange} className={actionClass}>{copy.actions.change}</button>
        <HelpRoutes routes={routes} />
      </div>
    );
  }
  return (
    <div className="flex flex-col gap-4">
      <div className="rounded-2xl bg-navy px-5 py-4 text-paper print:border print:border-ink">
        {data?.start_date && (
          <h1 ref={headingRef} tabIndex={-1} className="text-2xl font-bold text-balance outline-none">{fill(copy.result.heading, { date: formatPlanDate(data.start_date) })}</h1>
        )}
        <p className="mt-1 text-navy-soft">{hasPlan ? countLine(visits.length) : copy.result.status[envelope.status]}</p>
      </div>
      {hasPlan && (visits.length > 0 || data.unconfirmed.length > 0) && (
        <button type="button" onClick={() => window.print()} className={secondaryActionClass}>
          {copy.print.action}
        </button>
      )}
      {envelope.status === "partial" && <p className="font-medium">{copy.result.status.partial}</p>}
      {visits.map((v) => (
        <OptionCard key={v.resource_id} visit={v} />
      ))}
      {hasPlan && data.unconfirmed.length > 0 && (
        <section className="flex flex-col gap-1 rounded-2xl border border-line px-4 py-3">
          <h2 className="font-semibold">{copy.unconfirmed.heading}</h2>
          <ul className="flex flex-col gap-1">
            {data.unconfirmed.map((u) => (
              <li key={u.resource_id}>
                {u.provider}{" "}
                {telHref(u.contact) ? (
                  <a href={telHref(u.contact)!} className="font-medium text-navy underline underline-offset-4">
                    {u.contact}
                  </a>
                ) : (
                  <span className="text-ink-soft">{u.contact}</span>
                )}
              </li>
            ))}
          </ul>
        </section>
      )}
      {hasPlan && <WeekTiles days={laterDays(data)} />}
      <HelpRoutes routes={routes} />
    </div>
  );
}
