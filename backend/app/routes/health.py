from fastapi import APIRouter

from compiler_core import OPLangCompiler

router = APIRouter(tags=["system"])
compiler = OPLangCompiler()


@router.get("/health")
def health() -> dict:
    return {
        "status": "healthy",
        "compilerVersion": "0.1.0",
        "compilerCoreInstalled": compiler.is_installed(),
    }
