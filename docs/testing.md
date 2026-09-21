# Testing

Run commands from `D:\Project\OPLang-Compiler-Lite` unless a section says otherwise.

## Python environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If the environment has not been created yet:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Use the virtualenv interpreter explicitly when another Python installation is first on `PATH`.

## Compiler regression tests

```powershell
.\.venv\Scripts\python.exe -m pytest `
  tests/test_lexer.py `
  tests/test_parser.py `
  tests/test_ast_gen.py `
  tests/test_checker.py `
  tests/test_compiler_core.py `
  tests/test_examples.py `
  -q
```

## API tests

```powershell
.\.venv\Scripts\python.exe -m pytest backend/tests -q
```

## Frontend build

```powershell
cd frontend
npm install
npm run build
```

The frontend currently has no separate lint or browser-test script. `npm run build` performs strict TypeScript project checking before the Vite production build.

## Compile-only scope

Version 1 generates Jasmin text but does not assemble or execute it. `tests/test_codegen.py` belongs to the older JVM execution suite and is intentionally excluded from the v1 compile-only checkpoint because it invokes external Jasmin/Java runtime behavior. Facade tests verify generated `.j` files as text instead.

## Manual browser check

Start the backend:

```powershell
cd D:\Project\OPLang-Compiler-Lite
.\.venv\Scripts\Activate.ps1
uvicorn backend.app.main:app --reload --port 8000
```

Open `http://localhost:8000/api/v1/health` and `http://localhost:8000/docs`. Health should report `healthy` and `compilerCoreInstalled: true`.

In a second terminal:

```powershell
cd D:\Project\OPLang-Compiler-Lite\frontend
npm run dev
```

Open the URL printed by Vite, normally `http://localhost:5173`, then verify Hello World, Syntax Error, Semantic Error, Ctrl/Cmd+Enter, source persistence after reload, and a clear network error after stopping the backend.

## Common problems

- `ModuleNotFoundError: fastapi`: use `.venv\Scripts\python.exe -m pytest` rather than a different global Python.
- `compilerCoreInstalled: false`: generate the ANTLR files under `build/` and confirm all `src/` compiler modules are present.
- Browser network error while the backend is running: set `VITE_API_URL` to the backend origin and restart Vite.
- Vite cannot spawn esbuild in a restricted shell: run the build from a terminal that permits child processes.
