import click
import yaml
import os
import logging
from typing import Dict, Any
from .providers import get_provider, list_available_providers
from .base_server import start_server
from .logger import setup_logging, get_logger

logger = get_logger("cmllm.cli")
CONFIG_PATH = os.path.expanduser("~/.config/cloudmesh/llms-mock.yaml")

def load_config() -> Dict[str, Any]:
    if not os.path.exists(CONFIG_PATH):
        logger.info(f"Configuration file not found at {CONFIG_PATH}. Using defaults.")
        return {
            "active_provider": "ollama",
            "providers": {
                "ollama": {"default_model": "llama3"},
                "vllm": {"default_model": "gpt-4-mock"},
            }
        }
    try:
        with open(CONFIG_PATH, 'r') as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        logger.error(f"Error loading config file: {e}")
        return {}

def save_config(config: Dict[str, Any]):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, 'w') as f:
        yaml.dump(config, f)

@cli.group()
@click.option('--debug', is_flag=True, help='Enable debug logging.')
@click.pass_context
def cli(ctx, debug):
    """Cloudmesh AI CMLLM CLI - Manage and prompt mock LLM providers."""
    setup_logging(debug)
    ctx.ensure_object(dict)

@cli.group()
def provider():
    """Manage LLM providers."""
    pass

@provider.command('set')
@click.argument('name')
def provider_set(name):
    """Set the active LLM provider."""
    config = load_config()
    if name.lower() not in list_available_providers():
        click.secho(f"Error: Unsupported provider '{name}'. Available: {list_available_providers()}", fg='red')
        return
    config['active_provider'] = name.lower()
    save_config(config)
    click.secho(f"Active provider set to: {name}", fg='green')

@provider.command('get')
def provider_get():
    """Get the current active LLM provider."""
    config = load_config()
    active = config.get('active_provider', 'none')
    click.echo(f"Active provider: {active}")

@cli.command('prompt')
@click.argument('text')
@click.option('--provider', '-p', help='Override the active provider.')
@click.option('--model', '-m', help='Override the active model.')
def prompt(text, provider, model):
    """Send a prompt to the active LLM provider."""
    config = load_config()
    provider_name = provider or config.get('active_provider', 'ollama')

    try:
        provider_cfg = config.get('providers', {}).get(provider_name, {})
        llm = get_provider(provider_name, provider_cfg)
        response = llm.prompt(text, model=model)
        click.echo(response)
    except Exception as e:
        click.secho(f"Error: {e}", fg='red')

@cli.command('list')
@click.option('--provider', '-p', help='Override the active provider.')
def list_models(provider):
    """List available models for the active provider."""
    config = load_config()
    provider_name = provider or config.get('active_provider', 'ollama')

    try:
        provider_cfg = config.get('providers', {}).get(provider_name, {})
        llm = get_provider(provider_name, provider_cfg)
        models = llm.list_models()
        click.echo(f"Models available for {provider_name}:")
        for m in models:
            click.echo(f" - {m}")
    except Exception as e:
        click.secho(f"Error: {e}", fg='red')

@cli.command('init')
def config_init():
    """Initialize the default configuration file."""
    default_config = {
        "active_provider": "ollama",
        "providers": {
            "ollama": {"default_model": "llama3"},
            "vllm": {"default_model": "gpt-4-mock"},
        }
    }

    try:
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        if os.path.exists(CONFIG_PATH):
            click.echo(f"Configuration file already exists at {CONFIG_PATH}. Skipping.")
        else:
            with open(CONFIG_PATH, 'w') as f:
                yaml.dump(default_config, f)
            click.secho(f"Initialized default configuration at {CONFIG_PATH}", fg='green')
    except Exception as e:
        logger.error(f"Failed to initialize config: {e}")
        click.secho(f"Error initializing config: {e}", fg='red')

@cli.command('serve')
@click.option('--host', default='0.0.0.0', help='Host to bind the server to.')
@click.option('--port', default=8000, type=int, help='Port to bind the server to.')
def serve(host, port):
    """Start the OpenAI-compatible mock LLM server."""
    click.secho(f"Starting CMLLM Mock Server on http://{host}:{port}", fg='cyan')
    click.echo("Documentation available at http://localhost:8000/docs")
    start_server(host, port)

if __name__ == '__main__':
    cli()
