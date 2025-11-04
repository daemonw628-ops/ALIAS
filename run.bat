@echo off
REM ALIAS Universal Launch Script for Windows

echo.
echo 🤖 ALIAS - Advanced Learning Intelligence Assistant System
echo ==========================================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Install from https://python.org
    pause
    exit /b 1
)

echo ✓ Python detected
echo.

REM Install minimal requirements
pip install -q requests

echo 🚀 Starting ALIAS...
echo.
echo Features: Voice • 7 AI Modes • 50+ Tools • 100%% FREE
echo Keyboard: Ctrl+Enter (send) ^| Ctrl+L (voice) ^| Ctrl+M (mode) ^| F1 (help)
echo.

python alias.py

pause
