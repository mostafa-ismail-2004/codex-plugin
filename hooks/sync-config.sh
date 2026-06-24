#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Consume stdin to prevent SIGPIPE/clogging the hook process
cat > /dev/null 2>/dev/null || true

PLUGIN_HOME="${CODEX_PLUGIN_HOME:-${HOME}/.codex/codex-plugin}"
ENV_PATH="${PLUGIN_HOME}/.env"
BACKUP_PATH="${PLUGIN_HOME}/codex-plugin.env.bak"

# 1. If the live .env is missing or empty, but a valid backup exists: Restore it.
if [ ! -s "$ENV_PATH" ] && [ -s "$BACKUP_PATH" ]; then
  mkdir -p "$(dirname "$ENV_PATH")"
  cp "$BACKUP_PATH" "$ENV_PATH"
  exit 0
fi

# 2. If the live .env exists and is non-empty: Manage backup.
if [ -s "$ENV_PATH" ]; then
  # If backup is missing, empty, or differs from the live config: Update the backup.
  if [ ! -s "$BACKUP_PATH" ] || ! cmp -s "$ENV_PATH" "$BACKUP_PATH"; then
    cp "$ENV_PATH" "$BACKUP_PATH"
  fi
fi
