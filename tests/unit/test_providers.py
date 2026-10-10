import pytest
from cmllm.providers import get_provider

def test_ollama_mock():
    provider = get_provider("ollama", {"default_model": "llama3"})
    assert provider.get_name() == "ollama"
    assert "llama3" in provider.list_models()
    assert "[Ollama-llama3]" in provider.prompt("Hello")

def test_vllm_mock():
    provider = get_provider("vllm", {"default_model": "gpt-4-mock"})
    assert provider.get_name() == "vllm"
    assert "gpt-4-mock" in provider.list_models()
    assert "[vLLM-gpt-4-mock]" in provider.prompt("Hello")

def test_invalid_provider():
    with pytest.raises(ValueError):
        get_provider("unknown", {})
