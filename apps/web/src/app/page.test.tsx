import { afterEach, describe, expect, it, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import FoodTodayPage from "./page";

const successEnvelope = {
  status: "success",
  data: { start_date: "2026-09-09", days: [], food_today: [], unconfirmed: [], explanation: "" },
  evidence: [],
  missing: [],
  warnings: [],
  retryable: false,
  request_id: "test-request",
  help_routes: [],
};

afterEach(() => vi.unstubAllGlobals());

async function fillValidForm(user: ReturnType<typeof userEvent.setup>) {
  await user.type(screen.getByLabelText("ZIP code"), "53206");
  await user.click(screen.getByRole("checkbox", { name: "Bus" }));
}

describe("Food today page", () => {
  it("refuses a four-digit ZIP and sends nothing", async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    const user = userEvent.setup();
    render(<FoodTodayPage />);
    await user.type(screen.getByLabelText("ZIP code"), "5320");
    await user.click(screen.getByRole("checkbox", { name: "Bus" }));
    await user.click(screen.getByRole("button", { name: "Show food today" }));
    expect(screen.getByRole("alert")).toHaveTextContent("Enter a five-digit ZIP code.");
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("refuses an empty travel choice and sends nothing", async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    const user = userEvent.setup();
    render(<FoodTodayPage />);
    await user.type(screen.getByLabelText("ZIP code"), "53206");
    await user.click(screen.getByRole("button", { name: "Show food today" }));
    expect(screen.getByRole("alert")).toHaveTextContent("Pick at least one way you get around.");
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("posts the constraints with credentials and shows the API date", async () => {
    const fetchMock = vi.fn().mockResolvedValue({ status: 200, json: async () => successEnvelope });
    vi.stubGlobal("fetch", fetchMock);
    const user = userEvent.setup();
    render(<FoodTodayPage />);
    await fillValidForm(user);
    await user.click(screen.getByRole("button", { name: "Show food today" }));

    expect(await screen.findByRole("heading", { level: 1 })).toHaveTextContent("Food today, DELIBERATE BREAK");
    expect(screen.getByText("Listed options found.")).toBeInTheDocument();

    const [url, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(url).toBe("/api/plans");
    expect(init.credentials).toBe("same-origin");
    expect(JSON.parse(init.body as string)).toEqual({
      workflow: "food_today",
      constraints: { zip_code: "53206", budget_usd: 0, kitchen: "full", travel: ["bus"] },
    });
  });

  it("shows the checking line while waiting", async () => {
    vi.stubGlobal("fetch", vi.fn(() => new Promise(() => {})));
    const user = userEvent.setup();
    render(<FoodTodayPage />);
    await fillValidForm(user);
    await user.click(screen.getByRole("button", { name: "Show food today" }));
    expect(screen.getByText("Checking today's listings for 53206.")).toBeInTheDocument();
    expect(screen.getByText("This usually takes one to two minutes.")).toBeInTheDocument();
  });

  it("says the service could not be reached when fetch fails", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new TypeError("Failed to fetch")));
    const user = userEvent.setup();
    render(<FoodTodayPage />);
    await fillValidForm(user);
    await user.click(screen.getByRole("button", { name: "Show food today" }));
    expect(await screen.findByRole("alert")).toHaveTextContent("We could not reach the service.");
  });
});
