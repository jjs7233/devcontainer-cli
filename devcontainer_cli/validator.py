"""Validate devcontainer.json configurations."""

from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0


VALID_REMOTE_USERS = {"root", "vscode", "node", "codespace"}

KNOWN_LIFECYCLE_COMMANDS = [
    "postCreateCommand",
    "postStartCommand",
    "postAttachCommand",
    "initializeCommand",
    "onCreateCommand",
    "updateContentCommand",
    "waitFor",
]


def validate(config: dict) -> ValidationResult:
    """Run all validation checks on a parsed devcontainer config."""
    result = ValidationResult()
    _check_image_or_build(config, result)
    _check_features_format(config, result)
    _check_forward_ports(config, result)
    _check_remote_user(config, result)
    _check_lifecycle_commands(config, result)
    _check_unknown_top_level(config, result)
    return result


def _check_image_or_build(config: dict, result: ValidationResult):
    has_image = "image" in config
    has_dockerfile = "dockerFile" in config or "build" in config
    has_compose = "dockerComposeFile" in config
    if not has_image and not has_dockerfile and not has_compose:
        result.errors.append(
            "Missing container source: specify 'image', 'dockerFile', 'build', "
            "or 'dockerComposeFile'"
        )
    if has_image and has_dockerfile:
        result.warnings.append(
            "'image' and 'dockerFile'/'build' are both set — 'image' will be ignored"
        )


def _check_features_format(config: dict, result: ValidationResult):
    features = config.get("features")
    if features is None:
        return
    if not isinstance(features, dict):
        result.errors.append("'features' must be an object mapping feature IDs to options")
        return
    for feature_id, opts in features.items():
        if not isinstance(feature_id, str):
            result.errors.append(f"Feature key must be a string, got: {feature_id!r}")
        if not isinstance(opts, (dict, str)):
            result.warnings.append(
                f"Feature '{feature_id}': options should be an object or version string"
            )


def _check_forward_ports(config: dict, result: ValidationResult):
    ports = config.get("forwardPorts")
    if ports is None:
        return
    if not isinstance(ports, list):
        result.errors.append("'forwardPorts' must be an array")
        return
    for port in ports:
        if isinstance(port, int):
            if port < 1 or port > 65535:
                result.errors.append(f"Invalid port number: {port}")
        elif isinstance(port, str):
            # "host:container" format
            if ":" not in port:
                result.warnings.append(f"Port string '{port}' should use 'host:container' format")
        else:
            result.errors.append(f"Invalid port entry: {port!r}")


def _check_remote_user(config: dict, result: ValidationResult):
    user = config.get("remoteUser")
    if user and user not in VALID_REMOTE_USERS:
        result.warnings.append(
            f"Uncommon remoteUser '{user}' — typical values: {', '.join(sorted(VALID_REMOTE_USERS))}"
        )


def _check_lifecycle_commands(config: dict, result: ValidationResult):
    for cmd_key in KNOWN_LIFECYCLE_COMMANDS:
        val = config.get(cmd_key)
        if val is None:
            continue
        if not isinstance(val, (str, list, dict)):
            result.errors.append(f"'{cmd_key}' must be a string, array, or object")


KNOWN_TOP_LEVEL_KEYS = {
    "name", "image", "build", "dockerFile", "context", "dockerComposeFile",
    "service", "workspaceFolder", "features", "overrideFeatureInstallOrder",
    "forwardPorts", "portsAttributes", "otherPortsAttributes",
    "remoteUser", "containerUser", "updateRemoteUserUID",
    "remoteEnv", "containerEnv",
    "postCreateCommand", "postStartCommand", "postAttachCommand",
    "initializeCommand", "onCreateCommand", "updateContentCommand", "waitFor",
    "customizations", "mounts", "runArgs", "shutdownAction",
    "overrideCommand", "privileged", "capAdd", "securityOpt",
    "appPort", "hostRequirements",
}


def _check_unknown_top_level(config: dict, result: ValidationResult):
    for key in config:
        if key not in KNOWN_TOP_LEVEL_KEYS:
            result.warnings.append(f"Unknown top-level key: '{key}'")
