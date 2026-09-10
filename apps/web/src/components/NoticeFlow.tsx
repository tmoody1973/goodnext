"use client";

import { useRef, useState, type FormEvent } from "react";
import { HelpRoutes } from "@/components/HelpRoutes";
import { NoticeResult } from "@/components/NoticeResult";
import { postNotice, type HelpRoute, type LetterKind, type NoticeEnvelope } from "@/lib/api";
import { copy } from "@/lib/copy";
import { primaryActionClass, secondaryActionClass, textLinkClass } from "@/lib/styles";
import { useDelayedStatus } from "@/lib/useDelayedStatus";

const n = copy.notice;
const KINDS: LetterKind[] = ["sanction", "time_limited_warning", "six_month_report", "unknown"];

type State =
  | { kind: "idle"; error?: string }
  | { kind: "submitting" }
  | { kind: "done"; envelope: NoticeEnvelope };

function unreachable(): NoticeEnvelope {
  return { status: "temporarily_unavailable", data: null, evidence: [], missing: [], warnings: ["unreachable"], retryable: true, request_id: "local" };
}

type Props = { routes: HelpRoute[]; onRoutes: (routes: HelpRoute[]) => void; onFindFood: () => void };

// Understand my letter (spec docs/specs/understand-notice.md): upload or three
// answers, the shared waiting states, and the validated result.
export function NoticeFlow({ routes, onRoutes, onFindFood }: Props) {
  const [state, setState] = useState<State>({ kind: "idle" });
  const [manual, setManual] = useState(false);
  const [letterKind, setLetterKind] = useState<LetterKind>("six_month_report");
  const [dateText, setDateText] = useState("");
  const [asksText, setAsksText] = useState("");
  const fileInput = useRef<HTMLInputElement>(null);
  const controller = useRef<AbortController | null>(null);
  const lastForm = useRef<FormData | null>(null);
  const busy = state.kind === "submitting";
  const delayed = useDelayedStatus(busy);

  async function send(form: FormData) {
    lastForm.current = form;
    controller.current?.abort();
    const ac = new AbortController();
    controller.current = ac;
    setState({ kind: "submitting" });
    try {
      const envelope = await postNotice(form, ac.signal);
      if (ac.signal.aborted) return;
      if (envelope.help_routes?.length) onRoutes(envelope.help_routes);
      if (envelope.status === "needs_clarification" || envelope.status === "denied") {
        // A recoverable intake problem: the form stays, the limit is named.
        setState({ kind: "idle", error: envelope.missing[0] ?? copy.result.status.needs_clarification });
        return;
      }
      setState({ kind: "done", envelope });
    } catch (error) {
      if (ac.signal.aborted || (error instanceof DOMException && error.name === "AbortError")) return;
      setState({ kind: "done", envelope: unreachable() });
    }
  }

  function submitFile(event: FormEvent) {
    event.preventDefault();
    const file = fileInput.current?.files?.[0];
    if (!file) {
      setState({ kind: "idle", error: n.fileMissing });
      return;
    }
    const form = new FormData();
    form.append("file", file);
    void send(form);
  }

  function submitManual(event: FormEvent) {
    event.preventDefault();
    const form = new FormData();
    form.append("letter_kind", letterKind);
    form.append("date_text", dateText);
    form.append("asks_text", asksText);
    void send(form);
  }

  function cancel() {
    controller.current?.abort();
    setState({ kind: "idle" });
  }

  function retry() {
    if (lastForm.current) void send(lastForm.current);
  }

  const idle = state.kind === "idle";
  return (
    <div className="flex flex-col gap-6">
      {idle && !manual && (
        <form onSubmit={submitFile} noValidate className="flex flex-col gap-4">
          <h2 className="text-xl font-semibold text-balance">{n.heading}</h2>
          <div className="flex flex-col gap-1">
            <label htmlFor="letter-file" className="font-medium">{n.fileLabel}</label>
            <p id="letter-limits" className="text-sm text-ink-soft">{n.limits}</p>
            <input id="letter-file" ref={fileInput} type="file" accept="application/pdf,image/png,image/jpeg" aria-describedby="letter-limits letter-consent" className="rounded-xl border border-ink-soft px-4 py-3 file:mr-3 file:rounded-lg file:border-0 file:bg-navy-soft file:px-3 file:py-1.5 file:font-medium" />
          </div>
          <p id="letter-consent" className="text-sm">{n.consent}</p>
          {state.error && <p role="alert" className="text-sm font-medium text-alert">{state.error}</p>}
          <button type="submit" className={`${primaryActionClass} px-6 py-3 text-lg`}>{n.submit}</button>
          <button type="button" onClick={() => setManual(true)} className={`${textLinkClass} self-start`}>{n.manualLink}</button>
        </form>
      )}

      {idle && manual && (
        <form onSubmit={submitManual} noValidate className="flex flex-col gap-4">
          <h2 className="text-xl font-semibold text-balance">{n.heading}</h2>
          <div className="flex flex-col gap-1">
            <label htmlFor="letter-kind" className="font-medium">{n.kindLabel}</label>
            <select id="letter-kind" value={letterKind} onChange={(e) => setLetterKind(e.target.value as LetterKind)} className="w-full max-w-sm rounded-xl border border-ink-soft bg-paper px-4 py-3 text-lg">
              {KINDS.map((k) => <option key={k} value={k}>{n.kinds[k]}</option>)}
            </select>
          </div>
          <div className="flex flex-col gap-1">
            <label htmlFor="letter-date" className="font-medium">{n.dateLabel}</label>
            <input id="letter-date" value={dateText} onChange={(e) => setDateText(e.target.value)} maxLength={200} className="w-full max-w-sm rounded-xl border border-ink-soft px-4 py-3 text-lg" />
          </div>
          <div className="flex flex-col gap-1">
            <label htmlFor="letter-asks" className="font-medium">{n.asksLabel}</label>
            <textarea id="letter-asks" value={asksText} onChange={(e) => setAsksText(e.target.value)} maxLength={1000} rows={3} className="w-full rounded-xl border border-ink-soft px-4 py-3 text-lg" />
          </div>
          {state.error && <p role="alert" className="text-sm font-medium text-alert">{state.error}</p>}
          <button type="submit" className={`${primaryActionClass} px-6 py-3 text-lg`}>{n.manualSubmit}</button>
          <button type="button" onClick={() => setManual(false)} className={`${textLinkClass} self-start`}>{n.uploadLink}</button>
        </form>
      )}

      <section aria-live="polite" className="flex flex-col gap-4">
        {busy && (
          <div className="flex flex-col gap-2">
            <p className="font-medium">{n.checking}</p>
            <p className="text-ink-soft">{n.estimate}</p>
            {delayed && (
              <>
                <p role="status" className="font-medium">{copy.wait.delayed}</p>
                <button type="button" onClick={cancel} className={secondaryActionClass}>{copy.wait.cancel}</button>
                <HelpRoutes routes={routes} />
              </>
            )}
          </div>
        )}
        {state.kind === "done" && state.envelope.status === "temporarily_unavailable" && (
          <div className="flex flex-col gap-4">
            <p role="alert" className="font-medium text-alert">{copy.result.status.temporarily_unavailable}</p>
            <button type="button" onClick={retry} className={primaryActionClass}>{copy.actions.retry}</button>
            <HelpRoutes routes={state.envelope.help_routes?.length ? state.envelope.help_routes : routes} />
          </div>
        )}
        {state.kind === "done" && state.envelope.data && (
          <>
            <NoticeResult data={state.envelope.data} onFindFood={onFindFood} onAnother={() => setState({ kind: "idle" })} />
            <HelpRoutes routes={state.envelope.help_routes?.length ? state.envelope.help_routes : routes} />
          </>
        )}
      </section>
    </div>
  );
}
