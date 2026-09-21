from __future__ import annotations

import os


MAX_SOURCE_BYTES = int(os.getenv("OPLANG_MAX_SOURCE_BYTES", "102400"))
COMPILE_TIMEOUT_SECONDS = float(os.getenv("OPLANG_COMPILE_TIMEOUT_SECONDS", "5"))
ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("OPLANG_ALLOWED_ORIGINS", "http://localhost:5173").split(",")
    if origin.strip()
]
