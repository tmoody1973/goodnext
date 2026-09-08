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
        name="2-1-1 (IMPACT 211 in Milwaukee County)",
        purpose="Find local food and other help by phone, any day. In Milwaukee County you can also text MKEFOOD to 898-211, or call (414) 773-0211.",
        phone="2-1-1",
        url="https://www.impactinc.org/impact-211/",
        source_url="https://www.impactinc.org/impact-211/",
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
