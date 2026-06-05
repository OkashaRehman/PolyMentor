#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${GROQ_API_KEY:-}" ]]; then
    echo "GROQ_API_KEY is not set."
    echo "Create a Groq API key, then run:"
    echo "  export GROQ_API_KEY='your_key_here'"
    exit 1
fi

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ -x "$PROJECT_ROOT/venv/Scripts/python.exe" ]]; then
    PYTHON="$PROJECT_ROOT/venv/Scripts/python.exe"
elif [[ -x "$PROJECT_ROOT/venv/bin/python" ]]; then
    PYTHON="$PROJECT_ROOT/venv/bin/python"
else
    PYTHON="${PYTHON:-python}"
fi

"$PYTHON" "$PROJECT_ROOT/src/inference/tutor_mode.py" "$@"
