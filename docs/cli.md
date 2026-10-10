# CLI Reference

The Cloudmesh AI CMLLM tool is accessed via the `cmx llm` command.

## Command Summary

| Command | Description |
| :--- | :--- |
| `cmx llm provider set <provider>` | Set the active LLM provider |
| `cmx llm provider get` | Show the current active provider |
| `cmx llm prompt "<text>"` | Send a prompt to the active model |
| `cmx llm list` | List available models for the current provider |
| `cmx llm model set <model>` | Change the active model |
| `cmx llm -i` | Enter interactive LLM shell |

## Example Usage
```bash
# Prompt the default model
cmx llm prompt "What is Cloudmesh AI?"

# Prompt using a different provider
cmx llm prompt "Hello!" --provider anthropic
```
