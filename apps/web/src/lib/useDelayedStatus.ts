import { useEffect, useState } from "react";

// PRD section 8: after 30 s of waiting, show explicit delayed status.
export const DELAYED_AFTER_MS = 30_000;

// True once `waiting` has been true for DELAYED_AFTER_MS; resets when it turns false.
export function useDelayedStatus(waiting: boolean): boolean {
  const [delayed, setDelayed] = useState(false);
  useEffect(() => {
    if (!waiting) {
      setDelayed(false);
      return;
    }
    const timer = setTimeout(() => setDelayed(true), DELAYED_AFTER_MS);
    return () => clearTimeout(timer);
  }, [waiting]);
  return delayed;
}
