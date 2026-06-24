#!/usr/bin/env bash

# Exit on error
set -e

# Target directory
TARGET_DIR="${HOME}/.codex/plugins/codex-plugin"

echo "=========================================================="
echo "Codex Plugin - Real-time Dev Sync Helper"
echo "=========================================================="
echo "Local Workspace: $(pwd)"
echo "Target Plugin:   ${TARGET_DIR}"
echo "=========================================================="

# Ensure target directory exists
mkdir -p "${TARGET_DIR}"

# Run initial sync
echo "Running initial sync..."
rsync -av --delete \
  --exclude '.git' \
  --exclude 'node_modules' \
  --exclude '.env' \
  --exclude '.antigravitycli' \
  --exclude '.codex-plugin/local-cache' \
  ./ "${TARGET_DIR}/"

echo "Watcher started. Monitoring changes and syncing in real-time..."

# Start nodemon to watch the directory and sync on changes
# Watches files with common extensions and triggers rsync
nodemon --watch . \
  --ext json,js,ts,sh,md \
  --ignore node_modules \
  --ignore .git \
  --exec "rsync -av --delete --exclude '.git' --exclude 'node_modules' --exclude '.env' --exclude '.antigravitycli' --exclude '.codex-plugin/local-cache' . ${TARGET_DIR}/"
