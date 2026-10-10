from .base_provider import BaseLLMProvider
from typing import List, Dict, Any
from ..scenarios import get_scenario_response

class AzureOpenAIProvider(BaseLLMProvider):
    """Mock implementation of an Azure OpenAI provider."""

    def get_name(self) -> str:
        return "azure"

    def list_models(self) -> List[str]:
        return ["gpt-4", "gpt-35-turbo", "gpt-4-turbo"]

    def prompt(self, text: str, model: str = None) -> str:
        model = model or self.config.get("default_model", "gpt-4")
        return get_scenario_response(text, self.get_name(), model)
