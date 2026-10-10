# Installation Guide

This guide describes how to install and run the Cloudmesh AI cmm mock service.

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
