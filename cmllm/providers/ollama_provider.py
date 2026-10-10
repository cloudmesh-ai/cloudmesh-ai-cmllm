from .base_provider import BaseLLMProvider
from typing import List, Dict, Any

class OllamaProvider(BaseLLMProvider):
    """Mock implementation of an Ollama provider."""

    def get_name(self) -> str:
        return "ollama"

    def list_models(self) -> List[str]:
        return ["llama3", "mistral", "phi3", "gemma"]

    def prompt(self, text: str, model: str = None) -> str:
        model = model or self.config.get("default_model", "llama3")
        return f"[Ollama-{model}] Mock response to: '{text}'"
