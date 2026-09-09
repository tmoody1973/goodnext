// "2026-09-09" -> "Wednesday, September 9". Parsed as a calendar date so the
// browser's own time zone can never shift it a day.
export function formatPlanDate(isoDate: string): string {
  const [y, m, d] = isoDate.split("-").map(Number);
  if (!y || !m || !d) return isoDate;
  return new Intl.DateTimeFormat("en-US", {
    weekday: "long",
    month: "long",
    day: "numeric",
    timeZone: "UTC",
  }).format(new Date(Date.UTC(y, m - 1, d)));
}

// "2026-09-13" -> { weekday: "Sun", day: "Sep 13" } for a tile.
export function formatTileDate(isoDate: string): { weekday: string; day: string } {
  const [y, m, d] = isoDate.split("-").map(Number);
  if (!y || !m || !d) return { weekday: "", day: isoDate };
  const date = new Date(Date.UTC(y, m - 1, d));
  return {
    weekday: new Intl.DateTimeFormat("en-US", { weekday: "short", timeZone: "UTC" }).format(date),
    day: new Intl.DateTimeFormat("en-US", { month: "short", day: "numeric", timeZone: "UTC" }).format(date),
  };
}
