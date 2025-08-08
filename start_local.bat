@echo off
echo Starting HackRx API locally...
echo.

REM Check if virtual environment exists
if not exist "henv\Scripts\activate.bat" (
    echo Virtual environment not found. Please run: python -m venv henv
    echo Then activate it and install requirements.
    pause
    exit /b 1
)

REM Activate virtual environment
call henv\Scripts\activate.bat

REM Start the FastAPI server
echo Starting FastAPI server on http://localhost:8001
echo Press Ctrl+C to stop the server
echo.
python run_local.py 