# GUI Guide

Cloudmesh AI cmm provides two distinct web interfaces to make interacting with and managing the mock server intuitive and efficient.

## 1. User Chat Interface (`/chat`)

The User Chat Interface is designed to simulate the end-user experience of an LLM application. It allows you to test prompts and visualize the performance of the mock providers.

### Key Features:
- **Real-Time Interaction**: Send messages to the active mock provider and receive streaming responses.
- **Markdown Rendering**: Full support for markdown, including formatted code blocks and tables, ensuring that you see exactly how the final AI response will be rendered.
- **Live Latency Monitor**: A built-in monitor that visualizes the simulated server delay for every response, making it easy to see the effect of Chaos Engine latency settings.
- **Provider Integration**: The chat interface automatically fetches available models from the `/v1/models` endpoint, allowing you to switch models on the fly.

**Access it at**: `http://localhost:8888/chat`

---

## 2. Admin Dashboard (`/admin`)

The Admin Dashboard is the "control room" for your mock environment. It allows you to change the server's behavior in real-time without restarting the process.

### Control Panels:

#### A. Server Configuration
Directly modify the global state of the mock server:
- **Active Provider**: Switch the default provider (e.g., from `ollama` to `azure`).
- **Failure Rate**: Set the percentage of requests that should fail with 429 or 500 errors.
- **Latency Range**: Set the min/max delay (in seconds) for responses.
- **TPM Limit**: Configure the Tokens-Per-Minute limit to test rate-limiting.
- **Context Window**: Set the maximum token limit to test prompt truncation.
- **Loaded Models**: Enter a comma-separated list of models that are "in VRAM." Any model not on this list will trigger a 404 GPU OOM simulation.

#### B. Scenario Manager
Manage the keyword-based response system:
- **Create/Edit/Delete**: Add new scenarios or modify existing ones to simulate safety refusals, hallucinations, or specific edge cases.
- **Instant Updates**: Changes made in the dashboard are saved to `scenarios.json` and applied to the next request immediately.

#### C. The Panic Button
Toggles **Meltdown Mode**, which simulates a cascading service failure (Latency $\rightarrow$ Outage $\rightarrow$ Collapse). Use this to test your system's absolute worst-case scenario.

#### D. Live Server Logs
A real-time stream of server events. Chaos events (like triggered failures or latency injections) are highlighted in red, allowing you to correlate API errors with the Chaos Engine's actions.

**Access it at**: `http://localhost:8888/admin`
