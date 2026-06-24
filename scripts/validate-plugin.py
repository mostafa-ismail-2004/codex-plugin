#!/usr/bin/env python3
"""Lightweight public validator for the Codex Plugin package."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def fail(message: str) -> None:
    print(f"Validation failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_json(path: Path) -> dict:
    try:
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        fail(f"missing {path}")
    except json.JSONDecodeError as exc:
        fail(f"{path} is invalid JSON: {exc}")
    if not isinstance(data, dict):
        fail(f"{path} must contain a JSON object")
    return data


def validate_manifest(root: Path) -> None:
    manifest_path = root / ".codex-plugin" / "plugin.json"
    manifest = load_json(manifest_path)

    required = ["name", "version", "description", "author", "skills", "interface"]
    for key in required:
        if key not in manifest:
            fail(f"plugin.json missing required field: {key}")

    name = manifest["name"]
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", name):
        fail("plugin.json name must be kebab-case and <= 64 chars")

    if not isinstance(manifest["version"], str) or not re.fullmatch(
        r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", manifest["version"]
    ):
        fail("plugin.json version must be semver-like")

    author = manifest["author"]
    if not isinstance(author, dict) or not author.get("name"):
        fail("plugin.json author.name is required")

    interface = manifest["interface"]
    if not isinstance(interface, dict):
        fail("plugin.json interface must be an object")
    for key in ["displayName", "shortDescription", "longDescription", "developerName", "category"]:
        if not interface.get(key):
            fail(f"plugin.json interface.{key} is required")

    skills_path = root / manifest["skills"]
    if not skills_path.exists():
        fail(f"skills path does not exist: {skills_path}")

    if "mcpServers" in manifest:
        mcp_path = root / manifest["mcpServers"]
        mcp = load_json(mcp_path)
        if "mcpServers" not in mcp or not isinstance(mcp["mcpServers"], dict):
            fail(".mcp.json must contain an mcpServers object")


def validate_hooks(root: Path) -> None:
    hooks_path = root / "hooks" / "hooks.json"
    if not hooks_path.exists():
        return
    hooks = load_json(hooks_path)
    if "hooks" not in hooks or not isinstance(hooks["hooks"], dict):
        fail("hooks/hooks.json must contain a hooks object")


def main() -> None:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    validate_manifest(root)
    validate_hooks(root)
    print(f"Plugin validation passed: {root}")


if __name__ == "__main__":
    main()
