# Cloudmesh AI cmm Improvement Roadmap

## Phase 1: The Stability Foundation (High Priority)
Goal: Transform the project from a prototype into a stable, maintainable tool.

- [x] API Contract Testing: Implement a test suite using fastapi.testclient to verify that all endpoints strictly follow the OpenAI API specification.
- [x] CLI Testing: Add click.testing.CliRunner tests to ensure cmm prompt, provider set, and serve commands work across different OS environments.
- [x] CI/CD Repair: Update .github/workflows to use pyproject.toml (instead of requirements.txt) so that the project is automatically tested on every PR.
- [x] Smart Config Init: Add a cmm config init command to automatically generate a default llms-mock.yaml file for new users.
- [x] Logging System: Replace click.echo in the server and providers with a proper logging module to allow for --debug levels and log files.

## Phase 2: The Realism Engine (Medium Priority)
Goal: Make the mock server behave like a real, unpredictable production LLM API.

- [x] Simulated Latency: Add a configurable delay (min/max) to responses to test how frontends handle slow requests.
- [x] Chaos Engineering (Failure Simulation):
    - Implement a failure rate percentage.
    - Randomly inject 429 Too Many Requests (Rate Limits) and 500 Internal Server Error responses.
- [x] Dynamic Model State:
    - Add an API route to load/unload models.
    - Simulate GPU Out-of-Memory (OOM) errors when too many models are loaded.
- [x] Enhanced Mock Data: Move beyond simple strings to use Scenario Templates (e.g., simulating a Safety Refusal or a Hallucination based on specific prompt keywords).

## Phase 3: Expansion & DX (Low Priority)
Goal: Increase the utility and ease of use of the tool.

- [x] Broaden Provider Matrix: Implement mock drivers for other major players (e.g., Anthropic, Azure OpenAI, AWS Bedrock).
- [x] Interactive Dashboard: Add a simple FastAPI-based admin page to monitor active requests and toggle Chaos settings in real-time.
- [x] Advanced Streaming: Implement token-by-token timing that varies based on the mock model's size (e.g., a mock llama-70b streams slower than a phi-3).

## Phase 4: High-Fidelity Simulation (Future)
Goal: Move from a "mock" to a professional-grade simulation environment.

### 4.1 Technical Fidelity
- [x] True Tokenization Mocking: Implement token-count simulation to test Max Token limits and Context Window overflows.
- [x] Provider-Specific Quirks: Implement authentic error formats and header requirements for different providers (Azure vs Anthropic).
- [x] Runtime Scenario Management: Allow the Admin GUI to create, edit, and delete scenarios at runtime.

### 4.2 Stress Testing & Resilience
- [x] "The Meltdown" Profile: A one-click toggle to simulate a cascading service failure.
- [x] Token-Rate Limiting: Implement mock TPM (Tokens Per Minute) limits to test client-side exponential backoff.
- [x] Context Window Simulation: Simulate "forgetting" early conversation history once token limits are reached.

### 4.3 UI/UX Polish
- [x] Markdown Rendering: Integrate markdown rendering in the User GUI for code blocks and tables.
- [x] Latency Visualization: Add a real-time latency meter to the User GUI.
- [ ] Chaos Profiles: Allow saving and loading preset "Chaos Profiles" (e.g., "Regional Outage").

### 4.4 Infrastructure & Portability
- [x] Dockerization: Add Dockerfile and docker-compose.yml for one-click deployment.
- [ ] Cloudmesh Integration: Add a `cmx vm` command to deploy the mock server to a cloud VM.
