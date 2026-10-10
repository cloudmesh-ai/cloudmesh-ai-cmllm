# Contributing Guide

We welcome contributions to make Cloudmesh AI llm-mock a better tool for LLM developers!

## Adding a New Mock Provider

To simulate a new LLM provider (e.g., a mock for a new cloud offering), follow these steps:

1. **Create the Provider Class**: Create a new file in `cmm/providers/` (e.g., `new_provider.py`) that inherits from `BaseProvider`.
2. **Implement Required Methods**:
    - `prompt()`: Return a mock response that mimics the style of the provider.
    - `list_models()`: Return a list of models that the real provider would offer.
    - `get_name()`: Return a unique identifier for the provider.
3. **Define Provider Quirks**: 
    - Open `cmm/quirks.py`.
    - Create a new `ProviderQuirkProfile` that defines the specific error format and default headers for your provider.
    - Register the profile in the `QUIRK_PROFILES` dictionary.
    - In your provider class, implement `get_quirk_profile_name()` to return the key you used in `QUIRK_PROFILES`.
4. **Register the Provider**: Add your new provider class to the `_PROVIDERS` dictionary in `cmm/providers/__init__.py`.
5. **Update Documentation**: Add the new provider to the Mock Provider Matrix in `README.md`.

## Improving Mock Realism

We encourage contributors to make the mock responses more realistic. Instead of simple strings, consider:
- **Using Scenario Templates**: Add new default scenarios to `scenarios.py` to handle specific user intents.
- **Adding Random Delays**: Implement custom `get_model_speed()` logic in your provider to simulate different model sizes.
- **Implementing Simulated Error Codes**: Ensure your `ProviderQuirkProfile` maps HTTP status codes (429, 500, etc.) to the provider's authentic error codes.

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
