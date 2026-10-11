@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\pythonw.exe" (
    echo Please run install-windows.cmd first.
    pause
    exit /b 1
)
start "" ".venv\Scripts\pythonw.exe" "gui.py"
