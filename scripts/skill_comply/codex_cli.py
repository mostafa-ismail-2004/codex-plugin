"""Helpers for invoking Codex CLI from skill-comply."""

from __future__ import annotations

def codex_exec_command(
    prompt: str,
    model: str = "inherit",
    *,
    json_output: bool = False,
    extra_args: list[str] | None = None,
) -> list[str]:
    """Build a Codex non-interactive command for a prompt."""
    command = ["codex", "exec"]

    if model and model != "inherit":
        command.extend(["--model", model])

    if json_output:
        command.append("--json")

    if extra_args:
        command.extend(extra_args)

    command.append(prompt)
    return command
