#!/usr/bin/env bash
# Injects a list of available slash commands into Claude's context on every prompt,
# so Claude checks for a matching command before doing work from scratch.

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
COMMANDS_DIR="$REPO_ROOT/.claude/commands"
[ -d "$COMMANDS_DIR" ] || exit 0

LIST=""
for f in "$COMMANDS_DIR"/*.md; do
  [ -f "$f" ] || continue
  fn=$(basename "$f" .md)
  title=$(head -1 "$f" | sed 's/^#[[:space:]]*//')
  LIST="${LIST}\n- /${fn}: ${title}"
done

[ -n "$LIST" ] || exit 0

MSG="$(printf "IMPORTANT: Before acting on this request, check whether it matches one of the available slash commands below. If it does, use that command instead of doing the work from scratch.\n\nAvailable commands:%b" "$LIST")"

jq -n --arg ctx "$MSG" \
  '{"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":$ctx}}'
