from __future__ import annotations

from dataclasses import is_dataclass, asdict
from typing import Any


def serialize_ast(value: Any) -> Any:
    """Best-effort AST -> JSON-compatible object without coupling the API to node classes."""
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, list):
        return [serialize_ast(item) for item in value]
    if isinstance(value, tuple):
        return [serialize_ast(item) for item in value]
    if isinstance(value, dict):
        return {str(k): serialize_ast(v) for k, v in value.items()}
    if is_dataclass(value):
        return serialize_ast(asdict(value))
    if hasattr(value, "__dict__"):
        payload = {"type": value.__class__.__name__}
        for key, item in vars(value).items():
            if not key.startswith("_"):
                payload[key] = serialize_ast(item)
        return payload
    return str(value)
