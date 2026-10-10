# Configuration Guide

Cloudmesh AI llm-mock uses a combination of a static YAML configuration file for defaults and a dynamic runtime state managed via the Admin GUI.

## Static Configuration

Configuration is stored in `~/.config/cloudmesh/llms-mock.yaml`. This file determines the default behavior when the server starts.

### Environment Variable Overrides

You can override any configuration setting using environment variables. This is particularly useful for Docker deployments or CI/CD pipelines where you don't want to manage a physical YAML file.

#### Naming Convention
Environment variables must start with the `CMM_` prefix, followed by the configuration path in **uppercase**. For nested settings, use underscores (`_`) as separators.

| Target Setting | Environment Variable | Example Value |
| :--- | :--- | :--- |
| `active_provider` | `CMM_ACTIVE_PROVIDER` | `vllm` |
| `providers.ollama.default_model` | `CMM_PROVIDERS_OLLAMA_DEFAULT_MODEL` | `llama2` |
| `providers.vllm.default_model` | `CMM_PROVIDERS_VLLM_DEFAULT_MODEL` | `gpt-4-mock` |

#### Smart Type Casting
The system automatically casts environment variable values to the correct data type based on the existing value in the YAML file:
- **Booleans**: `true`/`false` (case-insensitive)
- **Numbers**: Automatically detected as `int` or `float`
- **Strings**: Default fallback

#### Dynamic Keys
If you provide an environment variable for a key that doesn't exist in the YAML file, the system will automatically create that key in the configuration object for the current session.

**Usage Example:**
```bash
# Override the active provider and a nested model setting
export CMM_ACTIVE_PROVIDER=vllm
export CMM_PROVIDERS_VLLM_DEFAULT_MODEL=mixtral-8x7b

cmm serve
```

Environment variables take absolute precedence over the settings in the YAML file.

### Configuration Schema
```yaml
# The provider used by the 'cmm prompt' command by default
active_provider: "ollama"

# Provider-specific settings
providers:
  ollama:
    default_model: "llama3"
  vllm:
    default_model: "gpt-4-mock"
  anthropic:
    default_model: "claude-3-sonnet"
  azure:
    default_model: "gpt-4"
  bedrock:
    default_model: "anthropic.claude-v2"
```

### Managing Configuration via CLI
You can modify the active provider without editing the file manually:
```bash
# Set the active provider to vllm
cmm provider set vllm

# Verify the current setting
cmm provider get
```

## Runtime Configuration (Admin GUI)

While the YAML file sets the defaults, the **Admin Dashboard** (`/admin`) allows you to change critical server behaviors in real-time without restarting the server.

| Setting | Description | Effect |
| :--- | :--- | :--- |
| **Active Provider** | The provider used for requests that don't specify a model. | Changes the response style and headers. |
| **Failure Rate** | % of requests that fail randomly. | Triggers 429 or 500 errors. |
| **Latency Range** | Min/Max delay in seconds. | Simulates slow network/inference. |
| **TPM Limit** | Max tokens processed per minute. | Triggers 429 errors when exceeded. |
| **Context Window** | Max tokens for prompt + response. | Triggers 400 errors when exceeded. |
| **Loaded Models** | List of models currently "in VRAM". | Triggers 404 errors for missing models. |

## Scenario Configuration

Scenarios are persisted in `~/.config/cloudmesh/scenarios.json`. While these are best managed via the Admin GUI, you can edit the JSON file directly for bulk updates.

**Format:**
```json
{
    "scenario_id": [
        ["keyword1", "keyword2"], 
        "Response template text"
    ]
}
```

## Server Startup Configuration

The mock server (`cmm serve`) can be configured via CLI flags:
- `--host`: Specify the network interface (default: `127.0.0.1`).
- `--port`: Specify the listening port (default: `8888`).
- `--kill-port`: Kill any process using the port before starting (default: `true`).
