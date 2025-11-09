# Unified Frontend Dockerfile for JobPortal
# Supports both development and production builds
# Cross-platform: Apple Silicon (ARM64), Intel/AMD (x86_64), Windows
#
# Usage:
#   Development:  docker build --target development -t jobportal-frontend:dev .
#   Production:   docker build --target production -t jobportal-frontend:prod .
#   (or just):    docker build -t jobportal-frontend:prod .

# =============================================================================
# Base stage - shared dependencies
# =============================================================================
FROM node:18-alpine AS base

# Install compatibility libraries
RUN apk add --no-cache libc6-compat

WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# =============================================================================
# Dependencies stage - Install node_modules
# =============================================================================
FROM base AS deps

# Install all dependencies (including devDependencies)
RUN npm ci

# =============================================================================
# Development stage - For local development with hot-reload
# Target this stage for development: --target development
# =============================================================================
FROM base AS development

# Copy all dependencies
COPY --from=deps /app/node_modules ./node_modules

# Copy application source
COPY . .

# Set development environment
ENV NODE_ENV=development
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

# Expose port
EXPOSE 3000

# Run development server with hot-reload
CMD ["npm", "run", "dev"]

# =============================================================================
# Builder stage - Build the production application
# =============================================================================
FROM base AS builder

# Copy dependencies
COPY --from=deps /app/node_modules ./node_modules

# Copy application source
COPY . .

# Set build-time environment
ENV NEXT_TELEMETRY_DISABLED=1

# Build the Next.js application
RUN npm run build

# =============================================================================
# Production stage - Optimized runtime (default target)
# Target this stage for production: --target production (or omit --target)
# =============================================================================
FROM node:18-alpine AS production

WORKDIR /app

# Set production environment
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

# Create non-root user for security
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Copy necessary files from builder
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./package.json

# Copy built application with proper ownership
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# Switch to non-root user
USER nextjs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000', (res) => {process.exit(res.statusCode === 200 ? 0 : 1)})"

# Run the production server
CMD ["node", "server.js"]

