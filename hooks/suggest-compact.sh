#!/usr/bin/env bash
# Strategic Compact Suggester
# Runs on PreToolUse to suggest manual compaction at logical intervals

# Use Codex session identifiers when present, or fallback to PPID.
SESSION_ID="${CODEX_SESSION_ID:-${PPID:-default}}"
# Use a hidden directory for temp files to keep it clean
TEMP_DIR="/tmp/.codex-plugin-compact"
mkdir -p "$TEMP_DIR"
COUNTER_FILE="${TEMP_DIR}/count-${SESSION_ID}"
# Use the environment variable injected from plugin settings
THRESHOLD=${CODEX_PLUGIN_COMPACT_THRESHOLD:-50}

# Initialize or increment counter
if [ -f "$COUNTER_FILE" ]; then
  count=$(cat "$COUNTER_FILE")
  count=$((count + 1))
  echo "$count" > "$COUNTER_FILE"
else
  echo "1" > "$COUNTER_FILE"
  count=1
fi

# Suggest compact after threshold tool calls
if [ "$count" -eq "$THRESHOLD" ]; then
  echo -e "\033[1;33m[StrategicCompact] $THRESHOLD tool calls reached - consider /compact if transitioning phases\033[0m" >&2
fi

# Suggest at regular intervals after threshold
if [ "$count" -gt "$THRESHOLD" ] && [ $((count % 25)) -eq 0 ]; then
  echo -e "\033[1;33m[StrategicCompact] $count tool calls - good checkpoint for /compact if context is stale\033[0m" >&2
fi
