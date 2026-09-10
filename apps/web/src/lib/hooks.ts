import { useEffect, useRef } from "react";

// The form or entry folds away when a result lands, which would drop keyboard
// focus on the body. Move it to the result heading so a keyboard or
// screen-reader user starts reading at the answer.
export function useFocusOnMount<T extends HTMLElement>() {
  const ref = useRef<T>(null);
  useEffect(() => {
    ref.current?.focus();
  }, []);
  return ref;
}
