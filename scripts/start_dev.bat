@echo off
REM start_dev.bat - start uvicorn in a Windows cmd shell
if exist .venv\Scripts\activate.bat (
  call .venv\Scripts\activate.bat
) else (
  echo virtualenv activation not found at .venv\Scripts\activate.bat
)
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
pause
