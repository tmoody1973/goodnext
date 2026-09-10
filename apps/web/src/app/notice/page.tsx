"use client";

import { useRef, useState, type ChangeEvent } from "react";
import { HelpRoutes } from "@/components/HelpRoutes";
import { Waiting } from "@/components/Waiting";
import { postNotice, unreachableEnvelope, type HelpRoute, type NoticeData, type NoticeEnvelope, type PolicyPassage } from "@/lib/api";
import { copy, fill } from "@/lib/copy";
import { useFocusOnMount } from "@/lib/hooks";
import { primaryActionClass, secondaryActionClass, textLinkClass } from "@/lib/styles";

type SampleName = keyof typeof copy.notice.samples;
const SAMPLES: SampleName[] = ["six_month_report", "proof_request"];

type State =
  | { kind: "idle" }
  | { kind: "submitting" }
  | { kind: "done"; envelope: NoticeEnvelope };

export default function UnderstandNoticePage() {
  const [state, setState] = useState<State>({ kind: "idle" });
  const [routes, setRoutes] = useState<HelpRoute[]>([]);
  const lastFile = useRef<File | null>(null);
  const controller = useRef<AbortController | null>(null);

  async function submit(file: File) {
    lastFile.current = file;
    controller.current?.abort();
    const ac = new AbortController();
    controller.current = ac;
    setState({ kind: "submitting" });
    try {
      const envelope = await postNotice(file, ac.signal);
      if (ac.signal.aborted) return;
      if (envelope.help_routes?.length) setRoutes(envelope.help_routes);
      setState({ kind: "done", envelope });
    } catch (error) {
      if (ac.signal.aborted || (error instanceof DOMException && error.name === "AbortError")) return;
      setState({ kind: "done", envelope: unreachableEnvelope<NoticeData>() });
    }
  }

  async function selectSample(name: SampleName) {
    try {
      const response = await fetch(`/samples/${name.replace(/_/g, "-")}.pdf`);
      const blob = await response.blob();
      await submit(new File([blob], `${name}.pdf`, { type: "application/pdf" }));
    } catch {
      setState({ kind: "done", envelope: unreachableEnvelope<NoticeData>() });
    }
  }

  function onFile(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (file) void submit(file);
  }

  function cancel() {
    controller.current?.abort();
    setState({ kind: "idle" });
  }

  function retry() {
    if (lastFile.current) void submit(lastFile.current);
  }

  return (
    <main className="mx-auto flex w-full max-w-2xl flex-col gap-8 px-4 py-6">
      <header className="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1">
        <p className="text-2xl font-bold tracking-[-0.02em] text-navy">{copy.site.name}</p>
        <p className="text-sm text-ink-soft">{copy.site.tagline}</p>
        <nav className="w-full">
          <a href="/" className={textLinkClass}>{copy.notice.navToFood}</a>
        </nav>
      </header>

      <div className="flex flex-col gap-4">
        <h2 className="text-2xl font-bold text-balance sm:text-3xl sm:tracking-[-0.02em]">{copy.notice.heading}</h2>
        <p className="text-ink-soft">{copy.notice.intro}</p>

        <section aria-labelledby="samples-heading" className="flex flex-col gap-3">
          <h2 id="samples-heading" className="font-semibold">{copy.notice.samplesHeading}</h2>
          <div className="flex flex-wrap gap-2">
            {SAMPLES.map((name) => (
              <button key={name} type="button" onClick={() => selectSample(name)} className={secondaryActionClass}>
                {copy.notice.samples[name]}
              </button>
            ))}
          </div>
          <div className="flex flex-col gap-1">
            <label htmlFor="letter" className="font-medium">{copy.notice.uploadLabel}</label>
            <p id="letter-help" className="text-sm text-ink-soft">{copy.notice.uploadHelp}</p>
            <input
              id="letter"
              type="file"
              accept="application/pdf,image/png,image/jpeg"
              onChange={onFile}
              aria-describedby="letter-help"
              className="max-w-full text-base"
            />
          </div>
        </section>
      </div>

      <section aria-live="polite" className="flex flex-col gap-4">
        {state.kind === "submitting" && (
          <Waiting checkingText={copy.notice.reading} routes={routes} onCancel={cancel} />
        )}
        {state.kind === "done" && (
          <Result
            envelope={state.envelope}
            routes={state.envelope.help_routes?.length ? state.envelope.help_routes : routes}
            onRetry={retry}
          />
        )}
      </section>
    </main>
  );
}

type ResultProps = { envelope: NoticeEnvelope; routes: HelpRoute[]; onRetry: () => void };

function Result({ envelope, routes, onRetry }: ResultProps) {
  const headingRef = useFocusOnMount<HTMLHeadingElement>();

  if (envelope.status === "temporarily_unavailable") {
    return (
      <div className="flex flex-col gap-4">
        <p role="alert" className="font-medium text-alert">{copy.notice.status.temporarily_unavailable}</p>
        <button type="button" onClick={onRetry} className={primaryActionClass}>{copy.actions.retry}</button>
        <HelpRoutes routes={routes} />
      </div>
    );
  }
  if (envelope.status === "denied") {
    return (
      <div className="flex flex-col gap-4">
        <p role="alert" className="font-medium">{copy.notice.status.denied}</p>
        <HelpRoutes routes={routes} />
      </div>
    );
  }

  const data = envelope.data;
  const classLabel = data ? copy.notice.classLabel[data.notice_class ?? "unknown"] : copy.notice.classLabel.unknown;
  return (
    <div className="flex flex-col gap-4">
      <div className="rounded-2xl bg-navy px-5 py-6 text-paper sm:px-7 sm:py-8">
        <h1 ref={headingRef} tabIndex={-1} className="text-2xl font-bold text-balance break-words outline-none sm:text-3xl sm:tracking-[-0.02em]">
          {classLabel}
        </h1>
      </div>

      {data && data.found_dates.length > 0 && (
        <section aria-labelledby="dates-heading" className="flex flex-col gap-1 rounded-2xl border border-line px-4 py-3">
          <h2 id="dates-heading" className="font-semibold">{copy.notice.datesHeading}</h2>
          <p className="text-sm text-ink-soft">{copy.notice.datesHelp}</p>
          <ul className="flex flex-wrap gap-x-4">
            {data.found_dates.map((d) => (
              <li key={d} className="font-medium">{d}</li>
            ))}
          </ul>
        </section>
      )}

      {envelope.status === "no_match" && <p className="font-medium">{copy.notice.noMatch}</p>}

      {data && data.passages.length > 0 && (
        <section aria-labelledby="passages-heading" className="flex flex-col gap-4">
          <h2 id="passages-heading" className="text-lg font-semibold">{copy.notice.passagesHeading}</h2>
          {data.passages.map((p) => (
            <Passage key={p.passage_id} passage={p} />
          ))}
        </section>
      )}

      {data && <ExtractedText text={data.extracted_text} />}

      <HelpRoutes routes={routes} />
    </div>
  );
}

function Passage({ passage }: { passage: PolicyPassage }) {
  return (
    <article className="flex flex-col gap-2 rounded-2xl border border-line px-4 py-4">
      <h3 className="font-semibold">{passage.topic}</h3>
      <p>{passage.passage}</p>
      <p><span className="font-medium">{copy.notice.passageAction}: </span>{passage.action_for_resident}</p>
      {passage.uncertainties.map((u) => (
        <p key={u} className="text-sm text-ink-soft">{u}</p>
      ))}
      <p className="text-sm">
        <span className="font-medium">{copy.notice.passageSource}: </span>
        <a href={passage.source_url} target="_blank" rel="noopener noreferrer" className={`${textLinkClass} [overflow-wrap:anywhere]`}>
          {new URL(passage.source_url).hostname}
        </a>
      </p>
      <p className="text-xs text-ink-soft">{fill(copy.help.checked, { date: passage.source_retrieved_on })}</p>
      <p className="text-xs text-ink-soft">{copy.notice.passageDraft}</p>
    </article>
  );
}

function ExtractedText({ text }: { text: string }) {
  return (
    <details className="rounded-2xl border border-line px-4 py-3">
      <summary className="cursor-pointer font-semibold">{copy.notice.textHeading}</summary>
      <pre className="mt-2 whitespace-pre-wrap break-words font-sans text-sm text-ink-soft">{text}</pre>
    </details>
  );
}
