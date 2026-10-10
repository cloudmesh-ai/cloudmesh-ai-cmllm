from .base_provider import BaseLLMProvider
from typing import List, Dict, Any

class VLLMProvider(BaseLLMProvider):
    """Mock implementation of a vLLM provider."""

    def get_name(self) -> str:
        return "vllm"

    def list_models(self) -> List[str]:
        return ["gpt-4-mock", "claude-3-mock", "mixtral-8x7b"]

    def prompt(self, text: str, model: str = None) -> str:
        model = model or self.config.get("default_model", "gpt-4-mock")
        return f"[vLLM-{model}] High-performance mock response to: '{text}'"
