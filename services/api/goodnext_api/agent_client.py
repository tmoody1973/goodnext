"""Bridge from FastAPI to the Strands agent.

Deployed: invoke the AgentCore Runtime with the backend's IAM role
(AgentCore Explained, section 3, step 2). Local: POST to the `agentcore dev`
server. Either way the browser never sees AWS credentials or the runtime ARN.
"""

import json
import os
from typing import Protocol

import httpx


class AgentClient(Protocol):
    def invoke(self, payload: dict, runtime_session_id: str) -> dict: ...


class LocalDevAgentClient:
    """Talks to `agentcore dev` (BedrockAgentCoreApp serves POST /invocations)."""

    def __init__(self, base_url: str | None = None, timeout_s: float = 60.0):
        self.base_url = (base_url or os.environ.get("GOODNEXT_AGENT_LOCAL_URL", "http://localhost:8080")).rstrip("/")
        self.timeout_s = timeout_s

    def invoke(self, payload: dict, runtime_session_id: str) -> dict:
        r = httpx.post(
            f"{self.base_url}/invocations",
            json=payload,
            headers={"X-Amzn-Bedrock-AgentCore-Runtime-Session-Id": runtime_session_id},
            timeout=self.timeout_s,
        )
        r.raise_for_status()
        return r.json()


class AgentCoreRuntimeClient:
    """Invokes the deployed runtime. Requires GOODNEXT_AGENT_RUNTIME_ARN."""

    def __init__(self, runtime_arn: str, region: str):
        import boto3  # imported here so local dev needs no AWS SDK session

        self.runtime_arn = runtime_arn
        self.client = boto3.client("bedrock-agentcore", region_name=region)

    def invoke(self, payload: dict, runtime_session_id: str) -> dict:
        response = self.client.invoke_agent_runtime(
            agentRuntimeArn=self.runtime_arn,
            runtimeSessionId=runtime_session_id,
            payload=json.dumps(payload).encode(),
            qualifier="DEFAULT",
        )
        return json.loads(response["response"].read())


def default_agent_client() -> AgentClient:
    arn = os.environ.get("GOODNEXT_AGENT_RUNTIME_ARN")
    if arn:
        return AgentCoreRuntimeClient(arn, os.environ.get("GOODNEXT_BEDROCK_REGION", "us-east-1"))
    return LocalDevAgentClient()
