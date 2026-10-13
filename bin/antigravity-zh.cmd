@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
set "PYTHONUTF8=1"
set "SCRIPT_DIR=%~dp0.."

where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    python "%SCRIPT_DIR%\cli.py" %*
    exit /b %ERRORLEVEL%
)

where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    py -3 "%SCRIPT_DIR%\cli.py" %*
    exit /b %ERRORLEVEL%
)

echo [Antigravity-ZH Error] 未找到 Python 3，请确认 Python 已安装并勾选 Add Python to PATH！
exit /b 1
