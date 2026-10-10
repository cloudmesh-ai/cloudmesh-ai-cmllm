# Contributing Guide

We welcome contributions to Cloudmesh AI CMLLM!

## Adding a New Provider

To add a new LLM provider, follow these steps:

1. **Implement the Driver**: Create a new class in `providers/` that inherits from the `BaseLLMProvider`.
2. **Implement Required Methods**:
    - `prompt()`: Handle the API request and return the response.
    - `list_models()`: Return a list of available models.
3. **Update Configuration**: Add the provider's required fields to the configuration guide.
4. **Add Tests**: Create a compliance test in `tests/compliance/` to ensure the new provider meets the project standards.

## Testing Requirements
All contributions must pass the following tests:
- **Unit Tests**: `pytest tests/unit`
- **Compliance Tests**: `pytest tests/compliance` (in mock mode)

## Pull Request Process
1. Create a feature branch.
2. Ensure all tests pass.
3. Submit a PR with a clear description of the changes.
