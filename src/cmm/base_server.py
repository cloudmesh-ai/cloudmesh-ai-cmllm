from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import StreamingResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, AsyncGenerator, Tuple, Set
import uvicorn
import random
import time
import json
import asyncio
import logging
import httpx
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from .providers import get_provider, list_available_providers
from .scenarios import load_scenarios, add_or_update_scenario, delete_scenario
from .quirks import get_quirk_profile

app = FastAPI(title="Cloudmesh AI CMM Mock Server", description="An OpenAI-compatible mock server for LLM orchestration testing.")

# Use absolute path for static files to avoid resolution issues
static_path = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

def provider_error(status_code: int, message: str, provider_name: str = "default"):
    """Returns a JSONResponse with provider-specific error format and headers."""
    profile = get_quirk_profile(provider_name)
    body = profile.format_error(status_code, message)
    return JSONResponse(
        status_code=status_code,
        content=body,
        headers=profile.headers
    )

def provider_response(data: Any, provider_name: str = "default"):
    """Returns a response with provider-specific headers."""
    profile = get_quirk_profile(provider_name)
    return JSONResponse(
        content=data,
        headers=profile.headers
    )

# --- Simulation State ---

class ServerState:
    def __init__(self):
        self.active_provider: str = "ollama"
        self.failure_rate: float = 0.0
        self.latency_range: Tuple[float, float] = (0.1, 0.5)
        self.loaded_models: Set[str] = set()
        self.tpm_limit: int = 100000
        self.current_tpm: int = 0
        self.context_window: int = 4096
        self.meltdown_mode: bool = False
        self.meltdown_start_time: Optional[float] = None
        self.last_tpm_reset: float = time.time()
        self.session_histories: Dict[str, List[ChatMessage]] = {}
        self.workflow_status: Dict[str, str] = {
            "ollama_engine": "pending",
            "model_available": "pending",
            "basic_inference": "pending",
            "latency_check": "pending"
        }
        self.workflow_status: Dict[str, str] = {
            "ollama_engine": "pending",
            "model_available": "pending",
            "basic_inference": "pending",
            "latency_check": "pending"
        }

    def should_fail(self) -> bool:
        """Check if a request should fail based on the failure rate."""
        return random.random() < self.failure_rate

    def get_simulated_latency(self) -> float:
        """Calculate a random delay within the latency range."""
        return random.uniform(*self.latency_range)

async def pull_model(model_name: str):
    """Triggers a model pull from Ollama and updates workflow status upon completion."""
    try:
        log_event(f"Ollama: Starting pull for model {model_name}...")
        async with httpx.AsyncClient(timeout=None) as client:
            # Ollama /api/pull is a streaming endpoint
            async with client.stream("POST", "http://localhost:11434/api/pull", json={"name": model_name}) as response:
                async for line in response.aiter_lines():
                    if line:
                        # We could parse the progress here, but for now just log
                        pass
        log_event(f"Ollama: Successfully pulled model {model_name}")
        state.workflow_status["model_available"] = "success"
    except Exception as e:
        log_event(f"Ollama: Failed to pull model {model_name}: {e}")
        state.workflow_status["model_available"] = "failure"

    async def simulate_chaos(self, provider_name: str = "default"):

        """Combined method to simulate failure and latency.
        Returns (status_code, message) if it should fail, else None.
        """
        if self.meltdown_mode:
            if self.meltdown_start_time is None:
                self.meltdown_start_time = time.time()

            elapsed = time.time() - self.meltdown_start_time

            if elapsed < 15:
                # Stage 1: Max Latency
                delay = self.latency_range[1] * 10
                log_event(f"Chaos: Meltdown Stage 1 - Max Latency {delay:.2f}s")
                await asyncio.sleep(delay)
                return None
            elif elapsed < 30:
                # Stage 2: 100% Failure
                log_event("Chaos: Meltdown Stage 2 - 100% Failure Rate")
                return (500, "Simulated cascading failure")
            else:
                # Stage 3: Connection Reset / 503
                log_event("Chaos: Meltdown Stage 3 - Connection Reset / 503")
                return (503, "Service Unavailable (Meltdown)")

        if self.should_fail():
            error_code = random.choice([429, 500])
            msg = "Simulated server error"
            log_event(f"Chaos: Triggered failure {error_code}")
            return (error_code, msg)

        delay = self.get_simulated_latency()
        if delay > 0:
            log_event(f"Chaos: Applied latency {delay:.2f}s")
            await asyncio.sleep(delay)
        return None

    def track_tpm(self, tokens: int):
        """Track and enforce TPM limit."""
        now = time.time()
        if now - self.last_tpm_reset >= 60:
            self.current_tpm = 0
            self.last_tpm_reset = now

        self.current_tpm += tokens
        if self.current_tpm > self.tpm_limit:
            log_event(f"TPM Limit Exceeded: {self.current_tpm}/{self.tpm_limit}")
            raise HTTPException(
                status_code=429,
                detail="Too Many Requests",
                headers={"Retry-After": "60"}
            )

    def manage_context(self, session_id: str, messages: List[ChatMessage]) -> List[ChatMessage]:
        """Track conversation history and simulate 'forgetting' by truncating oldest messages."""
        if session_id not in self.session_histories:
            self.session_histories[session_id] = []

        # Update history with current messages
        self.session_histories[session_id] = messages[:]

        current_messages = messages[:]
        total_tokens = sum(len(m.content) for m in current_messages)

        while total_tokens > self.context_window and len(current_messages) > 1:
            removed = current_messages.pop(0)
            total_tokens -= len(removed.content)
            log_event(f"Context: Session {session_id} truncated oldest message. Remaining tokens: {total_tokens}")

        return current_messages

state = ServerState()
server_logs: List[str] = []

def log_event(event: str):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    msg = f"[{timestamp}] {event}"
    server_logs.append(msg)
    if len(server_logs) > 100:
        server_logs.pop(0)
    logging.info(msg)

# Custom Jinja2 environment to bypass potential caching/hashing issues in Python 3.14
templates_path = Path(__file__).parent / "templates"
jinja_env = Environment(
    loader=FileSystemLoader(str(templates_path)),
    autoescape=True
)
templates = Jinja2Templates(directory=str(templates_path))

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

async def openai_stream_generator(provider, text: str, model: str, max_tokens: Optional[int] = None, chat=True):
    """Generates OpenAI-compatible Server-Sent Events (SSE)."""
    chat_id = f"chatcmx-{random.randint(1000, 9999)}"
    created = int(time.time())

    async for chunk, finish_reason in provider.stream_prompt(text, model, max_tokens):
        # Extract only the text content from the chunk if it's a tuple
        content = chunk[0] if isinstance(chunk, tuple) else chunk

        data = {
            "id": chat_id,
            "object": "chat.completion.chunk" if chat else "text_completion.chunk",
            "created": created,
            "model": model,
            "choices": [{
                "index": 0,
                "delta": {"content": content} if chat else {"text": content},
                "finish_reason": finish_reason
            }]
        }
        yield f"data: {json.dumps(data)}\n\n"

    yield "data: [DONE]\n\n"

async def pull_model(model_name: str):
    """Triggers a model pull from Ollama and updates workflow status upon completion."""
    try:
        log_event(f"Ollama: Starting pull for model {model_name}...")
        async with httpx.AsyncClient(timeout=None) as client:
            # Ollama /api/pull is a streaming endpoint
            async with client.stream("POST", "http://localhost:11434/api/pull", json={"name": model_name}) as response:
                async for line in response.aiter_lines():
                    if line:
                        # We could parse the progress here, but for now just log
                        pass
        log_event(f"Ollama: Successfully pulled model {model_name}")
        state.workflow_status["model_available"] = "success"
    except Exception as e:
        log_event(f"Ollama: Failed to pull model {model_name}: {e}")
        state.workflow_status["model_available"] = "failure"

# --- Admin Routes ---


@app.get("/admin/workflow", response_class=HTMLResponse)
async def get_workflow_status():
    """Returns the workflow verification panel as an HTML fragment."""
    steps = [
        ("ollama_engine", "Install Ollama", "Verify Ollama server is reachable"),
        ("model_available", "Model Available", "Verify phi3 model is pulled"),
        ("basic_inference", "Chat working", "Test simple prompt response"),
        ("latency_check", "Verify latency check", "Verify response timing"),
    ]

    html = '''<div id="workflow-panel" class="space-y-4">
        <div class="flex justify-between items-center mb-4 p-3 bg-blue-600/10 border border-blue-500/30 rounded-lg">
            <span class="text-sm font-medium text-blue-400">Full Service Setup</span>
            <button hx-post="/admin/workflow/run-all" hx-target="#workflow-panel"
                    class="bg-blue-600 hover:bg-blue-500 text-white px-3 py-1 rounded text-xs font-bold transition-all active:scale-95">
                Run All
            </button>
        </div>
    '''
    for sid, name, desc in steps:
        status = state.workflow_status.get(sid, "pending")
        icon = "⚪" if status == "pending" else "🟢" if status == "success" else "🔴"
        color = "text-slate-500" if status == "pending" else "text-green-400" if status == "success" else "text-red-400"

        html += f'''
            <div class="flex items-center justify-between p-3 bg-slate-900/50 rounded-lg border border-slate-700 group hover:border-blue-500/50 transition-all">
                <div class="flex items-center gap-3 cursor-pointer" hx-post="/admin/workflow/run/{sid}" hx-target="#workflow-panel">
                    <span class="{color} font-bold text-lg">{icon}</span>
                    <div>
                        <div class="text-sm font-semibold">{name}</div>
                        <div class="text-xs text-slate-500">{desc}</div>
                    </div>
                </div>
                <div class="text-xs font-mono text-slate-600 uppercase">{status}</div>
            </div>
        '''
    html += '</div>'
    return HTMLResponse(content=html)

@app.post("/admin/workflow/run/{step_id}", response_class=HTMLResponse)
async def run_workflow_step(step_id: str):
    """Executes a specific verification step and resets subsequent steps."""
    # Define step order for dependency resets
    steps_order = ["ollama_engine", "model_available", "basic_inference", "latency_check"]

    # Reset all subsequent steps to pending
    if step_id in steps_order:
        idx = steps_order.index(step_id)
        for subsequent_step in steps_order[idx + 1:]:
            state.workflow_status[subsequent_step] = "pending"

    success = False
    try:
        if step_id == "ollama_engine":
            async with httpx.AsyncClient() as client:
                resp = await client.get("http://localhost:11434/api/tags", timeout=2.0)
                success = resp.status_code == 200

        elif step_id == "model_available":
            async with httpx.AsyncClient() as client:
                resp = await client.get("http://localhost:11434/api/tags", timeout=2.0)
                data = resp.json()
                success = any(m["name"].startswith("phi3") for m in data.get("models", []))

                if not success:
                    log_event("Model phi3 not found. Triggering pull...")
                    # Trigger Ollama pull in the background
                    asyncio.create_task(pull_model("phi3"))
                    state.workflow_status[step_id] = "pulling"
                    return await get_workflow_status()


        elif step_id == "basic_inference":
            provider = get_provider("ollama", {"mode": "real"})
            resp, _ = await provider.prompt("Hi", model="phi3")
            success = len(resp) > 0

        elif step_id == "latency_check":
            start = time.time()
            provider = get_provider("ollama", {"mode": "real"})
            await provider.prompt("Hi", model="phi3")
            success = (time.time() - start) < 10.0 # Reasonable timeout for a local LLM

        else:
            success = False
    except Exception as e:
        log_event(f"Workflow step {step_id} failed: {e}")
        success = False

    state.workflow_status[step_id] = "success" if success else "failure"
    log_event(f"Workflow step {step_id}: {'SUCCESS' if success else 'FAILURE'}")

    # Return the updated panel
    return await get_workflow_status()

@app.post("/admin/workflow/run-all", response_class=HTMLResponse)
async def run_all_workflow():
    """Runs all verification steps sequentially."""
    steps = ["ollama_engine", "model_available", "basic_inference", "latency_check"]
    for sid in steps:
        await run_workflow_step(sid)

    return await get_workflow_status()

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    """Renders the Admin Dashboard."""
    all_models = []
    for p_name in list_available_providers():
        provider = get_provider(p_name, {})
        for m in provider.list_models():
            all_models.append(f"{p_name}-{m}")

    template = jinja_env.get_template("admin.html")
    content = template.render(
        request=request,
        state=state,
        providers=list_available_providers(),
        models=all_models
    )
    return HTMLResponse(content=content)

@app.post("/admin/config")
async def update_config(
    active_provider: str = Form("ollama"),
    failure_rate: float = Form(0.0),
    latency_min: float = Form(0.1),
    latency_max: float = Form(0.5),
    loaded_models: str = Form(""),
    tpm_limit: int = Form(100000),
    context_window: int = Form(4096)
):
    """Updates server settings."""
    state.active_provider = active_provider
    state.failure_rate = float(failure_rate) / 100.0
    state.latency_range = (float(latency_min), float(latency_max))
    state.loaded_models = set(m.strip() for m in loaded_models.split(",") if m.strip())
    state.tpm_limit = int(tpm_limit)
    state.context_window = int(context_window)

    log_event(f"Config updated: provider={active_provider}, failure={failure_rate}, latency=({latency_min}, {latency_max}), tpm={tpm_limit}, context={context_window}")
    return HTMLResponse(content="Config updated successfully")

@app.post("/admin/panic")
async def toggle_panic():
    """Toggles the Meltdown mode."""
    state.meltdown_mode = not state.meltdown_mode
    mode = "ACTIVATED" if state.meltdown_mode else "DEACTIVATED"
    log_event(f"PANIC BUTTON: Meltdown mode {mode}")
    return HTMLResponse(content=f"Meltdown mode {mode}")

@app.get("/admin/scenarios", response_class=HTMLResponse)
async def list_scenarios():
    """Returns the list of scenarios as an HTML fragment."""
    scenarios = load_scenarios()
    html = '<table class="admin-table"><thead><tr><th>ID</th><th>Keywords</th><th>Template</th><th>Actions</th></tr></thead><tbody]'
    for sid, (kws, tmpl) in scenarios.items():
        kws_str = ", ".join(kws) if kws else "<i class='text-slate-400'>(fallback)</i>"
        html += f'''
            <tr class="border-b border-slate-700">
                <td class="p-2 font-mono text-xs">{sid}</td>
                <td class="p-2 text-xs">{kws_str}</td>
                <td class="p-2 text-xs truncate max-w-xs">{tmpl}</td>
                <td class="p-2 text-xs">
                    <button hx-get="/admin/scenarios/edit/{sid}" hx-target="#scenario-editor" class="text-blue-400 hover:underline mr-2">Edit</button>
                    {"<button hx-delete='/admin/scenarios/" + sid + "' hx-target='#scenario-list' hx-confirm='Are you sure?' class='text-red-400 hover:underline'>" if sid != "generic_helpful" else ""}
                </td>
            </tr>
        '''
    html += '</tbody></table>'
    return HTMLResponse(content=f'<div id="scenario-list">{html}</div>')

@app.get("/admin/scenarios/edit/{scenario_id}", response_class=HTMLResponse)
async def edit_scenario_form(scenario_id: str):
    """Returns the edit form for a specific scenario."""
    scenarios = load_scenarios()
    if scenario_id not in scenarios:
        raise HTTPException(status_code=404, detail="Scenario not found")

    kws, tmpl = scenarios[scenario_id]
    kws_val = ",".join(kws)

    return HTMLResponse(content=f'''
        <div id="scenario-editor" class="bg-slate-800 p-4 rounded-lg border border-slate-700 mb-6">
            <h3 class="text-lg font-bold mb-4">Edit Scenario: {scenario_id}</h3>
            <form hx-put="/admin/scenarios/{scenario_id}" hx-target="#scenario-list" class="flex flex-col gap-4">
                <div>
                    <label class="block text-xs font-semibold text-slate-400 mb-1">Keywords (comma separated):</label>
                    <input type="text" name="keywords" value="{kws_val}" class="w-full p-2 bg-slate-900 border border-slate-700 rounded text-sm text-white">
                </div>
                <div>
                    <label class="block text-xs font-semibold text-slate-400 mb-1">Template:</label>
                    <textarea name="template" rows="3" class="w-full p-2 bg-slate-900 border border-slate-700 rounded text-sm text-white">{tmpl}</textarea>
                </div>
                <div class="flex gap-2">
                    <button type="submit" class="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded text-sm font-bold">Save Changes</button>
                    <button type="button" onclick="document.getElementById('scenario-editor').innerHTML=''" class="bg-slate-700 hover:bg-slate-600 text-white px-4 py-2 rounded text-sm">Cancel</button>
                </div>
            </form>
        </div>
    ''')

@app.post("/admin/scenarios", response_class=HTMLResponse)
async def create_scenario(
    scenario_id: str = Form(...),
    keywords: str = Form(""),
    template: str = Form(...)
):
    """Creates a new scenario."""
    kw_list = [k.strip() for k in keywords.split(",") if k.strip()]
    add_or_update_scenario(scenario_id, kw_list, template)
    log_event(f"Scenario created/updated: {scenario_id}")
    return HTMLResponse(content='<div class="alert success">Scenario saved!</div>')

@app.put("/admin/scenarios/{scenario_id}", response_class=HTMLResponse)
async def update_scenario(
    scenario_id: str,
    keywords: str = Form(""),
    template: str = Form(...)
):
    """Updates an existing scenario."""
    kw_list = [k.strip() for k in keywords.split(",") if k.strip()]
    add_or_update_scenario(scenario_id, kw_list, template)
    log_event(f"Scenario updated: {scenario_id}")
    return HTMLResponse(content='<div class="alert success">Scenario updated!</div>')

@app.delete("/admin/scenarios/{scenario_id}", response_class=HTMLResponse)
async def delete_scenario_route(scenario_id: str):
    """Deletes a scenario."""
    try:
        delete_scenario(scenario_id)
        log_event(f"Scenario deleted: {scenario_id}")
        return HTMLResponse(content='<div class="alert success">Scenario deleted!</div>')
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/admin/tpm_status")
async def tpm_status():
    """Returns current TPM usage."""
    return HTMLResponse(content=f'<div id="tpm-usage" class="font-mono text-blue-400">{state.current_tpm}/{state.tpm_limit} tokens/min</div>')

@app.get("/admin/logs", response_class=HTMLResponse)
async def admin_logs():
    """Returns the latest server logs as HTML fragments."""
    logs_html = []
    for log in server_logs:
        # Highlight Chaos events in red
        style = 'style="color: #e74c3c; font-weight: bold;"' if "Chaos:" in log else ''
        logs_html.append(f'<div {style}>{log}</div>')
    return HTMLResponse(content=f"<div id='logs'>{''.join(logs_html)}</div>")

# --- Chat Routes ---

@app.get("/chat", response_class=HTMLResponse)
async def chat_interface(request: Request):
    """Renders the Chat Interface."""
    template = jinja_env.get_template("chat.html")
    content = template.render(
        request=request,
        models=[] # Will be populated by /v1/models on client side
    )
    return HTMLResponse(content=content)

@app.post("/chat/send", response_class=HTMLResponse)
async def chat_send(message: str = Form(...)):
    """Handles user message and returns the initial response."""
    log_event(f"Chat message received: {message[:50]}...")
    # We return the user message rendered and a placeholder for the bot
    return HTMLResponse(content=f"""
        <div class="flex justify-end gap-4 mb-6">
            <div class="bg-blue-600 text-white p-4 rounded-2xl rounded-tr-none shadow-sm max-w-[80%] text-sm leading-relaxed">
                {message}
            </div>
            <div class="w-8 h-8 rounded-full bg-blue-100 flex-shrink-0 flex items-center justify-center text-xs font-bold text-blue-600">U</div>
        </div>
        <div class="flex gap-4 mb-6">
            <div class="w-8 h-8 rounded-full bg-slate-200 flex-shrink-0 flex items-center justify-center text-xs font-bold text-slate-500">AI</div>
            <div class="bg-white border border-slate-200 p-4 rounded-2xl rounded-tl-none shadow-sm max-w-[80%] text-sm leading-relaxed text-slate-700">
                <div class="flex justify-between items-center mb-2 gap-4">
                    <div id="model-badge" class="text-[10px] font-bold uppercase tracking-widest text-slate-400 bg-slate-100 px-2 py-0.5 rounded border border-slate-200">
                        Detecting model...
                    </div>
                </div>
                <div id="bot-response" data-message="{message}">
                    Waiting for response...
                </div>
            </div>
        </div>
    """)

@app.get("/chat/stream")
async def chat_stream(message: str, model: Optional[str] = None):
    """SSE endpoint for streaming the model response."""
    if model:
        provider_name = model.split('-')[0] if '-' in model else "ollama"
        provider = get_provider(provider_name, {})

        if "-real" in model:
            provider.config["mode"] = "real"
            actual_model = model.replace("-real", "")
            if "-" in actual_model:
                actual_model = actual_model.split("-")[1]
        else:
            provider.config["mode"] = "mock"
            actual_model = model.split('-')[1] if '-' in model else model
    else:
        # Fallback to active provider and mock mode
        provider_name = state.active_provider
        provider = get_provider(provider_name, {})
        provider.config["mode"] = "mock"
        actual_model = f"{provider_name}-mock"

    async def event_generator():
        async for chunk in provider.stream_prompt(message, actual_model):
            text = chunk[0] if isinstance(chunk, tuple) else chunk
            # Send as JSON to provide both views
            yield f"data: {json.dumps({'raw': str(chunk), 'text': text})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

# --- API Routes ---

@app.get("/v1/models")
async def list_models():
    """Lists available mock and real models. Real models are only shown if verified."""
    all_models = []
    for p_name in list_available_providers():
        provider = get_provider(p_name, {})
        for m in provider.list_models():
            # Standard mock model - always available
            all_models.append({"id": f"{p_name}-{m}", "owned_by": "cloudmesh-ai", "description": "Simulated response"})

            # Real model variant - only available if verified
            if p_name == "ollama" and state.workflow_status.get("latency_check") == "success":
                all_models.append({"id": f"{p_name}-{m}-real", "owned_by": "cloudmesh-ai", "description": "Real local LLM"})
            elif p_name != "ollama":
                # Other real providers might not have checks yet, but for now we only have Ollama checks
                all_models.append({"id": f"{p_name}-{m}-real", "owned_by": "cloudmesh-ai", "description": "Real local LLM"})

    return {"object": "list", "data": all_models}

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """Conversational endpoint with streaming support."""
    model_id = request.model
    provider_name = model_id.split('-')[0] if '-' in model_id else "ollama"
    actual_model = model_id.split('-')[1] if '-' in model_id else model_id

    chaos_error = await state.simulate_chaos(provider_name)
    if chaos_error:
        return provider_error(*chaos_error, provider_name)

    if state.loaded_models and model_id not in state.loaded_models:
        log_event(f"Error: Model {model_id} not loaded")
        return provider_error(404, f"Model {model_id} not loaded", provider_name)

    try:
        log_event(f"ChatCompletion request: model={model_id}, provider={provider_name}")
        provider = get_provider(provider_name, {})
        user_text = request.messages[-1].content if request.messages else ""

        # Token counting
        prompt_tokens = provider.tokenize(user_text)

        # Handle "real" model override
        if "-real" in model_id:
            provider.config["mode"] = "real"
            actual_model = model_id.replace("-real", "")
            if "-" in actual_model:
                actual_model = actual_model.split("-")[1]
        else:
            provider.config["mode"] = "mock"


        # Context Window Enforcement (Prompt only for streaming, prompt+response for non-streaming)
        if prompt_tokens > state.context_window:
            return provider_error(400, f"Context window exceeded by prompt: {prompt_tokens}/{state.context_window} tokens", provider_name)

        # TPM Enforcement
        try:
            state.track_tpm(prompt_tokens)
        except HTTPException as e:
            return provider_error(e.status_code, e.detail, provider_name)

        if request.stream:
            return StreamingResponse(
                openai_stream_generator(provider, user_text, model_id, max_tokens=request.max_tokens, chat=True),
                media_type="text/event-stream"
            )

        response_text, finish_reason = await provider.prompt(user_text, model=actual_model, max_tokens=request.max_tokens)
        completion_tokens = provider.tokenize(response_text)
        total_tokens = prompt_tokens + completion_tokens

        if total_tokens > state.context_window:
            return provider_error(400, f"Context window exceeded: {total_tokens}/{state.context_window} tokens", provider_name)

        data = ChatCompletionResponse(
            id=f"chatcmx-{random.randint(1000, 9999)}",
            created=int(time.time()),
            model=model_id,
            choices=[ChatCompletionChoice(index=0, message=ChatMessage(role="assistant", content=response_text), finish_reason=finish_reason)],
            usage={"prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens, "total_tokens": total_tokens}
        ).dict()
        return provider_response(data, provider_name)
    except Exception as e:
        log_event(f"ChatCompletion error: {str(e)}")
        return provider_error(400, str(e), provider_name)

@app.post("/v1/completions")
async def completions(request: CompletionRequest):
    """Legacy text-completion endpoint."""
    model_id = request.model
    provider_name = model_id.split('-')[0] if '-' in model_id else "ollama"
    actual_model = model_id.split('-')[1] if '-' in model_id else model_id

    chaos_error = await state.simulate_chaos(provider_name)
    if chaos_error:
        return provider_error(*chaos_error, provider_name)

    if state.loaded_models and model_id not in state.loaded_models:
        log_event(f"Error: Model {model_id} not loaded")
        return provider_error(404, f"Model {model_id} not loaded", provider_name)

    try:
        log_event(f"Completion request: model={model_id}, provider={provider_name}")
        provider = get_provider(provider_name, {})

        # TPM and Context Enforcement
        prompt_text = state.truncate_context(request.prompt)
        try:
            state.track_tpm(len(prompt_text))
        except HTTPException as e:
            return provider_error(e.status_code, e.detail, provider_name)

        response_text, finish_reason = await provider.prompt(prompt_text, model=actual_model)

        data = CompletionResponse(
            id=f"cmpx-{random.randint(1000, 9999)}",
            created=int(time.time()),
            model=model_id,
            choices=[{"text": response_text, "index": 0, "logprobs": None, "finish_reason": finish_reason}]
        ).dict()
        return provider_response(data, provider_name)
    except Exception as e:
        log_event(f"Completion error: {str(e)}")
        return provider_error(400, str(e), provider_name)

@app.post("/v1/embeddings", response_model=EmbeddingResponse)
async def embeddings(request: EmbeddingRequest):
    """Generates mock vector embeddings."""
    model_id = request.model
    provider_name = model_id.split('-')[0] if '-' in model_id else "ollama"

    chaos_error = await state.simulate_chaos(provider_name)
    if chaos_error:
        return provider_error(*chaos_error, provider_name)

    if state.loaded_models and model_id not in state.loaded_models:
        log_event(f"Error: Model {model_id} not loaded")
        return provider_error(404, f"Model {model_id} not loaded", provider_name)

    inputs = [request.input] if isinstance(request.input, str) else request.input
    data = []
    try:
        log_event(f"Embedding request: model={model_id}, inputs_count={len(inputs)}")

        total_tokens = 0
        processed_inputs = []
        for text in inputs:
            truncated = state.truncate_context(text)
            processed_inputs.append(truncated)
            total_tokens += len(truncated)

        try:
            state.track_tpm(total_tokens)
        except HTTPException as e:
            return provider_error(e.status_code, e.detail, provider_name)

        for i, text in enumerate(processed_inputs):
            vector = [random.uniform(-1, 1) for _ in range(1536)]
            data.append({"object": "embedding", "embedding": vector, "index": i})

        response_data = EmbeddingResponse(
            model=model_id,
            data=data,
            usage={"prompt_tokens": total_tokens, "total_tokens": total_tokens}
        ).dict()
        return provider_response(response_data, provider_name)
    except Exception as e:
        log_event(f"Embedding error: {str(e)}")
        return provider_error(400, str(e), provider_name)

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

def start_server(host: str = "0.0.0.0", port: int = 8888):
    uvicorn.run(app, host=host, port=port)
