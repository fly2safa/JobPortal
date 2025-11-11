#!/bin/bash
# ============================================================================
# Backend Server Startup Script (Bash)
# ============================================================================
#
# USAGE:
#   Default Port (8000):
#     ./ourscript/start-backend.sh
#
#   Custom Port (e.g., 8010):
#     ./ourscript/start-backend.sh 8010
#
#   Custom Host and Port:
#     ./ourscript/start-backend.sh 8010 0.0.0.0
#
# PREREQUISITES:
#   - Python 3.8+ installed
#   - Virtual environment created in backend/venv
#   - Dependencies installed (pip install -r requirements.txt)
#   - .env file configured in backend directory
#
# MAKE EXECUTABLE:
#   chmod +x ./ourscript/start-backend.sh
#
# NOTES:
#   - Script must be run from the JobPortal root directory
#   - Use Ctrl+C to stop the server
#   - Server runs with auto-reload enabled for development
# ============================================================================

# Default values
PORT=${1:-8000}
HOST=${2:-127.0.0.1}

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Helper functions
print_error() {
    echo -e "${RED}$1${NC}"
}

print_success() {
    echo -e "${GREEN}$1${NC}"
}

print_info() {
    echo -e "${CYAN}$1${NC}"
}

# Check if we're in the correct directory
if [ ! -d "backend" ]; then
    print_error "Error: backend directory not found!"
    print_error "Please run this script from the JobPortal root directory."
    exit 1
fi

# Check if virtual environment exists
if [ ! -f "backend/venv/bin/activate" ]; then
    print_error "Error: Virtual environment not found!"
    print_error "Please create a virtual environment first:"
    print_error "  cd backend"
    print_error "  python3 -m venv venv"
    exit 1
fi

# Display startup information
print_info "============================================"
print_info "  Starting Backend Server (FastAPI)"
print_info "============================================"
print_info "Host: $HOST"
print_info "Port: $PORT"
print_info "URL:  http://${HOST}:${PORT}"
print_info "Docs: http://${HOST}:${PORT}/docs"
print_info "============================================"
echo ""

# Navigate to backend directory
cd backend || exit 1

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate

# Start server
print_success "Starting Uvicorn server..."
print_info "Press Ctrl+C to stop the server"
echo ""

# Check Python version for compatibility
PYTHON_VERSION=$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
MAJOR_MINOR=$(echo "$PYTHON_VERSION" | awk -F. '{printf "%d%02d", $1, $2}')

if [ "$MAJOR_MINOR" -ge 313 ]; then
    print_info "Python 3.13+ detected - using alternative reload method"
    python -m uvicorn app.main:app --host "$HOST" --port "$PORT" --reload-dir app
else
    python -m uvicorn app.main:app --host "$HOST" --port "$PORT" --reload
fi

