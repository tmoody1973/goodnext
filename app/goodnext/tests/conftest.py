"""Shared test fixtures for the agent package."""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import main  # noqa: E402
import tools  # noqa: E402


@pytest.fixture(autouse=True)
def no_real_model(request, monkeypatch):
    """Safety net: no test reaches Bedrock unless marked @pytest.mark.live.
    A fixture test that accidentally builds the agent fails fast instead of spending money."""
    if request.node.get_closest_marker("live"):
        return

    def refuse(*_args, **_kwargs):
        raise AssertionError("build_agent called in a fixture test; mark it @pytest.mark.live if intended")

    monkeypatch.setattr(main, "build_agent", refuse)


@pytest.fixture
def fixture_without_res009(tmp_path, monkeypatch):
    """A temp copy of the fixture directory with res-009 removed. res-009 (MOO-772)
    has an empty zip_codes_served, so by rule it is returned for ANY ZIP; tests that
    need a true no-match ZIP must point tools.FIXTURE_PATH at a directory without it."""
    raw = json.loads(tools.FIXTURE_PATH.read_text())
    raw["resources"] = [r for r in raw["resources"] if r["resource_id"] != "res-009"]
    path = tmp_path / "no-res-009.json"
    path.write_text(json.dumps(raw))
    monkeypatch.setattr(tools, "FIXTURE_PATH", path)
