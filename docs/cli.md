# CLI Reference

The Cloudmesh AI llm-mock tool is accessed via the `cmm` command. It serves as a developer's interface to manage and test mock LLM providers.

## Command Summary

| Command | Description |
| :--- | :--- |
| `cmm serve` | Start the OpenAI-compatible mock API server |
| `cmm init` | Initialize the default configuration file |
| `cmm prompt "<text>"` | Send a prompt to the active mock provider |
| `cmm list` | List available models for the active provider |
| `cmm provider set <name>` | Set the active mock provider (e.g., `ollama`, `vllm`) |
| `cmm provider get` | Show the current active mock provider |

## Example Usage

### Starting the Mock Server
```bash
# Start the server on default port 8888
cmm serve

# Start the server on a custom port
cmm serve --port 9000
```

### Prompting and Provider Management
```bash
# Prompt the default mock provider
cmm prompt "Hello, mock LLM!"

# Switch to the vLLM mock provider
cmm provider set vllm

# List all available mock models for vLLM
cmm list

# Override provider for a single prompt
cmm prompt "Test this!" --provider ollama
```
