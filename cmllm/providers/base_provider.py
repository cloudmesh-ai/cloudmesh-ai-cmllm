from abc import ABC, abstractmethod
from typing import List, Dict, Any, AsyncGenerator

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

    async def stream_prompt(self, text: str, model: str = None) -> AsyncGenerator[str, None]:
        """
        Async generator that yields chunks of the response.
        Defaults to chunking the static prompt response.
        """
        response = self.prompt(text, model)
        # Simulate tokenization by splitting on spaces
        import asyncio
        import random

        tokens = response.split(" ")
        for token in tokens:
            yield token + " "
            await asyncio.sleep(random.uniform(0.01, 0.1))
