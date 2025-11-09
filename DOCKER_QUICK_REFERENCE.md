# Docker Quick Reference Card

Fast reference for common Docker commands for JobPortal.

## 🌍 Cross-Platform Support

✅ **Supported Platforms:**
- Apple Silicon (M1/M2/M3) - ARM64
- Intel/AMD (x86_64) - AMD64
- Windows (WSL2 recommended)

Docker automatically detects your system architecture and uses the correct images.

## 📦 Configuration Files

- **`docker-compose.yml`** - Production configuration
- **`docker-compose.dev.yml`** - Development configuration with hot-reload

## 🚀 Getting Started

### Development Mode (Recommended for local development)

```bash
# Setup environment files
cp backend/.env.example backend/.env
cp frontend/.env.local.example frontend/.env.local

# Edit with your credentials
nano backend/.env

# Start in development mode (hot-reload enabled)
docker-compose -f docker-compose.dev.yml up

# Or run in background
docker-compose -f docker-compose.dev.yml up -d
```

### Production Mode

```bash
# Setup environment files
cp backend/.env.example backend/.env
cp frontend/.env.local.example frontend/.env.local

# Start in production mode
docker-compose up -d
```

## 📋 Essential Commands

### Start/Stop

```bash
# === DEVELOPMENT MODE ===

# Start all services (dev mode with hot-reload)
docker-compose -f docker-compose.dev.yml up

# Start in background
docker-compose -f docker-compose.dev.yml up -d

# Stop all services (dev mode)
docker-compose -f docker-compose.dev.yml down

# === PRODUCTION MODE ===

# Start all services (production mode)
docker-compose up -d

# Start with logs visible
docker-compose up

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down --volumes
```

### Build

```bash
# === DEVELOPMENT MODE ===

# Build images (dev mode)
docker-compose -f docker-compose.dev.yml build

# Build without cache (dev mode)
docker-compose -f docker-compose.dev.yml build --no-cache

# Build and start (dev mode)
docker-compose -f docker-compose.dev.yml up -d --build

# === PRODUCTION MODE ===

# Build images (production)
docker-compose build

# Build without cache (production)
docker-compose build --no-cache

# Build and start (production)
docker-compose up -d --build
```

### Platform-Specific Notes

**Apple Silicon (M1/M2/M3):**
```bash
# No special configuration needed - auto-detected
docker-compose up -d
```

**Windows (WSL2):**
```bash
# Enable WSL2 backend in Docker Desktop settings
# Then run normally
docker-compose up -d
```

**Intel/AMD x86:**
```bash
# No special configuration needed - auto-detected
docker-compose up -d
```

### Logs

```bash
# All logs
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# Last 100 lines
docker-compose logs --tail=100 backend
```

### Status

```bash
# Check running containers
docker-compose ps

# Check resource usage
docker stats

# Check health
docker inspect jobportal-backend --format='{{.State.Health.Status}}'
```

## 🛠️ Development Commands

```bash
# Start in dev mode (hot-reload)
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Restart single service
docker-compose restart backend

# Execute command in container
docker-compose exec backend bash
docker-compose exec frontend sh

# Install new package
docker-compose exec backend pip install package-name
docker-compose exec frontend npm install package-name
```

## 🔧 Troubleshooting

```bash
# View logs for errors
docker-compose logs --tail=50 backend | grep ERROR

# Test backend health
curl http://localhost:8000/health

# Test backend from frontend container
docker-compose exec frontend curl http://backend:8000/health

# Restart problematic service
docker-compose restart backend

# Rebuild specific service
docker-compose up -d --build backend
```

## 🗄️ MongoDB Commands

```bash
# Start with local MongoDB
docker-compose up -d mongodb

# Access MongoDB shell
docker-compose exec mongodb mongosh -u admin -p admin123

# Start Mongo Express UI
docker-compose --profile tools up -d mongo-express
# Access: http://localhost:8081 (admin/admin)

# Backup database
docker-compose exec mongodb mongodump --out /backup

# Check MongoDB logs
docker-compose logs -f mongodb
```

## 🧹 Cleanup

```bash
# Stop and remove containers
docker-compose down

# Remove volumes too
docker-compose down --volumes

# Remove images
docker-compose down --rmi all

# Full cleanup
docker system prune -a --volumes
```

## 🌐 Access URLs

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | Web application |
| Backend | http://localhost:8000 | API server |
| API Docs | http://localhost:8000/docs | Swagger UI |
| ReDoc | http://localhost:8000/redoc | Alternative API docs |
| Mongo Express | http://localhost:8081 | MongoDB UI (optional) |

## 📊 Common Issues & Fixes

### Port Already in Use

```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or change port in docker-compose.yml
ports:
  - "8001:8000"  # Changed from 8000:8000
```

### Can't Connect to Backend

```bash
# Check if backend is running
docker-compose ps backend

# Check backend logs
docker-compose logs backend

# Test connection
curl http://localhost:8000/health

# Inside frontend container
docker-compose exec frontend curl http://backend:8000/health
```

### MongoDB Connection Error

```bash
# Check MONGODB_URI in backend/.env
cat backend/.env | grep MONGODB_URI

# Test connection
docker-compose exec backend python -c "
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
async def test():
    client = AsyncIOMotorClient('your-uri-here')
    await client.admin.command('ping')
    print('✅ Connected')
asyncio.run(test())
"
```

### Container Keeps Restarting

```bash
# Check logs for errors
docker-compose logs --tail=100 backend

# Check health status
docker inspect jobportal-backend

# Try starting without detached mode
docker-compose up backend
```

## 💡 Pro Tips

```bash
# Watch logs with grep
docker-compose logs -f | grep ERROR

# Check environment variables
docker-compose config

# Remove stopped containers
docker-compose rm

# Update and restart
git pull && docker-compose up -d --build

# Check disk usage
docker system df
```

## 🔄 Update Workflow

```bash
# 1. Pull latest code
git pull

# 2. Rebuild images
docker-compose build

# 3. Restart services
docker-compose up -d

# 4. Check logs
docker-compose logs -f
```

## 📝 Useful One-Liners

```bash
# Restart everything
docker-compose restart

# View all container IPs
docker-compose ps -q | xargs docker inspect -f '{{.Name}} - {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'

# Follow logs with timestamps
docker-compose logs -f -t

# Check CPU/Memory usage
docker stats --no-stream

# Find large images
docker images --format "{{.Repository}}:{{.Tag}} {{.Size}}" | sort -k 2 -h
```

---

**For more details, see:**
- `README.md` - Complete documentation
- `DOCKER_GUIDE.md` - Comprehensive guide
- `DOCKER_IMPLEMENTATION_SUMMARY.md` - Implementation details

