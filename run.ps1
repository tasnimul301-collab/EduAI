# EduSmart AI Startup Script
Set-Location $PSScriptRoot

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "       Starting EduSmart AI Web Application            " -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

if (Test-Path ".\venv\Scripts\python.exe") {
    Write-Host "[INFO] Running with virtual environment Python..." -ForegroundColor Green
    & ".\venv\Scripts\python.exe" app.py
} else {
    Write-Host "[INFO] Running with system Python..." -ForegroundColor Green
    python app.py
}
