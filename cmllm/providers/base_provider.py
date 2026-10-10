from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    def prompt(self, text: str, model: str = None) -> str:
        """Send a prompt to the LLM and return the response."""
        pass

    @abstractmethod
    def list_models(self) -> List[str]:
        """List available models for this provider."""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Return the provider name."""
        pass
