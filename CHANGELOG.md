# Changelog

All notable changes to this project will be documented in this file.

## [0.1.1] - 2026-10-10
- **UI/UX Improvements**:
    - Completely redesigned the Admin Dashboard for better clarity and layout.
    - Added collapsible panels for Global Settings and Real LLM Service.
    - Added a real-time "Meltdown" status indicator (green/white dot) and dynamic button text ("Activate" vs "Deactivate").
    - Integrated a model badge in the chat interface to visually distinguish between mock and real responses.
- **Real LLM Integration**:
    - Implemented dynamic model loading in the chat window via the `/v1/models` endpoint.
    - Fixed a critical bug where the chat stream was ignoring the selected model and defaulting to mock responses.
    - Tied "Real" model availability to the successful completion of the verification workflow.
- **Workflow & Verification**:
    - Refined the verification workflow steps to "Install Ollama", "Model Available", "Chat working", and "Verify latency check".
    - Updated status indicators to use color-coded dots (⚪, 🟡, 🟢, 🔴).
    - Unified "Install All" and "Run All" into a single, comprehensive health-check action.
- **Maintenance**:
    - Cleaned up Git history by purging `__pycache__` and `.egg-info` directories.
    - Updated `.gitignore` to ensure build artifacts are not tracked.

## [0.1.0] - 2026-10-10
- Initial repository setup
- Added README.md
- Added LICENSE
- Added CHANGELOG.md
