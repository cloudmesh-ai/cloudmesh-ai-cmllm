# Installation Guide

This guide describes how to install and run the Cloudmesh AI llm-mock service.

## Prerequisites
- Python 3.10 or newer
- Pip (Python package installer)

## Installation

### From Source
```bash
git clone https://github.com/cloudmesh-ai/cloudmesh-ai-cmm.git
cd cloudmesh-ai-cmm
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

#### 3. Enable Real Mode
Edit your configuration file (`~/.config/cloudmesh/llms-mock.yaml`) and set the mode to `real`:
```yaml
providers:
  ollama:
    default_model: "phi3"
    mode: "real"
```

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
