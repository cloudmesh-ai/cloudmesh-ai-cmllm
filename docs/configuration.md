# Configuration Guide

Cloudmesh AI CMLLM uses a simple YAML configuration to manage default behaviors for the CLI and mock providers.

## Configuration File
Configuration is stored in `~/.config/cloudmesh/llms-mock.yaml`.

## Configuration Schema
```yaml
# The provider used by the 'cmllm prompt' command by default
active_provider: "ollama"

# Provider-specific settings
providers:
  ollama:
    default_model: "llama3"
  vllm:
    default_model: "gpt-4-mock"
```

## Managing Configuration via CLI
You can modify the active provider without editing the file manually:
```bash
# Set the active provider to vllm
cmllm provider set vllm

# Verify the current setting
cmllm provider get
```

## Server Configuration
The mock server (`cmllm serve`) can be configured via CLI flags:
- `--host`: Specify the network interface (default: `0.0.0.0`).
- `--port`: Specify the listening port (default: `8000`).
