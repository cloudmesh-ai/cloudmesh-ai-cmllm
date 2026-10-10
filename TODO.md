# Cloudmesh AI CMLLM Improvement Roadmap

## Phase 1: The Stability Foundation (High Priority)
Goal: Transform the project from a prototype into a stable, maintainable tool.

- [x] API Contract Testing: Implement a test suite using fastapi.testclient to verify that all endpoints strictly follow the OpenAI API specification.
- [x] CLI Testing: Add click.testing.CliRunner tests to ensure cmllm prompt, provider set, and serve commands work across different OS environments.
- [x] CI/CD Repair: Update .github/workflows to use pyproject.toml (instead of requirements.txt) so that the project is automatically tested on every PR.
- [x] Smart Config Init: Add a cmllm config init command to automatically generate a default llms-mock.yaml file for new users.
- [x] Logging System: Replace click.echo in the server and providers with a proper logging module to allow for --debug levels and log files.

## Phase 2: The Realism Engine (Medium Priority)
Goal: Make the mock server behave like a real, unpredictable production LLM API.

- [ ] Simulated Latency: Add a configurable delay (min/max) to responses to test how frontends handle slow requests.
- [ ] Chaos Engineering (Failure Simulation):
    - Implement a failure rate percentage.
    - Randomly inject 429 Too Many Requests (Rate Limits) and 500 Internal Server Error responses.
- [ ] Dynamic Model State:
    - Add an API route to load/unload models.
    - Simulate GPU Out-of-Memory (OOM) errors when too many models are loaded.
- [x] Enhanced Mock Data: Move beyond simple strings to use Scenario Templates (e.g., simulating a Safety Refusal or a Hallucination based on specific prompt keywords).

## Phase 3: Expansion & DX (Low Priority)
Goal: Increase the utility and ease of use of the tool.

- [ ] Broaden Provider Matrix: Implement mock drivers for other major players (e.g., Anthropic, Azure OpenAI, AWS Bedrock).
- [ ] Interactive Dashboard: Add a simple FastAPI-based admin page to monitor active requests and toggle Chaos settings in real-time.
- [ ] Advanced Streaming: Implement token-by-token timing that varies based on the mock model's size (e.g., a mock llama-70b streams slower than a phi-3).
