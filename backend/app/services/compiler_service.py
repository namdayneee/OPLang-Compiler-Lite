from __future__ import annotations

from compiler_core import CompilationResult, OPLangCompiler


class CompilerService:
    """Thin application boundary around the compiler facade."""

    def __init__(self, compiler: OPLangCompiler | None = None) -> None:
        self._compiler = compiler or OPLangCompiler()

    def is_available(self) -> bool:
        return self._compiler.is_installed()

    def compile(
        self,
        source: str,
        *,
        include_ast: bool,
        include_jasmin: bool,
    ) -> CompilationResult:
        return self._compiler.compile(
            source,
            include_ast=include_ast,
            include_jasmin=include_jasmin,
        )


compiler_service = CompilerService()


def get_compiler_service() -> CompilerService:
    return compiler_service
