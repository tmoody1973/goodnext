"""Typed records for the food-today slice.

Field sets follow docs/FoodShare-Bridge-APIs-Data-and-Prompts.md section 3
(Food resource, Resident constraints, Plan and action) and PRD FR04.
"""

from typing import Literal

from pydantic import BaseModel, Field

ISODate = str  # YYYY-MM-DD, America/Chicago calendar date supplied by the server

# CONTEXT.md: verified (0-14 days), call to confirm (15-60 days), unconfirmed (>60 or none).
FreshnessTier = Literal["verified", "call_to_confirm", "unconfirmed"]


class HouseholdConstraints(BaseModel):
    zip_code: str = Field(pattern=r"^\d{5}$")
    household_size: Literal["1", "2-3", "4-5", "6+"] = "1"
    budget_usd: float = Field(ge=0, description="Spendable money for food this week; zero is valid")
    travel: list[Literal["walk", "bus", "car", "ride"]] = ["walk"]
    max_travel_minutes: int | None = Field(default=None, ge=0)
    kitchen: Literal["full", "microwave_only", "none"] = "full"
    refrigeration: bool = True
    food_on_hand: list[str] = []
    restrictions: list[str] = []
    urgency: Literal["today", "this_week"] = "today"


class ServiceWindow(BaseModel):
    date: ISODate
    open: str
    close: str
    note: str | None = None


class NextOpen(BaseModel):
    """MOO-774: the earliest still-open-or-future window carried when today's is already closed."""

    date: ISODate
    open: str
    close: str


ServiceType = Literal["free_pantry", "free_meal", "paid_market", "mobile_market"]
Cost = Literal["free", "paid", "sliding"]


class FoodResource(BaseModel):
    resource_id: str
    provider: str
    service_type: ServiceType
    cost: Cost
    address: str
    zip_codes_served: list[str]
    windows: list[ServiceWindow]
    requirements: list[str] = []
    appointment_required: bool = False
    visit_limit: str | None = None
    contact: str
    languages: list[str] = []
    last_verified: ISODate | None = None
    verifier: str
    status: Literal["published", "closed", "withdrawn"]
    source_url: str
    notes: str = ""


class Claims(BaseModel):
    """MOO-775 (D9): the eight permitted resident-facing statements for one visit,
    plus directions and the travel echo. Rendered by the application only, from
    record fields and resident constraints, never by the model. See claims.py."""

    open_today_text: str
    cost_label: str
    requirements_text: str
    appointment_text: str
    freshness_text: str
    inventory_text: str
    service_area_text: str
    travel_text: str
    directions_url: str
    travel_echo: str


class PlannedVisit(BaseModel):
    """One proposed visit. Every field the resident sees per PRD FR04."""

    resource_id: str
    provider: str
    date: ISODate
    service_type: ServiceType
    cost: Cost
    schedule_text: str = Field(description="Opening window in words, from the record")
    requirements: list[str] = []
    last_verified: ISODate
    contact: str
    freshness_tier: FreshnessTier = "unconfirmed"
    uncertainty: list[str] = Field(default=[], description="Unknowns the resident should confirm")
    backup_resource_id: str | None = None
    next_open: NextOpen | None = Field(default=None, description="Set when the resource's window today has already closed")
    claims: Claims | None = Field(default=None, description="MOO-775: the permitted claims, populated by the validator")


class DayPlan(BaseModel):
    date: ISODate
    visits: list[PlannedVisit] = []
    meal_notes: list[str] = Field(default=[], description="Only from known food or clearly conditional ingredients")
    unmet_needs: list[str] = []


class UnconfirmedRecord(BaseModel):
    """A tool-returned, unconfirmed-tier resource: phone number only, never a visit."""

    resource_id: str
    provider: str
    contact: str


class FoodPlanProposal(BaseModel):
    """Model output schema for P03. Schema validity is not factual correctness."""

    start_date: ISODate
    days: list[DayPlan] = Field(description="Exactly seven consecutive local dates")
    food_today: list[PlannedVisit] = []
    resource_ids_used: list[str] = []
    preparation_checklist: list[str] = []
    unmet_needs: list[str] = []
    unconfirmed: list[UnconfirmedRecord] = []
    explanation: str = Field(description="Short, evidence-based, resident-facing")


class HelpRoute(BaseModel):
    """CONTEXT.md: Help route. A maintained, verified way to reach a human."""

    name: str
    purpose: str = Field(description="One plain sentence")
    phone: str | None = None
    url: str | None = None
    source_url: str
    last_checked: ISODate


EnvelopeStatus = Literal[
    "success", "partial", "needs_clarification", "no_match", "denied", "temporarily_unavailable"
]


class Envelope(BaseModel):
    """Shared response envelope, APIs doc section 4."""

    status: EnvelopeStatus
    data: dict | None = None
    evidence: list[str] = []
    missing: list[str] = []
    warnings: list[str] = []
    retryable: bool = False
    request_id: str
    help_routes: list[HelpRoute] = []
