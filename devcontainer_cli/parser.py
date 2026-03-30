"""Parse and inspect devcontainer.json files."""

import json
from pathlib import Path

SEARCH_PATHS = [
    ".devcontainer/devcontainer.json",
    ".devcontainer.json",
]


def find_devcontainer(project_dir: str = ".") -> Path | None:
    """Locate the devcontainer.json file in a project directory."""
    root = Path(project_dir)
    for rel in SEARCH_PATHS:
        candidate = root / rel
        if candidate.is_file():
            return candidate
    return None


def load_devcontainer(path: str | Path) -> dict:
    """Load and parse a devcontainer.json file.

    Handles JSON with comments (JSONC) by stripping single-line comments.
    """
    text = Path(path).read_text(encoding="utf-8")
    stripped = _strip_jsonc_comments(text)
    return json.loads(stripped)


def _strip_jsonc_comments(text: str) -> str:
    """Remove single-line // comments outside of strings."""
    lines = []
    for line in text.splitlines():
        in_string = False
        i = 0
        while i < len(line):
            ch = line[i]
            if ch == '"' and (i == 0 or line[i - 1] != "\\"):
                in_string = not in_string
            elif not in_string and ch == "/" and i + 1 < len(line) and line[i + 1] == "/":
                line = line[:i]
                break
            i += 1
        lines.append(line)
    return "\n".join(lines)


def list_features(config: dict) -> list[str]:
    """Extract the list of devcontainer features from a parsed config."""
    features = config.get("features", {})
    return list(features.keys())


def get_summary(config: dict) -> dict:
    """Return a summary of key fields from a devcontainer config."""
    fields = ["name", "image", "dockerFile", "build", "features",
              "forwardPorts", "postCreateCommand", "remoteUser"]
    return {k: config[k] for k in fields if k in config}
