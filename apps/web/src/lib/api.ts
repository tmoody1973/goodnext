// Mirrors services/api/goodnext_api/main.py (request) and
// app/goodnext/schemas.py (envelope). Keep in step by hand for now.

export type Kitchen = "full" | "microwave_only" | "none";
export type Travel = "walk" | "bus" | "car" | "ride";

export type Constraints = {
  zip_code: string;
  budget_usd: number;
  kitchen: Kitchen;
  travel: Travel[];
  max_travel_minutes?: number;
};

export type EnvelopeStatus =
  | "success"
  | "partial"
  | "needs_clarification"
  | "no_match"
  | "denied"
  | "temporarily_unavailable";

export type FreshnessTier = "verified" | "call_to_confirm" | "unconfirmed";

export type Claims = {
  open_today_text: string;
  cost_label: string;
  requirements_text: string;
  appointment_text: string;
  freshness_text: string;
  inventory_text: string;
  service_area_text: string;
  travel_text: string;
  directions_url: string;
  travel_echo: string;
  source_text: string;
};

export type PlannedVisit = {
  resource_id: string;
  provider: string;
  date: string;
  cost: "free" | "paid" | "sliding" | "unknown";
  schedule_text: string;
  requirements: string[];
  last_verified: string;
  contact: string;
  freshness_tier: FreshnessTier;
  service_area_known: boolean;
  uncertainty: string[];
  next_open: { date: string; open: string; close: string } | null;
  claims: Claims | null;
};

export type DayPlan = { date: string; visits: PlannedVisit[]; meal_notes: string[]; unmet_needs: string[] };

export type HelpRoute = {
  name: string;
  purpose: string;
  phone: string | null;
  url: string | null;
  source_url: string;
  last_checked: string;
};

export type PlanData = {
  start_date: string;
  days: DayPlan[];
  food_today: PlannedVisit[];
  unconfirmed: { resource_id: string; provider: string; contact: string }[];
  explanation: string;
};

export type Envelope<T = PlanData> = {
  status: EnvelopeStatus;
  data: T | null;
  evidence: string[];
  missing: string[];
  warnings: string[];
  retryable: boolean;
  request_id: string;
  help_routes?: HelpRoute[];
};

// A network or fetch failure reads to the resident like the API's own 503.
export function unreachableEnvelope<T = PlanData>(): Envelope<T> {
  return { status: "temporarily_unavailable", data: null, evidence: [], missing: [], warnings: ["unreachable"], retryable: true, request_id: "local" };
}

// Understand my letter (MOO-791). The API reads the letter and matches it to
// reviewed policy passages; the site renders those, never a paraphrase.
export type NoticeClass = "six_month_report" | "proof_request";

export type PolicyPassage = {
  passage_id: string;
  topic: string;
  passage: string;
  action_for_resident: string;
  program: string;
  jurisdiction: string;
  source_url: string;
  source_retrieved_on: string;
  effective_dates: string;
  version: string;
  review_status: string;
  review_owner: string;
  uncertainties: string[];
};

export type NoticeData = {
  notice_class: NoticeClass | null;
  found_dates: string[];
  extracted_text: string;
  passages: PolicyPassage[];
};

export type NoticeEnvelope = Envelope<NoticeData>;

// Relative path on purpose (decision 008). Credentials so the API's session
// cookie round-trips. The API returns an envelope even on 503.
export async function postPlan(constraints: Constraints, signal?: AbortSignal): Promise<Envelope> {
  const response = await fetch("/api/plans", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "same-origin",
    body: JSON.stringify({ workflow: "food_today", constraints }),
    signal,
  });
  const body: unknown = await response.json();
  if (!isEnvelope(body)) throw new Error(`unexpected response shape (${response.status})`);
  return body as Envelope;
}

// A letter file (a chosen sample, or one the resident opens) goes up as
// multipart form data; the browser sets the Content-Type boundary itself.
export async function postNotice(file: File, signal?: AbortSignal): Promise<NoticeEnvelope> {
  const form = new FormData();
  form.append("file", file);
  const response = await fetch("/api/notices", {
    method: "POST",
    credentials: "same-origin",
    body: form,
    signal,
  });
  const body: unknown = await response.json();
  if (!isEnvelope(body)) throw new Error(`unexpected response shape (${response.status})`);
  return body as NoticeEnvelope;
}

// Checks the envelope frame only; the data shape is cast by each caller, since
// a plan and a notice share this frame but carry different data.
function isEnvelope(value: unknown): value is Envelope<unknown> {
  if (typeof value !== "object" || value === null) return false;
  const v = value as Record<string, unknown>;
  return typeof v.status === "string" && typeof v.request_id === "string" && "data" in v;
}
