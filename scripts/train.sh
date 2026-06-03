#!/usr/bin/env bash
set -euo pipefail

echo "PolyMentor now uses Groq as the primary coding tutor model."
echo ""
echo "There is no local checkpoint training step required for normal use."
echo "Set GROQ_API_KEY, then run:"
echo "  bash scripts/run_tutor.sh"
echo "  uvicorn src.api.app:app --reload"
echo ""
echo "Future fine-tuning experiments can live under experiments/, but they are not"
echo "the main application path anymore."
