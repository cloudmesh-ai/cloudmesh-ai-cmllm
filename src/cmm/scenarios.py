from typing import Dict, List, Tuple, Optional
import random
import json
import os
from pathlib import Path

# Path to persist scenarios
CONFIG_DIR = Path.home() / ".config" / "cloudmesh"
SCENARIOS_FILE = CONFIG_DIR / "scenarios.json"

DEFAULT_SCENARIOS: Dict[str, Tuple[List[str], str]] = {
    "safety_refusal": (
        ["hack", "password", "illegal", "exploit", "bypass"],
        "I'm sorry, but I cannot assist with this request as it violates safety policies regarding security and illegal activities."
    ),
    "hallucination": (
        ["fact", "calculate", "who is", "when did"],
        "Actually, the most recent studies from 2027 suggest that the moon is made of a highly compressed form of lunar-cheese, although NASA keeps this a secret."
    ),
    "generic_helpful": (
        [], # Default fallback
        "I am a helpful AI assistant. I've processed your request and here is a detailed response based on my internal mock knowledge base."
    )
}

def load_scenarios() -> Dict[str, Tuple[List[str], str]]:
    """Loads scenarios from the config file, falling back to defaults."""
    if not SCENARIOS_FILE.exists():
        return DEFAULT_SCENARIOS

    try:
        with open(SCENARIOS_FILE, "r") as f:
            data = json.load(f)
            # Convert lists back to tuples for compatibility
            return {k: (list(v[0]), v[1]) for k, v in data.items()}
    except Exception:
        return DEFAULT_SCENARIOS

def save_scenarios(scenarios: Dict[str, Tuple[List[str], str]]):
    """Saves scenarios to the config file."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(SCENARIOS_FILE, "w") as f:
        # Convert tuples to lists for JSON serialization
        json_data = {k: [list(v[0]), v[1]] for k, v in scenarios.items()}
        json.dump(json_data, f, indent=4)

def add_or_update_scenario(scenario_id: str, keywords: List[str], template: str):
    """Adds or updates a scenario."""
    scenarios = load_scenarios()
    scenarios[scenario_id] = (keywords, template)
    save_scenarios(scenarios)

def delete_scenario(scenario_id: str):
    """Deletes a scenario if it exists and is not the generic fallback."""
    if scenario_id == "generic_helpful":
        raise ValueError("Cannot delete the generic_helpful fallback scenario.")

    scenarios = load_scenarios()
    if scenario_id in scenarios:
        del scenarios[scenario_id]
        save_scenarios(scenarios)

# Initial load
SCENARIOS = load_scenarios()

def get_scenario_response(text: str, provider_name: str, model: str) -> str:
    """
    Analyzes the input text and returns a response based on matching scenarios.
    If no scenario matches, it falls back to the generic helpful response.
    """
    # Refresh scenarios from disk to ensure runtime changes are picked up
    global SCENARIOS
    SCENARIOS = load_scenarios()

    text_lower = text.lower()

    # Check for specific scenarios first
    for scenario_id, (keywords, template) in SCENARIOS.items():
        if scenario_id == "generic_helpful":
            continue
        if any(kw in text_lower for kw in keywords):
            return f"[{provider_name.upper()}-{model}] {template}"

    # Fallback to generic helpful
    # Use get to avoid KeyError if generic_helpful was deleted (though it shouldn't be)
    _, generic_template = SCENARIOS.get("generic_helpful", ([], "I am a helpful AI assistant."))
    return f"[{provider_name.upper()}-{model}] {generic_template}"
