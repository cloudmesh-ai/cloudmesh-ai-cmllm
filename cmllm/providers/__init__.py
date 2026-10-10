from .base_provider import BaseLLMProvider
from .ollama_provider import OllamaProvider
from .vllm_provider import VllmProvider
from typing import Dict, Any, Type

_PROVIDERS: Dict[str, Type[BaseLLMProvider]] = {
    "ollama": OllamaProvider,
    "vllm": VllmProvider,
}

def get_provider(name: str, config: Dict[str, Any]) -> BaseLLMProvider:
    """Factory function to get an LLM provider instance."""
    provider_cls = _PROVIDERS.get(name.lower())
    if not provider_cls:
        raise ValueError(f"Unsupported provider: {name}. Supported: {list(_PROVIDERS.keys())}")
    return provider_cls(config)

def list_available_providers():
    return list(_PROVIDERS.keys())
