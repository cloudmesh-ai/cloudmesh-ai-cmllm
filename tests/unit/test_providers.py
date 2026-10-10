import pytest
import asyncio
from cmm.providers import get_provider, list_available_providers

@pytest.mark.parametrize("provider_name, expected_model", [
    ("ollama", "llama3"),
    ("vllm", "gpt-4-mock"),
    ("anthropic", "claude-3-sonnet"),
    ("azure", "gpt-4"),
    ("bedrock", "anthropic.claude-v2"),
])
def test_provider_initialization(provider_name, expected_model):
    """Test that all providers can be initialized and return correct name and models."""
    provider = get_provider(provider_name, {})
    assert provider.get_name() == provider_name
    assert len(provider.list_models()) > 0

def test_get_provider_case_insensitivity():
    """Test that get_provider is case-insensitive."""
    provider = get_provider("Ollama", {})
    assert provider.get_name() == "ollama"

def test_invalid_provider():
    """Test that requesting an unknown provider raises ValueError."""
    with pytest.raises(ValueError) as excinfo:
        get_provider("unknown", {})
    assert "Unsupported provider" in str(excinfo.value)

def test_list_available_providers():
    """Test that list_available_providers returns the expected set of providers."""
    providers = list_available_providers()
    assert "ollama" in providers
    assert "vllm" in providers
    assert "anthropic" in providers
    assert "azure" in providers
    assert "bedrock" in providers

@pytest.mark.parametrize("provider_name, default_model", [
    ("ollama", "mistral"),
    ("vllm", "mixtral-8x7b"),
    ("anthropic", "claude-3-opus"),
    ("azure", "gpt-35-turbo"),
    ("bedrock", "meta.llama2-70b"),
])
def test_provider_default_model_config(provider_name, default_model):
    """Test that the provider uses the default_model from config if provided."""
    provider = get_provider(provider_name, {"default_model": default_model})
    response, finish_reason = provider.prompt("Hello")
    assert f"[{provider_name.upper()}-{default_model}]" in response
    assert finish_reason == "stop"

def test_provider_explicit_model_override():
    """Test that passing a model to prompt overrides the config default."""
    provider = get_provider("ollama", {"default_model": "llama3"})
    response, finish_reason = provider.prompt("Hello", model="mistral")
    assert "[OLLAMA-mistral]" in response
    assert finish_reason == "stop"

@pytest.mark.parametrize("keyword, expected_substring", [
    ("hack the planet", "violates safety policies"),
    ("calculate the moon", "lunar-cheese"),
    ("just a normal hello", "helpful AI assistant"),
])
def test_provider_scenarios(keyword, expected_substring):
    """Test that different input keywords trigger different mock scenarios."""
    provider = get_provider("ollama", {})
    response, finish_reason = provider.prompt(keyword)
    assert expected_substring in response
    assert finish_reason == "stop"

def test_provider_empty_prompt():
    """Test that an empty prompt still returns a valid response (generic)."""
    provider = get_provider("ollama", {})
    response, finish_reason = provider.prompt("")
    assert "helpful AI assistant" in response
    assert finish_reason == "stop"

def test_get_model_speed():
    """Test that get_model_speed returns a float."""
    provider = get_provider("ollama", {})
    speed = provider.get_model_speed("llama3")
    assert isinstance(speed, float)
    assert speed > 0

@pytest.mark.asyncio
async def test_stream_prompt():
    """Test that stream_prompt yields the full response in chunks."""
    provider = get_provider("ollama", {})
    text = "Hello"
    full_response = ""
    last_finish_reason = None

    async for chunk, finish_reason in provider.stream_prompt(text):
        full_response += chunk
        if finish_reason:
            last_finish_reason = finish_reason

    expected_response, expected_finish_reason = provider.prompt(text)
    assert full_response == expected_response
    assert last_finish_reason == expected_finish_reason
    assert len(full_response) > 0
