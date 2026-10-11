# Installation Guide

This guide describes how to install and run the Cloudmesh AI llm-mock service.

!!! note "System Requirements"
    Cloudmesh AI llm-mock requires **Python 3.10 or newer**. If you are using a version manager like `pyenv` or `conda`, ensure your active environment meets this requirement.

## Prerequisites
- Python 3.10 or newer
- Pip (Python package installer)

## Installation

### From Source
```bash
git clone https://github.com/cloudmesh-ai/cloudmesh-ai-llm-mock.git
cd cloudmesh-ai-llm-mock
pip install -e .
```

## Running the Mock Server

The mock server provides an OpenAI-compatible API. To start it:
```bash
cmm serve
```
Once started, the server will be available at `http://localhost:8888`. 

### Local LLM Setup (Ollama)
To use the "Real" mode with local models (like Phi-3), you need to install Ollama:

#### 1. Install Ollama
- **macOS**: Download and install the app from [ollama.com](https://ollama.com).
- **Linux**: Run the official installation script:
  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  ```
- **Windows**: Download and run the installer from [ollama.com](https://ollama.com).

#### 2. Pull the Model
After installing and starting Ollama, pull the Phi-3 model:
```bash
ollama pull phi3
```

#### 3. Enable Real Mode and Verify
You can enable "Real" mode through the Admin Dashboard:
1. Navigate to `http://localhost:8888/admin`.
2. Expand the **Real LLM Service** section.
3. Click **"Run All"** to verify the Ollama engine, model availability, inference, and latency.
4. Once the check is complete, the real model (e.g., `ollama-phi3-real`) will automatically become available in the chat interface.

### Testing the Server
You can test the server using `curl`:
```bash
curl http://localhost:8888/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ollama-llama3",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### Interactive API Docs
FastAPI automatically generates interactive documentation. Visit:
`http://localhost:8888/docs`

---

**Next Steps:** Now that you have the server running, learn how to [Configure the Mock Providers](configuration.md) to match your target environment.
