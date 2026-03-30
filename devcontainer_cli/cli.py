import json
import sys

import click

from devcontainer_cli import __version__
from devcontainer_cli.parser import find_devcontainer, load_devcontainer, list_features, get_summary
from devcontainer_cli.validator import validate
from devcontainer_cli.templates import list_templates, generate


@click.group()
@click.version_option(version=__version__)
def main():
    """A CLI tool to validate, inspect and generate devcontainer.json configurations."""
    pass


@main.command()
@click.argument("path", default=".", type=click.Path(exists=True))
def inspect(path):
    """Inspect a devcontainer.json and print a summary."""
    filepath = find_devcontainer(path)
    if not filepath:
        click.echo(f"Error: no devcontainer.json found in '{path}'", err=True)
        sys.exit(1)

    config = load_devcontainer(filepath)
    click.echo(f"File: {filepath}\n")

    summary = get_summary(config)
    for key, val in summary.items():
        click.echo(f"  {key}: {json.dumps(val)}")

    features = list_features(config)
    if features:
        click.echo(f"\nFeatures ({len(features)}):")
        for f in features:
            click.echo(f"  - {f}")


@main.command()
@click.argument("path", default=".", type=click.Path(exists=True))
def check(path):
    """Validate a devcontainer.json for common issues."""
    filepath = find_devcontainer(path)
    if not filepath:
        click.echo(f"Error: no devcontainer.json found in '{path}'", err=True)
        sys.exit(1)

    config = load_devcontainer(filepath)
    result = validate(config)

    if result.errors:
        click.echo("Errors:")
        for e in result.errors:
            click.echo(f"  ✗ {e}")

    if result.warnings:
        click.echo("Warnings:")
        for w in result.warnings:
            click.echo(f"  ! {w}")

    if result.ok:
        click.echo("✓ Configuration is valid.")
    else:
        sys.exit(1)


@main.command()
@click.argument("language")
@click.option("-o", "--output", default=".", help="Output directory for .devcontainer/")
def init(language, output):
    """Generate a devcontainer.json template for a language.

    Available languages: python, node, go, rust
    """
    try:
        filepath = generate(language, output)
        click.echo(f"Created {filepath}")
    except KeyError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command(name="templates")
def show_templates():
    """List available devcontainer templates."""
    click.echo("Available templates:")
    for name in list_templates():
        click.echo(f"  - {name}")
