# Docker Configuration

This directory contains all Docker-related files for the JobPortal application.

## 📦 What's Included

This Docker setup provides a complete containerized environment with just **4 files**:

### Core Files
1. **`backend.Dockerfile`** - Builds the backend container image
   - Installs Python 3.11 and all dependencies
   - Sets up the FastAPI application
   - Configures health checks

2. **`frontend.Dockerfile`** - Builds the frontend container image
   - Uses multi-stage build (deps → builder → runner)
   - Installs Node.js and builds the Next.js app
   - Optimized for production

3. **`docker-compose.yml`** - **The orchestrator** (main file you use)
   - Defines and connects both services (backend + frontend)
   - Sets up networking between containers
   - Manages environment variables
   - Configures volumes and ports
   - Handles service dependencies

4. **`README.md`** - This documentation file

### Supporting Files (Outside docker/ folder)
- **`backend/.dockerignore`** - Excludes unnecessary files (venv, __pycache__, etc.)
- **`frontend/.dockerignore`** - Excludes unnecessary files (node_modules, .next, etc.)
- **`backend/.env`** - Your environment variables (create from .env.example)
- **`frontend/.env.local`** - Your frontend config (create from .env.example)

---

## 🚀 Quick Start

### Prerequisites

#### Windows
- **Docker Desktop for Windows** (version 20.10+)
  - Download: https://www.docker.com/products/docker-desktop
  - Includes Docker Compose
  - Requires WSL 2 (Windows Subsystem for Linux)

#### macOS
- **Docker Desktop for Mac** (version 20.10+)
  - Download: https://www.docker.com/products/docker-desktop
  - Includes Docker Compose
  - Works on both Intel and Apple Silicon (M1/M2)

#### Linux
- **Docker Engine** (version 20.10+)
  ```bash
  # Ubuntu/Debian
  sudo apt-get update
  sudo apt-get install docker-ce docker-ce-cli containerd.io
  
  # Install Docker Compose
  sudo apt-get install docker-compose-plugin
  ```
  - Or follow: https://docs.docker.com/engine/install/

### Setup Instructions

#### Step 1: Configure Environment Variables

**Windows (PowerShell):**
```powershell
# From the project root
Copy-Item backend\.env.example backend\.env
Copy-Item frontend\.env.example frontend\.env.local

# Edit the files with your actual values
notepad backend\.env
notepad frontend\.env.local
```

**macOS/Linux (Bash/Zsh):**
```bash
# From the project root
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local

# Edit the files with your actual values
nano backend/.env
nano frontend/.env.local
```

**Required Variables:**
- `MONGODB_URI` - Your MongoDB Atlas connection string
- `DATABASE_NAME` - Database name (default: TalentNest)
- `SECRET_KEY` - Generate a strong random string
- `NEXT_PUBLIC_API_URL` - Backend URL (default: http://localhost:8000)

#### Step 2: Build and Run

**Option A: From the docker directory**

**Windows (PowerShell):**
```powershell
cd docker
docker-compose up --build
```

**macOS/Linux:**
```bash
cd docker
docker-compose up --build
```

**Option B: From the project root**

**Windows (PowerShell):**
```powershell
docker-compose -f docker\docker-compose.yml up --build
```

**macOS/Linux:**
```bash
docker-compose -f docker/docker-compose.yml up --build
```

#### Step 3: Access the Application

Once the containers are running, open your browser:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

#### Step 4: Stop the Application

Press `Ctrl + C` in the terminal, then:

**Windows (PowerShell):**
```powershell
docker-compose down
```

**macOS/Linux:**
```bash
docker-compose down
```

---

## 📋 Common Commands

All commands assume you're in the `docker/` directory. Commands are the same across all platforms unless noted.

### Start Services
```bash
docker-compose up
```

### Start in Detached Mode (Background)
```bash
docker-compose up -d
```

### Stop Services
```bash
docker-compose down
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Rebuild Images
```bash
docker-compose build --no-cache
```

### Remove Volumes (Clean Slate)
```bash
docker-compose down -v
```

### Restart Services
```bash
docker-compose restart
```

### Check Service Status
```bash
docker-compose ps
```

### Execute Commands in Running Container
```bash
# Backend
docker-compose exec backend bash

# Frontend
docker-compose exec frontend sh
```

## Architecture

### Backend Service
- **Base Image**: Python 3.11-slim
- **Port**: 8000
- **Health Check**: HTTP GET to `/health`
- **Volumes**: `../backend/uploads` mounted to `/app/uploads`

### Frontend Service
- **Base Image**: Node.js 20-alpine (multi-stage build)
- **Port**: 3000
- **Health Check**: HTTP GET to root
- **Depends On**: Backend service (waits for health check)

### Optional: MongoDB Service
Uncomment the MongoDB service in `docker-compose.yml` if you want to run a local MongoDB instance instead of using MongoDB Atlas.

## Environment Variables

### Backend (.env)
Required:
- `MONGODB_URI` - MongoDB connection string
- `DATABASE_NAME` - Database name (default: TalentNest)
- `SECRET_KEY` - JWT secret key

Optional:
- `OPENAI_API_KEY` - For AI features
- `SMTP_*` - For email notifications

See `backend/.env.example` for all options.

### Frontend (.env.local)
Required:
- `NEXT_PUBLIC_API_URL` - Backend API URL (default: http://localhost:8000)

See `frontend/.env.example` for all options.

---

## 🔧 Troubleshooting

### Port Already in Use

**Windows (PowerShell):**
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace <PID> with actual process ID)
taskkill /PID <PID> /F

# For port 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

**macOS:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# For port 3000
lsof -i :3000
kill -9 <PID>
```

**Linux:**
```bash
# Find process using port 8000
sudo netstat -tulpn | grep :8000

# Kill the process
sudo kill -9 <PID>

# Or use fuser
sudo fuser -k 8000/tcp
```

**Alternative: Use Different Ports**

Edit `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Map host:8001 to container:8000
  - "3001:3000"  # Map host:3001 to container:3000
```

### Permission Denied (Linux)

```bash
# Add your user to docker group
sudo usermod -aG docker $USER

# Log out and back in, then test
docker ps

# Or use sudo (not recommended for regular use)
sudo docker-compose up
```

### Docker Desktop Not Running (Windows/macOS)

**Error**: `Cannot connect to the Docker daemon`

**Solution**:
1. Open Docker Desktop application
2. Wait for it to fully start (whale icon in system tray)
3. Try the command again

### Container Keeps Restarting

**Check logs:**
```bash
docker-compose logs backend
docker-compose logs frontend
```

**Common Issues:**
- ❌ Missing or invalid `.env` variables
- ❌ MongoDB connection failure (check `MONGODB_URI`)
- ❌ Port conflicts
- ❌ Insufficient memory/resources

**Solutions:**
1. Verify `.env` files exist and have correct values
2. Test MongoDB connection string
3. Check Docker Desktop resource settings (Windows/macOS)
4. Ensure ports 3000 and 8000 are free

### Build Failures

**Windows - Line Ending Issues:**
```powershell
# If you get CRLF errors, configure git
git config --global core.autocrlf input

# Re-clone or reset files
git rm --cached -r .
git reset --hard
```

**macOS/Linux - Permission Issues:**
```bash
# Ensure files are readable
chmod -R 755 backend/ frontend/
```

### Clear Everything and Start Fresh

**All Platforms:**
```bash
# Stop and remove containers, networks, volumes
docker-compose down -v

# Remove all unused Docker resources
docker system prune -a

# Rebuild from scratch
docker-compose up --build
```

### MongoDB Connection Issues

**Error**: `Failed to connect to MongoDB`

**Solutions:**
1. Verify `MONGODB_URI` in `backend/.env`
2. Check MongoDB Atlas:
   - IP whitelist (add `0.0.0.0/0` for testing)
   - Database user credentials
   - Network access settings
3. Test connection:
   ```bash
   docker-compose exec backend python -c "from app.db.init_db import connect_to_mongo; import asyncio; asyncio.run(connect_to_mongo())"
   ```

### Out of Memory (Windows/macOS)

**Docker Desktop Settings:**
1. Open Docker Desktop
2. Go to Settings → Resources
3. Increase Memory allocation (recommend 4GB+)
4. Increase Swap (recommend 2GB+)
5. Click "Apply & Restart"

### Slow Build Times

**Solutions:**
1. Use BuildKit (faster builds):
   ```bash
   # Windows/macOS/Linux
   DOCKER_BUILDKIT=1 docker-compose build
   ```

2. Clean build cache occasionally:
   ```bash
   docker builder prune
   ```

3. Ensure `.dockerignore` files are in place (already configured)

## Production Considerations

For production deployment, consider:

1. **Use production-ready images**:
   - Pin specific versions instead of `latest`
   - Use official base images

2. **Security**:
   - Use secrets management (Docker secrets, Kubernetes secrets)
   - Don't commit `.env` files
   - Run containers as non-root users
   - Enable security scanning

3. **Performance**:
   - Use multi-stage builds (already implemented)
   - Optimize layer caching
   - Use `.dockerignore` files (already implemented)

4. **Monitoring**:
   - Add logging drivers
   - Implement health checks (already implemented)
   - Use monitoring tools (Prometheus, Grafana)

5. **Orchestration**:
   - Consider Kubernetes for production
   - Use Docker Swarm for simpler deployments
   - Implement auto-scaling

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Best Practices for Writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

