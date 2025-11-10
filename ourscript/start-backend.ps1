# ============================================================================
# Backend Server Startup Script (PowerShell)
# ============================================================================
#
# USAGE:
#   Default Port (8000):
#     .\ourscript\start-backend.ps1
#
#   Custom Port (e.g., 8010):
#     .\ourscript\start-backend.ps1 -Port 8010
#
#   Custom Host and Port:
#     .\ourscript\start-backend.ps1 -Port 8010 -HostAddress "0.0.0.0"
#
# PREREQUISITES:
#   - Python 3.8+ installed
#   - Virtual environment created in backend/venv
#   - Dependencies installed (pip install -r requirements.txt)
#   - .env file configured in backend directory
#
# NOTES:
#   - Script must be run from the JobPortal root directory
#   - Use Ctrl+C to stop the server
#   - Server runs with auto-reload enabled for development
# ============================================================================

param(
    [int]$Port = 8000,
    [string]$HostAddress = "127.0.0.1"
)

# Color output functions
function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Info { Write-Host $args -ForegroundColor Cyan }
function Write-Error { Write-Host $args -ForegroundColor Red }

# Check if we're in the correct directory
if (-not (Test-Path "backend")) {
    Write-Error "Error: backend directory not found!"
    Write-Error "Please run this script from the JobPortal root directory."
    exit 1
}

# Check if virtual environment exists
if (-not (Test-Path "backend\venv\Scripts\Activate.ps1")) {
    Write-Error "Error: Virtual environment not found!"
    Write-Error "Please create a virtual environment first:"
    Write-Error "  cd backend"
    Write-Error "  python -m venv venv"
    exit 1
}

# Display startup information
Write-Info "============================================"
Write-Info "  Starting Backend Server (FastAPI)"
Write-Info "============================================"
Write-Info "Host: $HostAddress"
Write-Info "Port: $Port"
Write-Info "URL:  http://${HostAddress}:${Port}"
Write-Info "Docs: http://${HostAddress}:${Port}/docs"
Write-Info "============================================"
Write-Host ""

# Navigate to backend directory, activate venv, and start server
Set-Location backend
Write-Info "Activating virtual environment..."
.\venv\Scripts\Activate.ps1

Write-Success "Starting Uvicorn server..."
Write-Info "Press Ctrl+C to stop the server"
Write-Host ""

python -m uvicorn app.main:app --host $HostAddress --port $Port --reload

