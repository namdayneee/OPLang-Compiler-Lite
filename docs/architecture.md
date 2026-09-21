# Architecture

OPLang Compiler Lite keeps transport, UI state, and compiler behavior in separate layers:

```text
React UI
  -> frontend compiler API client
  -> FastAPI compile route
  -> compiler service
  -> OPLangCompiler facade
  -> lexer -> parser -> AST -> semantic checker -> Jasmin codegen
```

## Frontend

- `frontend/src/App.tsx` composes the editor, example selector, shortcut, and result panel.
- `frontend/src/features/compiler/useCompiler.ts` owns request state, cancellation, domain results, and network errors.
- `frontend/src/services/compilerApi.ts` is the only module that knows the HTTP endpoint and request contract.
- `frontend/src/types/compiler.ts` defines the public response shape. The response uses `snake_case` to preserve the existing API contract; request options retain the established `includeAst` and `includeJasmin` aliases.
- `frontend/src/data/examples.ts` contains typed, compiler-verified sample programs.

## Backend

- Routes in `backend/app/routes/` validate HTTP concerns such as the 100 KiB source limit and map unavailable/internal failures to safe status codes.
- `backend/app/services/compiler_service.py` is a thin boundary around the compiler facade. FastAPI dependency injection makes failure behavior testable without mocking production routes.
- `backend/app/schemas.py` defines request and response models. Compiler errors remain HTTP 200 domain results; malformed HTTP payloads remain validation errors.

## Compiler core

- `compiler_core/OPLangCompiler` is the only compiler entry point used by the application.
- Each compilation creates a new checker, generator, and temporary output directory. Jasmin text is read before the directory is removed, so requests cannot overwrite one another or leave `Main.j` in the source tree.
- The compiler implementation under `src/` has no dependency on FastAPI or React.

The dependency direction is one-way. The compiler core does not import application layers, routes do not orchestrate individual compiler passes, and React components do not call `fetch` directly.
