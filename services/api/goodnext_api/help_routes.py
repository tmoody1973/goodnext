"""The reviewed help routes, read from the agent's own file (MOO-780).

One source: app/goodnext/help_routes.json. Override the path with
GOODNEXT_HELP_ROUTES_FILE when the API runs somewhere the agent folder is not
beside it (a container copies the file in and sets the variable). A missing
file logs once and yields an empty list; the site then shows no footer rather
than a made-up one.
"""

import json
import logging
import os
from functools import lru_cache
from pathlib import Path

log = logging.getLogger(__name__)

DEFAULT_PATH = Path(__file__).resolve().parents[3] / "app" / "goodnext" / "help_routes.json"


def _path() -> Path:
    return Path(os.environ.get("GOODNEXT_HELP_ROUTES_FILE", DEFAULT_PATH))


@lru_cache(maxsize=4)
def _load(path: str) -> tuple[dict, ...]:
    try:
        return tuple(json.loads(Path(path).read_text(encoding="utf-8")))
    except OSError as exc:
        log.warning("help routes file unreadable at %s (%s); serving none", path, exc.__class__.__name__)
        return ()


def help_routes() -> list[dict]:
    return [dict(r) for r in _load(str(_path()))]
