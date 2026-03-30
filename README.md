# devcontainer-cli

A command-line tool to validate, inspect, and generate [devcontainer.json](https://containers.dev/) configurations.

## Installation

```bash
pip install -e .
```

## Usage

### Inspect a devcontainer configuration

```bash
devcontainer-cli inspect .
```

Locates the `devcontainer.json` in the current directory and prints a summary of key fields and features.

### Validate a configuration

```bash
devcontainer-cli check .
```

Checks for common issues:
- Missing container source (image / Dockerfile / Compose)
- Invalid features format
- Invalid port numbers
- Uncommon remoteUser values
- Unknown top-level keys

### Generate a template

```bash
devcontainer-cli init python
```

Creates a `.devcontainer/devcontainer.json` with a ready-to-use template. Supported languages:

```bash
devcontainer-cli templates
```

Currently available: `go`, `node`, `python`, `rust`

### Options

```bash
devcontainer-cli --version
devcontainer-cli --help
devcontainer-cli init python -o /path/to/project
```

## Project Structure

```
devcontainer_cli/
├── __init__.py      # Package version
├── cli.py           # Click CLI entry point
├── parser.py        # JSONC parser and config inspector
├── validator.py     # Configuration validation checks
└── templates.py     # Template definitions and generator
```

## Requirements

- Python >= 3.10
- click >= 8.0
- jsonschema >= 4.0
