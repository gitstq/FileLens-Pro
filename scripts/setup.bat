@echo off
chcp 65001 >nul
REM FileLens Setup Script for Windows

echo 🔍 FileLens Setup Script
echo ========================

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    exit /b 1
)

for /f "tokens=2" %%a in ('python --version') do set PYTHON_VERSION=%%a
echo Python version: %PYTHON_VERSION%

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed or not in PATH
    exit /b 1
)

for /f "tokens=*" %%a in ('node --version') do set NODE_VERSION=%%a
echo Node.js version: %NODE_VERSION%
echo ✅ Node.js OK

REM Create virtual environment
echo Creating Python virtual environment...
if not exist "venv" (
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install Python dependencies
echo Installing Python dependencies...
pip install --upgrade pip
pip install -r requirements.txt

REM Install Node dependencies
echo Installing Node.js dependencies...
npm install

echo.
echo ✅ Setup completed successfully!
echo.
echo To start FileLens:
echo   1. Activate virtual environment: venv\Scripts\activate.bat
echo   2. Start backend: python src\main.py
echo   3. In another terminal, start frontend: npm start
echo.

pause
