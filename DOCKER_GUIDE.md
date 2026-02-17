# Docker Guide - Policy AI Lens

Complete guide to Docker containerization and deployment for the Policy AI Lens project.

## 📚 Table of Contents
1. [What is Docker?](#what-is-docker)
2. [Project Docker Architecture](#project-docker-architecture)
3. [Prerequisites](#prerequisites)
4. [Quick Start](#quick-start)
5. [Understanding Docker Files](#understanding-docker-files)
6. [Running Containers](#running-containers)
7. [Development vs Production](#development-vs-production)
8. [Troubleshooting](#troubleshooting)
9. [Deployment to Production](#deployment-to-production)

---

## What is Docker?

### The Problem Docker Solves

**Traditional deployment:**
```
Developer: "Works on my machine!" 🤷
Server Admin: "Doesn't work on production..." 😫
```

**With Docker:**
- ✅ Same environment everywhere (dev, staging, production)
- ✅ No "works on my machine" issues
- ✅ Easy to scale and deploy

### Key Docker Concepts

#### 1. **Image** 📦
- A blueprint/template for a container
- Like a snapshot of your application + dependencies
- Built once, run anywhere
- Example: `policy-ai-lens-backend:latest`

#### 2. **Container** 🚢
- Running instance of an image
- Isolated environment (own filesystem, network, processes)
- Lightweight (shares host OS kernel)
- Multiple containers from one image

#### 3. **Dockerfile** 📝
- Recipe to build an image
- Instructions: install dependencies, copy files, set environment
- Each instruction creates a layer

#### 4. **Docker Compose** 🎼
- Tool for multi-container applications
- Define services, networks, volumes in one YAML file
- Start everything with one command

#### 5. **Volume** 💾
- Persistent storage
- Data survives container restarts/removal
- Share data between host and container

#### 6. **Network** 🌐
- Allows containers to communicate
- Isolated from other Docker networks
- Service name = hostname

---

## Project Docker Architecture

```
┌─────────────────────────────────────────────────┐
│  Docker Compose (Orchestration)                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌─────────────────┐    ┌─────────────────┐   │
│  │  Frontend       │    │  Backend        │   │
│  │  (Nginx)        │───▶│  (FastAPI)      │   │
│  │                 │    │                 │   │
│  │  Port: 3000:80  │    │  Port: 8000     │   │
│  │  Size: ~40MB    │    │  Size: ~400MB   │   │
│  └─────────────────┘    └─────────────────┘   │
│          │                       │             │
│      HTML/JS/CSS           Python/API          │
│                                                 │
│  Network: policy-ai-lens-network               │
│                                                 │
│  Volumes:                                      │
│    - credentials/ (backend)                    │
│    - uploads/ (backend)                        │
│    - results.json (backend)                    │
└─────────────────────────────────────────────────┘
         ▲                      ▲
         │                      │
    localhost:3000        localhost:8000
```

---

## Prerequisites

### 1. Install Docker Desktop

**Windows/Mac:**
- Download: [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Install and start Docker Desktop
- Verify: Open terminal/PowerShell and run:
  ```bash
  docker --version
  docker-compose --version
  ```

**Linux:**
```bash
# Install Docker Engine
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Project Requirements

- ✅ `.env.prod` file in `backend/envs/`
- ✅ Service account JSON in `backend/credentials/`
- ✅ Docker Desktop running

---

## Quick Start

### Option 1: Using Docker Compose (Recommended)

**Start both frontend and backend:**
```bash
# From project root
docker-compose up --build
```

**Access:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

**Stop (Ctrl+C or):**
```bash
docker-compose down
```

### Option 2: Individual Containers

**Backend only:**
```bash
cd backend
docker build -t policy-ai-lens-backend .
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=your_key \
  -e GOOGLE_SHEET_ID=your_sheet_id \
  -v $(pwd)/credentials:/app/credentials \
  policy-ai-lens-backend
```

**Frontend only:**
```bash
cd frontend
docker build -t policy-ai-lens-frontend \
  --build-arg VITE_API_BASE_URL=http://localhost:8000 \
  .
docker run -p 3000:80 policy-ai-lens-frontend
```

---

## Understanding Docker Files

### Backend Dockerfile

Located: `backend/Dockerfile`

**Key stages:**
1. **Base image** - Python 3.11 slim
2. **System dependencies** - GCC, MuPDF, Tesseract
3. **Python dependencies** - Install from requirements.txt
4. **App code** - Copy application files
5. **Runtime** - Start uvicorn server

**Important concepts:**
```dockerfile
# Layer caching - Copy requirements first
COPY requirements.txt .
RUN pip install -r requirements.txt
# If requirements don't change, this layer is cached

# Copy code after (changes often, won't bust cache above)
COPY ./app ./app
```

**Why slim image?**
- `python:3.11` = 900MB
- `python:3.11-slim` = 150MB
- Saves storage, bandwidth, build time

### Frontend Dockerfile

Located: `frontend/Dockerfile`

**Multi-stage build:**

**Stage 1 - Build (node:18-alpine):**
- Install dependencies
- Build React/Vite app
- Output: `/app/dist` folder

**Stage 2 - Production (nginx:alpine):**
- Copy built files from Stage 1
- Serve with nginx
- Final image: ~40MB (only static files + nginx)

**Why multi-stage?**
```
Single stage:  Node + build tools + source + built files = 1.5GB
Multi-stage:   Only nginx + built files               = 40MB
Reduction: 97% smaller!
```

### docker-compose.yml

Located: Project root

**Defines two services:**

```yaml
services:
  backend:
    build: ./backend
    ports: "8000:8000"
    volumes:
      - ./backend/credentials:/app/credentials
    networks:
      - policy-ai-lens-network
  
  frontend:
    build: ./frontend
    ports: "3000:80"
    depends_on:
      - backend  # Wait for backend first
    networks:
      - policy-ai-lens-network
```

**Key features:**
- **Networks**: Containers communicate via service names
- **Volumes**: Persist data outside containers
- **Depends_on**: Control startup order
- **Health checks**: Monitor container health

---

## Running Containers

### Docker Compose Commands

**Build and start:**
```bash
docker-compose up --build
```
- Builds images from Dockerfiles
- Creates containers
- Starts services
- Shows logs

**Start in background (detached mode):**
```bash
docker-compose up -d
```
- Runs containers in background
- Returns terminal control

**View logs:**
```bash
docker-compose logs -f          # All services, follow
docker-compose logs backend     # Just backend
docker-compose logs --tail=50   # Last 50 lines
```

**Stop containers:**
```bash
docker-compose down             # Stop and remove containers
docker-compose down -v          # Also remove volumes
docker-compose stop             # Just stop (keep containers)
```

**Rebuild specific service:**
```bash
docker-compose build backend    # Rebuild backend image
docker-compose up -d backend    # Restart backend container
```

**Check status:**
```bash
docker-compose ps               # Running services
docker-compose top              # What's running in containers
```

**Execute commands in containers:**
```bash
docker-compose exec backend python -c "print('Hello')"
docker-compose exec backend bash  # Open shell in backend
docker-compose exec frontend sh   # Open shell in frontend (alpine has sh)
```

### Direct Docker Commands

**List images:**
```bash
docker images
```

**List containers:**
```bash
docker ps          # Running containers
docker ps -a       # All containers (including stopped)
```

**Remove images/containers:**
```bash
docker rm <container_id>        # Remove container
docker rmi <image_id>           # Remove image
docker system prune -a          # Clean up everything (careful!)
```

**Inspect container:**
```bash
docker inspect <container_name>
docker logs <container_name>
```

---

## Development vs Production

### Development

**Using local files (no Docker):**
```bash
# Backend
cd backend
python -m uvicorn app.main:app --reload

# Frontend
cd frontend
npm run dev
```

**Benefits:**
- Fast iteration (no rebuild)
- Hot reload
- Direct debugging

### Production (Docker)

**Build once, deploy anywhere:**
```bash
docker-compose up --build
```

**Benefits:**
- Consistent environment
- Easy deployment
- Isolation
- Scalability

### Best Practice

- **Develop**: Use local setup for coding/testing
- **Test**: Use Docker locally to verify it works
- **Deploy**: Use Docker in production

---

## Troubleshooting

### Container won't start

**Check logs:**
```bash
docker-compose logs backend
```

**Common issues:**
- Missing environment variables
- Port already in use
- Invalid credentials path

### Frontend can't reach backend

**Check network:**
```bash
docker-compose exec frontend ping backend
```

**Verify:**
- Both containers in same network
- Backend is healthy: `docker-compose ps`
- CORS settings allow frontend URL

### Volume permission issues

**Fix ownership:**
```bash
# Linux/Mac
sudo chown -R $(id -u):$(id -g) backend/uploads

# Windows - usually not an issue
```

### "Address already in use"

**Find process using port:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

### Cache/rebuild issues

**Clean rebuild:**
```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

### Out of disk space

**Clean Docker:**
```bash
docker system df                      # Check usage
docker system prune -a --volumes      # Remove everything unused
```

---

## Deployment to Production

### Platform Options

#### 1. **Railway** (Easiest)
- Auto-detects Dockerfile
- Built-in environment variables
- Free tier available

**Steps:**
1. Push code to GitHub
2. Connect Railway to GitHub
3. Deploy backend and frontend separately
4. Set environment variables in Railway dashboard

#### 2. **Render** (Similar to Railway)
- Dockerfile support
- Free tier with limitations
- Good for small apps

#### 3. **AWS ECS / Google Cloud Run** (Advanced)
- More control and scalability
- Requires more setup
- Production-grade

### Deployment Checklist

- [ ] `.env.prod` has production values
- [ ] Service account JSON uploaded to platform
- [ ] Environment variables set on platform
- [ ] CORS includes production frontend URL
- [ ] Build succeeds locally
- [ ] Health checks working
- [ ] Separate dev and production Google Sheets

### Environment Variables for Production

**Backend:**
```env
GEMINI_API_KEY=<production_key>
APP_ENV=prod
DEBUG=False
GOOGLE_SHEET_ID=<production_sheet_id>
GOOGLE_SHEETS_CREDENTIALS_FILE=/app/credentials/prod-creds.json
CORS_ORIGINS=["https://your-frontend.vercel.app"]
```

**Frontend build args:**
```bash
VITE_API_BASE_URL=https://your-backend.railway.app
VITE_APP_ENV=production
```

---

## Docker Cheat Sheet

### Most Used Commands

```bash
# Build and start
docker-compose up --build

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Rebuild one service
docker-compose build backend
docker-compose up -d backend

# Execute command in container
docker-compose exec backend python script.py

# Clean everything
docker-compose down -v
docker system prune -a
```

### Debugging

```bash
# Shell access
docker-compose exec backend bash
docker-compose exec frontend sh

# Check container status
docker-compose ps

# View resource usage
docker stats

# Inspect container
docker inspect policy-ai-lens-backend
```

---

## Learning Resources

### Official Documentation
- [Docker Docs](https://docs.docker.com/)
- [Docker Compose Docs](https://docs.docker.com/compose/)

### Tutorials
- [Docker 101](https://www.docker.com/101-tutorial/)
- [Docker for Beginners](https://docker-curriculum.com/)

### Best Practices
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

---

## Summary

**What we've containerized:**
- ✅ Backend (FastAPI + Python)
- ✅ Frontend (React + Nginx)
- ✅ Orchestration (Docker Compose)

**Benefits achieved:**
- 🚀 Consistent environment across dev and production
- 📦 Easy deployment to any Docker-compatible platform
- 🔄 Simple updates (rebuild image, restart container)
- 📊 Scalability (run multiple containers)
- 🔒 Isolation (dependencies don't conflict)

**Next steps:**
1. Test locally: `docker-compose up --build`
2. Verify both services work
3. Choose deployment platform
4. Deploy to production
5. Add Google Sheets Apps Script for reminders

Ready to test your Docker setup! 🐳
