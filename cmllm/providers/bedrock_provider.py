from .base_provider import BaseLLMProvider
from typing import List, Dict, Any
from ..scenarios import get_scenario_response

class BedrockProvider(BaseLLMProvider):
    """Mock implementation of an AWS Bedrock provider."""

    def get_name(self) -> str:
        return "bedrock"

    def list_models(self) -> List[str]:
        return ["anthropic.claude-v2", "amazon.titan-text-express", "meta.llama2-70b"]

    def prompt(self, text: str, model: str = None) -> str:
        model = model or self.config.get("default_model", "anthropic.claude-v2")
        return get_scenario_response(text, self.get_name(), model)
