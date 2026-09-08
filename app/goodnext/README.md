# GoodNext agent (Strands on AgentCore Runtime)

The resident-facing Strands agent. `main.py` is the AgentCore entrypoint.
Prompts live in `prompts.py` (extracted verbatim from the APIs doc), typed
records in `schemas.py`, application tools in `tools.py`, and the
post-generation checks in `validators.py`.

Local run: `agentcore dev` from the repo root. Tests: `uv run pytest`.
Deployment and hosting decisions: `docs/decisions/`.
