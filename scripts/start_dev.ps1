# Start dev server for EcoTrack (PowerShell)
# Usage: powershell -ExecutionPolicy Bypass -File .\scripts\start_dev.ps1

$activate = Join-Path $PSScriptRoot "..\.venv\Scripts\Activate.ps1"
if (Test-Path $activate) {
    Write-Host "Activating virtualenv..."
    & $activate
} else {
    Write-Host "Virtualenv activate script not found at $activate"
    Write-Host "Make sure you created the venv: python -m venv .venv"
}

Write-Host "Starting uvicorn (127.0.0.1:8000)..."
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
