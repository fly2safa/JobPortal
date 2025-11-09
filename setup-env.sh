#!/bin/bash

# Environment Setup Script for JobPortal
# This script creates .env files with default development settings
# Works on: macOS, Linux, Windows (Git Bash/WSL)

set -e

echo "🚀 JobPortal Environment Setup"
echo "==============================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Detect platform
PLATFORM="unknown"
case "$(uname -s)" in
    Darwin*)    PLATFORM="macOS";;
    Linux*)     PLATFORM="Linux";;
    MINGW*|MSYS*|CYGWIN*)    PLATFORM="Windows";;
esac

echo "Platform detected: $PLATFORM"
echo ""

# Generate secret keys
echo "🔐 Generating secure secret keys..."
if command -v openssl &> /dev/null; then
    BACKEND_SECRET=$(openssl rand -hex 32)
    FRONTEND_SECRET=$(openssl rand -base64 32)
    print_success "Secret keys generated"
else
    print_warning "OpenSSL not found. Using default keys (CHANGE IN PRODUCTION!)"
    BACKEND_SECRET="development-secret-key-please-change-in-production"
    FRONTEND_SECRET="development-nextauth-secret-please-change-in-production"
fi
echo ""

# Create backend .env
echo "📝 Creating backend/.env..."
if [ -f "backend/.env" ]; then
    print_warning "backend/.env already exists. Creating backup..."
    cp backend/.env backend/.env.backup
    print_success "Backup created: backend/.env.backup"
fi

cat > backend/.env << EOF
# Backend Environment Configuration
# Generated on $(date)

# ======================
# APPLICATION SETTINGS
# ======================
ENVIRONMENT=development
HOST=0.0.0.0
PORT=8000

# ======================
# DATABASE CONFIGURATION
# ======================
MONGODB_URL=mongodb://admin:admin123@mongodb:27017/jobportal?authSource=admin
MONGODB_DB_NAME=jobportal

# ======================
# SECURITY & AUTHENTICATION
# ======================
SECRET_KEY=${BACKEND_SECRET}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# ======================
# CORS SETTINGS
# ======================
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# ======================
# LOGGING
# ======================
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
RELOAD=true
DEBUG=false

# ======================
# FILE UPLOAD SETTINGS
# ======================
MAX_UPLOAD_SIZE=10485760
ALLOWED_RESUME_TYPES=pdf,doc,docx
EOF

print_success "backend/.env created"
echo ""

# Create frontend .env.local
echo "📝 Creating frontend/.env.local..."
if [ -f "frontend/.env.local" ]; then
    print_warning "frontend/.env.local already exists. Creating backup..."
    cp frontend/.env.local frontend/.env.local.backup
    print_success "Backup created: frontend/.env.local.backup"
fi

cat > frontend/.env.local << EOF
# Frontend Environment Configuration
# Generated on $(date)

# ======================
# API CONFIGURATION
# ======================
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=JobPortal
NEXT_PUBLIC_APP_URL=http://localhost:3000

# ======================
# APPLICATION SETTINGS
# ======================
NODE_ENV=development

# ======================
# AUTHENTICATION
# ======================
NEXTAUTH_SECRET=${FRONTEND_SECRET}
NEXTAUTH_URL=http://localhost:3000

# ======================
# FEATURE FLAGS
# ======================
NEXT_PUBLIC_ENABLE_ANALYTICS=false
NEXT_PUBLIC_ENABLE_CHAT=false
NEXT_PUBLIC_ENABLE_NOTIFICATIONS=true

# ======================
# FILE UPLOAD
# ======================
NEXT_PUBLIC_MAX_FILE_SIZE=10
NEXT_PUBLIC_ALLOWED_RESUME_TYPES=.pdf,.doc,.docx

# ======================
# DEVELOPMENT SETTINGS
# ======================
WATCHPACK_POLLING=true
NEXT_TELEMETRY_DISABLED=1
EOF

print_success "frontend/.env.local created"
echo ""

# Create logs directory
echo "📁 Creating logs directory..."
mkdir -p backend/logs
print_success "backend/logs directory created"
echo ""

# Summary
echo "==============================="
echo "✨ Setup Complete!"
echo "==============================="
echo ""
echo "📋 Summary:"
echo "  • Platform: $PLATFORM"
echo "  • Backend config: backend/.env"
echo "  • Frontend config: frontend/.env.local"
echo "  • Logs directory: backend/logs"
echo ""
echo "🚀 Next steps:"
echo ""
echo "  Development mode (with hot-reload):"
echo "    docker-compose -f docker-compose.dev.yml up"
echo ""
echo "  Production mode:"
echo "    docker-compose up -d"
echo ""
echo "⚠️  Important:"
echo "  • Review and customize the generated .env files"
echo "  • For production, generate NEW secret keys"
echo "  • Never commit .env files to version control"
echo ""
print_success "Happy coding! 🎉"

