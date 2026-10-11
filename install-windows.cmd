@echo off
setlocal
cd /d "%~dp0"
set "DICTATE_NO_PAUSE="
set "DICTATE_SETUP_ARGS="
if "%~1"=="--no-pause" set "DICTATE_NO_PAUSE=1"
if "%~2"=="--skip-model-download" set "DICTATE_SETUP_ARGS=--skip-model-download"

echo Dictate Windows - local German speech recognition
py -3.12 -c "import sys; assert sys.maxsize > 2**32" >nul 2>&1
if not errorlevel 1 (
    set "DICTATE_PYTHON=py -3.12"
) else (
    python -c "import sys; assert sys.version_info[:2] == (3,12) and sys.maxsize > 2**32" >nul 2>&1
    if errorlevel 1 goto missing_python
    set "DICTATE_PYTHON=python"
)

if not exist ".venv\Scripts\python.exe" (
    %DICTATE_PYTHON% -m venv .venv
    if errorlevel 1 goto failed
)
".venv\Scripts\python.exe" -m pip install -r requirements-windows.txt
if errorlevel 1 goto failed
".venv\Scripts\python.exe" setup_windows.py %DICTATE_SETUP_ARGS%
if errorlevel 1 goto failed
echo.
echo Ready. Double-click start-windows.cmd to start dictating.
if not defined DICTATE_NO_PAUSE pause
exit /b 0

:missing_python
echo.
echo Python 3.12 64-bit is required. Install it from https://www.python.org/downloads/windows/
echo Enable the Python launcher during installation, then run this file again.
if not defined DICTATE_NO_PAUSE pause
exit /b 1

:failed
echo.
echo Installation failed. See the error above.
if not defined DICTATE_NO_PAUSE pause
exit /b 1
