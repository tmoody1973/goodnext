"""The three fixed help routes, on every envelope status.

CONTEXT.md: "Help route" — a maintained, verified way to reach a human,
shown whenever the site cannot help. Facts per docs/specs/food-today.md D10,
D11 and docs/FoodShare-Bridge-APIs-Data-and-Prompts.md section 2 (Official
sources). Reviewed 2026-09-08.

MOO-780: the facts live in help_routes.json next to this file so the API
service can read the very same file for its own outage answer. Edit the JSON,
never this module or prompt text, to change a route.
"""

import json
from pathlib import Path

from schemas import HelpRoute

HELP_ROUTES_PATH = Path(__file__).parent / "help_routes.json"

HELP_ROUTES: list[HelpRoute] = [HelpRoute(**r) for r in json.loads(HELP_ROUTES_PATH.read_text(encoding="utf-8"))]
