from abc import ABC, abstractmethod
from typing import List, Dict, Any, AsyncGenerator, Tuple, Optional
import asyncio
import random

class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def get_quirk_profile_name(self) -> str:
        """Return the quirk profile name this provider uses. Defaults to 'default'."""
        return "default"

    def tokenize(self, text: str) -> int:
        """Simulate token counting (1 token approx 4 characters)."""
        return len(text) // 4 if text else 0

    def prompt(self, text: str, model: str = None, max_tokens: int = None) -> Tuple[str, str]:
        """
        Send a prompt to the LLM and return the response and finish_reason.
        The response is truncated if it exceeds max_tokens.
        """
        response = self._generate_response(text, model)
        finish_reason = "stop"

        if max_tokens is not None:
            # 1 token approx 4 characters
            max_chars = max_tokens * 4
            if len(response) > max_chars:
                response = response[:max_chars]
                finish_reason = "length"

        return response, finish_reason

    @abstractmethod
    def _generate_response(self, text: str, model: str = None) -> str:
        """Internal method to be implemented by providers to get raw response text."""
        pass

    @abstractmethod
    def list_models(self) -> List[str]:
        """List available models for this provider."""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Return the provider name."""
        pass

    def get_model_speed(self, model: str) -> float:
        """
        Returns the average delay per token for the given model.
        Default is 0.05 seconds.
        """
        return 0.05

    async def stream_prompt(self, text: str, model: str = None, max_tokens: int = None) -> AsyncGenerator[Tuple[str, Optional[str]], None]:
        """
        Async generator that yields chunks of the response and the finish_reason.
        Simulates token-by-token timing based on the model's speed.
        """
        model = model or self.config.get("default_model", "default")
        response, finish_reason = self.prompt(text, model, max_tokens)

        delay = self.get_model_speed(model)
        # Split by space to simulate tokens
        tokens = response.split(" ")

        for i, token in enumerate(tokens):
            chunk = token + " "
            # Only send finish_reason on the last chunk
            current_finish_reason = finish_reason if i == len(tokens) - 1 else None
            yield chunk, current_finish_reason

            actual_delay = delay * random.uniform(0.8, 1.2)
            await asyncio.sleep(actual_delay)
