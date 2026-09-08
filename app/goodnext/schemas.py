"""Typed records for the food-today slice.

Field sets follow docs/FoodShare-Bridge-APIs-Data-and-Prompts.md section 3
(Food resource, Resident constraints, Plan and action) and PRD FR04.
"""

from typing import Literal

from pydantic import BaseModel, Field

ISODate = str  # YYYY-MM-DD, America/Chicago calendar date supplied by the server


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
    last_verified: ISODate
    verifier: str
    status: Literal["published", "closed", "withdrawn"]
    source_url: str
    notes: str = ""


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
    uncertainty: list[str] = Field(default=[], description="Unknowns the resident should confirm")
    backup_resource_id: str | None = None


class DayPlan(BaseModel):
    date: ISODate
    visits: list[PlannedVisit] = []
    meal_notes: list[str] = Field(default=[], description="Only from known food or clearly conditional ingredients")
    unmet_needs: list[str] = []


class FoodPlanProposal(BaseModel):
    """Model output schema for P03. Schema validity is not factual correctness."""

    start_date: ISODate
    days: list[DayPlan] = Field(description="Exactly seven consecutive local dates")
    food_today: list[PlannedVisit] = []
    resource_ids_used: list[str] = []
    preparation_checklist: list[str] = []
    unmet_needs: list[str] = []
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
