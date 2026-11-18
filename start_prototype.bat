@echo off
title Coastal Climate Risk Intelligence Dashboard - Prototype Launcher
echo ======================================================================
echo  COASTAL CLIMATE RISK INTELLIGENCE DASHBOARD - JUDGE PROTOTYPE
echo ======================================================================
cd /d "%~dp0"
if exist "backend\.venv\Scripts\python.exe" (
    backend\.venv\Scripts\python.exe run_prototype.py
) else (
    python run_prototype.py
)
pause

