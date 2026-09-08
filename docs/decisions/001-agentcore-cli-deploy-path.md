# 001 Deploy the agent with the AgentCore CLI, not the Python starter toolkit

**Decision** — Package and deploy the Strands agent with the `@aws/agentcore` command-line tool (version 0.28.1) and the CDK stack it generates.

**Why this came up** — The planning documents describe the Python "starter toolkit," a separate tool with different commands. Tarik installed the newer AgentCore CLI on September 8, 2026. Picking the wrong one would mean two config formats and a wasted day six days before the hackathon deadline.

**Options**
- *AgentCore CLI (npm).* Scaffolds a Strands agent for Bedrock in one command, keeps config in one JSON file, deploys through CDK (infrastructure as code: the cloud resources are described in files, not clicked together). Cost: newer than the docs, so the Strands guide's commands do not match.
- *Python starter toolkit.* Matches the Strands and Tech Stack docs word for word. Cost: a second tool to install, and it is the older path.
- *Hand-written CDK.* Full control. Cost: the most code for the least gain this week.

**What we chose and why** — The CLI. Joint call: Claude recommended it, Tarik confirmed. It produces the runtime, role, and deployment we need with the least code we own.

**What we gave up** — Doc alignment. The Tech Stack and Strands docs reference the starter toolkit; anyone following them will hit a command that does not exist here. The CLI also defaulted to Python 3.14 and a global Sonnet 4.5 model profile; both were changed to match the Tech Stack (Python 3.12, US Sonnet 4.6 profile).

**How we'll know if this was right** — `agentcore deploy` produces a runtime that FastAPI can invoke, and a redeploy after a code change takes minutes, not hours, before September 14.

**What actually happened** —
