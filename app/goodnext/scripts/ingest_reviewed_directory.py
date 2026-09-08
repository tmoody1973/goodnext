"""Convert the GoodNext reviewed Milwaukee directory into a directory fixture.

Input: fixtures/reviewed/*.source.json (records checked against official
provider pages, with recurring schedules, published ZIPs, evidence, and
uncertainties). Output: fixtures/milwaukee-food-resources-reviewed.json with
dated windows for the demo weeks, per the file's own use rules.
Run: uv run python scripts/ingest_reviewed_directory.py
"""

import json
import re
from datetime import date, timedelta
from pathlib import Path

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"
SRC = sorted((FIXTURES / "reviewed").glob("*.source.json"))[-1]
OUT = FIXTURES / "milwaukee-food-resources-reviewed.json"
# ponytail: dated windows for two demo weeks; regenerate when the demo week moves.
WEEK_START = date(2026, 9, 8)
WEEKS = 2
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
SERVES_ALL = re.compile(r"welcomes everyone|anyone|milwaukee community|city of milwaukee residents|no specific geographic", re.I)


def week_ordinal(d: date) -> int:
    return (d.day - 1) // 7 + 1


def materialize(schedule: list[dict]) -> list[dict]:
    windows = []
    for rule in schedule:
        days = {DAYS.index(x) for x in rule["days"]}
        ordinals = {"weekly": None, "first_weekday_of_month": {1}, "second_and_fourth_weekday_of_month": {2, 4}}[rule["frequency"]]
        for i in range(7 * WEEKS):
            d = WEEK_START + timedelta(days=i)
            if d.weekday() in days and (ordinals is None or week_ordinal(d) in ordinals):
                windows.append({"date": d.isoformat(), "open": rule["open"], "close": rule["close"], "note": rule.get("note") or None})
    return sorted(windows, key=lambda w: (w["date"], w["open"]))


def convert(r: dict, retrieved_default: str) -> dict:
    serves_all = bool(SERVES_ALL.search(r.get("service_area", "")))
    appt = r.get("appointment_required")
    return {
        "resource_id": r["resource_id"],
        "provider": r["provider"],
        "service_type": r["service_type"],
        "cost": r.get("cost", "unknown"),
        "address": r["address"],
        "zip_codes_served": list(r.get("zip_codes_served") or []),
        "serves_all_milwaukee": serves_all,
        "service_area_text": r.get("service_area", ""),
        "windows": materialize(r.get("recurring_schedule") or []),
        "requirements": list(r.get("requirements") or []),
        "appointment_required": {"yes": True, "no": False, True: True, False: False}.get(appt, "unknown"),
        "visit_limit": None if str(r.get("visit_limit", "unknown")).lower() == "unknown" else r["visit_limit"],
        "contact": r.get("contact") or "no phone listed",
        "languages": list(r.get("languages") or []),
        "last_verified": r.get("source_retrieved_on") or retrieved_default,
        "review_due_on": r.get("review_due_on"),
        "verifier": "GoodNext review of the official provider page",
        "status": r.get("status", "published"),
        "source_url": r["source_url"],
        "source": f"Official provider page, checked {r.get('source_retrieved_on') or retrieved_default}",
        "uncertainties": list(r.get("uncertainties") or []),
        "notes": " ".join(r.get("evidence") or []) + (" Services: " + "; ".join(r["services"]) if r.get("services") else ""),
    }


def main() -> None:
    raw = json.loads(SRC.read_text())
    version = raw.get("_directory_version", "")
    records = [convert(r, version[:10]) for r in raw["resources"] if r.get("status") == "published"]
    OUT.write_text(json.dumps({
        "_fixture_note": f"REVIEWED DATA. {raw.get('_directory_name')} version {version}. Each record was checked against its official provider page on the retrieval date. Recurring schedules materialized into dated windows for {WEEKS} weeks from {WEEK_START}; holiday exceptions are not known. Use rules from the source file apply. Not a live inventory, reservation, or eligibility feed.",
        "_source_file": SRC.name,
        "_official_help_fallback": raw.get("_maintenance", {}).get("official_help_fallback"),
        "resources": records,
    }, indent=2))
    print(f"loaded {len(records)} reviewed records | with windows {sum(1 for r in records if r['windows'])} | serves-all {sum(1 for r in records if r['serves_all_milwaukee'])} | with ZIP list {sum(1 for r in records if r['zip_codes_served'])} | cost unknown {sum(1 for r in records if r['cost']=='unknown')} -> {OUT.name}")


if __name__ == "__main__":
    main()
