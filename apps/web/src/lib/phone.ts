// A directory contact is free text: "(414) 249-3866", "no phone listed", a URL.
// Only a real number becomes a tap-to-call link; anything else is shown as text.
// Three-digit N11 codes (2-1-1, 9-1-1) are dialable too.
export function telHref(contact: string): string | null {
  const digits = contact.replace(/[^\d+]/g, "");
  const count = digits.replace(/\D/g, "").length;
  const isN11 = /^\d11$/.test(digits);
  return count >= 7 || isN11 ? `tel:${digits}` : null;
}
