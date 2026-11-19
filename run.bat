@echo off
title EduSmart AI Server
echo ========================================================
echo        Starting EduSmart AI Web Application
echo ========================================================
echo.
cd /d "%~dp0"

REM Prefer virtual environment Python if available, fallback to system Python
if exist "venv\Scripts\python.exe" (
    echo [INFO] Running with virtual environment Python...
    venv\Scripts\python.exe app.py
) else (
    echo [INFO] Running with system Python...
    python app.py
)

pause
