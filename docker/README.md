# JobPortal Docker Setup Guide

This guide provides complete instructions for running JobPortal using Docker and Docker Compose.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Building and Running](#building-and-running)
- [Accessing the Application](#accessing-the-application)
- [Troubleshooting](#troubleshooting)
- [Production Deployment](#production-deployment)

---

## 🔧 Prerequisites

### Required Software

1. **Docker** (v20.10+)
   - Download: https://www.docker.com/get-started
   - Verify: `docker --version`

2. **Docker Compose** (v2.0+)
   - Usually included with Docker Desktop
   - Verify: `docker-compose --version`

### Required Accounts/Services

1. **MongoDB Atlas** (Recommended) or local MongoDB
   - Sign up: https://www.mongodb.com/cloud/atlas
   - Create a free cluster
   - Get your connection string

2. **OpenAI API Key** (Required for AI features)
   - Sign up: https://platform.openai.com/
   - Create an API key

3. **SMTP Email Account** (Optional, for notifications)
   - Gmail, SendGrid, or any SMTP provider

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd JobPortal/docker
```

### 2. Create Environment File

```bash
# Copy the example environment file
cp env.example .env

# Edit the .env file with your actual values
nano .env  # or use your preferred editor
```

**Minimum Required Configuration:**

```env
# MongoDB (REQUIRED)
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=jobportal

# JWT Secret (REQUIRED)
SECRET_KEY=your-super-secret-jwt-key-change-this

# OpenAI (REQUIRED for AI features)
OPENAI_API_KEY=sk-your-openai-api-key-here
```

### 3. Build and Run

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode (background)
docker-compose up -d --build
```

### 4. Access the Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

---

## ⚙️ Configuration

### Environment Variables

The `.env` file contains all configuration. See `env.example` for all available options.

#### Essential Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `MONGODB_URI` | MongoDB connection string | `mongodb+srv://...` |
| `SECRET_KEY` | JWT secret key | Generate with `openssl rand -hex 32` |
| `OPENAI_API_KEY` | OpenAI API key | `sk-...` |

#### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | Anthropic API key (fallback) | - |
| `SMTP_USER` | Email for notifications | - |
| `SMTP_PASSWORD` | Email password | - |
| `N8N_API_KEY` | n8n workflow automation | - |
| `DEBUG` | Enable debug mode | `false` |
| `LOG_LEVEL` | Logging level | `INFO` |

### Generating a Secure JWT Secret

```bash
# On Linux/Mac
openssl rand -hex 32

# On Windows (PowerShell)
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))
```

---

## 🏗️ Building and Running

### Build Images

```bash
# Build all services
docker-compose build

# Build specific service
docker-compose build backend
docker-compose build frontend
```

### Start Services

```bash
# Start all services (foreground)
docker-compose up

# Start all services (background)
docker-compose up -d

# Start specific service
docker-compose up backend
```

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Stop and remove images
docker-compose down --rmi all
```

### View Logs

```bash
# View all logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View specific service logs
docker-compose logs backend
docker-compose logs frontend

# View last 100 lines
docker-compose logs --tail=100
```

### Restart Services

```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart backend
```

---

## 🌐 Accessing the Application

### Frontend (Next.js)

- **URL:** http://localhost:3000
- **Features:**
  - User registration and login
  - Job seeker dashboard
  - Employer dashboard
  - Job search and applications
  - AI-powered recommendations

### Backend API (FastAPI)

- **URL:** http://localhost:8000
- **Interactive Docs:** http://localhost:8000/docs
- **Alternative Docs:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

### API Endpoints

Key endpoints:
- `POST /api/v1/register` - User registration
- `POST /api/v1/login` - User login
- `GET /api/v1/jobs` - List jobs
- `POST /api/v1/applications` - Submit application
- `GET /api/v1/recommendations` - AI job recommendations

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Port Already in Use

**Error:** `Bind for 0.0.0.0:3000 failed: port is already allocated`

**Solution:**
```bash
# Find and kill process using the port
# On Linux/Mac
lsof -ti:3000 | xargs kill -9

# On Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Or change the port in docker-compose.yml
ports:
  - "3001:3000"  # Use port 3001 instead
```

#### 2. MongoDB Connection Failed

**Error:** `MongoServerError: Authentication failed`

**Solutions:**
- Verify `MONGODB_URI` is correct
- Check MongoDB Atlas network access (allow your IP)
- Ensure database user has correct permissions
- Test connection string in MongoDB Compass

#### 3. Backend Health Check Failing

**Error:** `backend is unhealthy`

**Solutions:**
```bash
# Check backend logs
docker-compose logs backend

# Common causes:
# - Missing MONGODB_URI
# - Missing SECRET_KEY
# - MongoDB connection issues
# - Missing required dependencies
```

#### 4. Frontend Can't Connect to Backend

**Error:** `Network Error` or `Failed to fetch`

**Solutions:**
- Ensure backend is running: `docker-compose ps`
- Check `NEXT_PUBLIC_API_URL` in `.env`
- For Docker internal communication, use `http://backend:8000`
- For browser access, use `http://localhost:8000`

#### 5. Build Failures

**Error:** `failed to solve with frontend Dockerfile`

**Solutions:**
```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache

# Check Dockerfile paths
# Ensure context paths in docker-compose.yml are correct
```

### Debugging Commands

```bash
# Check service status
docker-compose ps

# Inspect container
docker inspect jobportal-backend

# Execute command in container
docker-compose exec backend bash
docker-compose exec frontend sh

# Check container resources
docker stats

# View Docker system info
docker system df
docker system info
```

---

## 🚀 Production Deployment

### Security Checklist

- [ ] Change `SECRET_KEY` to a strong, unique value
- [ ] Set `DEBUG=false`
- [ ] Use strong MongoDB credentials
- [ ] Enable HTTPS/TLS
- [ ] Configure firewall rules
- [ ] Set up proper CORS origins
- [ ] Enable rate limiting
- [ ] Use environment-specific `.env` files
- [ ] Secure API keys (use secrets management)
- [ ] Enable MongoDB authentication
- [ ] Set up monitoring and logging

### Production Environment Variables

```env
# Production settings
DEBUG=false
LOG_LEVEL=WARNING
NODE_ENV=production

# Secure JWT
SECRET_KEY=<strong-random-key>

# Production MongoDB
MONGODB_URI=mongodb+srv://prod-user:strong-password@prod-cluster.mongodb.net/

# Production CORS
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Production API URL
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

### Docker Compose Override for Production

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  backend:
    restart: always
    environment:
      - DEBUG=false
      - LOG_LEVEL=WARNING
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G

  frontend:
    restart: always
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

Run with:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Monitoring

```bash
# View resource usage
docker stats

# Set up health checks
curl http://localhost:8000/health
curl http://localhost:3000/

# Monitor logs
docker-compose logs -f --tail=100
```

---

## 📊 Service Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Network                        │
│                  (jobportal-network)                     │
│                                                          │
│  ┌──────────────┐         ┌──────────────┐             │
│  │   Frontend   │────────▶│   Backend    │             │
│  │   Next.js    │         │   FastAPI    │             │
│  │   Port 3000  │         │   Port 8000  │             │
│  └──────────────┘         └──────────────┘             │
│                                  │                       │
│                                  │                       │
│                                  ▼                       │
│                           MongoDB Atlas                  │
│                        (External Service)                │
└─────────────────────────────────────────────────────────┘
```

### Service Dependencies

- **Frontend** depends on **Backend** (health check)
- **Backend** depends on **MongoDB** (external)
- **Both** use shared network for internal communication

---

## 📝 Additional Resources

### Documentation

- [Backend README](../backend/README.md)
- [Frontend README](../frontend/README.md)
- [API Documentation](http://localhost:8000/docs)
- [Project Implementation Plan](../JobPortal%20Implementation%20Plan.md)

### Docker Commands Reference

```bash
# List all containers
docker ps -a

# Remove stopped containers
docker container prune

# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Clean everything
docker system prune -a --volumes

# View container logs
docker logs jobportal-backend
docker logs jobportal-frontend
```

---

## 🆘 Getting Help

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review service logs: `docker-compose logs`
3. Verify environment variables in `.env`
4. Check Docker and Docker Compose versions
5. Ensure all prerequisites are installed
6. Review the [Backend README](../backend/README.md) and [Frontend README](../frontend/README.md)

---

## 📄 License

See the main project LICENSE file.

---

**Happy Deploying! 🚀**

