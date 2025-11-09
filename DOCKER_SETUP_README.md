# Docker Setup - Cross-Platform Guide

Complete guide for running JobPortal with Docker on any platform.

## 🌍 Supported Platforms

✅ **Apple Silicon (M1/M2/M3)** - ARM64  
✅ **Intel/AMD (x86_64)** - AMD64  
✅ **Windows** - Via WSL2 or Docker Desktop  

Docker **automatically detects** your system architecture and uses the correct images. No manual platform configuration needed!

## 📦 Quick Start

### 1. Prerequisites

- **Docker Desktop** (latest version)
  - [Mac](https://docs.docker.com/desktop/install/mac-install/)
  - [Windows](https://docs.docker.com/desktop/install/windows-install/)
  - [Linux](https://docs.docker.com/desktop/install/linux-install/)
- **Docker Compose** (included with Docker Desktop)

**Windows Users:** Enable WSL2 backend in Docker Desktop settings for best performance.

### 2. Setup Environment

**Option A: Automated Setup (Recommended)**
```bash
# Run the setup script
./setup-env.sh
```

**Option B: Manual Setup**
```bash
# Copy and edit environment files manually
cp backend/.env.example backend/.env
cp frontend/.env.local.example frontend/.env.local

# Edit files with your preferred editor
nano backend/.env
nano frontend/.env.local
```

See [ENVIRONMENT_SETUP.md](./ENVIRONMENT_SETUP.md) for detailed configuration options.

### 3. Start Services

**Development Mode (Recommended for local development)**
```bash
# Start with hot-reload enabled
docker-compose -f docker-compose.dev.yml up

# Or run in background
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f
```

**Production Mode**
```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f
```

## 📁 Configuration Files

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Production configuration |
| `docker-compose.dev.yml` | Development with hot-reload |
| `backend/Dockerfile` | Backend build |
| `frontend/Dockerfile` | Frontend unified build (dev & prod targets) |

## 🚀 Common Commands

### Development Workflow

```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up

# Rebuild after dependency changes
docker-compose -f docker-compose.dev.yml up --build

# Stop services
docker-compose -f docker-compose.dev.yml down

# View logs for specific service
docker-compose -f docker-compose.dev.yml logs -f backend
docker-compose -f docker-compose.dev.yml logs -f frontend
```

### Production Workflow

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Check status
docker-compose ps

# Stop services
docker-compose down

# Stop and remove volumes (CAUTION: deletes database)
docker-compose down --volumes
```

### Database Management

```bash
# Access MongoDB shell
docker exec -it jobportal-mongodb-dev mongosh -u admin -p admin123

# View MongoDB logs
docker-compose -f docker-compose.dev.yml logs -f mongodb

# Backup database
docker exec jobportal-mongodb-dev mongodump --uri="mongodb://admin:admin123@localhost:27017/jobportal?authSource=admin" --out=/data/backup

# Access Mongo Express (Database UI)
# Open browser: http://localhost:8081
# Username: admin
# Password: admin
```

### Troubleshooting

```bash
# View all running containers
docker ps

# View all containers (including stopped)
docker ps -a

# Remove all stopped containers
docker container prune

# Remove unused images
docker image prune -a

# Remove unused volumes (CAUTION)
docker volume prune

# Complete cleanup (CAUTION: removes everything)
docker system prune -a --volumes

# Restart specific service
docker-compose restart backend
docker-compose restart frontend

# Access container shell
docker exec -it jobportal-backend-dev /bin/sh
docker exec -it jobportal-frontend-dev /bin/sh
```

## 🔧 Platform-Specific Setup

### Apple Silicon (M1/M2/M3)

**Works out of the box!** No additional configuration needed.

```bash
# Verify Docker is using correct architecture
docker info | grep Architecture
# Should show: Architecture: aarch64

# Start normally
docker-compose -f docker-compose.dev.yml up
```

### Intel/AMD x86

**Works out of the box!** No additional configuration needed.

```bash
# Verify Docker is using correct architecture
docker info | grep Architecture
# Should show: Architecture: x86_64

# Start normally
docker-compose -f docker-compose.dev.yml up
```

### Windows

**Prerequisites:**
1. Install WSL2: [Microsoft Guide](https://learn.microsoft.com/en-us/windows/wsl/install)
2. Install Docker Desktop: [Download](https://docs.docker.com/desktop/install/windows-install/)
3. Enable WSL2 backend in Docker Desktop settings

**Setup:**
```bash
# Clone repository in WSL2
cd ~
git clone <repository-url>
cd jobpotal_greenfield

# Run setup script
./setup-env.sh

# Start services
docker-compose -f docker-compose.dev.yml up
```

**Windows Tips:**
- Use WSL2 terminal (Ubuntu) for best performance
- File watching is slower on Windows; `WATCHPACK_POLLING=true` is enabled by default
- Keep project files in WSL2 filesystem (`~/projects/`) not Windows (`/mnt/c/`)

## 🌐 Service URLs

Once started, access services at:

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | Next.js application |
| Backend API | http://localhost:8000 | FastAPI backend |
| API Docs | http://localhost:8000/docs | Interactive API documentation |
| MongoDB | mongodb://localhost:27017 | Database (use MongoDB Compass) |
| Mongo Express | http://localhost:8081 | Database admin UI |

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│                  Docker Network                  │
│              (jobportal-network)                 │
│                                                  │
│  ┌──────────────┐      ┌──────────────┐        │
│  │   Frontend   │◄────►│   Backend    │        │
│  │   Next.js    │      │   FastAPI    │        │
│  │   Port 3000  │      │   Port 8000  │        │
│  └──────────────┘      └──────┬───────┘        │
│                                │                 │
│                                ▼                 │
│                        ┌──────────────┐         │
│                        │   MongoDB    │         │
│                        │   Port 27017 │         │
│                        └──────┬───────┘         │
│                                │                 │
│                                ▼                 │
│                        ┌──────────────┐         │
│                        │Mongo Express │         │
│                        │   Port 8081  │         │
│                        └──────────────┘         │
└─────────────────────────────────────────────────┘
```

## 🔒 Security Notes

### Development
- Default credentials are simple (e.g., `admin123`)
- Ports exposed to localhost only
- Debug logging enabled

### Production
- **Generate strong secrets** (see ENVIRONMENT_SETUP.md)
- **Use HTTPS** with reverse proxy (nginx/traefik)
- **Restrict CORS** to your domain only
- **Use managed MongoDB** (Atlas) instead of local instance
- **Enable MongoDB authentication**
- **Review and restrict exposed ports**

## 📊 Monitoring & Logs

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend

# Last 100 lines
docker-compose logs --tail=100 backend

# Logs with timestamps
docker-compose logs -ft backend
```

### Resource Usage
```bash
# Container stats
docker stats

# Service-specific stats
docker stats jobportal-backend-dev jobportal-frontend-dev
```

## 🐛 Troubleshooting Guide

### "Port already in use"
```bash
# Find what's using the port
lsof -i :3000  # macOS/Linux
netstat -ano | findstr :3000  # Windows

# Change port in docker-compose.yml
ports:
  - "3001:3000"  # Use 3001 instead
```

### "Cannot connect to Docker daemon"
```bash
# macOS/Windows: Start Docker Desktop
# Linux: Start Docker service
sudo systemctl start docker
```

### "Build failed: no space left on device"
```bash
# Clean up Docker
docker system prune -a --volumes
docker builder prune
```

### "Hot reload not working"
- Ensure `WATCHPACK_POLLING=true` in frontend/.env.local
- Ensure `RELOAD=true` in backend/.env
- Restart containers: `docker-compose restart`

### "Database connection error"
```bash
# Check MongoDB is running
docker ps | grep mongodb

# Check MongoDB logs
docker logs jobportal-mongodb-dev

# Verify connection string in backend/.env
MONGODB_URL=mongodb://admin:admin123@mongodb:27017/jobportal?authSource=admin
```

## 📚 Additional Resources

- [Unified Dockerfile Guide](./UNIFIED_DOCKERFILE_GUIDE.md) - Multi-target Dockerfile explanation
- [Docker Quick Reference](./DOCKER_QUICK_REFERENCE.md) - Essential commands
- [Environment Setup](./ENVIRONMENT_SETUP.md) - Configuration details
- [Docker Guide](./DOCKER_GUIDE.md) - Comprehensive guide
- [Cross-Platform Summary](./CROSS_PLATFORM_SUMMARY.md) - Platform support overview
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

## 🤝 Contributing

When making changes to Docker configuration:

1. Test on multiple platforms if possible
2. Update relevant documentation
3. Keep platform auto-detection (no hardcoded platforms)
4. Document any platform-specific quirks

## 📝 License

See main project LICENSE file.

