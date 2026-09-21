from fastapi import APIRouter, HTTPException

from compiler_core import OPLangCompiler
from compiler_core.exceptions import CompilerCoreNotInstalled
from backend.app.schemas import CompileRequest
from backend.app.settings import MAX_SOURCE_BYTES

router = APIRouter(tags=["compiler"])
compiler = OPLangCompiler()


@router.post("/compile")
def compile_source(payload: CompileRequest) -> dict:
    source_bytes = len(payload.source.encode("utf-8"))
    if source_bytes > MAX_SOURCE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"Source is too large ({source_bytes} bytes). Limit: {MAX_SOURCE_BYTES} bytes.",
        )

    try:
        result = compiler.compile(
            payload.source,
            include_ast=payload.options.include_ast,
            include_jasmin=payload.options.include_jasmin,
        )
    except CompilerCoreNotInstalled as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return result.to_dict()
