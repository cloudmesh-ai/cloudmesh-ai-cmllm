# Architecture Overview

Cloudmesh AI CMLLM is designed as a **Mock Service**, providing a thin, OpenAI-compatible layer over a set of simulated LLM providers. This allows developers to test LLM-integrated applications without relying on actual model weights or cloud credits.

## System Components

### 1. Mock API Server (FastAPI)
The server implements the standard OpenAI REST API. It acts as the entry point for external applications.
- **Request Validation**: Uses Pydantic to ensure incoming requests match the OpenAI specification.
- **Routing**: Maps API endpoints (like `/v1/chat/completions`) to the internal provider logic.
- **Dynamic Dispatch**: Routes requests to different `BaseProvider` implementations based on the `model` parameter in the request.

### 2. Provider Abstraction Layer
To simulate different LLM behaviors, the project uses a provider pattern:
- **`BaseProvider`**: An abstract base class defining the required interface (`prompt`, `list_models`).
- **Concrete Providers**: Specific implementations (e.g., `OllamaProvider`, `VllmProvider`) that simulate the response patterns, model lists, and characteristics of the real-world counterparts.

### 3. CLI Orchestrator
The `cmllm` CLI provides a management layer for the mock service, allowing developers to:
- Launch the server.
- Test prompts without writing a client.
- Configure which mock provider is active by default.

## Data Flow
`External Request` $\rightarrow$ `FastAPI Route` $\rightarrow$ `Provider Factory` $\rightarrow$ `Mock Provider` $\rightarrow$ `Deterministic Mock Response` $\rightarrow$ `OpenAI-Formatted JSON`
