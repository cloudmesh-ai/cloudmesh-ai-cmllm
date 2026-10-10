# Configuration Guide

Cloudmesh AI CMLLM requires configuration to connect to various LLM providers.

## Configuration File
Configuration is stored in `~/.config/cloudmesh/llms.yaml`.

## Example Configuration
```yaml
providers:
  openai:
    api_key: "your-openai-key"
    default_model: "gpt-4o"
  anthropic:
    api_key: "your-anthropic-key"
    default_model: "claude-3-5-sonnet"
  local:
    endpoint: "http://localhost:11434" # e.g., Ollama
```

## Managing Providers
You can manage the active provider via the CLI:
```bash
cmx llm provider set openai
```
