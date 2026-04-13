@echo off
setlocal

REM StreamIQ Stop Script
REM Terminates backend.py and Streamlit dashboard processes

echo ===========================================
echo   Stopping StreamIQ Demo
echo ===========================================

REM Kill Flask backend (backend.py)
taskkill /F /IM python.exe /T >nul 2>&1

REM Kill Streamlit dashboard
taskkill /F /IM streamlit.exe /T >nul 2>&1

echo All StreamIQ processes stopped successfully.
endlocal

