$ErrorActionPreference = "Stop"

if (-not (Test-Path ".venv")) {
  py -3.12 -m venv .venv
}

.\.venv\Scripts\python.exe -m pip install -r requirements.txt

if (Test-Path "src\grammar\OPLang.g4") {
  Write-Host "Compiler source detected. Build ANTLR before starting the API."
}

Write-Host "Start API: .\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload --port 8000"
Write-Host "Start web in another terminal: cd frontend; npm install; npm run dev"
