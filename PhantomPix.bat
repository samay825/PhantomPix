@echo off

:: Developed by zork
net session >nul 2>&1
if %errorLevel% == 0 (
    goto :run
) else (
    echo Requesting administrator privileges ...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:run
cd /d "%~dp0"
set PYTHONPATH=%~dp0
python phantompix\main.py
pause
