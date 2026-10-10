import pytest
from click.testing import CliRunner
from cmllm.main import cli

runner = CliRunner()

def test_cli_prompt():
    # Test prompting with default provider
    result = runner.invoke(cli, ['prompt', 'Hello'])
    assert result.exit_code == 0
    assert "[Ollama" in result.output or "[vLLM" in result.output

def test_cli_provider_set():
    # Test setting provider
    result = runner.invoke(cli, ['provider', 'set', 'vllm'])
    assert result.exit_code == 0
    assert "Active provider set to: vllm" in result.output

def test_cli_provider_get():
    # Set then get
    runner.invoke(cli, ['provider', 'set', 'ollama'])
    result = runner.invoke(cli, ['provider', 'get'])
    assert result.exit_code == 0
    assert "Active provider: ollama" in result.output

def test_cli_list_models():
    result = runner.invoke(cli, ['list'])
    assert result.exit_code == 0
    assert "Models available for" in result.output

def test_cli_invalid_provider():
    result = runner.invoke(cli, ['provider', 'set', 'unknown-provider'])
    assert result.exit_code == 0
    assert "Error: Unsupported provider" in result.output

def test_cli_serve_help():
    # We only test that the command exists and shows help, as running the server would block
    result = runner.invoke(cli, ['serve', '--help'])
    assert result.exit_code == 0
    assert "Start the OpenAI-compatible mock LLM server" in result.output
