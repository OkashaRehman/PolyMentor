#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

if [[ -x "$PROJECT_ROOT/venv/Scripts/python.exe" ]]; then
    PYTHON="$PROJECT_ROOT/venv/Scripts/python.exe"
elif [[ -x "$PROJECT_ROOT/venv/bin/python" ]]; then
    PYTHON="$PROJECT_ROOT/venv/bin/python"
else
    PYTHON="${PYTHON:-python}"
fi

BASE_MODEL="${BASE_MODEL:-Qwen/Qwen2.5-Coder-0.5B-Instruct}"
OUTPUT_DIR="${OUTPUT_DIR:-models_saved/polymentor-chatbot-lora}"
EPOCHS="${EPOCHS:-3}"
BATCH_SIZE="${BATCH_SIZE:-1}"
GRAD_ACCUM="${GRAD_ACCUM:-8}"
LEARNING_RATE="${LEARNING_RATE:-2e-4}"
MAX_LENGTH="${MAX_LENGTH:-1024}"
INCLUDE_VENDOR="${INCLUDE_VENDOR:-1}"
MAX_VENDOR_FILES="${MAX_VENDOR_FILES:-200}"

echo "PolyMentor local fine-tuning"
echo "Python:      $PYTHON"
echo "Base model:  $BASE_MODEL"
echo "Output:      $OUTPUT_DIR"
echo ""

"$PYTHON" - <<'PY'
import sys

if sys.version_info >= (3, 13):
    print(f"Python: {sys.version.split()[0]}")
    print()
    print("PyTorch CUDA wheels on Windows are not available for this Python version.")
    print("Use Python 3.12 for RTX/CUDA training.")
    print()
    print("Create a fresh Windows venv like this:")
    print("  deactivate  # if a venv is active")
    print("  py -3.12 -m venv venv312")
    print("  .\\venv312\\Scripts\\Activate.ps1")
    print("  python -m pip install --upgrade pip")
    print("  python -m pip install -e .")
    print("  python -m pip install -r requirements-groq.txt")
    print("  python -m pip install --index-url https://download.pytorch.org/whl/cu124 torch torchvision torchaudio")
    print("  bash scripts/train.sh")
    sys.exit(1)

try:
    import torch
except Exception as exc:
    raise SystemExit(f"PyTorch is not installed correctly: {exc}")

print("Torch:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
else:
    print()
    print("CUDA is not available in this environment.")
    print("Your current PyTorch build is probably CPU-only.")
    print("Install a CUDA PyTorch build, then run this script again.")
    print()
    print("Example for many Windows/NVIDIA setups:")
    print("  python -m pip uninstall -y torch torchvision torchaudio")
    print("  python -m pip install --index-url https://download.pytorch.org/whl/cu124 torch torchvision torchaudio")
    sys.exit(1)
PY

mkdir -p "$OUTPUT_DIR"

ARGS=(
    --base-model "$BASE_MODEL"
    --output-dir "$OUTPUT_DIR"
    --epochs "$EPOCHS"
    --batch-size "$BATCH_SIZE"
    --grad-accum "$GRAD_ACCUM"
    --learning-rate "$LEARNING_RATE"
    --max-length "$MAX_LENGTH"
    --max-vendor-files "$MAX_VENDOR_FILES"
)

if [[ "$INCLUDE_VENDOR" == "1" || "$INCLUDE_VENDOR" == "true" ]]; then
    ARGS+=(--include-vendor)
fi

"$PYTHON" src/training/finetune_chatbot.py "${ARGS[@]}"

echo ""
echo "Training finished."
echo "Checkpoint saved in: $OUTPUT_DIR"
echo ""
echo "Note: this is a local LoRA adapter checkpoint. Groq remains the default"
echo "runtime unless you add a local-model inference path."
