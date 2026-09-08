"""The three fixed help routes for a no-match response.

CONTEXT.md: "Help route" — a maintained, verified way to reach a human,
shown whenever the site cannot help. Facts per docs/specs/food-today.md D10,
D11 and docs/FoodShare-Bridge-APIs-Data-and-Prompts.md section 2 (Official
sources). Reviewed 2026-09-08. Do not invent other numbers here; this module
is the single reviewed source, never prompt text.
"""

from schemas import HelpRoute

LAST_CHECKED = "2026-09-08"

HELP_ROUTES: list[HelpRoute] = [
    HelpRoute(
        name="2-1-1",
        purpose="Find local food and other help by phone, any day.",
        phone="2-1-1",
        url="https://www.211.org",
        source_url="https://www.211.org",
        last_checked=LAST_CHECKED,
    ),
    HelpRoute(
        name="Hunger Task Force emergency food",
        purpose="Milwaukee County pantry and meal map.",
        url="https://www.hungertaskforce.org/get-help/emergency-food/",
        source_url="https://www.hungertaskforce.org/get-help/emergency-food/",
        last_checked=LAST_CHECKED,
    ),
    HelpRoute(
        name="FoodShare member line",
        purpose="Questions about your FoodShare case or QUEST card.",
        phone="1-800-362-3002",
        url="https://www.dhs.wisconsin.gov/foodshare/index.htm",
        source_url="https://www.dhs.wisconsin.gov/foodshare/index.htm",
        last_checked=LAST_CHECKED,
    ),
]
