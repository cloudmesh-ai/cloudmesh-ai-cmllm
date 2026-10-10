import os
import pytest
from cmm import config

def test_apply_env_overrides_top_level():
    """Test that a top-level config value can be overridden by an env var."""
    initial_config = {"active_provider": "ollama", "providers": {}}
    os.environ["CMM_ACTIVE_PROVIDER"] = "vllm"
    
    result = config.apply_env_overrides(initial_config.copy())
    
    assert result["active_provider"] == "vllm"
    del os.environ["CMM_ACTIVE_PROVIDER"]

def test_apply_env_overrides_nested():
    """Test that a nested config value can be overridden by an env var."""
    initial_config = {
        "active_provider": "ollama",
        "providers": {
            "ollama": {"default_model": "llama3"}
        }
    }
    os.environ["CMM_PROVIDERS_OLLAMA_DEFAULT_MODEL"] = "llama2"
    
    result = config.apply_env_overrides(initial_config.copy())
    
    assert result["providers"]["ollama"]["default_model"] == "llama2"
    del os.environ["CMM_PROVIDERS_OLLAMA_DEFAULT_MODEL"]

def test_apply_env_overrides_new_keys():
    """Test that new keys can be created via env vars."""
    initial_config = {}
    os.environ["CMM_NEW_SETTING"] = "value"
    
    result = config.apply_env_overrides(initial_config.copy())
    
    assert result["new_setting"] == "value"
    del os.environ["CMM_NEW_SETTING"]

def test_apply_env_overrides_casting():
    """Test that values are cast to the correct type based on existing config."""
    initial_config = {
        "timeout": 30,
        "enabled": True,
        "ratio": 0.5
    }
    os.environ["CMM_TIMEOUT"] = "60"
    os.environ["CMM_ENABLED"] = "false"
    os.environ["CMM_RATIO"] = "0.7"
    
    result = config.apply_env_overrides(initial_config.copy())
    
    assert result["timeout"] == 60
    assert result["enabled"] is False
    assert result["ratio"] == 0.7
    
    del os.environ["CMM_TIMEOUT"]
    del os.environ["CMM_ENABLED"]
    del os.environ["CMM_RATIO"]

def test_apply_env_overrides_invalid_cast():
    """Test that invalid casts fall back to strings."""
    initial_config = {"timeout": 30}
    os.environ["CMM_TIMEOUT"] = "not-a-number"
    
    result = config.apply_env_overrides(initial_config.copy())
    
    assert result["timeout"] == "not-a-number"
    del os.environ["CMM_TIMEOUT"]

def test_apply_env_overrides_deep_nesting():
    """Test that deep nesting is handled correctly."""
    initial_config = {"a": {"b": {"c": 1}}}
    os.environ["CMM_A_B_C"] = "2"
    
    result = config.apply_env_overrides(initial_config.copy())
    
    assert result["a"]["b"]["c"] == 2
    del os.environ["CMM_A_B_C"]

def test_load_config_with_env():
    """Integration test for load_config and env overrides."""
    # Mock CONFIG_PATH to avoid touching user config
    original_path = config.CONFIG_PATH
    config.CONFIG_PATH = "tests/unit/test_mock_config.yaml"
    
    with open(config.CONFIG_PATH, "w") as f:
        f.write("active_provider: ollama\nproviders:\n  ollama:\n    default_model: llama3")
    
    os.environ["CMM_ACTIVE_PROVIDER"] = "vllm"
    
    try:
        res = config.load_config()
        assert res["active_provider"] == "vllm"
        assert res["providers"]["ollama"]["default_model"] == "llama3"
    finally:
        if os.path.exists(config.CONFIG_PATH):
            os.remove(config.CONFIG_PATH)
        config.CONFIG_PATH = original_path
        del os.environ["CMM_ACTIVE_PROVIDER"]
