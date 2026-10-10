import pytest
from click.testing import CliRunner
from unittest.mock import patch, MagicMock, ANY, mock_open
from cmm.main import cli

runner = CliRunner()

@pytest.fixture
def mock_provider():
    with patch('cmm.main.get_provider') as mock_get:
        mock_llm = MagicMock()
        mock_llm.prompt.return_value = "Mocked response"
        mock_llm.list_models.return_value = ["model-1", "model-2"]
        mock_get.return_value = mock_llm
        yield mock_get

def test_cli_prompt(mock_provider):
    # Test prompting with default provider
    result = runner.invoke(cli, ['prompt', 'Hello'])
    assert result.exit_code == 0
    assert "Mocked response" in result.output

def test_cli_prompt_provider_override(mock_provider):
    # Test prompting with provider override
    result = runner.invoke(cli, ['prompt', 'Hello', '--provider', 'vllm'])
    assert result.exit_code == 0
    assert "Mocked response" in result.output
    mock_provider.assert_called_with('vllm', ANY)

def test_cli_prompt_model_override(mock_provider):
    # Test prompting with model override
    result = runner.invoke(cli, ['prompt', 'Hello', '--model', 'gpt-4-mock'])
    assert result.exit_code == 0
    assert "Mocked response" in result.output
    mock_provider.return_value.prompt.assert_called_with('Hello', model='gpt-4-mock')

def test_cli_provider_set():
    # Test setting provider
    with patch('cmm.main.save_config'), patch('cmm.main.load_config') as mock_load:
        mock_load.return_value = {"active_provider": "ollama", "providers": {}}
        result = runner.invoke(cli, ['provider', 'set', 'vllm'])
        assert result.exit_code == 0
        assert "Active provider set to: vllm" in result.output

def test_cli_provider_get():
    # Set then get
    with patch('cmm.main.load_config') as mock_load:
        mock_load.return_value = {"active_provider": "ollama"}
        result = runner.invoke(cli, ['provider', 'get'])
        assert result.exit_code == 0
        assert "Active provider: ollama" in result.output

def test_cli_list_models(mock_provider):
    result = runner.invoke(cli, ['list'])
    assert result.exit_code == 0
    assert "Models available for" in result.output
    assert "- model-1" in result.output
    assert "- model-2" in result.output

def test_cli_list_provider_override(mock_provider):
    result = runner.invoke(cli, ['list', '--provider', 'vllm'])
    assert result.exit_code == 0
    assert "Models available for vllm" in result.output
    mock_provider.assert_called_with('vllm', ANY)

def test_cli_invalid_provider():
    with patch('cmm.main.list_available_providers', return_value=['ollama', 'vllm']):
        result = runner.invoke(cli, ['provider', 'set', 'unknown-provider'])
        assert result.exit_code == 0
        assert "Error: Unsupported provider" in result.output

def test_cli_init():
    # Test init creates the config file
    with patch('cmm.main.os.path.exists', return_value=False), \
         patch('cmm.main.os.makedirs'), \
         patch('cmm.main.open', mock_open()):
        result = runner.invoke(cli, ['init'])
        assert result.exit_code == 0
        assert "Initialized default configuration" in result.output

def test_cli_config_missing(mock_provider):
    # Test that defaults are used when config is missing
    with patch('cmm.main.os.path.exists', return_value=False):
        result = runner.invoke(cli, ['prompt', 'Hello'])
        assert result.exit_code == 0
        assert "Mocked response" in result.output

def test_cli_config_corrupt(mock_provider):
    # Test behavior when config is invalid yaml
    with patch('cmm.main.os.path.exists', return_value=True), \
         patch('cmm.main.open', mock_open(read_data="invalid: yaml: :")), \
         patch('cmm.main.yaml.safe_load', side_effect=Exception("YAML Error")):
        result = runner.invoke(cli, ['prompt', 'Hello'])
        assert result.exit_code == 0
        assert "Mocked response" in result.output

def test_cli_serve_help():
    # We only test that the command exists and shows help, as running the server would block
    result = runner.invoke(cli, ['serve', '--help'])
    assert result.exit_code == 0
    assert "Start the OpenAI-compatible mock LLM server" in result.output
