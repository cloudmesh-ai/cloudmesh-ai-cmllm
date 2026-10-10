# CLI Reference

The Cloudmesh AI CMLLM tool is accessed via the `cmllm` command. It serves as a developer's interface to manage and test mock LLM providers.

## Command Summary

| Command | Description |
| :--- | :--- |
| `cmllm serve` | Start the OpenAI-compatible mock API server |
| `cmllm prompt "<text>"` | Send a prompt to the active mock provider |
| `cmllm list` | List available models for the active provider |
| `cmllm provider set <name>` | Set the active mock provider (e.g., `ollama`, `vllm`) |
| `cmllm provider get` | Show the current active mock provider |

## Example Usage

### Starting the Mock Server
```bash
# Start the server on default port 8000
cmllm serve

# Start the server on a custom port
cmllm serve --port 9000
```

### Prompting and Provider Management
```bash
# Prompt the default mock provider
cmllm prompt "Hello, mock LLM!"

# Switch to the vLLM mock provider
cmllm provider set vllm

# List all available mock models for vLLM
cmllm list

# Override provider for a single prompt
cmllm prompt "Test this!" --provider ollama
```
