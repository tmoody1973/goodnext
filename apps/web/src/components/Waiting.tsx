"use client";

import { useEffect, useState } from "react";
import { HelpRoutes } from "@/components/HelpRoutes";
import type { HelpRoute } from "@/lib/api";
import { copy } from "@/lib/copy";
import { secondaryActionClass } from "@/lib/styles";

// PRD section 8: after 30 s of waiting, show explicit delayed status. Shared by
// the food and the notice screens; both waits are slow for the same reason.
export const DELAYED_AFTER_MS = 30_000;

// The waiting and delayed states, lifted out of the page so both screens show
// the same honest message, estimate, and help routes while a request is out.
// The delayed timer lives here: mounting means a request just started, so it
// starts on mount and clears when the wait ends and this unmounts.
export function Waiting({
  checkingText,
  routes,
  onCancel,
}: {
  checkingText: string;
  routes: HelpRoute[];
  onCancel: () => void;
}) {
  const [delayed, setDelayed] = useState(false);
  useEffect(() => {
    const timer = setTimeout(() => setDelayed(true), DELAYED_AFTER_MS);
    return () => clearTimeout(timer);
  }, []);
  return (
    <div className="flex flex-col gap-2">
      <p className="font-medium">{checkingText}</p>
      <p className="text-ink-soft">{copy.wait.estimate}</p>
      {delayed && (
        <>
          <p role="status" className="font-medium">{copy.wait.delayed}</p>
          <button type="button" onClick={onCancel} className={secondaryActionClass}>
            {copy.wait.cancel}
          </button>
          <HelpRoutes routes={routes} />
        </>
      )}
    </div>
  );
}
