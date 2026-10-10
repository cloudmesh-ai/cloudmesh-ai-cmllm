# Architecture Overview

Cloudmesh AI CMLLM follows a provider-based architecture to ensure a unified interface across different LLM backends.

## Core Components

- **CLI Layer**: Handles user input and command parsing.
- **Orchestrator**: Manages provider selection, configuration loading, and session state.
- **Provider Interface**: A standardized abstract base class that all LLM providers must implement.
- **Provider Drivers**: Specific implementations for each API (e.g., OpenAI, Anthropic, Local/Ollama).

## Design Goals
- **Consistency**: The same command should work regardless of the underlying model.
- **Extensibility**: Adding a new provider should only require implementing a new driver.
- **Transparency**: Users can easily switch providers for A/B testing or cost optimization.
