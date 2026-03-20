#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"
PYTHON_BIN="${PYTHON_BIN:-python3}"
TORCH_INDEX_URL="${TORCH_INDEX_URL:-https://download.pytorch.org/whl/rocm7.1}"
TORCH_VERSION="${TORCH_VERSION:-2.10.0}"

if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  echo "Python interpreter not found: ${PYTHON_BIN}" >&2
  exit 1
fi

if [[ ! -d "${VENV_DIR}" ]]; then
  "${PYTHON_BIN}" -m venv "${VENV_DIR}"
fi

source "${VENV_DIR}/bin/activate"

python -m pip install --upgrade pip setuptools wheel
python -m pip install \
  --index-url "${TORCH_INDEX_URL}" \
  "torch==${TORCH_VERSION}" \
  "torchvision==${TORCH_VERSION}" \
  "torchaudio==${TORCH_VERSION}"

python -m pip install -r "${ROOT_DIR}/requirements.txt"

if [[ -d /usr/share/libdrm ]]; then
  export AMDGPU_ASIC_ID_TABLE_PATHS="/usr/share/libdrm"
fi

python - <<'PY'
import os
import torch

print("Torch:", torch.__version__)
print("HIP:", getattr(torch.version, "hip", None))
print("CUDA visible to torch:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("Device count:", torch.cuda.device_count())
    print("Device 0:", torch.cuda.get_device_name(0))
    try:
        props = torch.cuda.get_device_properties(0)
        print("VRAM GB:", round(props.total_memory / (1024 ** 3), 2))
        gcn = getattr(props, "gcnArchName", None)
        if gcn:
            print("GCN Arch:", gcn)
    except Exception as exc:
        print("Device props unavailable:", exc)
print("AMDGPU_ASIC_ID_TABLE_PATHS:", os.environ.get("AMDGPU_ASIC_ID_TABLE_PATHS"))
PY

echo "ROCm venv ready at: $VENV_DIR"
echo "Activate with: source \"$VENV_DIR/bin/activate\""
