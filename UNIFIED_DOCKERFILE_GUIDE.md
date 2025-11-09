# Unified Dockerfile Guide

## 📋 Overview

The frontend now uses a **single Dockerfile** with multiple named stages (build targets) instead of separate `Dockerfile` and `Dockerfile.dev` files. This approach keeps all build logic in one place while still optimizing for different environments.

## 🎯 Build Targets

The Dockerfile has **4 stages**, but you only need to target 2 of them:

| Target | Purpose | Usage |
|--------|---------|-------|
| `development` | Local development with hot-reload | Dev environment |
| `production` | Optimized production build (default) | Production deployment |

The other stages (`base` and `deps`) are intermediate stages used by both targets.

## 🏗️ Dockerfile Structure

```dockerfile
# Unified Dockerfile with 4 stages:

┌─────────────────────────────────────────┐
│  Stage 1: base                          │
│  - Base node:18-alpine                  │
│  - Install compatibility libs           │
│  - Copy package.json                    │
└────────────┬────────────────────────────┘
             │
             ├──────────┬─────────────────┐
             │          │                 │
┌────────────▼──────┐  │  ┌──────────────▼─────────┐
│ Stage 2: deps     │  │  │ Stage 3: builder       │
│ - npm ci          │  │  │ - npm run build        │
│ - All deps        │  │  │ - Production artifacts │
└────────────┬──────┘  │  └──────────────┬─────────┘
             │          │                 │
             │          │                 │
┌────────────▼──────────▼──┐  ┌──────────▼─────────┐
│ TARGET: development       │  │ TARGET: production │
│ - Hot reload              │  │ - Optimized        │
│ - All source mounted      │  │ - Minimal size     │
│ - Fast iteration          │  │ - Non-root user    │
└───────────────────────────┘  └────────────────────┘
```

## 🚀 Usage

### Development Mode

**Using docker-compose (recommended):**
```bash
# Automatically targets 'development' stage
docker-compose -f docker-compose.dev.yml up
```

**Using docker build directly:**
```bash
# Build development image
docker build --target development -t jobportal-frontend:dev ./frontend

# Run it
docker run -p 3000:3000 -v $(pwd)/frontend:/app jobportal-frontend:dev
```

### Production Mode

**Using docker-compose (recommended):**
```bash
# Automatically targets 'production' stage
docker-compose up -d
```

**Using docker build directly:**
```bash
# Build production image (production is default target)
docker build -t jobportal-frontend:prod ./frontend

# Or explicitly specify target
docker build --target production -t jobportal-frontend:prod ./frontend

# Run it
docker run -p 3000:3000 jobportal-frontend:prod
```

## 📊 Stage Comparison

### Development Stage
```dockerfile
FROM base AS development

COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NODE_ENV=development
CMD ["npm", "run", "dev"]
```

**Characteristics:**
- ✅ Includes all source code
- ✅ All dependencies (including dev)
- ✅ Hot-reload enabled
- ✅ Fast startup
- ❌ Larger image size (~500MB)
- ❌ Runs as root (fine for dev)

### Production Stage
```dockerfile
FROM node:18-alpine AS production

COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

ENV NODE_ENV=production
USER nextjs
CMD ["node", "server.js"]
```

**Characteristics:**
- ✅ Minimal image size (~150MB)
- ✅ Only production dependencies
- ✅ Pre-built, optimized
- ✅ Non-root user (security)
- ✅ Fast startup
- ❌ No source code
- ❌ No hot-reload

## 🔧 Configuration Files

### docker-compose.dev.yml
```yaml
frontend:
  build:
    context: ./frontend
    dockerfile: Dockerfile
    target: development  # ← Targets dev stage
  volumes:
    - ./frontend:/app    # Mount source for hot-reload
```

### docker-compose.yml
```yaml
frontend:
  build:
    context: ./frontend
    dockerfile: Dockerfile
    target: production   # ← Targets prod stage
  # No volumes - uses built code
```

## 💡 Benefits of Unified Approach

### ✅ Advantages

1. **Single Source of Truth**
   - All build logic in one file
   - Easier to maintain consistency
   - Changes affect both environments

2. **Shared Base Stages**
   - DRY principle (Don't Repeat Yourself)
   - Common dependencies cached once
   - Consistent tooling versions

3. **Clear Separation**
   - Named stages are self-documenting
   - Easy to see differences
   - Target selection is explicit

4. **Flexibility**
   - Can build any stage independently
   - Test production build locally
   - Debug intermediate stages

### ⚠️ Considerations

1. **Slightly More Complex**
   - Need to understand stage concept
   - Must specify `--target` when building manually
   - docker-compose handles this automatically

2. **File Size**
   - Single file is longer (~110 lines vs ~30+70)
   - But eliminates duplication

## 🔍 Advanced Usage

### Build Specific Stage for Testing

```bash
# Test just the base stage
docker build --target base -t test:base ./frontend

# Test just the deps stage
docker build --target deps -t test:deps ./frontend

# Test the builder stage
docker build --target builder -t test:builder ./frontend
```

### Inspect Stage Outputs

```bash
# Build and run a specific stage interactively
docker build --target deps -t test:deps ./frontend
docker run -it test:deps /bin/sh

# Inside container, explore what's installed
ls -la
npm list
```

### Cache Optimization

```bash
# Build with BuildKit (better caching)
DOCKER_BUILDKIT=1 docker build --target production ./frontend

# Clear cache and rebuild
docker build --no-cache --target production ./frontend
```

## 📝 Best Practices

### 1. Use docker-compose for Daily Work
```bash
# Development
docker-compose -f docker-compose.dev.yml up

# Production testing
docker-compose up
```

### 2. Explicit Targets in CI/CD
```yaml
# .github/workflows/deploy.yml
- name: Build production image
  run: |
    docker build \
      --target production \
      --tag myregistry/frontend:${{ github.sha }} \
      ./frontend
```

### 3. Layer Caching
```bash
# First build takes longer
docker build --target production -t frontend:prod ./frontend

# Subsequent builds reuse layers (much faster)
docker build --target production -t frontend:prod ./frontend
```

### 4. Development Workflow
```bash
# Start dev environment
docker-compose -f docker-compose.dev.yml up

# Edit code in your IDE
# Changes appear instantly (hot-reload)

# To rebuild after dependency changes:
docker-compose -f docker-compose.dev.yml up --build
```

## 🐛 Troubleshooting

### "Stage not found"
```bash
# Make sure target name matches exactly
docker build --target development ./frontend  # ✅ Correct
docker build --target dev ./frontend          # ❌ Wrong
```

### "Changes not appearing in dev mode"
```bash
# Ensure volume is mounted in docker-compose.dev.yml
volumes:
  - ./frontend:/app
  - /app/node_modules  # Don't overwrite node_modules
```

### "Production build failing"
```bash
# Check if Next.js build succeeds locally
cd frontend
npm run build

# If it fails, fix TypeScript errors first
npm run build 2>&1 | less
```

### "Image too large"
```bash
# Check which target you built
docker images | grep frontend

# Production should be ~150MB
# Development can be ~500MB

# Rebuild with correct target
docker build --target production -t frontend:prod ./frontend
```

## 📚 Related Documentation

- [Docker Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [DOCKER_SETUP_README.md](./DOCKER_SETUP_README.md) - General Docker setup
- [CROSS_PLATFORM_SUMMARY.md](./CROSS_PLATFORM_SUMMARY.md) - Platform support

## 🎓 Quick Reference

```bash
# === BUILD COMMANDS ===

# Development
docker build --target development -t frontend:dev ./frontend

# Production  
docker build --target production -t frontend:prod ./frontend
# or (production is default)
docker build -t frontend:prod ./frontend

# === RUN COMMANDS ===

# Development (with source mounted)
docker run -p 3000:3000 -v $(pwd)/frontend:/app frontend:dev

# Production
docker run -p 3000:3000 frontend:prod

# === DOCKER-COMPOSE (RECOMMENDED) ===

# Development
docker-compose -f docker-compose.dev.yml up

# Production
docker-compose up -d
```

---

**Summary:** One Dockerfile, multiple targets, maximum flexibility! 🎯

