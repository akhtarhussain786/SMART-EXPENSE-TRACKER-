@echo off
title Smart Expense Tracker Web Application
cd /d "%~dp0"
echo ==============================================================
echo    Starting Smart Expense Tracker Web Application...
echo    Opening your web browser at http://127.0.0.1:8000
echo ==============================================================
python run_web.py
pause

