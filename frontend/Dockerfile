# ============================================
# MULTI-STAGE BUILD for Frontend
# ============================================
# Why multi-stage? Build the React app, then serve only the built files
# Result: Build tools stay in build stage, final image only has static files + nginx

# ============================================
# STAGE 1: Build Stage
# ============================================
# Use Node.js to build the React/Vite application
FROM node:18-alpine AS build

# Why 'alpine'? It's a minimal Linux distro (~5MB vs ~900MB for full Node)
# alpine = Smaller images, faster builds, less attack surface

# Set working directory
WORKDIR /app

# Copy package files first (layer caching optimization)
# If package.json/package-lock.json don't change, npm install is cached
COPY package*.json ./

# Install dependencies
# npm ci = Clean install (faster & more reliable than npm install)
# Uses package-lock.json for exact versions
RUN npm ci

# Copy application source code
COPY . .

# Build arguments (passed during docker build)
# These become environment variables during build
ARG VITE_API_BASE_URL=http://localhost:8000
ARG VITE_APP_ENV=production

# Set environment variables for the build
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
ENV VITE_APP_ENV=$VITE_APP_ENV

# Build the production bundle
# Vite outputs to /app/dist
RUN npm run build

# ============================================
# STAGE 2: Production Stage (Nginx)
# ============================================
# Use nginx to serve the static files
FROM nginx:alpine AS production

# Why nginx? Lightweight, fast static file server
# Why alpine nginx? Minimal image (~24MB)

# Copy built files from build stage to nginx html directory
# --from=build: Copy from the 'build' stage
COPY --from=build /app/dist /usr/share/nginx/html

# Copy custom nginx configuration
# This handles React Router (client-side routing)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 (nginx default HTTP port)
EXPOSE 80

# Health check - ensure nginx is serving files
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost/ || exit 1

# nginx starts automatically with alpine image
# No CMD needed - nginx:alpine already has: CMD ["nginx", "-g", "daemon off;"]

# ============================================
# BUILD INSTRUCTIONS:
# ============================================
# From frontend directory:
#   docker build -t policy-ai-lens-frontend \
#     --build-arg VITE_API_BASE_URL=http://localhost:8000 \
#     .
#
# For production with real backend URL:
#   docker build -t policy-ai-lens-frontend \
#     --build-arg VITE_API_BASE_URL=https://your-backend.onrender.com \
#     --build-arg VITE_APP_ENV=production \
#     .
#
# RUN INSTRUCTIONS:
#   docker run -p 3000:80 policy-ai-lens-frontend
#
# Then open: http://localhost:3000
#
# EXPLANATION:
# -p 3000:80  : Map container port 80 to host port 3000
#               (Nginx serves on 80, we access via 3000)
# ============================================

# ============================================
# SIZE COMPARISON:
# ============================================
# Without multi-stage: ~1.5GB (includes Node + all build tools)
# With multi-stage:    ~40MB  (only nginx + static files)
# Reduction: 97% smaller!
# ============================================
