#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MENU_PY="$SCRIPT_DIR/menu.py"

if command -v python3 >/dev/null 2>&1; then
    exec python3 "$MENU_PY" "$@"
elif command -v python >/dev/null 2>&1; then
    exec python "$MENU_PY" "$@"
else
    echo "ERROR: Python was not found on PATH." >&2
    exit 1
fi
