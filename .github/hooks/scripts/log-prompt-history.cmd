@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "PYTHON_SCRIPT=%SCRIPT_DIR%log-prompt-history.sh"

where py >nul 2>nul
if %ERRORLEVEL%==0 (
  py -3 "%PYTHON_SCRIPT%"
  exit /b 0
)

where python >nul 2>nul
if %ERRORLEVEL%==0 (
  python "%PYTHON_SCRIPT%"
  exit /b 0
)

exit /b 0