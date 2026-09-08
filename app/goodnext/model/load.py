import os

from strands.models.bedrock import BedrockModel

# Tech Stack section 3: pick the model id explicitly, US inference profile, no
# silent global profile. Bedrock id form confirmed from the AWS model card page
# 2026-09-08; enablement on this account is NOT yet verified (AWS was logged out).
DEFAULT_MODEL_ID = "us.anthropic.claude-sonnet-4-6"
DEFAULT_REGION = "us-east-1"


def load_model() -> BedrockModel:
    """Bedrock model client using the runtime's IAM role. Override with env vars."""
    return BedrockModel(
        model_id=os.environ.get("GOODNEXT_MODEL_ID", DEFAULT_MODEL_ID),
        region_name=os.environ.get("GOODNEXT_BEDROCK_REGION", DEFAULT_REGION),
        temperature=0.2,
        max_tokens=32000,
    )
