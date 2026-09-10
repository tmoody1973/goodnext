import { afterEach, describe, expect, it, vi } from "vitest";
import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import axe from "axe-core";
import FoodTodayPage from "./page";
import { NEVER_LIST, VENDOR_NEVER_LIST, neverListHits } from "@/lib/never-list";
import { NOTICE_NEVER_LIST } from "@/lib/never-list";

const routes = [
  { name: "2-1-1 (IMPACT 211 in Milwaukee County)", purpose: "Find local food and other help by phone, any day.", phone: "2-1-1", url: "https://www.impactinc.org/impact-211/", source_url: "https://www.impactinc.org/impact-211/", last_checked: "2026-09-08" },
  { name: "Hunger Task Force emergency food", purpose: "Milwaukee County pantry and meal map.", phone: null, url: "https://www.hungertaskforce.org/get-help/emergency-food/", source_url: "https://www.hungertaskforce.org/get-help/emergency-food/", last_checked: "2026-09-08" },
  { name: "FoodShare member line", purpose: "Questions about your FoodShare case or QUEST card.", phone: "1-800-362-3002", url: "https://www.dhs.wisconsin.gov/foodshare/index.htm", source_url: "https://www.dhs.wisconsin.gov/foodshare/index.htm", last_checked: "2026-09-08" },
];

// Hand-written until the first live run saves a real envelope under docs/evidence.
const sanction = {
  status: "success",
  data: {
    letter_kind: "sanction",
    screening: "action_identified",
    findings: [{ label: "What the letter says", text: "A sanction means you will not get FoodShare from 10/01/2026 to 12/31/2026.", passage_ids: ["p1-2"] }],
    next_step: { text: "Call your agency to ask about good cause and your right to a fair hearing.", passage_ids: ["p1-3"] },
    tasks: [
      { kind: "reapply", text: "Reapply for FoodShare after the sanction period.", date_text: "01/01/2027", date_kind: "official", passage_ids: ["p1-4"] },
      { kind: "fair_hearing", text: "Ask for a fair hearing if you disagree.", date_text: "not stated", date_kind: "unknown", passage_ids: ["p1-3"] },
    ],
    questions_to_ask: [{ text: "Does good cause apply to why I left the job?", policy_ids: ["pol-001"] }],
    routes: [{ name: "Your agency (from your letter)", phone: "1-888-947-6583", url: null, source: "from your letter" }],
    unknowns: ["Whether you have a good cause reason is for the agency to decide."],
    explanation: "This letter says a sanction starts 10/01/2026. You can reapply after it ends and can ask for a fair hearing.",
    passages: [
      { id: "p1-1", page: 1, text: "FoodShare Notice of Sanction" },
      { id: "p1-2", page: 1, text: "This letter is to notify you that you have voluntarily quit a job without good cause. As a result, you will not be eligible for FoodShare from 10/01/2026 to 12/31/2026." },
      { id: "p1-3", page: 1, text: "If you do not agree with this decision, you have the right to a fair hearing." },
      { id: "p1-4", page: 1, text: "You can reapply for benefits any time on or after 01/01/2027 or any time you become exempt from the work requirement." },
    ],
  },
  evidence: ["p1-2", "p1-3", "p1-4", "pol-001"],
  missing: [],
  warnings: [],
  retryable: false,
  request_id: "n-1",
  help_routes: routes,
};
const unknownLetter = { ...sanction, data: { ...sanction.data, letter_kind: "unknown", screening: "more_information_needed", findings: [], next_step: null, tasks: [], questions_to_ask: [], passages: [{ id: "p1-1", page: 1, text: "Dear neighbor, your library card expires soon." }] } };
const rejected = { status: "needs_clarification", data: null, evidence: [], missing: ["We can read a PDF, JPG, or PNG up to 10 MB and 6 pages. This file does not look like one."], warnings: [], retryable: false, request_id: "n-2", help_routes: routes };

afterEach(() => vi.unstubAllGlobals());

function stub(envelope: unknown, status = 200) {
  const fetchMock = vi.fn().mockResolvedValue({ status, json: async () => envelope });
  vi.stubGlobal("fetch", fetchMock);
  return fetchMock;
}

async function openLetter() {
  const user = userEvent.setup();
  render(<FoodTodayPage />);
  await user.click(screen.getByRole("tab", { name: "Understand my letter" }));
  return user;
}

async function uploadPdf(user: ReturnType<typeof userEvent.setup>) {
  const file = new File(["%PDF-1.4 fake"], "letter.pdf", { type: "application/pdf" });
  await user.upload(screen.getByLabelText(/Your letter/), file);
  await user.click(screen.getByRole("button", { name: "Read my letter" }));
}

async function seriousAxeFindings() {
  const result = await axe.run(document.body, { rules: { "color-contrast": { enabled: false } } });
  return result.violations.filter((v) => v.impact === "serious" || v.impact === "critical").map((v) => v.id);
}

describe("Understand my letter", () => {
  it("the front door keeps Find food today first and switches without losing the ZIP", async () => {
    stub(sanction);
    const user = userEvent.setup();
    render(<FoodTodayPage />);
    expect(screen.getByRole("tab", { name: "Find food today" })).toHaveAttribute("aria-selected", "true");
    await user.type(screen.getByLabelText("ZIP code"), "53206");
    await user.click(screen.getByRole("tab", { name: "Understand my letter" }));
    expect(screen.getByLabelText(/Your letter/)).toBeInTheDocument();
    expect(screen.getByText(/read once to find what it asks and is not stored/)).toBeInTheDocument();
    expect(screen.getByText(/PDF, JPG, or PNG up to 10 MB/)).toBeInTheDocument();
    await user.click(screen.getByRole("tab", { name: "Find food today" }));
    expect(screen.getByLabelText("ZIP code")).toHaveValue("53206");
  });

  it("uploads the file as multipart with credentials and renders the result beside its passages", async () => {
    const fetchMock = stub(sanction);
    const user = await openLetter();
    await uploadPdf(user);
    expect(await screen.findByRole("heading", { level: 1 })).toHaveTextContent("Notice of Sanction");
    const [url, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(url).toBe("/api/notices");
    expect(init.credentials).toBe("same-origin");
    expect(init.body).toBeInstanceOf(FormData);
    expect((init.body as FormData).get("file")).toBeInstanceOf(File);

    expect(screen.getByText("Something to do")).toBeInTheDocument();
    const finding = screen.getByText("A sanction means you will not get FoodShare from 10/01/2026 to 12/31/2026.").closest("article")!;
    expect(within(finding).getByText(/This letter is to notify you/)).toBeInTheDocument();
    expect(within(finding).getByText("Page 1")).toBeInTheDocument();
    expect(within(finding).getByRole("heading", { level: 3 })).toHaveTextContent("What the letter says");
    expect(screen.getByText("Call your agency to ask about good cause and your right to a fair hearing.")).toBeInTheDocument();
    const tasks = screen.getByRole("list", { name: "Tasks" });
    expect(within(tasks).getAllByRole("listitem")).toHaveLength(2);
    expect(tasks).toHaveTextContent("01/01/2027");
    expect(tasks).toHaveTextContent("Date not stated in the letter");
    expect(screen.getByText("Does good cause apply to why I left the job?")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Call 1-888-947-6583, Your agency (from your letter)" })).toHaveAttribute("href", "tel:18889476583");
    expect(screen.getByText("Whether you have a good cause reason is for the agency to decide.")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Find food today" })).toBeInTheDocument();
    expect(screen.getByRole("region", { name: "Need more help?" })).toBeInTheDocument();
  });

  it("Find food today from a result switches back to the food form", async () => {
    stub(sanction);
    const user = await openLetter();
    await uploadPdf(user);
    await screen.findByRole("heading", { level: 1 });
    await user.click(screen.getByRole("button", { name: "Find food today" }));
    expect(screen.getByLabelText("ZIP code")).toBeVisible();
  });

  it("an unrecognized letter says so and shows the routes, no verdicts", async () => {
    stub(unknownLetter);
    const user = await openLetter();
    await uploadPdf(user);
    expect(await screen.findByRole("heading", { level: 1 })).toHaveTextContent("We could not tell what this letter is");
    expect(screen.getByText("More information needed")).toBeInTheDocument();
    expect(screen.queryByRole("list", { name: "Tasks" })).not.toBeInTheDocument();
    expect(screen.getByRole("region", { name: "Need more help?" })).toBeInTheDocument();
  });

  it("a rejected file shows the limit and keeps the form", async () => {
    stub(rejected, 400);
    const user = await openLetter();
    await uploadPdf(user);
    expect(await screen.findByRole("alert")).toHaveTextContent("PDF, JPG, or PNG up to 10 MB");
    expect(screen.getByLabelText(/Your letter/)).toBeInTheDocument();
  });

  it("the three questions post without a file", async () => {
    const fetchMock = stub(sanction);
    const user = await openLetter();
    await user.click(screen.getByRole("button", { name: /Answer three questions/ }));
    await user.selectOptions(screen.getByLabelText("What kind of letter is it?"), "six_month_report");
    await user.type(screen.getByLabelText(/What date does it show/), "March 2027");
    await user.type(screen.getByLabelText(/What does it seem to ask/), "Fill out a form");
    await user.click(screen.getByRole("button", { name: "Read my answers" }));
    await screen.findByRole("heading", { level: 1 });
    const body = (fetchMock.mock.calls[0] as [string, RequestInit])[1].body as FormData;
    expect(body.get("file")).toBeNull();
    expect(body.get("letter_kind")).toBe("six_month_report");
    expect(body.get("date_text")).toBe("March 2027");
  });

  it("never-list scans pass over the copy and the rendered result", async () => {
    stub(sanction);
    const user = await openLetter();
    await uploadPdf(user);
    await screen.findByRole("heading", { level: 1 });
    const page = { page: document.body.textContent };
    expect(neverListHits(page, NEVER_LIST)).toEqual([]);
    expect(neverListHits(page, VENDOR_NEVER_LIST)).toEqual([]);
    expect(neverListHits(page, NOTICE_NEVER_LIST)).toEqual([]);
  });

  it("axe: letter form and result have no serious or critical findings", async () => {
    stub(sanction);
    const user = await openLetter();
    expect(await seriousAxeFindings()).toEqual([]);
    await uploadPdf(user);
    await screen.findByRole("heading", { level: 1 });
    expect(await seriousAxeFindings()).toEqual([]);
  });
});
