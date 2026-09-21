from __future__ import annotations

from pydantic import BaseModel, Field


class CompileOptions(BaseModel):
    include_ast: bool = Field(default=True, alias="includeAst")
    include_jasmin: bool = Field(default=True, alias="includeJasmin")

    model_config = {"populate_by_name": True}


class CompileRequest(BaseModel):
    source: str
    options: CompileOptions = CompileOptions()
