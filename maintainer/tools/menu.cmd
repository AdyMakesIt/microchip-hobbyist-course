@echo off
setlocal
set "SCRIPT=%~dp0menu.py"

where python >nul 2>&1
if %errorlevel%==0 (
    python "%SCRIPT%" %*
    exit /b %errorlevel%
)

where python3 >nul 2>&1
if %errorlevel%==0 (
    python3 "%SCRIPT%" %*
    exit /b %errorlevel%
)

echo ERROR: Python was not found on PATH. 1>&2
exit /b 1
