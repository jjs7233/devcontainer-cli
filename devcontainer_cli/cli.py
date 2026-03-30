import click

from devcontainer_cli import __version__


@click.group()
@click.version_option(version=__version__)
def main():
    """A CLI tool to validate, inspect and generate devcontainer.json configurations."""
    pass
