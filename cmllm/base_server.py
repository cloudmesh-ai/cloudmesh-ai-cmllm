from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, AsyncGenerator
import uvicorn
import random
import time
import json
import asyncio

from .providers import get_provider, list_available_providers

app = FastAPI(title="Cloudmesh AI CMLLM Mock Server", description="An OpenAI-compatible mock server for LLM orchestration testing.")

# --- Request/Response Models ---

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 256
    stream: Optional[bool] = False

class ChatCompletionChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: str = "stop"

class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatCompletionChoice]
    usage: Dict[str, int]

class CompletionRequest(BaseModel):
    model: str
    prompt: str
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 256

class CompletionResponse(BaseModel):
    id: str
    object: str = "text_completion"
    created: int
    model: str
    choices: List[Dict[str, Any]]

class EmbeddingRequest(BaseModel):
    model: str
    input: Any # Can be string or list of strings

class EmbeddingResponse(BaseModel):
    object: str = "list"
    data: List[Dict[str, Any]]
    model: str
    usage: Dict[str, int]

# --- Helper for OpenAI Streaming Format ---

async def openai_stream_generator(provider, text: str, model: str, chat=True):
    """Generates OpenAI-compatible Server-Sent Events (SSE)."""
    chat_id = f"chatcmx-{random.randint(1000, 9999)}"
    created = int(time.time())

    async for chunk in provider.stream_prompt(text, model):
        data = {
            "id": chat_id,
            "object": "chat.completion.chunk" if chat else "text_completion.chunk",
            "created": created,
            "model": model,
            "choices": [{
                "index": 0,
                "delta": {"content": chunk} if chat else {"text": chunk},
                "finish_reason": None
            }]
        }
        yield f"data: {json.dumps(data)}\n\n"

    yield "data: [DONE]\n\n"

# --- Routes ---

@app.get("/v1/models")
async def list_models():
    """Lists available mock models."""
    all_models = []
    for p_name in list_available_providers():
        provider = get_provider(p_name, {})
        for m in provider.list_models():
            all_models.append({"id": f"{p_name}-{m}", "owned_by": "cloudmesh-ai"})

    return {"object": "list", "data": all_models}

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """Conversational endpoint with streaming support."""
    model_id = request.model
    provider_name = model_id.split('-')[0] if '-' in model_id else "ollama"
    actual_model = model_id.split('-')[1] if '-' in model_id else model_id

    try:
        provider = get_provider(provider_name, {})
        user_text = request.messages[-1].content if request.messages else ""

        if request.stream:
            return StreamingResponse(
                openai_stream_generator(provider, user_text, model_id, chat=True),
                media_type="text/event-stream"
            )

        response_text = provider.prompt(user_text, model=actual_model)
        return ChatCompletionResponse(
            id=f"chatcmx-{random.randint(1000, 9999)}",
            created=int(time.time()),
            model=model_id,
            choices=[ChatCompletionChoice(index=0, message=ChatMessage(role="assistant", content=response_text))],
            usage={"prompt_tokens": len(user_text), "completion_tokens": len(response_text), "total_tokens": len(user_text) + len(response_text)}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/v1/completions")
async def completions(request: CompletionRequest):
    """Legacy text-completion endpoint."""
    model_id = request.model
    provider_name = model_id.split('-')[0] if '-' in model_id else "ollama"
    actual_model = model_id.split('-')[1] if '-' in model_id else model_id

    try:
        provider = get_provider(provider_name, {})
        response_text = provider.prompt(request.prompt, model=actual_model)

        return CompletionResponse(
            id=f"cmpx-{random.randint(1000, 9999)}",
            created=int(time.time()),
            model=model_id,
            choices=[{"text": response_text, "index": 0, "logprobs": None, "finish_reason": "stop"}]
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/v1/embeddings", response_model=EmbeddingResponse)
async def embeddings(request: EmbeddingRequest):
    """Generates mock vector embeddings."""
    inputs = [request.input] if isinstance(request.input, str) else request.input
    data = []
    for text in inputs:
        vector = [random.uniform(-1, 1) for _ in range(1536)]
        data.append({"object": "embedding", "embedding": vector, "index": inputs.index(text)})

    return EmbeddingResponse(
        model=request.model,
        data=data,
        usage={"prompt_tokens": sum(len(t) for t in inputs), "total_tokens": sum(len(t) for t in inputs)}
    )

@app.get("/health")
async def health():
    """Liveness probe."""
    return {"status": "ok", "provider_count": len(list_available_providers())}

@app.get("/metrics")
async def metrics():
    """Prometheus-style mock metrics."""
    return {
        "gpu_memory_utilization": f"{random.randint(10, 90)}%",
        "tokens_per_second": random.randint(50, 150),
        "active_requests": random.randint(0, 5),
        "uptime_seconds": 3600
    }

def start_server(host: str = "0.0.0.0", port: int = 8000):
    uvicorn.run(app, host=host, port=port)
