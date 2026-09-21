from __future__ import annotations

import importlib.util
import time
from pathlib import Path

from .exceptions import CompilerCoreNotInstalled
from .result import CompilationResult, CompilerError


class OPLangCompiler:
    """Stable application-facing facade for the compiler pipeline.

    Phase 1 keeps this interface stable while the coursework compiler is migrated
    into this repository. The web/API layer should never import lexer/parser/
    checker/codegen classes directly.
    """

    def __init__(self, project_root: Path | None = None) -> None:
        self.project_root = project_root or Path(__file__).resolve().parents[1]

    def is_installed(self) -> bool:
        required = [
            self.project_root / "src" / "grammar" / "OPLang.g4",
            self.project_root / "src" / "astgen" / "ast_generation.py",
            self.project_root / "src" / "semantics" / "static_checker.py",
            self.project_root / "src" / "codegen" / "codegen.py",
        ]
        return all(path.exists() for path in required) and importlib.util.find_spec("build.OPLangParser") is not None

    def compile(self, source: str, *, include_ast: bool = True, include_jasmin: bool = True) -> CompilationResult:
        started = time.perf_counter()
        if not self.is_installed():
            raise CompilerCoreNotInstalled(
                "Compiler implementation has not been migrated yet. Follow docs/02-MIGRATE-COMPILER.md."
            )

        # Implemented in Phase 2 after the original compiler source is copied into
        # this independent repository. Keeping this explicit prevents a hidden
        # runtime dependency on the old BTL-PPL repository.
        elapsed = (time.perf_counter() - started) * 1000
        return CompilationResult(
            success=False,
            stage="bootstrap",
            errors=[CompilerError("bootstrap", "NOT_IMPLEMENTED", "Compiler facade migration is not complete")],
            compilation_time_ms=elapsed,
        )
