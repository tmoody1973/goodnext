import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { act, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import FoodTodayPage from "./page";

const routes = [
  { name: "2-1-1 (IMPACT 211 in Milwaukee County)", purpose: "Find local food and other help by phone, any day.", phone: "2-1-1", url: "https://www.impactinc.org/impact-211/", source_url: "https://www.impactinc.org/impact-211/", last_checked: "2026-09-08" },
  { name: "Hunger Task Force emergency food", purpose: "Milwaukee County pantry and meal map.", phone: null, url: "https://www.hungertaskforce.org/get-help/emergency-food/", source_url: "https://www.hungertaskforce.org/get-help/emergency-food/", last_checked: "2026-09-08" },
  { name: "FoodShare member line", purpose: "Questions about your FoodShare case or QUEST card.", phone: "1-800-362-3002", url: "https://www.dhs.wisconsin.gov/foodshare/index.htm", source_url: "https://www.dhs.wisconsin.gov/foodshare/index.htm", last_checked: "2026-09-08" },
];
const base = { data: null, evidence: [], missing: [], warnings: [], retryable: false, request_id: "r" };
const unavailable = { ...base, status: "temporarily_unavailable", retryable: true, warnings: ["agent unavailable: ConnectError"], help_routes: routes };
const denied = { ...base, status: "denied", help_routes: routes };

// A fetch that never resolves unless aborted (then rejects like a browser would).
function hangingFetch() {
  return vi.fn((_url: string, init?: RequestInit) => new Promise((_, reject) => {
    init?.signal?.addEventListener("abort", () => reject(new DOMException("The user aborted a request.", "AbortError")));
  }));
}

beforeEach(() => vi.useFakeTimers({ shouldAdvanceTime: true }));
afterEach(() => { vi.useRealTimers(); vi.unstubAllGlobals(); });

async function submit(user: ReturnType<typeof userEvent.setup>) {
  await user.type(screen.getByLabelText("ZIP code"), "53206");
  await user.click(screen.getByRole("checkbox", { name: "Bus" }));
  await user.click(screen.getByRole("button", { name: "Show food today" }));
}

describe("waiting, delayed status, unavailable", () => {
  it("shows the delayed status at 30 seconds and not at 29", async () => {
    vi.stubGlobal("fetch", hangingFetch());
    const user = userEvent.setup({ advanceTimers: vi.advanceTimersByTime });
    render(<FoodTodayPage />);
    await submit(user);
    expect(screen.getByText("This usually takes one to two minutes.")).toBeInTheDocument();
    act(() => { vi.advanceTimersByTime(29_000); });
    expect(screen.queryByRole("status")).not.toBeInTheDocument();
    act(() => { vi.advanceTimersByTime(1_000); });
    expect(screen.getByRole("status")).toHaveTextContent("Still checking. You can wait, or use one of these help routes.");
    expect(screen.getByRole("button", { name: "Cancel" })).toBeInTheDocument();
    expect(screen.getByText("Checking today's listings for 53206.")).toBeInTheDocument();
  });

  it("Cancel aborts the request and keeps the form values", async () => {
    const fetchMock = hangingFetch();
    vi.stubGlobal("fetch", fetchMock);
    const user = userEvent.setup({ advanceTimers: vi.advanceTimersByTime });
    render(<FoodTodayPage />);
    await submit(user);
    act(() => { vi.advanceTimersByTime(30_000); });
    await user.click(screen.getByRole("button", { name: "Cancel" }));
    const init = fetchMock.mock.calls[0][1] as RequestInit;
    expect(init.signal?.aborted).toBe(true);
    expect(screen.queryByText(/Checking today's listings/)).not.toBeInTheDocument();
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
    expect(screen.getByLabelText("ZIP code")).toHaveValue("53206");
    expect(screen.getByRole("checkbox", { name: "Bus" })).toBeChecked();
    expect(screen.getByRole("button", { name: "Show food today" })).toBeEnabled();
  });

  it("shows a sentence, Retry, and the help routes on the API's 503 envelope; Retry re-sends the same request", async () => {
    const fetchMock = vi.fn().mockResolvedValue({ status: 503, json: async () => unavailable });
    vi.stubGlobal("fetch", fetchMock);
    const user = userEvent.setup({ advanceTimers: vi.advanceTimersByTime });
    render(<FoodTodayPage />);
    await submit(user);
    expect(await screen.findByRole("alert")).toHaveTextContent("Temporarily unavailable. Try again in a moment.");
    expect(screen.getByText("Need more help?")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "1-800-362-3002" })).toHaveAttribute("href", "tel:18003623002");
    expect(screen.getByRole("link", { name: "www.hungertaskforce.org" })).toHaveAttribute("target", "_blank");
    expect(document.body.textContent).not.toContain("ConnectError");
    await user.click(screen.getByRole("button", { name: "Try again" }));
    expect(fetchMock).toHaveBeenCalledTimes(2);
    expect(fetchMock.mock.calls[1][1].body).toEqual(fetchMock.mock.calls[0][1].body);
  });

  it("treats a network failure as temporarily unavailable, with the last known help routes", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new TypeError("Failed to fetch")));
    const user = userEvent.setup({ advanceTimers: vi.advanceTimersByTime });
    render(<FoodTodayPage />);
    await submit(user);
    expect(await screen.findByRole("alert")).toHaveTextContent("Temporarily unavailable.");
    expect(screen.getByRole("button", { name: "Try again" })).toBeInTheDocument();
  });

  it("shows the generic message and Change on a denied envelope", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ status: 200, json: async () => denied }));
    const user = userEvent.setup({ advanceTimers: vi.advanceTimersByTime });
    render(<FoodTodayPage />);
    await submit(user);
    expect(await screen.findByRole("alert")).toHaveTextContent("We could not build a list for that answer.");
    await user.click(screen.getByRole("button", { name: "Change my answers" }));
    expect(screen.getByLabelText("ZIP code")).toHaveFocus();
    expect(screen.getByText("2-1-1 (IMPACT 211 in Milwaukee County)")).toBeInTheDocument();
  });

  it("remembers help routes from a prior response and shows them in the delayed status", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce({ status: 200, json: async () => denied })
      .mockImplementationOnce(hangingFetch());
    vi.stubGlobal("fetch", fetchMock);
    const user = userEvent.setup({ advanceTimers: vi.advanceTimersByTime });
    render(<FoodTodayPage />);
    await submit(user);
    await screen.findByRole("alert");
    await user.click(screen.getByRole("button", { name: "Change my answers" }));
    await user.click(screen.getByRole("button", { name: "Show food today" }));
    act(() => { vi.advanceTimersByTime(30_000); });
    expect(screen.getByRole("status")).toBeInTheDocument();
    expect(screen.getByText("FoodShare member line")).toBeInTheDocument();
  });
});
