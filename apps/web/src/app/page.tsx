"use client";

import { useState } from "react";
import { ConstraintForm, toConstraints, type FormValues } from "@/components/ConstraintForm";
import { OptionCard } from "@/components/OptionCard";
import { postPlan, type Envelope, type PlanData } from "@/lib/api";
import { copy, fill } from "@/lib/copy";
import { formatPlanDate } from "@/lib/format";

type State =
  | { kind: "idle" }
  | { kind: "submitting"; zip: string }
  | { kind: "done"; envelope: Envelope }
  | { kind: "unreachable" };

export default function FoodTodayPage() {
  const [state, setState] = useState<State>({ kind: "idle" });

  async function submit(next: FormValues) {
    setState({ kind: "submitting", zip: next.zip });
    try {
      const envelope = await postPlan(toConstraints(next));
      setState({ kind: "done", envelope });
    } catch {
      setState({ kind: "unreachable" });
    }
  }

  return (
    <main className="mx-auto flex w-full max-w-2xl flex-col gap-8 px-4 py-6">
      <header className="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1">
        <p className="text-2xl font-bold tracking-[-0.02em] text-navy">{copy.site.name}</p>
        <p className="text-sm text-ink-soft">{copy.site.tagline}</p>
      </header>

      <ConstraintForm busy={state.kind === "submitting"} onSubmit={submit} />

      <section aria-live="polite" className="flex flex-col gap-2">
        {state.kind === "submitting" && (
          <>
            <p className="font-medium">{fill(copy.wait.checking, { zip: state.zip })}</p>
            <p className="text-ink-soft">{copy.wait.estimate}</p>
          </>
        )}
        {state.kind === "unreachable" && <p role="alert" className="font-medium text-alert">{copy.result.unreachable}</p>}
        {state.kind === "done" && <Result envelope={state.envelope} />}
      </section>
    </main>
  );
}

// Spec: today's visits are the plan's first day. food_today mirrors it.
function todayVisits(data: PlanData) {
  return data.days.find((d) => d.date === data.start_date)?.visits ?? data.food_today;
}

function countLine(n: number) {
  if (n === 0) return copy.result.noneListedToday;
  if (n === 1) return copy.result.oneListedToday;
  return fill(copy.result.listedToday, { n: String(n) });
}

function Result({ envelope }: { envelope: Envelope }) {
  const data = envelope.data;
  const hasPlan = (envelope.status === "success" || envelope.status === "partial") && data !== null;
  const visits = hasPlan ? todayVisits(data) : [];
  return (
    <div className="flex flex-col gap-4">
      <div className="rounded-2xl bg-navy px-5 py-4 text-paper">
        {data?.start_date && (
          <h1 className="text-2xl font-bold text-balance">{fill(copy.result.heading, { date: formatPlanDate(data.start_date) })}</h1>
        )}
        <p className="mt-1 text-navy-soft">{hasPlan ? countLine(visits.length) : copy.result.status[envelope.status]}</p>
      </div>
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
                <a href={`tel:${u.contact.replace(/[^\d+]/g, "")}`} className="font-medium text-navy underline underline-offset-4">
                  {u.contact}
                </a>
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  );
}
