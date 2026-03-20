#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"

if [[ ! -d "${VENV_DIR}" ]]; then
  echo "Missing virtual environment at $VENV_DIR. Run ./setup_rocm_venv.sh first." >&2
  exit 1
fi

source "${VENV_DIR}/bin/activate"

export HSA_OVERRIDE_GFX_VERSION="${HSA_OVERRIDE_GFX_VERSION:-10.3.0}"
if [[ -d /usr/share/libdrm ]]; then
  export AMDGPU_ASIC_ID_TABLE_PATHS="${AMDGPU_ASIC_ID_TABLE_PATHS:-/usr/share/libdrm}"
fi
export OMNILOTTIE_DEVICE="${OMNILOTTIE_DEVICE:-auto}"
export OMNILOTTIE_DTYPE="${OMNILOTTIE_DTYPE:-float16}"
export MODEL_PATH="${MODEL_PATH:-$ROOT_DIR}"
export PROCESSOR_PATH="${PROCESSOR_PATH:-Qwen/Qwen2.5-VL-3B-Instruct}"

exec python app_hf.py "$@"
