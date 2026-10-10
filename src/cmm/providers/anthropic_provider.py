from .base_provider import BaseLLMProvider
from typing import List, Dict, Any
from ..scenarios import get_scenario_response

class AnthropicProvider(BaseLLMProvider):
    """Mock implementation of an Anthropic provider."""

    def get_name(self) -> str:
        return "anthropic"

    def get_quirk_profile_name(self) -> str:
        return "anthropic"

    def list_models(self) -> List[str]:
        return ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"]

    async def _generate_response(self, text: str, model: str = None) -> str:
        model = model or self.config.get("default_model", "claude-3-sonnet")
        return get_scenario_response(text, self.get_name(), model)
