import click
import yaml
import os
import asyncio
import logging
from typing import Dict, Any
from .providers import get_provider, list_available_providers
from .base_server import start_server
from .logger import setup_logging, get_logger
from .utils import kill_process_on_port
from .config import load_config, save_config, CONFIG_PATH

logger = get_logger("cmm.cli")

@click.group()
@click.option('--debug', is_flag=True, help='Enable debug logging.')
@click.pass_context
def cli(ctx, debug):
    """Cloudmesh AI CMM CLI - Manage and prompt mock LLM providers."""
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

    async def run_prompt():
        try:
            provider_cfg = config.get('providers', {}).get(provider_name, {})
            llm = get_provider(provider_name, provider_cfg)
            response, finish_reason = await llm.prompt(text, model=model)
            return response
        except Exception as e:
            return e

    result = asyncio.run(run_prompt())
    if isinstance(result, Exception):
        click.secho(f"Error: {result}", fg='red')
    else:
        click.echo(result)

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
            "ollama": {"default_model": "llama3", "mode": "mock"},
            "vllm": {"default_model": "gpt-4-mock", "mode": "mock"},
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
@click.option('--host', default='127.0.0.1', help='Host to bind the server to.')
@click.option('--port', default=8888, type=int, help='Port to bind the server to.')
@click.option('--kill-port', is_flag=True, default=True, help='Kill any process using the port before starting.')
def serve(host, port, kill_port):
    """Start the OpenAI-compatible mock LLM server."""
    if kill_port:
        kill_process_on_port(port)
    click.secho(f"Starting CMM Mock Server on http://{host}:{port}", fg='cyan')
    click.echo(f"User Chat UI:    http://{host}:{port}/chat")
    click.echo(f"Admin Dashboard: http://{host}:{port}/admin")
    click.echo(f"API Documentation: http://{host}:{port}/docs")
    start_server(host, port)

if __name__ == '__main__':
    cli()
