"""Helpers for invoking Codex CLI from skill-comply."""

from __future__ import annotations


MODEL_ALIASES = {
    "flash": "gpt-5.5-flash",
    "flash-8b": "gpt-5.5-flash",
    "pro": "gpt-5.5-pro",
}


def codex_exec_command(
    prompt: str,
    model: str = "inherit",
    *,
    json_output: bool = False,
    extra_args: list[str] | None = None,
) -> list[str]:
    """Build a Codex non-interactive command for a prompt."""
    command = ["codex", "exec"]

    resolved_model = MODEL_ALIASES.get(model, model)
    if resolved_model and resolved_model != "inherit":
        command.extend(["--model", resolved_model])

    if json_output:
        command.append("--json")

    if extra_args:
        command.extend(extra_args)

    command.append(prompt)
    return command
