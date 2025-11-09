# Docker Deployment Guide for JobPortal

Complete guide for deploying JobPortal using Docker and Docker Compose.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Deployment Options](#deployment-options)
- [Troubleshooting](#troubleshooting)
- [Advanced Usage](#advanced-usage)

## 🎯 Prerequisites

1. **Docker Desktop** installed and running
   - Docker Engine 20.10+
   - Docker Compose 2.0+

2. **Environment Configuration**
   - MongoDB Atlas account (or local MongoDB)
   - OpenAI API key (for AI features)

## 🚀 Quick Start

### 1. Clone and Navigate

```bash
git clone <repository-url>
cd jobpotal_greenfield
```

### 2. Configure Environment

```bash
# Backend
cp backend/.env.example backend/.env
nano backend/.env  # or use your preferred editor

# Frontend
cp frontend/.env.local.example frontend/.env.local
```

### 3. Update Backend .env

```env
# Required configurations
MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/
DATABASE_NAME=jobportal
SECRET_KEY=your-super-secret-key-here
OPENAI_API_KEY=sk-your-openai-api-key
```

### 4. Build and Run

```bash
# Build images
docker-compose build

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### 5. Access Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **MongoDB Express:** http://localhost:8081 (if using --profile tools)

## ⚙️ Configuration

### Backend Configuration (backend/.env)

```env
# Application
APP_NAME=JobPortal
APP_VERSION=1.0.0
ENVIRONMENT=production
DEBUG=False

# Server
HOST=0.0.0.0
PORT=8000

# Database - MongoDB Atlas (Recommended)
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=jobportal

# OR use local MongoDB from docker-compose
# MONGODB_URI=mongodb://admin:admin123@mongodb:27017/jobportal?authSource=admin

# Security
SECRET_KEY=generate-with-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI
OPENAI_API_KEY=sk-your-openai-api-key

# Email (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# CORS
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

### Frontend Configuration (frontend/.env.local)

```env
# For Docker deployment (services communicate via Docker network)
NEXT_PUBLIC_API_URL=http://backend:8000

# For local development
# NEXT_PUBLIC_API_URL=http://localhost:8000

NEXT_PUBLIC_APP_NAME=JobPortal
NEXT_PUBLIC_APP_VERSION=1.0.0
```

## 🎪 Deployment Options

### Option 1: Production Deployment (Recommended)

Uses optimized production builds with MongoDB Atlas:

```bash
# Update backend/.env with MongoDB Atlas URI
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/

# Build and start
docker-compose up -d --build

# Monitor
docker-compose logs -f backend frontend
```

### Option 2: Development Mode with Hot Reload

```bash
# Start with development overrides
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Code changes will auto-reload
```

### Option 3: With Local MongoDB

Include local MongoDB container:

```bash
# docker-compose.yml already includes MongoDB service

# Update backend/.env
MONGODB_URI=mongodb://admin:admin123@mongodb:27017/jobportal?authSource=admin

# Start all services
docker-compose up -d

# Access MongoDB UI (optional)
docker-compose --profile tools up -d mongo-express
# Access at http://localhost:8081 (admin/admin)
```

### Option 4: Individual Services

Run services separately:

```bash
# Backend only
docker-compose up -d backend

# Frontend only
docker-compose up -d frontend

# MongoDB only
docker-compose up -d mongodb
```

## 🔍 Monitoring and Management

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mongodb

# Last 100 lines
docker-compose logs --tail=100 backend
```

### Check Service Health

```bash
# Check all services
docker-compose ps

# Check specific service health
docker inspect jobportal-backend --format='{{.State.Health.Status}}'
docker inspect jobportal-frontend --format='{{.State.Health.Status}}'
```

### Execute Commands in Containers

```bash
# Backend - Python shell
docker-compose exec backend python

# Backend - Run migrations (if applicable)
docker-compose exec backend python -m alembic upgrade head

# Frontend - Install new packages
docker-compose exec frontend npm install <package-name>

# MongoDB - Access mongo shell
docker-compose exec mongodb mongosh -u admin -p admin123
```

### Scale Services

```bash
# Scale backend (for load balancing)
docker-compose up -d --scale backend=3

# Note: You'll need a load balancer (nginx) in front
```

## 🛠️ Troubleshooting

### Issue: Container won't start

```bash
# Check logs
docker-compose logs backend

# Common issues:
# 1. MongoDB connection error - Check MONGODB_URI in .env
# 2. Port already in use - Kill process on port or change port
# 3. Build errors - Rebuild with --no-cache
docker-compose build --no-cache
```

### Issue: Backend can't connect to MongoDB

```bash
# Test MongoDB connection
docker-compose exec backend python -c "
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
async def test():
    client = AsyncIOMotorClient('your-mongodb-uri')
    await client.admin.command('ping')
    print('✅ Connected')
asyncio.run(test())
"

# Check if MongoDB is running
docker-compose ps mongodb

# Check MongoDB logs
docker-compose logs mongodb
```

### Issue: Frontend can't reach Backend

```bash
# Inside Docker network, use service name
# frontend/.env.local should have:
NEXT_PUBLIC_API_URL=http://backend:8000

# Test from frontend container
docker-compose exec frontend curl http://backend:8000/health
```

### Issue: Permission Errors

```bash
# Fix ownership (Linux/macOS)
sudo chown -R $USER:$USER .

# Rebuild with correct permissions
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Issue: Out of disk space

```bash
# Clean up Docker resources
docker system prune -a --volumes

# Remove specific items
docker-compose down --volumes --rmi all
```

## 🔄 Updates and Maintenance

### Update Application Code

```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

### Update Dependencies

```bash
# Backend
docker-compose exec backend pip install -r requirements.txt

# Frontend
docker-compose exec frontend npm install

# Or rebuild images
docker-compose build --no-cache
```

### Backup MongoDB Data

```bash
# Using docker-compose MongoDB
docker-compose exec mongodb mongodump --out /backup

# Copy backup from container
docker cp jobportal-mongodb:/backup ./backup

# Using MongoDB Atlas
# Use Atlas UI or mongodump with connection string
```

### Restore MongoDB Data

```bash
# Copy backup to container
docker cp ./backup jobportal-mongodb:/backup

# Restore
docker-compose exec mongodb mongorestore /backup
```

## 🚀 Production Deployment Tips

### 1. Security

- Use strong `SECRET_KEY`: `openssl rand -hex 32`
- Don't expose MongoDB port publicly (comment out ports in docker-compose.yml)
- Use HTTPS (add nginx reverse proxy)
- Keep environment files secure (never commit to git)

### 2. Performance

```yaml
# Add resource limits in docker-compose.yml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

### 3. Logging

```yaml
# Add logging configuration
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 4. Health Checks

Already configured in docker-compose.yml:
- Backend: `curl http://localhost:8000/health`
- Frontend: Node.js HTTP check
- MongoDB: `mongosh --eval "db.adminCommand('ping')"`

### 5. Use Docker Secrets (Production)

```yaml
# docker-compose.prod.yml
services:
  backend:
    secrets:
      - mongodb_uri
      - secret_key
      
secrets:
  mongodb_uri:
    external: true
  secret_key:
    external: true
```

## 📊 Monitoring with Docker Stats

```bash
# Real-time resource usage
docker stats

# Specific services
docker stats jobportal-backend jobportal-frontend
```

## 🔗 Useful Commands Cheat Sheet

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Restart specific service
docker-compose restart backend

# View logs
docker-compose logs -f

# Execute command
docker-compose exec backend bash

# Rebuild
docker-compose build --no-cache

# Remove everything
docker-compose down --volumes --rmi all

# Check status
docker-compose ps

# Environment variables
docker-compose config
```

## 🆘 Getting Help

1. Check container logs: `docker-compose logs -f`
2. Verify environment variables: `docker-compose config`
3. Test connectivity: `docker-compose exec backend curl http://backend:8000/health`
4. Review Docker documentation: https://docs.docker.com

---

**Need more help?** Open an issue on GitHub or consult the main README.md

