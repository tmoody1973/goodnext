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

export type Envelope = {
  status: EnvelopeStatus;
  data: PlanData | null;
  evidence: string[];
  missing: string[];
  warnings: string[];
  retryable: boolean;
  request_id: string;
  help_routes?: HelpRoute[];
};

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
  return body;
}

function isEnvelope(value: unknown): value is Envelope {
  if (typeof value !== "object" || value === null) return false;
  const v = value as Record<string, unknown>;
  return typeof v.status === "string" && typeof v.request_id === "string" && "data" in v;
}

// Understand my letter (spec docs/specs/understand-notice.md). Mirrors
// app/goodnext/schemas.py NoticePlanProposal plus the passages the server supplied.

export type LetterKind = "sanction" | "time_limited_warning" | "six_month_report" | "unknown";
export type Screening = "action_identified" | "more_information_needed" | "no_action_identified";
export type DateKind = "official" | "continuity" | "suggested" | "unknown";

export type NoticePassage = { id: string; page: number; text: string };
export type Finding = { label: string; text: string; passage_ids: string[] };
export type NoticeTask = { kind: string; text: string; date_text: string; date_kind: DateKind; passage_ids: string[] };
export type NoticeRoute = { name: string; phone: string | null; url: string | null; source: string };

export type NoticeData = {
  letter_kind: LetterKind;
  screening: Screening;
  findings: Finding[];
  next_step: { text: string; passage_ids: string[] } | null;
  tasks: NoticeTask[];
  questions_to_ask: { text: string; policy_ids: string[] }[];
  routes: NoticeRoute[];
  unknowns: string[];
  explanation: string;
  passages: NoticePassage[];
};

export type NoticeEnvelope = Omit<Envelope, "data"> & { data: NoticeData | null };

// The letter travels as multipart form data: the file, or the three answers.
// Read once by the API, never stored (decision 011).
export async function postNotice(form: FormData, signal?: AbortSignal): Promise<NoticeEnvelope> {
  const response = await fetch("/api/notices", { method: "POST", body: form, credentials: "same-origin", signal });
  const body: unknown = await response.json();
  if (!isEnvelope(body)) throw new Error(`unexpected response shape (${response.status})`);
  return body as NoticeEnvelope;
}
