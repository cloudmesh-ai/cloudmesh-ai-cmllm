from .base_provider import BaseLLMProvider
from typing import List, Dict, Any
from ..scenarios import get_scenario_response
import httpx
import logging

logger = logging.getLogger("cmm.providers.ollama")

class OllamaProvider(BaseLLMProvider):
    """Implementation of an Ollama provider (Mock or Real)."""

    def get_name(self) -> str:
        return "ollama"

    def list_models(self) -> List[str]:
        return ["llama3", "mistral", "phi3", "gemma"]

    async def _generate_response(self, text: str, model: str = None) -> str:
        model = model or self.config.get("default_model", "llama3")
        mode = self.config.get("mode", "mock")

        if mode == "real":
            return await self._generate_real_response(text, model)

        return get_scenario_response(text, self.get_name(), model)

    async def _generate_real_response(self, text: str, model: str) -> str:
        """Call the actual local Ollama API."""
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": model,
            "prompt": text,
            "stream": False
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
                return data.get("response", "Error: No response field in Ollama output.")
        except httpx.RequestError as e:
            logger.error(f"Ollama connection error: {e}")
            return f"Error: Could not connect to local Ollama server. Please ensure Ollama is running. ({e})"
        except Exception as e:
            logger.error(f"Ollama API error: {e}")
            return f"Error: Ollama API returned an error. ({e})"
