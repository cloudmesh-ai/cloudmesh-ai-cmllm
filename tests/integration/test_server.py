import pytest
from fastapi.testclient import TestClient
from cmllm.base_server import app

client = TestClient(app)

def test_get_models():
    response = client.get("/v1/models")
    assert response.status_code == 200
    data = response.json()
    assert data["object"] == "list"
    assert len(data["data"]) > 0
    assert "id" in data["data"][0]

def test_chat_completions_non_streaming():
    payload = {
        "model": "ollama-llama3",
        "messages": [{"role": "user", "content": "Hello!"}],
        "stream": False
    }
    response = client.post("/v1/chat/completions", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["object"] == "chat.completion"
    assert data["choices"][0]["message"]["content"].startswith("[Ollama-llama3]")

def test_chat_completions_streaming():
    payload = {
        "model": "ollama-llama3",
        "messages": [{"role": "user", "content": "Hello!"}],
        "stream": True
    }
    response = client.post("/v1/chat/completions", json=payload)
    assert response.status_code == 200
    # Streaming responses are returned as iterators in TestClient
    content = response.text
    assert "data: " in content
    assert "[DONE]" in content

def test_completions():
    payload = {
        "model": "vllm-gpt-4-mock",
        "prompt": "Once upon a time",
    }
    response = client.post("/v1/completions", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["object"] == "text_completion"
    assert "[vLLM-gpt-4-mock]" in data["choices"][0]["text"]

def test_embeddings():
    payload = {
        "model": "ollama-llama3",
        "input": "Hello world",
    }
    response = client.post("/v1/embeddings", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["object"] == "list"
    assert len(data["data"][0]["embedding"]) == 1536

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "gpu_memory_utilization" in response.json()
