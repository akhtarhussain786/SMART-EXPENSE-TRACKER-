@echo off
title Smart Expense Tracker - Automated Launcher
cd /d "%~dp0"

echo ======================================================================
echo          SMART EXPENSE TRACKER - WEB APPLICATION
echo              Developed by Disha Prajapati
echo ======================================================================
echo.

:: 1. Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is NOT installed or NOT added to PATH on this laptop!
    echo.
    echo Please follow these 2 simple steps:
    echo 1. Download Python from: https://www.python.org/downloads/
    echo 2. IMPORTANT: During setup, CHECK the box: "Add python.exe to PATH"
    echo.
    echo Press any key to open Python download page in your browser...
    pause >nul
    start https://www.python.org/downloads/
    exit /b 1
)

:: 2. Check if required libraries are installed, auto-install if missing
echo [CHECK] Verifying required libraries...
python -c "import fastapi, uvicorn, reportlab" >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [SETUP] First-time run detected on this laptop!
    echo [SETUP] Installing required packages from requirements.txt...
    echo [SETUP] Please wait 10-20 seconds...
    echo.
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo.
        echo [ERROR] Failed to install packages. Please check your internet connection.
        pause
        exit /b 1
    )
    echo.
    echo [SUCCESS] All libraries installed successfully!
    echo.
)

:: 3. Launch Web Application and Browser
echo [LAUNCH] Starting Web Server...
echo [LAUNCH] Opening your default web browser at http://127.0.0.1:8000
echo.
python run_web.py

if %errorlevel% neq 0 (
    echo.
    echo [INFO] Server stopped.
    pause
)
