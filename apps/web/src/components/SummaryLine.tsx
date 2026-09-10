import type { FormValues } from "@/components/ConstraintForm";
import { copy, fill } from "@/lib/copy";
import { textLinkClass } from "@/lib/styles";

// After a result the form folds into one line so the options come first.
export function SummaryLine({ values, onChange }: { values: FormValues; onChange: () => void }) {
  const parts = [
    values.zip,
    fill(copy.summary.money, { money: String(Math.max(0, Math.floor(Number(values.money) || 0))) }),
    copy.form.kitchen[values.kitchen],
    values.travel.map((t) => copy.form.travel[t]).join(", ") + (values.minutes ? ` ${fill(copy.summary.minutes, { n: values.minutes })}` : ""),
  ];
  return (
    <div role="group" aria-label={copy.summary.label} className="flex flex-wrap items-center gap-x-2 gap-y-1 rounded-xl bg-navy-soft px-4 py-3 text-sm">
      {parts.map((part, i) => (
        <span key={i} className="flex items-center gap-x-2">
          {i > 0 && <span aria-hidden="true">·</span>}
          <span>{part}</span>
        </span>
      ))}
      <span aria-hidden="true" className="print:hidden">·</span>
      <button type="button" onClick={onChange} className={`${textLinkClass} font-semibold`}>
        {copy.summary.change}
      </button>
    </div>
  );
}
