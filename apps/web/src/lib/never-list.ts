import { readFileSync } from "node:fs";

// Mirrors NEVER_LIST in app/goodnext/claims.py. Reviewed 2026-09-08.
export const NEVER_LIST = [
  "in stock",
  "reserved",
  "available",
  "guaranteed",
  "confirmed for you",
  "secured",
  "food covered",
] as const;

// The `_Avoid_:` lines in CONTEXT.md, read at test time so the glossary stays
// the single source.
export function avoidWordsFrom(contextMd: string): string[] {
  return contextMd
    .split("\n")
    .filter((line) => line.startsWith("_Avoid_:"))
    .flatMap((line) => line.replace("_Avoid_:", "").split(","))
    .map((w) => w.trim().toLowerCase())
    .filter(Boolean);
}

export function readContextAvoidWords(path: string): string[] {
  return avoidWordsFrom(readFileSync(path, "utf8"));
}

const escape = (s: string) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

// Whole-word, case-insensitive hits of any term in any string of a JSON-like value.
export function neverListHits(value: unknown, terms: readonly string[]): string[] {
  const patterns = terms.map((t) => ({ t, rx: new RegExp(`\\b${escape(t)}\\b`, "i") }));
  const hits: string[] = [];
  const walk = (node: unknown, path: string) => {
    if (typeof node === "string") {
      for (const { t, rx } of patterns) if (rx.test(node)) hits.push(`${path}: "${t}"`);
    } else if (Array.isArray(node)) {
      node.forEach((n, i) => walk(n, `${path}[${i}]`));
    } else if (node && typeof node === "object") {
      for (const [k, v] of Object.entries(node)) walk(v, path ? `${path}.${k}` : k);
    }
  };
  walk(value, "");
  return hits;
}
