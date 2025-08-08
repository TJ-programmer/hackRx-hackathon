# PowerShell script to start HackRx API locally
Write-Host "Starting HackRx API locally..." -ForegroundColor Green
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path "henv\Scripts\Activate.ps1")) {
    Write-Host "Virtual environment not found. Please run: python -m venv henv" -ForegroundColor Red
    Write-Host "Then activate it and install requirements." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Activate virtual environment
& "henv\Scripts\Activate.ps1"

# Start the FastAPI server
Write-Host "Starting FastAPI server on http://localhost:8001" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""
python run_local.py 