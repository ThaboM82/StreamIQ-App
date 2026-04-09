@echo off
setlocal enabledelayedexpansion

REM Kill any existing Streamlit processes
echo Checking for running Streamlit servers...
tasklist /FI "IMAGENAME eq python.exe" /V | findstr streamlit >nul
if %errorlevel%==0 (
    echo Found running Streamlit process. Terminating...
    taskkill /F /IM python.exe /T >nul 2>&1
)

REM Starting StreamIQ Dashboard with automatic port selection
set PORT=8507

:CHECK_PORT
netstat -ano | findstr :%PORT% >nul
if %errorlevel%==0 (
    echo Port %PORT% is in use, trying next...
    set /a PORT=%PORT%+1
    goto CHECK_PORT
)

echo Launching StreamIQ Dashboard on port %PORT%...

REM Write to log file
echo [%date% %time%] Launching StreamIQ Dashboard on port %PORT% >> launch_log.txt

REM Auto-open browser
start "" http://localhost:%PORT%

REM Run Streamlit
streamlit run app.py --server.port %PORT%

endlocal
