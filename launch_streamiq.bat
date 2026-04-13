@echo off
setlocal

REM StreamIQ Demo Launcher
REM Starts backend.py and dashboard, with optional cleanup

set BACKEND_URL=http://127.0.0.1:8000

echo ===========================================
echo   StreamIQ Demo Launcher
echo ===========================================
echo.
echo Options:
echo   1. Start demo normally
echo   2. Clear logs + history, then start demo
echo.

set /p choice="Enter choice (1 or 2): "

if "%choice%"=="2" (
    echo Clearing backend logs...
    curl -X DELETE %BACKEND_URL%/logs
    echo Clearing backend history...
    curl -X DELETE %BACKEND_URL%/history
    echo Cleanup complete.
)

echo Starting backend...
start cmd /c "python src\backend\backend.py"

timeout /t 3 >nul

echo Starting dashboard...
start cmd /c "streamlit run src\dashboards\app.py --server.port 8501"

echo Demo launched successfully 🚀
endlocal
