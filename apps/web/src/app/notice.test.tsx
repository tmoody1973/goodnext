import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { act, render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import path from "node:path";
import UnderstandNoticePage from "./notice/page";
import { copy } from "@/lib/copy";
import { NEVER_LIST, VENDOR_NEVER_LIST, neverListHits, readContextAvoidWords } from "@/lib/never-list";

const CONTEXT_MD = path.resolve(__dirname, "../../../../CONTEXT.md");

const routes = [
  { name: "2-1-1 (IMPACT 211 in Milwaukee County)", purpose: "Find local food and other help by phone, any day.", phone: "2-1-1", url: "https://www.impactinc.org/impact-211/", source_url: "https://www.impactinc.org/impact-211/", last_checked: "2026-09-08" },
  { name: "Hunger Task Force emergency food", purpose: "Milwaukee County pantry and meal map.", phone: null, url: "https://www.hungertaskforce.org/get-help/emergency-food/", source_url: "https://www.hungertaskforce.org/get-help/emergency-food/", last_checked: "2026-09-08" },
  { name: "FoodShare member line", purpose: "Questions about your FoodShare case or QUEST card.", phone: "1-800-362-3002", url: "https://www.dhs.wisconsin.gov/foodshare/index.htm", source_url: "https://www.dhs.wisconsin.gov/foodshare/index.htm", last_checked: "2026-09-08" },
];

const passage = {
  passage_id: "fs-six-month-report-basics",
  topic: "What a six-month report is",
  passage: "A six-month report is a periodic report some FoodShare households must return to keep their benefits. The letter states the household's own due date.",
  action_for_resident: "Read the due date on your own letter and return the report by that date.",
  program: "FoodShare (Wisconsin SNAP)",
  jurisdiction: "Wisconsin",
  source_url: "https://www.dhs.wisconsin.gov/foodshare/index.htm",
  source_retrieved_on: "2026-09-08",
  effective_dates: "",
  version: "2026-09-08.1",
  review_status: "draft",
  review_owner: "GoodNext maintainer — benefits-staff review required before pilot",
  uncertainties: ["Whether a given household must file this report, and the exact due date, come from the resident's own letter and case, not from this file."],
};
const base = { evidence: [], missing: [], warnings: [], retryable: false, request_id: "r", help_routes: routes };
const success = { ...base, status: "success", data: { notice_class: "six_month_report", found_dates: ["September 30, 2026"], extracted_text: "Six-Month Report Due. Your report is due by September 30, 2026.", passages: [passage] } };
const noMatch = { ...base, status: "no_match", data: { notice_class: null, found_dates: [], extracted_text: "A postcard about a picnic.", passages: [] } };
const unavailable = { ...base, status: "temporarily_unavailable", data: null, retryable: true, warnings: ["could not read the letter: ExtractionUnavailable"] };

const letter = () => new File([new Uint8Array([0x25, 0x50, 0x44, 0x46])], "letter.pdf", { type: "application/pdf" });

afterEach(() => vi.unstubAllGlobals());

async function upload(envelope: unknown) {
  const fetchMock = vi.fn().mockResolvedValue({ status: 200, json: async () => envelope });
  vi.stubGlobal("fetch", fetchMock);
  const user = userEvent.setup();
  render(<UnderstandNoticePage />);
  await user.upload(screen.getByLabelText(/open a letter file/), letter());
  return { user, fetchMock };
}

describe("understand my letter", () => {
  it("renders the class, the dates, the reviewed passage, and the help routes", async () => {
    await upload(success);
    expect(await screen.findByRole("heading", { level: 1 })).toHaveTextContent("This looks like a six-month report.");
    const dates = screen.getByRole("region", { name: "Dates your letter mentions" });
    expect(within(dates).getByText("September 30, 2026")).toBeInTheDocument();
    const guidance = screen.getByRole("region", { name: "Guidance we have reviewed" });
    const card = within(guidance).getByRole("article");
    expect(within(card).getByRole("heading", { level: 3 })).toHaveTextContent("What a six-month report is");
    expect(within(card).getByText(/return the report by that date/)).toBeInTheDocument();
    expect(within(card).getByRole("link", { name: "www.dhs.wisconsin.gov" })).toHaveAttribute("href", "https://www.dhs.wisconsin.gov/foodshare/index.htm");
    expect(within(card).getByText("Checked 2026-09-08")).toBeInTheDocument();
    expect(within(card).getByText(/Confirm with a caseworker/)).toBeInTheDocument();
    expect(screen.getByRole("region", { name: "Need more help?" })).toBeInTheDocument();
    // The letter text is available to read but does not compete with the guidance.
    expect(screen.getByText("What we read from your letter")).toBeInTheDocument();
  });

  it("moves focus to the result heading", async () => {
    await upload(success);
    const heading = await screen.findByRole("heading", { level: 1 });
    expect(heading).toHaveFocus();
    expect(heading.closest("[aria-live]")).not.toBeNull();
  });

  it("says so plainly when no reviewed guidance fits, and still shows help routes", async () => {
    await upload(noMatch);
    expect(await screen.findByText("We read your letter but found no reviewed guidance that fits it.")).toBeInTheDocument();
    expect(screen.queryByRole("article")).not.toBeInTheDocument();
    expect(screen.getByRole("region", { name: "Need more help?" })).toBeInTheDocument();
  });

  it("shows a temporarily unavailable message with Retry that re-sends the same file", async () => {
    const { user, fetchMock } = await upload(unavailable);
    expect(await screen.findByRole("alert")).toHaveTextContent("Temporarily unavailable. Try again in a moment.");
    expect(document.body.textContent).not.toContain("ExtractionUnavailable");
    await user.click(screen.getByRole("button", { name: "Try again" }));
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it("treats a network failure as temporarily unavailable", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new TypeError("Failed to fetch")));
    const user = userEvent.setup();
    render(<UnderstandNoticePage />);
    await user.upload(screen.getByLabelText(/open a letter file/), letter());
    expect(await screen.findByRole("alert")).toHaveTextContent("Temporarily unavailable.");
  });

  it("no reviewed-content word list term or vendor name reaches the copy or the page", async () => {
    const avoid = readContextAvoidWords(CONTEXT_MD);
    expect(neverListHits(copy.notice, NEVER_LIST)).toEqual([]);
    expect(neverListHits(copy.notice, avoid)).toEqual([]);
    expect(neverListHits(copy.notice, VENDOR_NEVER_LIST)).toEqual([]);
    await upload(success);
    await screen.findByRole("heading", { level: 1 });
    const page = { text: document.body.textContent };
    expect(neverListHits(page, NEVER_LIST)).toEqual([]);
    expect(neverListHits(page, VENDOR_NEVER_LIST)).toEqual([]);
  });
});

describe("waiting, lifted from the page", () => {
  beforeEach(() => vi.useFakeTimers({ shouldAdvanceTime: true }));
  afterEach(() => vi.useRealTimers());

  it("shows the delayed status at 30 seconds while a letter is being read", async () => {
    vi.stubGlobal("fetch", vi.fn(() => new Promise(() => {})));
    const user = userEvent.setup({ advanceTimers: vi.advanceTimersByTime });
    render(<UnderstandNoticePage />);
    await user.upload(screen.getByLabelText(/open a letter file/), letter());
    expect(screen.getByText("Reading your letter.")).toBeInTheDocument();
    act(() => { vi.advanceTimersByTime(30_000); });
    expect(screen.getByRole("status")).toHaveTextContent("Still checking. You can wait, or use one of these help routes.");
    expect(screen.getByRole("button", { name: "Cancel" })).toBeInTheDocument();
  });
});
