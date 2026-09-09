import { afterEach, describe, expect, it, vi } from "vitest";
import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import FoodTodayPage from "./page";
import day9 from "../../../../docs/evidence/moo-777-live-53206-2026-09-09-demo.json";

const routes = [
  { name: "2-1-1 (IMPACT 211 in Milwaukee County)", purpose: "Find local food and other help by phone, any day.", phone: "2-1-1", url: "https://www.impactinc.org/impact-211/", source_url: "https://www.impactinc.org/impact-211/", last_checked: "2026-09-08" },
  { name: "Hunger Task Force emergency food", purpose: "Milwaukee County pantry and meal map.", phone: null, url: "https://www.hungertaskforce.org/get-help/emergency-food/", source_url: "https://www.hungertaskforce.org/get-help/emergency-food/", last_checked: "2026-09-08" },
  { name: "FoodShare member line", purpose: "Questions about your FoodShare case or QUEST card.", phone: "1-800-362-3002", url: "https://www.dhs.wisconsin.gov/foodshare/index.htm", source_url: "https://www.dhs.wisconsin.gov/foodshare/index.htm", last_checked: "2026-09-08" },
];
const noMatch = { status: "no_match", data: null, evidence: [], missing: ["No feasible resource found; see help route"], warnings: [], retryable: false, request_id: "r-nm", help_routes: routes };

afterEach(() => vi.unstubAllGlobals());

async function submit(envelope: unknown, zip = "53001") {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ status: 200, json: async () => envelope }));
  const user = userEvent.setup();
  render(<FoodTodayPage />);
  await user.type(screen.getByLabelText("ZIP code"), zip);
  await user.click(screen.getByRole("radio", { name: "No kitchen" }));
  await user.click(screen.getByRole("checkbox", { name: "Bus" }));
  await user.type(screen.getByLabelText(/how many minutes/), "30");
  await user.click(screen.getByRole("button", { name: "Show food today" }));
  return user;
}

describe("no-match, footer, summary line", () => {
  it("renders the statement, three route cards, and Try another ZIP; no option cards", async () => {
    const user = await submit(noMatch);
    expect(await screen.findByRole("heading", { level: 1 })).toHaveTextContent("Nothing is listed for 53001 today.");
    const help = screen.getByRole("region", { name: "Need more help?" });
    expect(within(help).getAllByRole("listitem")).toHaveLength(3);
    expect(within(help).getByRole("link", { name: "1-800-362-3002" })).toHaveAttribute("href", "tel:18003623002");
    expect(within(help).getByRole("link", { name: "www.impactinc.org" })).toHaveAttribute("href", "https://www.impactinc.org/impact-211/");
    expect(within(help).getAllByText("Checked 2026-09-08")).toHaveLength(3);
    expect(screen.queryAllByRole("article")).toHaveLength(0);

    await user.click(screen.getByRole("button", { name: "Try another ZIP" }));
    const zipField = screen.getByLabelText("ZIP code");
    expect(zipField).toBeVisible();
    expect(zipField).toHaveValue("53001");
    expect(zipField).toHaveFocus();
  });

  it("folds the form into a summary line after a result; Change reopens it with values kept", async () => {
    const user = await submit(day9, "53206");
    await screen.findByRole("heading", { level: 1 });
    expect(screen.getByLabelText("ZIP code")).not.toBeVisible();
    const summary = screen.getByLabelText("Your answers");
    expect(summary).toHaveTextContent("53206");
    expect(summary).toHaveTextContent("$0");
    expect(summary).toHaveTextContent("No kitchen");
    expect(summary).toHaveTextContent("Bus up to 30 min");

    await user.click(within(summary).getByRole("button", { name: "Change" }));
    expect(screen.getByLabelText("ZIP code")).toBeVisible();
    expect(screen.getByLabelText("ZIP code")).toHaveValue("53206");
    expect(screen.getByRole("checkbox", { name: "Bus" })).toBeChecked();
    expect(screen.getByRole("radio", { name: "No kitchen" })).toBeChecked();
    expect(screen.queryByLabelText("Your answers")).not.toBeInTheDocument();
  });

  it("shows the footer under a success with routes, and not without", async () => {
    await submit({ ...day9, help_routes: routes }, "53206");
    await screen.findByRole("heading", { level: 1 });
    expect(screen.getByRole("region", { name: "Need more help?" })).toBeInTheDocument();
    vi.unstubAllGlobals();
    document.body.innerHTML = "";
    await submit(day9, "53206");
    await screen.findByRole("heading", { level: 1 });
    expect(screen.queryByRole("region", { name: "Need more help?" })).not.toBeInTheDocument();
  });
});
