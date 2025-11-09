# Environment Setup Guide

This guide helps you configure environment variables for both backend and frontend services.

## Quick Setup

Run this in your terminal to create environment files from templates:

```bash
# Create backend .env file
cat > backend/.env << 'EOF'
# Backend Environment Configuration
ENVIRONMENT=development
HOST=0.0.0.0
PORT=8000

# Database
MONGODB_URL=mongodb://admin:admin123@mongodb:27017/jobportal?authSource=admin
MONGODB_DB_NAME=jobportal

# Security (CHANGE THESE IN PRODUCTION!)
SECRET_KEY=development-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
RELOAD=true
DEBUG=false
EOF

# Create frontend .env.local file
cat > frontend/.env.local << 'EOF'
# Frontend Environment Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=JobPortal
NEXT_PUBLIC_APP_URL=http://localhost:3000
NODE_ENV=development

# NextAuth (CHANGE THIS IN PRODUCTION!)
NEXTAUTH_SECRET=development-nextauth-secret-change-in-production
NEXTAUTH_URL=http://localhost:3000

# Features
NEXT_PUBLIC_ENABLE_ANALYTICS=false
NEXT_PUBLIC_ENABLE_CHAT=false
NEXT_PUBLIC_ENABLE_NOTIFICATIONS=true

# Development
WATCHPACK_POLLING=true
NEXT_TELEMETRY_DISABLED=1
EOF

echo "✅ Environment files created successfully!"
```

## Backend Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `ENVIRONMENT` | Application environment | `development` or `production` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `MONGODB_URL` | MongoDB connection string | `mongodb://admin:admin123@mongodb:27017/jobportal` |
| `SECRET_KEY` | JWT secret key | Generate with `openssl rand -hex 32` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CORS_ORIGINS` | Allowed origins for CORS | `http://localhost:3000` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token expiration | `30` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `RELOAD` | Enable hot-reload (dev only) | `true` |

### Email Configuration (Optional)

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=noreply@jobportal.com
SMTP_FROM_NAME=JobPortal
```

### AWS S3 Configuration (Optional)

```env
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=us-east-1
AWS_S3_BUCKET=jobportal-uploads
```

## Frontend Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:8000` |
| `NEXTAUTH_SECRET` | NextAuth secret | Generate with `openssl rand -base64 32` |
| `NEXTAUTH_URL` | Application URL | `http://localhost:3000` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_APP_NAME` | Application name | `JobPortal` |
| `WATCHPACK_POLLING` | Enable file watching (Docker) | `true` |
| `NEXT_TELEMETRY_DISABLED` | Disable Next.js telemetry | `1` |

### OAuth Providers (Optional)

```env
# LinkedIn
LINKEDIN_CLIENT_ID=your-linkedin-client-id
LINKEDIN_CLIENT_SECRET=your-linkedin-client-secret

# Google
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# GitHub
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
```

## Platform-Specific Notes

### Apple Silicon (M1/M2/M3)

No special configuration needed. Docker automatically detects ARM64 architecture.

### Windows (WSL2)

1. Enable WSL2 backend in Docker Desktop settings
2. Set `WATCHPACK_POLLING=true` in frontend `.env.local` for file watching

### Intel/AMD x86

No special configuration needed. Docker automatically detects AMD64 architecture.

## Security Best Practices

### Development

- Use the provided default values
- Keep credentials simple (e.g., `admin123`)

### Production

1. **Generate Strong Secrets:**
   ```bash
   # For SECRET_KEY
   openssl rand -hex 32
   
   # For NEXTAUTH_SECRET
   openssl rand -base64 32
   ```

2. **Use Environment-Specific URLs:**
   ```env
   # Production backend
   NEXT_PUBLIC_API_URL=https://api.yourdomain.com
   
   # Production frontend
   NEXTAUTH_URL=https://yourdomain.com
   ```

3. **Secure MongoDB:**
   ```env
   # Use strong passwords and authentication
   MONGODB_URL=mongodb+srv://username:strongpassword@cluster.mongodb.net/jobportal
   ```

4. **Restrict CORS:**
   ```env
   # Only allow your production domain
   CORS_ORIGINS=https://yourdomain.com
   ```

## Verification

After setting up environment files, verify they're correct:

```bash
# Check backend .env exists
ls -la backend/.env

# Check frontend .env.local exists
ls -la frontend/.env.local

# Test with Docker
docker-compose -f docker-compose.dev.yml config

# Start services
docker-compose -f docker-compose.dev.yml up
```

## Troubleshooting

### "Cannot connect to MongoDB"
- Check `MONGODB_URL` is correct
- Ensure MongoDB container is running: `docker ps | grep mongodb`

### "CORS Error"
- Add your frontend URL to `CORS_ORIGINS` in backend `.env`
- Example: `CORS_ORIGINS=http://localhost:3000`

### "Environment variables not loading"
- Ensure files are named correctly: `.env` (backend) and `.env.local` (frontend)
- Restart containers: `docker-compose restart`

### "Hot-reload not working (Windows/Mac)"
- Set `WATCHPACK_POLLING=true` in frontend `.env.local`
- Set `RELOAD=true` in backend `.env`

