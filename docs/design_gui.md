# Design Document: cmm Simulation Interfaces

## 1. Overview
To transform the Cloudmesh AI llm-mock server into a full simulation environment, we are implementing two distinct graphical user interfaces (GUIs): an **Admin GUI** for server management and a **User GUI** for simulating the end-user chat experience.

## 2. Technology Stack (The "Lean Stack")
To maintain the project's portability and avoid a complex frontend build pipeline, we use the following open-source tools:

- **Backend**: FastAPI (Python)
- **Templating**: Jinja2 (Server-side HTML rendering)
- **Reactivity**: HTMX (Client-side dynamic updates via HTML attributes)
- **Styling**: Tailwind CSS (via CDN for modern, responsive design)
- **Communication**: Standard JSON and Server-Sent Events (SSE) for streaming

## 3. Interface Specifications

### 3.1 Admin GUI (`/admin`)
The Admin GUI is the "control room" for the mock server.

**Key Features:**
- **Provider Management**: A dropdown to change the `active_provider` globally.
- **Chaos Engine Controls**:
    - **Failure Rate**: A slider to set the percentage of requests that should return errors (429, 500).
    - **Latency Simulation**: A slider to set the artificial response delay (min/max).
    - **Scenario Toggles**: Checkboxes to enable/disable specific scenarios (e.g., "Safety Refusals").
- **Model State**: A list of available models with toggles to simulate "Loaded" vs "Unloaded" states.
- **Real-time Monitor**: A log stream showing incoming requests, the triggered provider, and the scenario used.

### 3.2 User GUI (`/chat`)
The User GUI simulates a real-world LLM chat application.

**Key Features**:
- **Chat Window**: A modern, scrollable conversation history.
- **Model Selector**: A dropdown to choose the target model (calling `/v1/models`).
- **Streaming Output**: Real-time token-by-token rendering using the server's SSE implementation.
- **Markdown Rendering**: Integrated `marked.js` for rich text, tables, and `Prism.js` for syntax highlighting in code blocks.
- **Latency Visualization**: A real-time latency meter in the header that tracks inter-token arrival times during streaming.
- **Session Management**: 'Clear Chat' functionality to reset the local conversation history.
- **Settings**: Simple toggles for "Stream" mode and "Temperature".

## 4. Technical Architecture

### 4.1 Route Mapping
| Route | Method | Description |
| :--- | :--- | :--- |
| `/admin` | GET | Renders the Admin Dashboard. |
| `/admin/config` | POST | Updates server settings (Provider, Chaos, Latency). |
| `/admin/logs` | GET | Returns the latest server logs as HTML fragments. |
| `/chat` | GET | Renders the Chat Interface. |
| `/chat/send` | POST | Handles user message and returns the initial response. |
| `/chat/stream` | GET | SSE endpoint for streaming the model response. |

### 4.2 State Management
Since the server is a singleton, a global `ServerState` object will be implemented in `base_server.py` to track:
- `active_provider`: Current default provider.
- `failure_rate`: Probability of simulated error.
- `latency_range`: Tuple of (min_delay, max_delay).
- `loaded_models`: Set of models currently "active" in memory.

The `BaseLLMProvider` and `base_server` routes will consult this `ServerState` before processing every request.
