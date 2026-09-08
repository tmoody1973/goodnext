"""Load the Milwaukee Food Environment Map layer into a directory fixture.

Source: Data You Can Use / Milwaukee Food Council, ArcGIS layer
EmergencyFood_MKE_2024 (public, no license stated; decision 006). Hours are
free text; this parser handles weekday lists, "through" ranges, and ordinal
weeks ("second and fourth Saturday"). Anything else keeps its text in notes
and gets no windows. Run: uv run python scripts/ingest_mfc_map.py [input.json]
"""

import json
import re
import sys
import urllib.request
from datetime import date, timedelta
from pathlib import Path

LAYER = "https://services5.arcgis.com/3kr3fkJcIf6EOY6g/ArcGIS/rest/services/EmergencyFood_MKE/FeatureServer/0/query?where=1%3D1&outFields=*&f=json"
SOURCE = "Milwaukee Food Environment Map (Data You Can Use / Milwaukee Food Council), data as of 2024-08-27"
SOURCE_URL = "https://experience.arcgis.com/experience/4883a0957d124294aa236d9e9cc696a5"
DATA_DATE = "2024-08-27"
# ponytail: dated windows for two demo weeks; regenerate when the demo week moves.
WEEK_START = date(2026, 9, 8)
WEEKS = 2
OUT = Path(__file__).resolve().parents[1] / "fixtures" / "milwaukee-food-environment-map-2024.json"

DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_RE = r"\b(monday|mon|tuesday|tues|tue|wednesday|wed|thursday|thurday|thurs|thur|thu|friday|fri|saturday|satuday|sat|sunday|sun)s?\b"
ORDINALS = {"first": 1, "1st": 1, "second": 2, "2nd": 2, "third": 3, "3rd": 3, "fourth": 4, "4th": 4, "fouth": 4, "forth": 4, "fifth": 5}
TIME_RE = r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)"
RANGE_RE = re.compile(TIME_RE + r"\s*-\s*" + TIME_RE)
TYPES = {"Food Pantry": "free_pantry", "Meal Program": "free_meal", "Food Bank": "free_pantry", "Food Pantry and Recovery": "free_pantry"}


def to_hhmm(h, m, ap):
    h = int(h) % 12 + (12 if ap == "pm" else 0)
    return f"{h:02d}:{m or '00'}"


def parse_days(text):
    """'Monday through Friday' -> [0..4]; 'Tuesdays and Thursdays' -> [1,3]. Also returns ordinals if any."""
    text = text.lower()
    ordinals = sorted({ORDINALS[w] for w in re.findall(r"\b(first|second|third|fourth|fifth|1st|2nd|3rd|4th|fouth|forth)\b", text)})
    tokens = re.findall(DAY_RE, text)
    if not tokens:
        return [], ordinals
    idx = [DAYS.index(next(d for d in DAYS if d.startswith(t[:3]))) for t in tokens]
    if re.search(r"\b(through|thru|to)\b|\s-\s", re.sub(RANGE_RE, "", text)) and len(idx) == 2:
        lo, hi = idx
        idx = list(range(lo, hi + 1)) if lo <= hi else idx
    return sorted(set(idx)), ordinals


def week_ordinal(d):
    return (d.day - 1) // 7 + 1


def expand(days, ordinals, ranges):
    windows = []
    for i in range(7 * WEEKS):
        d = WEEK_START + timedelta(days=i)
        if d.weekday() not in days:
            continue
        if ordinals and week_ordinal(d) not in ordinals:
            continue
        for o, c in ranges:
            windows.append({"date": d.isoformat(), "open": o, "close": c})
    return windows


def parse_hours(text):
    """Return (windows, parsed_fully). Segments split on , ; and ' and ' between day groups."""
    if not text:
        return [], False
    clean = re.sub(r"^(hot meals|bagged food|pantry|meals)\s*:\s*", "", text.strip(), flags=re.I)
    clean = re.sub(r"\b(every|each)\b", "", clean, flags=re.I)
    segments = [s.strip() for s in re.split(r"[,;]|\.\s", clean) if s.strip()]
    windows, pending_days, pending_ord, any_range, unparsed = [], [], [], False, False
    for seg in segments:
        ranges = [(to_hhmm(a, b, c), to_hhmm(d, e, f)) for a, b, c, d, e, f in RANGE_RE.findall(seg)]
        days, ordinals = parse_days(RANGE_RE.sub("", seg))
        if days:
            pending_days, pending_ord = days, ordinals or pending_ord
        if ranges and pending_days:
            windows += expand(pending_days, pending_ord, ranges)
            any_range = True
        elif not ranges and not days:
            unparsed = True  # e.g. "visits are limited to once per month"
        elif not ranges and days and re.search(TIME_RE, seg):
            unparsed = True  # a start time with no end: hours unknown
    return windows, any_range and not unparsed


def zips_from(text):
    return sorted(set(re.findall(r"\b5[0-9]{4}\b", str(text or ""))))


def visit_limit(text):
    m = re.search(r"(once per month|one visit every 30 days|once a month|limited to once per month)", str(text or ""), re.I)
    return "Once per month" if m else None


def convert(feature):
    a = feature["attributes"]
    notes = str(a.get("USER_Notes") or "").strip().replace("\n", " ")
    windows, parsed = parse_hours(notes)
    zip_code = str(a.get("USER_Zip_Code") or "").strip()[:5]
    return {
        "resource_id": f"mfc-{int(a['ObjectID']):03d}",
        "provider": str(a.get("USER_Company_Business_Name") or "").strip(),
        "service_type": TYPES.get(str(a.get("USER_Type") or "").strip(), "free_pantry"),
        "cost": "free",
        "address": f"{str(a.get('USER_Address') or '').strip()}, {str(a.get('USER_City') or 'Milwaukee').strip()}, WI {zip_code}".strip(", "),
        "zip_codes_served": zips_from(a.get("USER_Service_Area")),
        "windows": windows,
        "requirements": [],
        "appointment_required": False,
        "visit_limit": visit_limit(notes),
        "contact": str(a.get("USER_Phone_Number") or "").strip() or "no phone listed",
        "languages": [],
        "last_verified": DATA_DATE,
        "verifier": "map publisher",
        "status": "published",
        "source_url": str(a.get("USER_Website") or "").strip() or SOURCE_URL,
        "source": SOURCE,
        "notes": (f"Listed hours: {notes}. " if notes else "No hours listed. ") + ("" if parsed else "Hours could not be fully parsed; call to confirm. "),
    }, parsed, bool(notes)


def main(path=None):
    raw = json.load(open(path)) if path else json.load(urllib.request.urlopen(LAYER, timeout=30))
    records, parsed_n, with_hours = [], 0, 0
    for f in raw["features"]:
        r, parsed, has_hours = convert(f)
        if not r["provider"]:
            continue
        records.append(r); parsed_n += parsed; with_hours += has_hours
    OUT.write_text(json.dumps({"_fixture_note": f"REAL DATA. {SOURCE}. Public layer, no license stated; used for the hackathon demo per docs/decisions/006. Hours parsed from free text into dated windows for {WEEKS} weeks from {WEEK_START}; unparsed hours are kept in notes. Not verified by phone.", "resources": records}, indent=2))
    with_windows = sum(1 for r in records if r["windows"])
    print(f"loaded {len(records)} records | with hours text {with_hours} | fully parsed {parsed_n} | with at least one window {with_windows} | service-area ZIPs parsed {sum(1 for r in records if r['zip_codes_served'])} -> {OUT.name}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
