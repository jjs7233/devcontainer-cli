"""Generate devcontainer.json templates for common languages and frameworks."""

import json
from pathlib import Path

TEMPLATES: dict[str, dict] = {
    "python": {
        "name": "Python Dev Container",
        "image": "mcr.microsoft.com/devcontainers/python:3.12",
        "features": {
            "ghcr.io/devcontainers/features/common-utils:2": {},
        },
        "customizations": {
            "vscode": {
                "extensions": [
                    "ms-python.python",
                    "ms-python.pylint",
                ],
            },
        },
        "postCreateCommand": "pip install -r requirements.txt",
        "forwardPorts": [],
        "remoteUser": "vscode",
    },
    "node": {
        "name": "Node.js Dev Container",
        "image": "mcr.microsoft.com/devcontainers/javascript-node:20",
        "features": {
            "ghcr.io/devcontainers/features/common-utils:2": {},
        },
        "customizations": {
            "vscode": {
                "extensions": [
                    "dbaeumer.vscode-eslint",
                    "esbenp.prettier-vscode",
                ],
            },
        },
        "postCreateCommand": "npm install",
        "forwardPorts": [3000],
        "remoteUser": "node",
    },
    "go": {
        "name": "Go Dev Container",
        "image": "mcr.microsoft.com/devcontainers/go:1.22",
        "features": {
            "ghcr.io/devcontainers/features/common-utils:2": {},
        },
        "customizations": {
            "vscode": {
                "extensions": [
                    "golang.go",
                ],
            },
        },
        "postCreateCommand": "go mod download",
        "forwardPorts": [],
        "remoteUser": "vscode",
    },
    "rust": {
        "name": "Rust Dev Container",
        "image": "mcr.microsoft.com/devcontainers/rust:latest",
        "features": {
            "ghcr.io/devcontainers/features/common-utils:2": {},
        },
        "customizations": {
            "vscode": {
                "extensions": [
                    "rust-lang.rust-analyzer",
                ],
            },
        },
        "postCreateCommand": "cargo build",
        "forwardPorts": [],
        "remoteUser": "vscode",
    },
}


def list_templates() -> list[str]:
    """Return available template names."""
    return sorted(TEMPLATES.keys())


def generate(language: str, output_dir: str = ".") -> Path:
    """Generate a .devcontainer/devcontainer.json from a template.

    Returns the path to the created file.
    Raises KeyError if the language template does not exist.
    """
    if language not in TEMPLATES:
        available = ", ".join(list_templates())
        raise KeyError(f"Unknown template '{language}'. Available: {available}")

    config = TEMPLATES[language]
    out = Path(output_dir) / ".devcontainer"
    out.mkdir(parents=True, exist_ok=True)

    filepath = out / "devcontainer.json"
    filepath.write_text(
        json.dumps(config, indent=4) + "\n",
        encoding="utf-8",
    )
    return filepath
