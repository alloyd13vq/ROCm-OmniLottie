from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Optional

if os.path.isdir("/usr/share/libdrm"):
    os.environ.setdefault("AMDGPU_ASIC_ID_TABLE_PATHS", "/usr/share/libdrm")

import torch


_DTYPE_MAP = {
    "float16": torch.float16,
    "fp16": torch.float16,
    "half": torch.float16,
    "bfloat16": torch.bfloat16,
    "bf16": torch.bfloat16,
    "float32": torch.float32,
    "fp32": torch.float32,
}


@dataclass(frozen=True)
class TorchRuntime:
    device: torch.device
    torch_dtype: torch.dtype
    accelerator: str


def is_rocm_build() -> bool:
    return bool(getattr(torch.version, "hip", None))


def parse_torch_dtype(value: Optional[object]) -> Optional[torch.dtype]:
    if value is None or isinstance(value, torch.dtype):
        return value

    normalized = str(value).strip().lower()
    if normalized in {"", "auto"}:
        return None
    if normalized not in _DTYPE_MAP:
        valid = ", ".join(sorted(_DTYPE_MAP))
        raise ValueError(f"Unsupported torch dtype '{value}'. Expected one of: auto, {valid}")
    return _DTYPE_MAP[normalized]


def dtype_to_name(dtype: torch.dtype) -> str:
    for name, mapped in _DTYPE_MAP.items():
        if mapped == dtype and len(name) > 2:
            return name
    return str(dtype).replace("torch.", "")


def select_device(requested: Optional[str] = "auto") -> torch.device:
    normalized = (requested or "auto").strip().lower()
    if normalized != "auto":
        return torch.device(requested)

    if torch.cuda.is_available():
        return torch.device("cuda:0")
    if hasattr(torch, "xpu") and torch.xpu.is_available():
        return torch.device("xpu:0")
    return torch.device("cpu")


def supports_bfloat16(device: torch.device) -> bool:
    if device.type == "cuda":
        checker = getattr(torch.cuda, "is_bf16_supported", None)
        if callable(checker):
            try:
                return bool(checker())
            except Exception:
                return False
    if device.type == "xpu":
        checker = getattr(torch.xpu, "is_bf16_supported", None)
        if callable(checker):
            try:
                return bool(checker())
            except Exception:
                return False
    return False


def select_torch_dtype(device: torch.device, requested: Optional[object] = "auto") -> torch.dtype:
    parsed = parse_torch_dtype(requested)
    if parsed is not None:
        return parsed

    if device.type == "cpu":
        return torch.float32

    if is_rocm_build() and device.type == "cuda":
        return torch.float16

    if supports_bfloat16(device):
        return torch.bfloat16
    return torch.float16


def accelerator_name(device: torch.device) -> str:
    if device.type == "cuda":
        return "rocm" if is_rocm_build() else "cuda"
    return device.type


def get_runtime(requested_device: Optional[str] = "auto", requested_dtype: Optional[object] = "auto") -> TorchRuntime:
    device = select_device(requested_device)
    return TorchRuntime(
        device=device,
        torch_dtype=select_torch_dtype(device, requested_dtype),
        accelerator=accelerator_name(device),
    )


def clear_device_cache(device: torch.device) -> None:
    if device.type == "cuda" and torch.cuda.is_available():
        torch.cuda.empty_cache()
        return
    if device.type == "xpu" and hasattr(torch, "xpu") and torch.xpu.is_available():
        torch.xpu.empty_cache()


def runtime_summary(runtime: TorchRuntime) -> str:
    return (
        f"device={runtime.device}, accelerator={runtime.accelerator}, "
        f"dtype={dtype_to_name(runtime.torch_dtype)}"
    )
