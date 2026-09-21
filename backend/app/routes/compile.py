from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from compiler_core.exceptions import CompilerCoreNotInstalled
from backend.app.schemas import CompilationResponse, CompileRequest
from backend.app.services.compiler_service import CompilerService, get_compiler_service
from backend.app.settings import MAX_SOURCE_BYTES

router = APIRouter(tags=["compiler"])


@router.post("/compile", response_model=CompilationResponse)
def compile_source(
    payload: CompileRequest,
    service: Annotated[CompilerService, Depends(get_compiler_service)],
) -> CompilationResponse:
    source_bytes = len(payload.source.encode("utf-8"))
    if source_bytes > MAX_SOURCE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"Source is too large ({source_bytes} bytes). Limit: {MAX_SOURCE_BYTES} bytes.",
        )

    try:
        result = service.compile(
            payload.source,
            include_ast=payload.options.include_ast,
            include_jasmin=payload.options.include_jasmin,
        )
    except CompilerCoreNotInstalled as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail={
                "code": "INTERNAL_COMPILER_ERROR",
                "message": "Compilation failed unexpectedly.",
            },
        ) from exc

    return CompilationResponse.model_validate(result.to_dict())
