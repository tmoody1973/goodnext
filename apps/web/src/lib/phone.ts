// A directory contact is free text: "(414) 249-3866", "no phone listed", a URL.
// Only a real number becomes a tap-to-call link; anything else is shown as text.
export function telHref(contact: string): string | null {
  const digits = contact.replace(/[^\d+]/g, "");
  return digits.replace(/\D/g, "").length >= 7 ? `tel:${digits}` : null;
}
