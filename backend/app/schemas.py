from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class CompileOptions(BaseModel):
    include_ast: bool = Field(default=True, alias="includeAst")
    include_jasmin: bool = Field(default=True, alias="includeJasmin")

    model_config = ConfigDict(populate_by_name=True)


class CompileRequest(BaseModel):
    source: str
    options: CompileOptions = Field(default_factory=CompileOptions)


class CompilerErrorResponse(BaseModel):
    stage: str
    code: str
    message: str
    line: int | None = None
    column: int | None = None


class CompilationResponse(BaseModel):
    success: bool
    stage: str
    ast: Any | None = None
    jasmin_files: dict[str, str] = Field(default_factory=dict)
    errors: list[CompilerErrorResponse] = Field(default_factory=list)
    compilation_time_ms: float


class HealthResponse(BaseModel):
    status: str
    compilerVersion: str
    compilerCoreInstalled: bool
