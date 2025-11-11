# Docker Configuration

This directory contains all Docker-related files for the JobPortal application.

## Files

- **`backend.Dockerfile`**: Dockerfile for the FastAPI backend service
- **`frontend.Dockerfile`**: Dockerfile for the Next.js frontend service
- **`docker-compose.yml`**: Docker Compose configuration to orchestrate all services

## Quick Start

### Prerequisites
- Docker installed (version 20.10+)
- Docker Compose installed (version 2.0+)

### Setup

1. **Configure environment variables**:
   ```bash
   # From the project root
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env.local
   
   # Edit the .env files with your actual values
   ```

2. **Build and run from the docker directory**:
   ```bash
   cd docker
   docker-compose up --build
   ```

   Or from the project root:
   ```bash
   docker-compose -f docker/docker-compose.yml up --build
   ```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Common Commands

#### Start services
```bash
cd docker
docker-compose up
```

#### Start in detached mode (background)
```bash
docker-compose up -d
```

#### Stop services
```bash
docker-compose down
```

#### View logs
```bash
docker-compose logs -f
```

#### Rebuild images
```bash
docker-compose build --no-cache
```

#### Remove volumes (clean slate)
```bash
docker-compose down -v
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

## Troubleshooting

### Port already in use
```bash
# Find and kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use different ports in docker-compose.yml
ports:
  - "8001:8000"  # Map host:8001 to container:8000
```

### Permission denied
```bash
# On Linux/Mac, you may need sudo
sudo docker-compose up
```

### Container keeps restarting
```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend

# Common issues:
# - Missing or invalid .env variables
# - MongoDB connection failure
# - Port conflicts
```

### Clear everything and start fresh
```bash
docker-compose down -v
docker system prune -a
docker-compose up --build
```

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

