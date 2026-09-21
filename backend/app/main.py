from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routes.compile import router as compile_router
from backend.app.routes.health import router as health_router
from backend.app.settings import ALLOWED_ORIGINS

app = FastAPI(
    title="OPLang Compiler API",
    description="Compile OPLang source into AST and Jasmin.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api/v1")
app.include_router(compile_router, prefix="/api/v1")


@app.get("/")
def root() -> dict:
    return {"name": "OPLang Compiler API", "docs": "/docs"}
