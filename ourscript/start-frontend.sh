#!/bin/bash
# ============================================================================
# Frontend Server Startup Script (Bash)
# ============================================================================
#
# USAGE:
#   Default Port (3000):
#     ./ourscript/start-frontend.sh
#
#   Custom Port (e.g., 3001):
#     ./ourscript/start-frontend.sh 3001
#
# PREREQUISITES:
#   - Node.js 18+ and npm installed
#   - Dependencies installed (npm install in frontend directory)
#   - .env.local file configured in frontend directory
#
# MAKE EXECUTABLE:
#   chmod +x ./ourscript/start-frontend.sh
#
# NOTES:
#   - Script must be run from the JobPortal root directory
#   - Use Ctrl+C to stop the server
#   - Server runs in development mode with hot-reload
#   - For custom port, you may need to update NEXT_PUBLIC_API_URL in .env.local
# ============================================================================

# Default values
PORT=${1:-3000}

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
if [ ! -d "frontend" ]; then
    print_error "Error: frontend directory not found!"
    print_error "Please run this script from the JobPortal root directory."
    exit 1
fi

# Check if node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    print_error "Error: node_modules not found!"
    print_error "Please install dependencies first:"
    print_error "  cd frontend"
    print_error "  npm install"
    exit 1
fi

# Display startup information
print_info "============================================"
print_info "  Starting Frontend Server (Next.js)"
print_info "============================================"
print_info "Port: $PORT"
print_info "URL:  http://localhost:${PORT}"
print_info "============================================"
echo ""

# Navigate to frontend directory
cd frontend || exit 1

# Start server
print_success "Starting Next.js development server..."
print_info "Press Ctrl+C to stop the server"
echo ""

# Set port environment variable and start Next.js
PORT=$PORT npm run dev

