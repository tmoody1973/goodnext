import { describe, expect, it } from "vitest";
import path from "node:path";
import { copy } from "./copy";
import { NEVER_LIST, VENDOR_NEVER_LIST, avoidWordsFrom, neverListHits, readContextAvoidWords } from "./never-list";

const CONTEXT_MD = path.resolve(__dirname, "../../../../CONTEXT.md");

describe("never-list", () => {
  it("parses avoid words from CONTEXT.md lines", () => {
    expect(avoidWordsFrom("**X**:\nfoo\n_Avoid_: A, b c, D\n")).toEqual(["a", "b c", "d"]);
  });

  it("the copy module contains none of the seven never-list terms", () => {
    expect(neverListHits(copy, NEVER_LIST)).toEqual([]);
  });

  it("the copy module contains none of the CONTEXT.md avoid-words", () => {
    const avoid = readContextAvoidWords(CONTEXT_MD);
    expect(avoid.length).toBeGreaterThan(20);
    expect(neverListHits(copy, avoid)).toEqual([]);
  });

  it("catches a banned word as a whole word only", () => {
    expect(neverListHits({ a: "Food is available now" }, NEVER_LIST)).toEqual(['a: "available"']);
    expect(neverListHits({ a: "Temporarily unavailable" }, NEVER_LIST)).toEqual([]);
  });
});

describe("vendor never-list", () => {
  it("the copy module names no vendor or build technology", () => {
    expect(neverListHits(copy, VENDOR_NEVER_LIST)).toEqual([]);
  });
});
