import { afterEach, describe, expect, it, vi } from "vitest";
import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import FoodTodayPage from "./page";
import { NEVER_LIST, neverListHits } from "@/lib/never-list";
import day9 from "../../../../docs/evidence/moo-777-live-53206-2026-09-09-demo.json";

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

describe("later this week tiles", () => {
  it("renders six tiles with listed counts, an empty day as text, and the heading", async () => {
    await submit(day9);
    const strip = screen.getByRole("region", { name: "Later this week" });
    const tiles = within(strip).getAllByRole("listitem");
    expect(tiles).toHaveLength(6);
    expect(within(strip).getAllByRole("button")).toHaveLength(5);
    expect(tiles[0]).toHaveTextContent("Thu");
    expect(tiles[0]).toHaveTextContent("Sep 10");
    expect(tiles[0]).toHaveTextContent("3 listed");
    expect(tiles[3]).toHaveTextContent("Sun");
    expect(tiles[3]).toHaveTextContent("Nothing listed");
    expect(within(tiles[3]).queryByRole("button")).not.toBeInTheDocument();
    expect(strip.textContent).not.toMatch(/\bopen\b/i);
  });

  it("unfolds a day with schedule text and record fields, never the today claim text", async () => {
    const user = await submit(day9);
    const strip = screen.getByRole("region", { name: "Later this week" });
    const thu = within(strip).getByRole("button", { name: /Thu/ });
    expect(thu).toHaveAttribute("aria-expanded", "false");
    await user.click(thu);
    expect(thu).toHaveAttribute("aria-expanded", "true");
    const entries = within(strip).getAllByRole("article");
    expect(entries).toHaveLength(3);
    expect(entries[1]).toHaveTextContent("Northside Community Pantry");
    expect(entries[1]).toHaveTextContent("Thu Sep 10: 10:00 AM–2:00 PM");
    expect(entries[1]).toHaveTextContent("Free");
    expect(entries[1]).toHaveTextContent("Last checked 2026-09-05");
    expect(within(entries[1]).getByRole("link", { name: "Call (414) 555-0101" })).toHaveAttribute("href", "tel:4145550101");
    expect(within(entries[1]).getByRole("link", { name: "Directions" })).toHaveAttribute("href", expect.stringContaining("google.com/maps"));
    expect(strip.textContent).not.toContain("Not open today");
    expect(strip.textContent).not.toContain("We can't confirm they have food today");
  });

  it("opening a second tile closes the first", async () => {
    const user = await submit(day9);
    const strip = screen.getByRole("region", { name: "Later this week" });
    await user.click(within(strip).getByRole("button", { name: /Thu/ }));
    await user.click(within(strip).getByRole("button", { name: /Sat/ }));
    expect(within(strip).getByRole("button", { name: /Thu/ })).toHaveAttribute("aria-expanded", "false");
    expect(within(strip).getByRole("button", { name: /Sat/ })).toHaveAttribute("aria-expanded", "true");
    const entries = within(strip).getAllByRole("article");
    expect(entries).toHaveLength(3);
    expect(entries[0]).toHaveTextContent("COA Goldin Center");
  });

  it("never-list scan passes with a day unfolded", async () => {
    const user = await submit(day9);
    await user.click(within(screen.getByRole("region", { name: "Later this week" })).getByRole("button", { name: /Fri/ }));
    expect(neverListHits({ page: document.body.textContent }, NEVER_LIST)).toEqual([]);
  });
});
