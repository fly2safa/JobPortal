# ============================================================================
# Frontend Server Startup Script (PowerShell)
# ============================================================================
#
# USAGE:
#   Default Port (3000):
#     .\ourscript\start-frontend.ps1
#
#   Custom Port (e.g., 3001):
#     .\ourscript\start-frontend.ps1 -Port 3001
#
# PREREQUISITES:
#   - Node.js 18+ and npm installed
#   - Dependencies installed (npm install in frontend directory)
#   - .env.local file configured in frontend directory
#
# NOTES:
#   - Script must be run from the JobPortal root directory
#   - Use Ctrl+C to stop the server
#   - Server runs in development mode with hot-reload
#   - For custom port, you may need to update NEXT_PUBLIC_API_URL in .env.local
# ============================================================================

param(
    [int]$Port = 3000
)

# Color output functions
function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Info { Write-Host $args -ForegroundColor Cyan }
function Write-Error { Write-Host $args -ForegroundColor Red }

# Check if we're in the correct directory
if (-not (Test-Path "frontend")) {
    Write-Error "Error: frontend directory not found!"
    Write-Error "Please run this script from the JobPortal root directory."
    exit 1
}

# Check if node_modules exists
if (-not (Test-Path "frontend\node_modules")) {
    Write-Error "Error: node_modules not found!"
    Write-Error "Please install dependencies first:"
    Write-Error "  cd frontend"
    Write-Error "  npm install"
    exit 1
}

# Display startup information
Write-Info "============================================"
Write-Info "  Starting Frontend Server (Next.js)"
Write-Info "============================================"
Write-Info "Port: $Port"
Write-Info "URL:  http://localhost:${Port}"
Write-Info "============================================"
Write-Host ""

# Navigate to frontend directory and start server
Set-Location frontend
Write-Success "Starting Next.js development server..."
Write-Info "Press Ctrl+C to stop the server"
Write-Host ""

# Set port environment variable and start Next.js
$env:PORT = $Port
npm run dev

