from typing import Annotated

from fastapi import APIRouter, Depends

from backend.app.schemas import HealthResponse
from backend.app.services.compiler_service import CompilerService, get_compiler_service

router = APIRouter(tags=["system"])


@router.get("/health", response_model=HealthResponse)
def health(
    service: Annotated[CompilerService, Depends(get_compiler_service)],
) -> HealthResponse:
    return HealthResponse(
        status="healthy",
        compilerVersion="0.1.0",
        compilerCoreInstalled=service.is_available(),
    )
