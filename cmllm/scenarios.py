from typing import Dict, List, Tuple, Optional
import random

# A Scenario is a tuple of (Keywords, Response Template)
# If any keyword in the list is found in the prompt, the corresponding template is used.
SCENARIOS: Dict[str, Tuple[List[str], str]] = {
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

def get_scenario_response(text: str, provider_name: str, model: str) -> str:
    """
    Analyzes the input text and returns a response based on matching scenarios.
    If no scenario matches, it falls back to the generic helpful response.
    """
    text_lower = text.lower()

    # Check for specific scenarios first
    for scenario_id, (keywords, template) in SCENARIOS.items():
        if scenario_id == "generic_helpful":
            continue
        if any(kw in text_lower for kw in keywords):
            return f"[{provider_name.upper()}-{model}] {template}"

    # Fallback to generic helpful
    _, generic_template = SCENARIOS["generic_helpful"]
    return f"[{provider_name.upper()}-{model}] {generic_template}"
