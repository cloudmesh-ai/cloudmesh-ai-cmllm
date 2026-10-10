# Scenario Management Guide

Static mock responses (like "I am a helpful AI") are often insufficient for testing real-world edge cases. Cloudmesh AI llm-mock uses a **Scenario-Based Mocking** system that allows you to simulate specific model behaviors based on the content of the user's prompt.

## How Scenarios Work

A scenario consists of a set of **Keywords** and a **Response Template**. 

When a request arrives, the Scenario Manager scans the prompt for any of the configured keywords. If a match is found, the manager returns the corresponding template instead of the generic fallback response.

### The Matching Process:
1. **Input Analysis**: The prompt is converted to lowercase.
2. **Keyword Search**: The system iterates through all active scenarios.
3. **Template Selection**: The first scenario that has a keyword present in the prompt is selected.
4. **Fallback**: If no keywords match, the `generic_helpful` scenario is used as the final fallback.

## Managing Scenarios

Scenarios are managed in real-time via the **Admin Dashboard** (`/admin`).

### Creating and Editing Scenarios
In the Admin Dashboard, you can:
- **Add a New Scenario**: Provide a unique ID, a comma-separated list of keywords, and the response text.
- **Edit Existing Scenarios**: Modify keywords or templates for an existing scenario.
- **Delete Scenarios**: Remove outdated scenarios (except the `generic_helpful` fallback).

### Scenario Persistence
All scenarios are persisted in a JSON file located at `~/.config/cloudmesh/scenarios.json`. You can edit this file manually if you prefer to bulk-import scenarios.

**Example `scenarios.json` format:**
```json
{
    "safety_refusal": [
        ["hack", "password", "illegal"],
        "I'm sorry, but I cannot assist with this request as it violates safety policies."
    ],
    "hallucination": [
        ["fact", "calculate"],
        "Actually, the moon is made of lunar-cheese, according to recent 2027 studies."
    ]
}
```

## Recommended Scenarios for Testing

To get the most out of cmm, we recommend creating the following types of scenarios:

| Scenario Type | Keywords | Purpose |
| :--- | :--- | :--- |
| **Safety/Policy** | `illegal`, `exploit`, `bypass` | Test how your app displays refusals to the user. |
| **Hallucinations** | `fact`, `who is`, `when did` | Test how your app handles confidently wrong information. |
| **Edge Cases** | `weird`, `strange`, `complex` | Test if your UI breaks with unusually formatted responses. |
| **Integration Triggers** | `trigger_action`, `book_flight` | Test if your application's function-calling or agentic logic triggers correctly. |
