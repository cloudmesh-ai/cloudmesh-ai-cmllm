# Cloudmesh AI CMLLM (Mock LLM Provider)

`cloudmesh-ai-cmllm` is a lightweight, OpenAI-compatible mock LLM service designed for developers and testers. It allows you to simulate various LLM providers (like Ollama and vLLM) without needing actual GPU infrastructure or expensive API keys, making it ideal for CI/CD pipelines, local development, and architectural prototyping.

## Key Features

- **OpenAI-Compatible API**: Implements the standard `/v1/chat/completions`, `/v1/completions`, and `/v1/embeddings` endpoints, allowing you to swap real LLM endpoints for this mock server with zero code changes.
- **Multi-Provider Simulation**: Switch between different mock provider behaviors (e.g., Ollama vs. vLLM) to test how your application handles different model responses and availability.
- **Zero Infrastructure Required**: No GPUs, no Docker, and no API keys needed. The mock server runs as a simple Python process.
- **Developer-Friendly Tools**:
    - **Mock Server**: A FastAPI-powered server with built-in Swagger documentation (`/docs`).
    - **CLI Tool**: A dedicated `cmllm` command for quick prompting and provider management.
- **Observability Mocks**: Includes mock `/health` and `/metrics` endpoints to test monitoring and orchestration (e.g., Kubernetes probes).

## Quick Start

### 1. Installation

```bash
git clone https://github.com/cloudmesh-ai/cloudmesh-ai-cmllm.git
cd cloudmesh-ai-cmllm
pip install -e .
```

### 2. Using the Mock Server

Start the server to expose an OpenAI-compatible API:
```bash
cmllm serve --port 8000
```
The server is now available at `http://localhost:8000`. You can explore the API via the built-in docs at `http://localhost:8000/docs`.

**Example API call:**
```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ollama-llama3",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### 3. Using the CLI

The `cmllm` command allows you to interact with the mock providers directly from your terminal:

```bash
# Send a prompt using the default provider
cmllm prompt "What is Cloudmesh AI?"

# Switch the active provider to vLLM
cmllm provider set vllm

# List available models for the active provider
cmllm list
```

## Mock Provider Matrix

| Provider | Simulated Behavior | Key Models | Implementation |
| :--- | :--- | :--- | :--- |
| **Ollama** | Local-first LLM feel | `llama3`, `mistral`, `phi3` | ✅ Mocked |
| **vLLM** | High-throughput API feel | `gpt-4-mock`, `mixtral` | ✅ Mocked |

## Documentation

Detailed guides are available in the `/docs` folder:

- [Installation Guide](docs/installation.md)
- [Configuration Guide](docs/configuration.md)
- [CLI Reference](docs/cli.md)
- [Architecture Overview](docs/architecture.md)
- [Contributing Guide](docs/contributing.md)

## Testing

The project ensures consistency across mock providers using a tiered testing strategy:

- **Unit Tests**: Verify that each provider returns the expected mock format.
- **API Tests**: Validate the FastAPI routes against the OpenAI API specification.
- **Compliance Suite**: Ensures all mock providers implement the same base interface.

## Contributing

We welcome contributions to add new mock providers or expand the simulated API responses. Please see [Contributing](docs/contributing.md) for guidelines.
