import { afterEach, describe, expect, it, vi } from "vitest";
import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import axe from "axe-core";
import { readFileSync } from "node:fs";
import path from "node:path";
import FoodTodayPage from "./page";
import { VENDOR_NEVER_LIST, neverListHits } from "@/lib/never-list";
import day9 from "../../../../docs/evidence/moo-777-live-53206-2026-09-09-demo.json";

const routes = [
  { name: "2-1-1 (IMPACT 211 in Milwaukee County)", purpose: "Find local food and other help by phone, any day.", phone: "2-1-1", url: "https://www.impactinc.org/impact-211/", source_url: "https://www.impactinc.org/impact-211/", last_checked: "2026-09-08" },
  { name: "Hunger Task Force emergency food", purpose: "Milwaukee County pantry and meal map.", phone: null, url: "https://www.hungertaskforce.org/get-help/emergency-food/", source_url: "https://www.hungertaskforce.org/get-help/emergency-food/", last_checked: "2026-09-08" },
  { name: "FoodShare member line", purpose: "Questions about your FoodShare case or QUEST card.", phone: "1-800-362-3002", url: "https://www.dhs.wisconsin.gov/foodshare/index.htm", source_url: "https://www.dhs.wisconsin.gov/foodshare/index.htm", last_checked: "2026-09-08" },
];
const success = { ...day9, help_routes: routes };
const noMatch = { status: "no_match", data: null, evidence: [], missing: [], warnings: [], retryable: false, request_id: "r-nm", help_routes: routes };

afterEach(() => vi.unstubAllGlobals());

async function submit(envelope: unknown) {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ status: 200, json: async () => envelope }));
  const user = userEvent.setup();
  render(<FoodTodayPage />);
  await user.type(screen.getByLabelText("ZIP code"), "53206");
  await user.click(screen.getByRole("checkbox", { name: "Bus" }));
  await user.click(screen.getByRole("button", { name: "Show food today" }));
  await screen.findByRole("heading", { level: 1 });
  return user;
}

// jsdom has no layout engine, so axe cannot measure color contrast here; the
// contrast pairs are computed from the palette in docs/evidence/moo-786-contrast.txt
// and checked live in the browser round.
async function seriousAxeFindings() {
  const result = await axe.run(document.body, { rules: { "color-contrast": { enabled: false } } });
  return result.violations.filter((v) => v.impact === "serious" || v.impact === "critical").map((v) => `${v.id}: ${v.nodes.map((n) => n.target.join(" ")).join(", ")}`);
}

describe("finish pass: print, links, focus, axe", () => {
  it("offers Print this list on a plan and calls the browser's print", async () => {
    const print = vi.fn();
    vi.stubGlobal("print", print);
    const user = await submit(success);
    await user.click(screen.getByRole("button", { name: "Print this list" }));
    expect(print).toHaveBeenCalledTimes(1);
  });

  it("does not offer Print on a no-match", async () => {
    await submit(noMatch);
    expect(screen.queryByRole("button", { name: "Print this list" })).not.toBeInTheDocument();
  });

  it("the print stylesheet hides the form, the week tiles, and buttons", () => {
    const css = readFileSync(path.resolve(__dirname, "globals.css"), "utf8");
    const print = css.slice(css.indexOf("@media print"));
    expect(print).toContain("form");
    expect(print).toContain('section[aria-labelledby="week-heading"]');
    expect(print).toContain("button");
    expect(print).toContain("display: none");
  });

  it("Directions and Call links name their provider for a screen reader", async () => {
    await submit(success);
    const card = screen.getAllByRole("article")[0];
    expect(within(card).getByRole("link", { name: "Directions to Capuchin Community Services – House of Peace" })).toHaveAttribute("href", expect.stringContaining("google.com/maps"));
    expect(within(card).getByRole("link", { name: "Call 414-933-1300, Capuchin Community Services – House of Peace" })).toHaveAttribute("href", "tel:4149331300");
  });

  it("2-1-1 in the help routes is a tel:211 link", async () => {
    await submit(success);
    const help = screen.getByRole("region", { name: "Need more help?" });
    expect(within(help).getByRole("link", { name: "2-1-1" })).toHaveAttribute("href", "tel:211");
  });

  it("moves keyboard focus to the result heading inside the live region", async () => {
    await submit(success);
    const heading = screen.getByRole("heading", { level: 1 });
    expect(heading).toHaveFocus();
    expect(heading.closest("[aria-live]")).not.toBeNull();
  });

  it("axe: idle form has no serious or critical findings", async () => {
    render(<FoodTodayPage />);
    expect(await seriousAxeFindings()).toEqual([]);
  });

  it("axe: plan with a day unfolded has no serious or critical findings", async () => {
    const user = await submit(success);
    await user.click(within(screen.getByRole("region", { name: "Later this week" })).getByRole("button", { name: /Thu/ }));
    expect(await seriousAxeFindings()).toEqual([]);
  });

  it("axe: no-match has no serious or critical findings", async () => {
    await submit(noMatch);
    expect(await seriousAxeFindings()).toEqual([]);
  });

  it("no vendor or build name reaches the rendered page", async () => {
    await submit(success);
    expect(neverListHits({ page: document.body.textContent }, VENDOR_NEVER_LIST)).toEqual([]);
  });
});
