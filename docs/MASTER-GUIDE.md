# OPLang Compiler Lite — Master Implementation Guide

This guide turns the OPLang coursework compiler into a standalone portfolio product without modifying or depending on the old repository at runtime.

## 0. Final product

The v1 product is intentionally small:

```text
Browser
  ↓
React + TypeScript + Monaco Editor
  ↓ HTTPS JSON
FastAPI Compiler API
  ↓
OPLangCompiler facade
  ↓
Lexer → Parser → AST → Static Checker → Jasmin Generator
  ↓
JSON: success/errors + AST + Jasmin + timing
```

Do **not** add login, PostgreSQL, Redis, cloud storage, queues, payments, online judge, AI repair, or arbitrary program execution in v1.

The frontend stores the current editor content in `localStorage`, so no persistent backend storage is required.

---

# PHASE 1 — Create the independent repository

## Step 1.1 — Create the GitHub repository

Create a new public repository named:

```text
oplang-compiler-lite
```

Recommended settings:

- Public repository.
- Do not initialize with a second README if you are pushing this starter.
- Do not add a paid GitHub feature.
- Keep the old `BTL-PPL` repository untouched.

Then, from the extracted starter directory:

```bash
git init -b main
git add .
git commit -m "chore: bootstrap OPLang Compiler Lite"
git remote add origin https://github.com/<your-username>/oplang-compiler-lite.git
git push -u origin main
```

After this push, the project has its own history and is independent.

## Step 1.2 — Development branch

```bash
git checkout -b develop
```

Use feature branches from `develop`, for example:

```bash
git checkout -b feat/compiler-core
```

For a solo student project, a simpler `feature branch → main PR` flow is also acceptable.

---

# PHASE 2 — Migrate the compiler implementation once

The old project is a source of code, not a runtime dependency. Do not use a Git submodule, package URL, symlink, network fetch at startup, or import from another checkout.

## Step 2.1 — Copy only the compiler implementation

Copy these directories into the new repository root:

```text
src/grammar/
src/astgen/
src/semantics/
src/codegen/
src/utils/
src/runtime/io.java
```

Also copy the language documents if you want the new repository to be self-contained:

```text
oplang_specification.md
oplang-semantic_constraints_and_errors.md
```

Do not copy generated or environment-specific files:

```text
build/
venv/
reports/
__pycache__/
.DS_Store
src/runtime/Main.j
src/runtime/Main.class
```

You do not need to commit `antlr-4.13.2-complete.jar`; `scripts/build_antlr.sh` downloads it during build.

For Compile-only v1, `jasmin.jar` and `io.class` are not required to return Jasmin text. Keep `io.java` for the later Run milestone and documentation.

## Step 2.2 — Preserve imports first

The existing compiler uses imports such as:

```python
from src.utils.nodes import *
from build.OPLangParser import OPLangParser
```

Do not reorganize all packages during migration. First make the copied compiler pass locally with the same `src/` and `build/` locations. Refactor packages only after tests are green.

## Step 2.3 — Build ANTLR

On macOS/Linux/WSL:

```bash
bash scripts/build_antlr.sh
```

On Windows, either use Git Bash/WSL or run the equivalent commands:

```powershell
New-Item -ItemType Directory -Force build
curl.exe -L https://www.antlr.org/download/antlr-4.13.2-complete.jar -o $env:TEMP\antlr.jar
java -jar $env:TEMP\antlr.jar -Dlanguage=Python3 -visitor -no-listener -o build src/grammar/OPLang.g4
New-Item -ItemType File -Force build\__init__.py
Copy-Item src\grammar\lexererr.py build\lexererr.py
```

Check:

```text
build/OPLangLexer.py
build/OPLangParser.py
build/OPLangVisitor.py
```

---

# PHASE 3 — Make code generation request-safe

This is the most important refactor before exposing the compiler as a web service.

The coursework implementation writes generated `.j` files to a shared runtime directory. That can cause two HTTP requests to overwrite each other's files.

## Step 3.1 — Make Emitter accept an output directory

Change the `Emitter` constructor conceptually from:

```python
Emitter(filename)
```

to:

```python
Emitter(filename, output_dir=None)
```

When `output_dir` is absent, keep the historical runtime directory for backward compatibility. When it is supplied, write there.

Target behavior:

```python
class Emitter:
    def __init__(self, filename: str, output_dir: str | None = None):
        self.filename = filename
        if output_dir is None:
            output_dir = default_runtime_dir
        self.filepath = os.path.join(output_dir, filename)
        self.buff = []
        self.jvm = JasminCode()
```

## Step 3.2 — Pass output directory through CodeGenerator

Add:

```python
CodeGenerator(output_dir=...)
```

and when creating an emitter:

```python
self.emit = Emitter(class_file, output_dir=self.output_dir)
```

## Step 3.3 — Each compile uses its own temporary workspace

Use:

```python
from tempfile import TemporaryDirectory

with TemporaryDirectory(prefix="oplang-") as workdir:
    generator = CodeGenerator(output_dir=workdir)
    generator.visit(ast)
```

Read every generated `.j` file into memory before leaving the context:

```python
jasmin_files = {
    path.name: path.read_text(encoding="utf-8")
    for path in Path(workdir).glob("*.j")
}
```

After the request finishes, the directory disappears automatically.

Benefits:

- no database;
- no object storage;
- no cleanup cron;
- no collision between users;
- no generated artifacts committed to Git.

---

# PHASE 4 — Implement `OPLangCompiler.compile()`

Only this layer should know the complete compiler pipeline.

## Step 4.1 — Pipeline

```text
source string
↓
InputStream
↓
OPLangLexer
↓
CommonTokenStream
↓
OPLangParser.program()
↓
ASTGeneration
↓
StaticChecker.check_program(ast)
↓
CodeGenerator(output_dir=tempdir)
↓
read *.j
↓
CompilationResult
```

## Step 4.2 — Error stages

Normalize every failure to one of:

```text
lexer
parser
ast
semantic
codegen
internal
```

Do not expose Python tracebacks to the browser.

Recommended error shape:

```json
{
  "stage": "parser",
  "code": "SYNTAX_ERROR",
  "message": "Unexpected token ...",
  "line": 4,
  "column": 12
}
```

Map the existing lexer exceptions separately:

```text
ErrorToken      → ERROR_TOKEN
UncloseString   → UNCLOSED_STRING
IllegalEscape   → ILLEGAL_ESCAPE
```

Map semantic exception class names to stable API codes, for example:

```text
UndeclaredIdentifier      → UNDECLARED_IDENTIFIER
Redeclared                → REDECLARED
TypeMismatchInStatement   → TYPE_MISMATCH_STATEMENT
NoEntryPoint              → NO_ENTRY_POINT
```

## Step 4.3 — AST JSON

Do not make the frontend depend on Python `__str__` formatting long term. Use `compiler_core/serializer.py` to convert node attributes recursively into JSON-compatible values.

AST response example:

```json
{
  "type": "Program",
  "class_decls": [
    {
      "type": "ClassDecl",
      "name": "Main"
    }
  ]
}
```

---

# PHASE 5 — Backend API

The starter already contains FastAPI scaffolding.

## Step 5.1 — Local environment

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

macOS/Linux:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Step 5.2 — Run API

```bash
uvicorn backend.app.main:app --reload --port 8000
```

Open:

```text
http://localhost:8000/docs
http://localhost:8000/api/v1/health
```

## Step 5.3 — API contract

Health:

```http
GET /api/v1/health
```

Compile:

```http
POST /api/v1/compile
Content-Type: application/json
```

Request:

```json
{
  "source": "class Main { ... }",
  "options": {
    "includeAst": true,
    "includeJasmin": true
  }
}
```

Keep source input as text only in v1. Do not accept arbitrary file paths or shell commands.

## Step 5.4 — Limits

Start with:

```text
source size:        100 KiB
compile timeout:    5 seconds target
error count:        max 100
response target:    <= 1 MiB
```

A timeout implemented only with a Python thread does not safely stop CPU-bound work. For v1 Compile-only, keep the grammar/compiler bounded and measure durations. Before Run or hostile public traffic, move compilation into an isolated worker/process with a hard timeout.

---

# PHASE 6 — Frontend

The starter contains React + TypeScript + Monaco.

## Step 6.1 — Install

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```

## Step 6.2 — Environment

Create `frontend/.env.local`:

```env
VITE_API_URL=http://localhost:8000
```

Production will point to the Render API URL.

## Step 6.3 — UI v1

Keep the UI focused:

```text
Header: OPLang Compiler Lite + Compile button

Left:
  Monaco source editor

Right tabs:
  Summary
  Errors
  AST
  Jasmin
```

Add later:

- example selector;
- copy Jasmin;
- download `.j` file;
- dark/light mode;
- resizable panes;
- AST tree visualization;
- Ctrl+Enter compile shortcut.

## Step 6.4 — Browser persistence

Use only:

```javascript
localStorage.setItem("oplang-source", source)
```

No database is needed for v1.

---

# PHASE 7 — Examples

Add verified examples only after the migrated compiler accepts them.

Recommended set:

```text
hello.opl
variables.opl
arithmetic.opl
if_else.opl
for_loop.opl
arrays.opl
classes.opl
inheritance.opl
syntax_error.opl
semantic_error.opl
```

Every example should have a corresponding automated test so the website never ships a broken demo example.

---

# PHASE 8 — Testing strategy

Do not chase a test count for its own sake. Test layers.

## Layer A — coursework compiler tests

Copy and keep useful lexer/parser/AST/checker/codegen tests from the source project. They now belong to the new repository and evolve independently.

## Layer B — compiler facade tests

Add:

```text
valid compilation
lexer failure
parser failure
semantic failure
multiple classes
Jasmin files returned
workspace cleanup
same class name compiled concurrently
large source rejection
```

## Layer C — API tests

Add:

```text
GET /health
POST /compile valid
POST /compile invalid
empty source
100 KiB boundary
101 KiB rejection
API never returns traceback
```

## Layer D — frontend tests (later)

Focus on interaction, not snapshots:

```text
compile button sends source
error response renders
AST tab renders JSON
Jasmin tab renders generated files
localStorage restores source
```

## Critical concurrency test

Run several compilations in parallel using the same class name. Each request must receive its own generated Jasmin with no cross-request data.

---

# PHASE 9 — Docker

## Step 9.1 — Build

```bash
docker build -t oplang-compiler-api .
```

## Step 9.2 — Run

```bash
docker run --rm -p 8000:10000 \
  -e OPLANG_ALLOWED_ORIGINS=http://localhost:5173 \
  oplang-compiler-api
```

Then open:

```text
http://localhost:8000/docs
```

## Step 9.3 — Full local stack

```bash
docker compose up --build
```

Expected:

```text
Frontend  http://localhost:5173
API       http://localhost:8000
Swagger   http://localhost:8000/docs
```

---

# PHASE 10 — GitHub Actions CI

The starter has `.github/workflows/ci.yml`.

Target pipeline:

```text
push / pull request
│
├─ backend tests
├─ compiler tests
├─ frontend TypeScript build
└─ Docker build
```

After compiler migration, extend the backend job:

```yaml
- name: Install Java
  run: sudo apt-get update && sudo apt-get install -y default-jdk
- name: Generate ANTLR
  run: bash scripts/build_antlr.sh
- name: Test compiler
  run: pytest tests -q
```

Do not deploy a commit with red CI.

---

# PHASE 11 — Zero-cost deployment

## Frontend — Cloudflare Pages

Use the public GitHub repository.

Settings:

```text
Framework preset: Vite
Root directory: frontend
Build command: npm run build
Build output: dist
```

Environment variable:

```text
VITE_API_URL=https://<your-api>.onrender.com
```

Use the generated `*.pages.dev` hostname. Do not buy a domain for v1.

## Backend — Render Free

Create a Web Service from the same repository:

```text
Runtime: Docker
Plan: Free
Health Check: /api/v1/health
```

Set:

```text
OPLANG_ALLOWED_ORIGINS=https://<your-pages-project>.pages.dev
OPLANG_MAX_SOURCE_BYTES=102400
```

For a strict zero-cash portfolio setup, do not add a payment method. If the free service reaches relevant included limits that would otherwise create charges, Render suspends/disables the free services/builds instead of charging an absent payment method.

Render Free services spin down after 15 minutes without inbound traffic and can take about one minute to wake. Make the frontend display a friendly “Starting compiler service…” state for slow first requests.

## Why no database

The compiler is stateless:

```text
request source
→ compile in temp directory
→ return result
→ delete temp directory
```

Persistent storage required: 0 GB.

---

# PHASE 12 — Security boundary

Compile-only is materially safer than Run, but still treat input as untrusted.

Required controls:

```text
request size limit
CORS allowlist
no arbitrary path input
no shell command input
no user-selected output directory
unique temp directory per request
cleanup after request
no secrets in error responses
no Python traceback returned to client
bounded response size
```

Do not use `eval`, `exec`, or `shell=True` on user source.

## Do not implement Run in v1

Executing generated bytecode changes the threat model. Before adding Run, require:

```text
separate execution worker/process
hard wall-clock timeout
memory limit
process limit
output limit
non-root execution
read-only base filesystem where possible
no Docker socket
no cloud credentials/secrets
no unrestricted network
fresh temp workspace
cleanup after execution
low concurrency
```

Do not run arbitrary user programs inside the FastAPI process.

---

# PHASE 13 — Suggested milestones

## v0.1 — Repository bootstrap

- new independent repository;
- docs;
- FastAPI health endpoint;
- React editor shell;
- Docker/CI skeleton.

## v0.2 — Compiler migration

- compiler source copied into new repo;
- ANTLR build works;
- legacy tests pass.

## v0.3 — Compiler facade

- `OPLangCompiler.compile(source)` works;
- normalized errors;
- AST JSON;
- Jasmin returned from temp workspace.

## v0.4 — API

- `/compile` wired to real compiler;
- limits;
- API tests.

## v0.5 — Web UI

- Monaco;
- summary/errors/AST/Jasmin;
- examples;
- localStorage;
- loading and cold-start states.

## v0.6 — DevOps

- Docker;
- compose;
- CI;
- branch protection if desired.

## v1.0 — Public portfolio release

- Render API;
- Cloudflare Pages frontend;
- screenshots;
- architecture diagram;
- demo video;
- clean README;
- release tag `v1.0.0`.

## v1.1+ — Optional expansions

- Run worker with sandbox;
- CLI package;
- VS Code extension;
- shareable snippets without accounts;
- custom Monaco syntax highlighting;
- compiler diagnostics inline in editor;
- visualization of compiler stages;
- performance metrics.

---

# PHASE 14 — Professional Git workflow

Example commit sequence:

```text
chore: bootstrap project structure
chore: migrate OPLang compiler sources
test: restore compiler regression suite
refactor: isolate codegen output directory
feat: add compiler facade
feat: normalize compiler diagnostics
feat: add compile API
feat: add Monaco editor
feat: add AST and Jasmin result tabs
chore: add Docker development stack
ci: add compiler backend frontend checks
docs: add deployment and architecture guide
```

Use PRs even when working alone if you want the repository history to demonstrate professional workflow.

---

# PHASE 15 — Definition of done for v1.0

Compiler:

- [ ] lexer works;
- [ ] parser works;
- [ ] AST generation works;
- [ ] semantic checking works;
- [ ] Jasmin generation works;
- [ ] temporary workspace is isolated;
- [ ] no runtime dependency on old repository.

API:

- [ ] `/health`;
- [ ] `/compile`;
- [ ] structured errors;
- [ ] source size limit;
- [ ] no traceback leakage;
- [ ] OpenAPI docs.

Frontend:

- [ ] Monaco editor;
- [ ] Compile button;
- [ ] loading state;
- [ ] error panel;
- [ ] AST panel;
- [ ] Jasmin panel;
- [ ] examples;
- [ ] localStorage;
- [ ] responsive layout.

Engineering:

- [ ] compiler tests;
- [ ] core integration tests;
- [ ] API tests;
- [ ] CI green;
- [ ] Docker build green;
- [ ] README explains architecture;
- [ ] public demo works.

Deployment:

- [ ] public GitHub repository;
- [ ] Cloudflare Pages Free;
- [ ] Render Free;
- [ ] no database;
- [ ] no paid domain;
- [ ] no payment method on Render if strict zero-cash protection is desired.

---

# PHASE 16 — What to learn from each stage

This project is valuable because each milestone maps to a real engineering topic:

```text
Grammar       → formal languages, lexical/syntax analysis
AST           → compiler IR and tree transformations
Static check  → type systems, symbol tables, scopes
Jasmin/JVM    → bytecode, stack machine, code generation
Facade        → software architecture, dependency boundaries
FastAPI       → HTTP, REST, serialization, validation
React         → frontend state and API integration
Monaco        → editor integration
Temp workspace→ concurrency and filesystem isolation
Docker        → reproducible runtime environments
CI            → automated quality gates
Render        → backend cloud deployment
Cloudflare    → CDN/static deployment
Security      → untrusted input and code-execution boundaries
```

The v1 goal is not “make another school assignment.” The goal is to demonstrate that you can take a compiler implementation and engineer it into a deployable software product.
