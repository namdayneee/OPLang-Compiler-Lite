# OPLang Compiler Lite

A standalone, cloud-hosted educational compiler product for OPLang.

> Goal: turn a compiler pipeline into a real web application while keeping the first public version stateless and deployable at 0 VND/month on free tiers.

## Product scope — v1

```text
OPLang source
    ↓
Lexer
    ↓
Parser
    ↓
AST Generation
    ↓
Static Semantic Analysis
    ↓
Jasmin Generation
    ↓
Web result: Errors | AST | Jasmin
```

The first release intentionally **does not execute user programs**. Runtime execution is a later security milestone.

## Architecture

```text
Cloudflare Pages
React + TypeScript + Monaco
        │
        │ HTTPS / JSON
        ▼
Render Free
FastAPI Compiler API
        │
        ▼
OPLangCompiler facade
        │
        ├─ Lexer / Parser
        ├─ AST Generation
        ├─ Static Checker
        └─ Jasmin Generator
             │
             ▼
       per-request temp dir
```

No database, Redis, object storage, account system, or paid domain is required for v1.

## Repository layout

```text
oplang-compiler-lite/
├── backend/                 FastAPI HTTP layer
├── compiler_core/           stable application-facing compiler facade
├── frontend/                React + TypeScript + Monaco
├── examples/                verified OPLang examples
├── docs/                    implementation/deployment guides
├── scripts/                 local/build scripts
├── .github/workflows/       CI
├── Dockerfile
├── compose.yaml
├── render.yaml
└── requirements.txt
```

After the compiler migration phase, the repository also contains the independent compiler implementation under `src/` and generated ANTLR modules under ignored `build/`.

## Current starter status

This starter intentionally separates platform bootstrap from compiler migration.

Already scaffolded:

- FastAPI app and health endpoint;
- compile API contract and request-size guard;
- `OPLangCompiler` facade boundary;
- React/Vite/TypeScript frontend;
- Monaco editor;
- result tabs;
- browser `localStorage` persistence;
- Docker/Compose;
- Render blueprint;
- GitHub Actions CI skeleton;
- zero-cost and security documentation.

Next required milestone:

1. copy the compiler implementation into this repository once;
2. build ANTLR;
3. restore compiler tests;
4. make code generation use a per-request output directory;
5. implement the real `OPLangCompiler.compile()` pipeline.

See **[docs/MASTER-GUIDE.md](docs/MASTER-GUIDE.md)**.

## Local API quick start

```bash
python -m venv .venv
# activate the venv
pip install -r requirements.txt
uvicorn backend.app.main:app --reload --port 8000
```

Open:

```text
http://localhost:8000/docs
http://localhost:8000/api/v1/health
```

Before compiler migration, `/health` works and reports `compilerCoreInstalled: false`; `/compile` intentionally returns a bootstrap error rather than silently depending on another repository.

## Local frontend quick start

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

For local API integration create `frontend/.env.local`:

```env
VITE_API_URL=http://localhost:8000
```

## Full local stack

```bash
docker compose up --build
```

Expected URLs:

```text
Frontend  http://localhost:5173
API       http://localhost:8000
Swagger   http://localhost:8000/docs
```

## Zero-cost target

- GitHub public repository + standard Actions runners: 0 VND.
- Cloudflare Pages Free frontend: 0 VND.
- Render Free backend: 0 VND if kept on Free and no payment method is attached for strict no-charge protection.
- Database/storage: not used.
- Domain: generated `pages.dev` and `onrender.com` hostnames.

Free-tier policies can change; verify provider limits before release. See `docs/ZERO-COST.md`.

## Security boundary

v1 compiles only. It does **not** run arbitrary user bytecode.

Required before a future Run feature:

- separate worker/process;
- hard timeout;
- RAM/process/output limits;
- no secrets;
- no Docker socket;
- restricted network;
- non-root execution;
- ephemeral workspace.

## Documentation

- `docs/MASTER-GUIDE.md` — complete end-to-end implementation plan.
- `docs/02-MIGRATE-COMPILER.md` — one-time compiler migration checklist.
- `docs/ZERO-COST.md` — free-tier guardrails.

## Portfolio release checklist

A `v1.0.0` release should include a live demo, API docs, screenshots, architecture diagram, CI badge, verified examples, a short demo video, and a clear explanation of compiler stages and security boundaries.
