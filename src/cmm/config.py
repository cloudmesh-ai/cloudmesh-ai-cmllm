import os
import yaml
import logging
from typing import Dict, Any

logger = logging.getLogger("cmm.config")
CONFIG_PATH = os.path.expanduser("~/.config/cloudmesh/llms-mock.yaml")

def _cast_value(value: str, original_value: Any) -> Any:
    """Cast the environment variable string value to the type of the original value."""
    if original_value is None:
        return value
    if isinstance(original_value, bool):
        return value.lower() in ("true", "1", "yes", "on")
    if isinstance(original_value, int):
        try:
            return int(value)
        except ValueError:
            return value
    if isinstance(original_value, float):
        try:
            return float(value)
        except ValueError:
            return value
    return value

def _update_config_recursive(current_config: Dict[str, Any], path_str: str, value: str):
    """
    Recursively update the config dict based on the path string.
    Tries to match the longest prefix of path_str that corresponds to a key in current_config.
    """
    if not path_str:
        return

    # Try to find the longest prefix of path_str that matches a key in current_config
    for i in range(len(path_str), 0, -1):
        key_candidate = path_str[:i]
        if key_candidate in current_config:
            # Found a match!
            remaining_path = path_str[i:]
            
            if remaining_path:
                # Remove leading underscore if present
                if remaining_path.startswith('_'):
                    remaining_path = remaining_path[1:]
                
                # If the current value is a dict, recurse.
                # If not, but we have more path, we create a dict to allow nesting.
                if not isinstance(current_config[key_candidate], dict):
                    current_config[key_candidate] = {}
                
                _update_config_recursive(current_config[key_candidate], remaining_path, value)
            else:
                # No more path, set the value with casting
                current_config[key_candidate] = _cast_value(value, current_config[key_candidate])
            return

    # If no key was found at this level, we create it to allow adding new configuration via env vars.
    current_config[path_str] = _cast_value(value, current_config.get(path_str))

def apply_env_overrides(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Override configuration settings using environment variables starting with CMM_.
    
    Example: CMM_ACTIVE_PROVIDER overrides config['active_provider']
    Example: CMM_PROVIDERS_OLLAMA_DEFAULT_MODEL overrides config['providers']['ollama']['default_model']
    """
    prefix = "CMM_"
    for env_name, env_val in os.environ.items():
        if env_name.startswith(prefix):
            # Remove prefix and lowercase the name
            path_str = env_name[len(prefix):].lower()
            _update_config_recursive(config, path_str, env_val)
    return config

def load_config() -> Dict[str, Any]:
    """Load configuration from YAML file and apply environment variable overrides."""
    config = {}
    if not os.path.exists(CONFIG_PATH):
        logger.info(f"Configuration file not found at {CONFIG_PATH}. Using defaults.")
        config = {
            "active_provider": "ollama",
            "providers": {
                "ollama": {"default_model": "llama3"},
                "vllm": {"default_model": "gpt-4-mock"},
            }
        }
    else:
        try:
            with open(CONFIG_PATH, 'r') as f:
                config = yaml.safe_load(f) or {}
        except Exception as e:
            logger.error(f"Error loading config file: {e}")
            config = {}

    return apply_env_overrides(config)

def save_config(config: Dict[str, Any]):
    """Save configuration to YAML file."""
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    try:
        with open(CONFIG_PATH, 'w') as f:
            yaml.dump(config, f)
    except Exception as e:
        logger.error(f"Error saving config file: {e}")
