# Contributing Guide

We welcome contributions to make Cloudmesh AI CMLLM a better tool for LLM developers!

## Adding a New Mock Provider

To simulate a new LLM provider (e.g., a mock for Anthropic or Azure OpenAI), follow these steps:

1. **Create the Provider Class**: Create a new file in `cmllm/providers/` (e.g., `anthropic_provider.py`) that inherits from `BaseProvider`.
2. **Implement Required Methods**:
    - `prompt()`: Return a mock response that mimics the style of the provider.
    - `list_models()`: Return a list of models that the real provider would offer.
    - `get_name()`: Return a unique identifier for the provider.
3. **Register the Provider**: Add your new provider class to the `_PROVIDERS` dictionary in `cmllm/providers/__init__.py`.
4. **Update Documentation**: Add the new provider to the Mock Provider Matrix in `README.md`.

## Improving Mock Realism

We encourage contributors to make the mock responses more realistic. Instead of simple strings, consider:
- Using a set of predefined templates.
- Adding random delays to simulate network latency.
- Implementing simulated error codes (e.g., 429 Too Many Requests) to test application resilience.

## Testing Your Changes
Ensure your changes don't break existing mocks:
```bash
# Run unit tests for providers
PYTHONPATH=. pytest tests/unit
```

## Pull Request Process
1. Create a feature branch.
2. Ensure all tests pass.
3. Submit a PR with a clear description of the mock behavior you've added or improved.
