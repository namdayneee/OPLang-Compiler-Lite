from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class CompilerError:
    stage: str
    code: str
    message: str
    line: int | None = None
    column: int | None = None


@dataclass(slots=True)
class CompilationResult:
    success: bool
    stage: str
    ast: Any | None = None
    jasmin_files: dict[str, str] = field(default_factory=dict)
    errors: list[CompilerError] = field(default_factory=list)
    compilation_time_ms: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
