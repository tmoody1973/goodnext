"use client";

import { useState, type FormEvent } from "react";
import { copy } from "@/lib/copy";
import type { Constraints, Kitchen, Travel } from "@/lib/api";

const KITCHENS: Kitchen[] = ["full", "microwave_only", "none"];
const TRAVELS: Travel[] = ["walk", "bus", "car", "ride"];

export type FormValues = {
  zip: string;
  money: string;
  kitchen: Kitchen;
  travel: Travel[];
  minutes: string;
};

const emptyValues: FormValues = { zip: "", money: "0", kitchen: "full", travel: [], minutes: "" };

export function toConstraints(v: FormValues): Constraints {
  const minutes = Number(v.minutes);
  return {
    zip_code: v.zip,
    budget_usd: Math.max(0, Math.floor(Number(v.money) || 0)),
    kitchen: v.kitchen,
    travel: v.travel,
    ...(v.minutes !== "" && Number.isFinite(minutes) && minutes >= 0 ? { max_travel_minutes: Math.floor(minutes) } : {}),
  };
}

type Props = {
  busy?: boolean;
  onSubmit: (values: FormValues) => void;
};

// One pill per option: a visually hidden native input inside a styled label,
// so keyboard, screen readers, and the browser's own form semantics all work.
function Pill({ type, name, value, label, checked, onChange }: {
  type: "radio" | "checkbox";
  name: string;
  value: string;
  label: string;
  checked: boolean;
  onChange: () => void;
}) {
  const cls = `rounded-xl border px-4 py-3 text-base font-medium transition-colors ${
    checked ? "border-navy bg-navy text-paper" : "border-line bg-paper text-ink hover:border-navy"
  }`;
  return (
    <label className={cls}>
      <input type={type} name={name} value={value} checked={checked} onChange={onChange} className="sr-only" />
      {label}
    </label>
  );
}

export function ConstraintForm({ busy = false, onSubmit }: Props) {
  const [values, setValues] = useState<FormValues>(emptyValues);
  const [errors, setErrors] = useState<{ zip?: string; travel?: string }>({});
  const set = <K extends keyof FormValues>(key: K, value: FormValues[K]) =>
    setValues((prev) => ({ ...prev, [key]: value }));

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const next: typeof errors = {};
    if (!/^\d{5}$/.test(values.zip)) next.zip = copy.form.zipInvalid;
    if (values.travel.length === 0) next.travel = copy.form.travelInvalid;
    setErrors(next);
    if (Object.keys(next).length === 0) onSubmit(values);
  }

  const toggleTravel = (t: Travel) =>
    set("travel", values.travel.includes(t) ? values.travel.filter((x) => x !== t) : [...values.travel, t]);

  return (
    <form onSubmit={handleSubmit} noValidate aria-busy={busy} className="flex flex-col gap-6">
      <h2 className="text-xl font-semibold text-balance">{copy.form.heading}</h2>

      <div className="flex flex-col gap-1">
        <label htmlFor="zip" className="font-medium">{copy.form.zipLabel}</label>
        <p id="zip-help" className="text-sm text-ink-soft">{copy.form.zipHelp}</p>
        <input
          id="zip"
          name="zip"
          inputMode="numeric"
          autoComplete="postal-code"
          maxLength={5}
          value={values.zip}
          onChange={(e) => set("zip", e.target.value.replace(/\D/g, ""))}
          aria-describedby={errors.zip ? "zip-help zip-error" : "zip-help"}
          aria-invalid={errors.zip ? true : undefined}
          className="w-40 rounded-xl border border-ink-soft px-4 py-3 text-lg"
        />
        {errors.zip && <p id="zip-error" role="alert" className="text-sm font-medium text-alert">{errors.zip}</p>}
      </div>

      <div className="flex flex-col gap-1">
        <label htmlFor="money" className="font-medium">{copy.form.moneyLabel}</label>
        <p id="money-help" className="text-sm text-ink-soft">{copy.form.moneyHelp}</p>
        <div className="flex items-center gap-2">
          <span aria-hidden="true" className="text-lg">$</span>
          <input
            id="money"
            name="money"
            type="number"
            inputMode="numeric"
            min={0}
            step={1}
            value={values.money}
            onChange={(e) => set("money", e.target.value)}
            aria-describedby="money-help"
            className="w-32 rounded-xl border border-ink-soft px-4 py-3 text-lg"
          />
        </div>
      </div>

      <fieldset className="flex flex-col gap-2">
        <legend className="font-medium">{copy.form.kitchenLabel}</legend>
        <div className="flex flex-wrap gap-2">
          {KITCHENS.map((k) => (
            <Pill key={k} type="radio" name="kitchen" value={k} label={copy.form.kitchen[k]} checked={values.kitchen === k} onChange={() => set("kitchen", k)} />
          ))}
        </div>
      </fieldset>

      <fieldset className="flex flex-col gap-2" aria-describedby={errors.travel ? "travel-help travel-error" : "travel-help"}>
        <legend className="font-medium">{copy.form.travelLabel}</legend>
        <p id="travel-help" className="text-sm text-ink-soft">{copy.form.travelHelp}</p>
        <div className="flex flex-wrap gap-2">
          {TRAVELS.map((t) => (
            <Pill key={t} type="checkbox" name="travel" value={t} label={copy.form.travel[t]} checked={values.travel.includes(t)} onChange={() => toggleTravel(t)} />
          ))}
        </div>
        {errors.travel && <p id="travel-error" role="alert" className="text-sm font-medium text-alert">{errors.travel}</p>}
      </fieldset>

      <div className="flex flex-col gap-1">
        <label htmlFor="minutes" className="font-medium">{copy.form.minutesLabel}</label>
        <input
          id="minutes"
          name="minutes"
          type="number"
          inputMode="numeric"
          min={0}
          step={5}
          value={values.minutes}
          onChange={(e) => set("minutes", e.target.value)}
          className="w-32 rounded-xl border border-ink-soft px-4 py-3 text-lg"
        />
      </div>

      <button
        type="submit"
        disabled={busy}
        className="self-start rounded-xl bg-amber px-6 py-3 text-lg font-semibold text-ink shadow-[0_2px_8px_rgba(11,42,74,0.18)] disabled:opacity-60"
      >
        {copy.form.submit}
      </button>
    </form>
  );
}
