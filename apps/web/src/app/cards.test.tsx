import { afterEach, describe, expect, it, vi } from "vitest";
import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import FoodTodayPage from "./page";
import { NEVER_LIST, VENDOR_NEVER_LIST, neverListHits } from "@/lib/never-list";
import day9 from "../../../../docs/evidence/moo-777-live-53206-2026-09-09-demo.json";
import day10 from "../../../../docs/evidence/moo-778-live-53206-2026-09-10-demo.json";

afterEach(() => vi.unstubAllGlobals());

async function submitWith(envelope: unknown) {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ status: 200, json: async () => envelope }));
  const user = userEvent.setup();
  render(<FoodTodayPage />);
  await user.type(screen.getByLabelText("ZIP code"), "53206");
  await user.click(screen.getByRole("checkbox", { name: "Bus" }));
  await user.click(screen.getByRole("button", { name: "Show food today" }));
  await screen.findByRole("heading", { level: 1 });
}

describe("today's cards", () => {
  it("renders one card per today visit from the 2026-09-09 response, claims in order", async () => {
    await submitWith(day9);
    expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent("Food today, Wednesday, September 9");
    // The count is a heading, so a screen-reader user can reach it as a result.
    expect(screen.getByRole("heading", { level: 2, name: "2 listed today" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Print this list" })).toBeInTheDocument();

    const cards = screen.getAllByRole("article");
    expect(cards).toHaveLength(2);

    const first = within(cards[0]);
    const text = cards[0].textContent ?? "";
    const order = [
      "8:30 AM",
      "12:00 PM",
      "Capuchin Community Services – House of Peace",
      "Free",
      "No requirements listed",
      "Last checked 2024-08-27; call to confirm",
      "We can't confirm they have food today.",
      "You said: bus, up to 30 minutes",
      "Directions",
      "Call 414-933-1300",
      "Source: Milwaukee Food Environment Map",
    ];
    const positions = order.map((s) => text.indexOf(s));
    expect(positions.every((p) => p >= 0)).toBe(true);
    expect([...positions].sort((a, b) => a - b)).toEqual(positions);

    const directions = first.getByRole("link", { name: "Directions to Capuchin Community Services – House of Peace" });
    expect(directions).toHaveAttribute("href", expect.stringContaining("google.com/maps"));
    expect(directions).toHaveAttribute("target", "_blank");
    expect(first.getByRole("link", { name: "Call Capuchin Community Services – House of Peace at 414-933-1300" })).toHaveAttribute(
      "href",
      "tel:4149331300",
    );

    // Second card has no source line and no appointment line.
    expect(cards[1].textContent).not.toContain("Source:");
    expect(cards[1].textContent).not.toContain("Appointment");

    // Model free text never reaches the card.
    expect(text).not.toContain("Hours last confirmed");
  });

  it("lists unconfirmed records by name and phone, not as cards", async () => {
    await submitWith(day9);
    const heading = screen.getByText("Not checked recently. Call before you go.");
    const section = heading.closest("section")!;
    expect(within(section).getByText(/Placeholder Pop-Up Pantry/)).toBeInTheDocument();
    expect(within(section).getByRole("link", { name: "(414) 555-0107" })).toHaveAttribute("href", "tel:4145550107");
    expect(screen.getAllByRole("article")).toHaveLength(2);
  });

  it("renders the 2026-09-10 response: three cards with appointment and source lines", async () => {
    await submitWith(day10);
    expect(screen.getByText("3 listed today")).toBeInTheDocument();
    const cards = screen.getAllByRole("article");
    expect(cards).toHaveLength(3);
    expect(cards[0].textContent).toContain("The Gathering at Running Rebels");
    expect(cards[0].textContent).toContain("Appointment: not stated; call to ask");
    expect(cards[0].textContent).toContain("Source: Official provider page");
    expect(screen.queryByText("Not checked recently. Call before you go.")).not.toBeInTheDocument();
  });

  it("shows the fixed partial sentence and hides warnings", async () => {
    const partial = { ...day9, status: "partial", warnings: ["stripped visit res-999: fabricated id", "paid at zero budget"] };
    await submitWith(partial);
    expect(screen.getByText("Some suggestions were left out because they did not pass our checks.")).toBeInTheDocument();
    expect(document.body.textContent).not.toContain("fabricated id");
    expect(document.body.textContent).not.toContain("paid at zero budget");
    expect(screen.getAllByRole("article")).toHaveLength(2);
  });

  it("shows a contact with no digits as text, not a call link", async () => {
    const noPhone = JSON.parse(JSON.stringify(day9));
    noPhone.data.days[0].visits[0].contact = "no phone listed";
    await submitWith(noPhone);
    const card = screen.getAllByRole("article")[0];
    expect(within(card).queryByRole("link", { name: /^Call/ })).not.toBeInTheDocument();
    expect(within(card).getByText("no phone listed")).toBeInTheDocument();
  });

  it("never-list scan passes over the rendered fixture pages", async () => {
    await submitWith(day10);
    const page = { page: document.body.textContent };
    expect(neverListHits(page, NEVER_LIST)).toEqual([]);
    expect(neverListHits(page, VENDOR_NEVER_LIST)).toEqual([]);
  });
});
