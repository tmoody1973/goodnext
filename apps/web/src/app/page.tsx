"use client";

import { useState } from "react";
import { ConstraintForm, toConstraints, type FormValues } from "@/components/ConstraintForm";
import { postPlan, type Envelope } from "@/lib/api";
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

function Result({ envelope }: { envelope: Envelope }) {
  const date = envelope.data?.start_date;
  return (
    <div className="rounded-2xl bg-navy px-5 py-4 text-paper">
      {date && <h1 className="text-2xl font-bold text-balance">{fill(copy.result.heading, { date: formatPlanDate(date) })}</h1>}
      <p className="mt-1 text-navy-soft">{copy.result.status[envelope.status]}</p>
    </div>
  );
}
