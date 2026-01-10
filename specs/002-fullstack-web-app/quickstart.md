# Quickstart Guide: Full-Stack Web Application

**Feature**: Full-Stack Web Application
**Branch**: 002-fullstack-web-app
**Date**: 2026-01-03

---

## Overview

This guide walks you through setting up and running the full-stack Todo application on your local machine using Docker Compose. The application consists of a Next.js frontend, FastAPI backend, and Neon PostgreSQL database.

**Time to First Run**: ~10 minutes

---

## Prerequisites

### Required Software

| Software | Minimum Version | Purpose | Installation Link |
|----------|----------------|---------|-------------------|
| **Docker** | 24.0+ | Container runtime | [Get Docker](https://docs.docker.com/get-docker/) |
| **Docker Compose** | 2.20+ | Multi-container orchestration | Included with Docker Desktop |
| **Git** | 2.40+ | Version control | [Download Git](https://git-scm.com/downloads) |

### Optional (for development without Docker)

| Software | Version | Purpose |
|----------|---------|---------|
| Node.js | 20+ | Frontend development |
| Python | 3.13+ | Backend development |
| pnpm/npm | Latest | Node package manager |
| uv | Latest | Python package manager |

### External Services

- **Neon PostgreSQL Database** (required):
  - Sign up at [neon.tech](https://neon.tech)
  - Create a new project
  - Copy connection string (format: `postgresql://user:password@host/dbname`)

---

## Quick Start (Docker Compose)

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd todo-web-app
git checkout 002-fullstack-web-app
```

### Step 2: Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and fill in required values:
   ```bash
   # Database
   DATABASE_URL=postgresql+asyncpg://user:password@host.neon.tech:5432/dbname?sslmode=require

   # Authentication (generate a secure random string)
   JWT_SECRET=your-super-secret-jwt-key-min-32-chars

   # API Configuration
   BACKEND_PORT=8000
   FRONTEND_PORT=3000

   # Frontend (for API calls)
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

   **Generate JWT Secret** (Linux/macOS):
   ```bash
   openssl rand -base64 32
   ```

   **Generate JWT Secret** (Windows PowerShell):
   ```powershell
   -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | % {[char]$_})
   ```

### Step 3: Start Application

```bash
docker-compose up --build
```

**Expected Output**:
```
backend_1   | INFO:     Uvicorn running on http://0.0.0.0:8000
frontend_1  | ✓ Ready in 2.1s
```

### Step 4: Verify Services

1. **Backend API**: http://localhost:8000/health
   ```json
   {"status": "healthy"}
   ```

2. **Frontend**: http://localhost:3000
   - Should see landing/login page

3. **API Documentation**: http://localhost:8000/docs
   - Interactive Swagger UI

---

## First-Time Setup

### Create Your First User

1. Open http://localhost:3000/register
2. Fill in registration form:
   - Email: `user@example.com`
   - Password: `SecurePass123` (min 8 chars, 1 letter, 1 number)
3. Click "Register"
4. You'll be redirected to task dashboard

### Create Your First Task

1. In task dashboard, click "New Task"
2. Fill in:
   - Title: `My First Task`
   - Description: `Testing the application`
3. Click "Create"
4. Task appears in your task list

---

## Development Workflow

### Running with Auto-Reload

Both frontend and backend support hot-reload during development:

```bash
# Start with live reload
docker-compose up

# Backend changes auto-reload (FastAPI --reload flag)
# Frontend changes auto-reload (Next.js fast refresh)
```

### Viewing Logs

```bash
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend
```

### Stopping Services

```bash
# Graceful shutdown
docker-compose down

# Remove volumes (reset database)
docker-compose down -v
```

### Rebuilding After Changes

```bash
# Rebuild all containers
docker-compose up --build

# Rebuild specific service
docker-compose up --build backend
```

---

## Running Tests

### Backend Tests

```bash
# Run pytest in backend container
docker-compose exec backend pytest

# Run with coverage
docker-compose exec backend pytest --cov=src

# Run specific test file
docker-compose exec backend pytest tests/test_auth.py
```

### Frontend Tests

```bash
# Run Jest tests in frontend container
docker-compose exec frontend npm test

# Run with coverage
docker-compose exec frontend npm test -- --coverage

# Run specific test file
docker-compose exec frontend npm test -- TaskList.test.tsx
```

---

## Accessing Services

### Service URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | Web application UI |
| Backend API | http://localhost:8000 | REST API |
| API Docs (Swagger) | http://localhost:8000/docs | Interactive API documentation |
| API Docs (ReDoc) | http://localhost:8000/redoc | Alternative API documentation |
| Health Check | http://localhost:8000/health | Backend health status |

### Database Access

```bash
# Connect to Neon database via psql
psql "postgresql://user:password@host.neon.tech:5432/dbname?sslmode=require"

# List tables
\dt

# View users
SELECT * FROM users;

# View tasks
SELECT * FROM tasks;
```

---

## Common Tasks

### Reset Database

```bash
# 1. Stop services
docker-compose down

# 2. Connect to Neon and drop tables
psql $DATABASE_URL -c "DROP TABLE IF EXISTS tasks CASCADE; DROP TABLE IF EXISTS users CASCADE;"

# 3. Restart (tables recreated on startup)
docker-compose up
```

### View Container Shell

```bash
# Backend shell
docker-compose exec backend /bin/bash

# Frontend shell
docker-compose exec frontend /bin/sh
```

### Check Environment Variables

```bash
# Backend env
docker-compose exec backend env | grep -E '(DATABASE_URL|JWT_SECRET)'

# Frontend env
docker-compose exec frontend env | grep -E '(NEXT_PUBLIC|JWT_SECRET)'
```

---

## Troubleshooting

### Issue: "Port already in use"

**Symptom**: `Error starting userland proxy: listen tcp4 0.0.0.0:3000: bind: address already in use`

**Solution**:
```bash
# Find process using port
lsof -i :3000  # macOS/Linux
netstat -ano | findstr :3000  # Windows

# Kill process or change port in .env
FRONTEND_PORT=3001
```

### Issue: "Database connection failed"

**Symptom**: `asyncpg.exceptions.InvalidCatalogNameError: database "..." does not exist`

**Solution**:
1. Verify DATABASE_URL in `.env` is correct
2. Check Neon dashboard that database exists
3. Ensure connection string includes `?sslmode=require`
4. Test connection manually: `psql $DATABASE_URL`

### Issue: "JWT token invalid"

**Symptom**: API returns `401 Unauthorized` after login

**Solution**:
1. Ensure JWT_SECRET is identical in frontend and backend
2. Check `.env` file has no trailing spaces
3. Restart both services: `docker-compose restart`

### Issue: "Module not found"

**Symptom**: Backend/Frontend fails to start with import errors

**Solution**:
```bash
# Rebuild containers with --no-cache
docker-compose build --no-cache

# Reinstall dependencies
docker-compose run backend pip install -r requirements.txt
docker-compose run frontend npm install
```

### Issue: "CORS error"

**Symptom**: Frontend can't call backend API

**Solution**:
1. Verify NEXT_PUBLIC_API_URL matches backend URL
2. Check backend CORS middleware allows frontend origin
3. Restart services after environment changes

### Issue: Docker Compose not found

**Symptom**: `docker-compose: command not found`

**Solution**:
- Docker Desktop includes Docker Compose
- Alternatively, use `docker compose` (no hyphen) - newer syntax

---

## Environment Variables Reference

### Backend (.env)

| Variable | Required | Example | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | `postgresql+asyncpg://...` | Neon PostgreSQL connection string |
| `JWT_SECRET` | Yes | `abc123...` (min 32 chars) | Shared secret for JWT signing/verification |
| `BACKEND_PORT` | No | `8000` | Port for backend API |
| `LOG_LEVEL` | No | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |

### Frontend (.env)

| Variable | Required | Example | Description |
|----------|----------|---------|-------------|
| `NEXT_PUBLIC_API_URL` | Yes | `http://localhost:8000` | Backend API base URL |
| `JWT_SECRET` | Yes | `abc123...` | Shared secret (must match backend) |
| `FRONTEND_PORT` | No | `3000` | Port for frontend dev server |

---

## Performance Tips

### Optimize Docker Build Times

1. **Use Docker Layer Caching**:
   ```bash
   # First build is slow, subsequent builds are fast
   docker-compose build --parallel
   ```

2. **Persist Dependencies**:
   - `node_modules` and `__pycache__` are in `.dockerignore`
   - Dependencies installed in container layers (cached)

### Optimize Application Performance

1. **Database Connection Pooling**: Already configured (10 connections, 20 overflow)
2. **Frontend Production Build**:
   ```bash
   docker-compose -f docker-compose.prod.yml up
   ```

---

## Next Steps

### Development

1. Review API documentation: http://localhost:8000/docs
2. Explore codebase structure (see `plan.md`)
3. Run tests to verify setup
4. Create additional users to test multi-user isolation

### Production Deployment

1. Set up environment-specific `.env` files
2. Use production Docker Compose file
3. Configure HTTPS/TLS certificates
4. Set up monitoring and logging
5. Review security checklist

---

## Additional Resources

- **API Contract**: [contracts/api-spec.yaml](./contracts/api-spec.yaml)
- **Data Model**: [data-model.md](./data-model.md)
- **Implementation Plan**: [plan.md](./plan.md)
- **Feature Specification**: [spec.md](./spec.md)

---

## Getting Help

### Check Logs First

```bash
# All logs
docker-compose logs

# Last 100 lines
docker-compose logs --tail=100

# Follow logs
docker-compose logs -f
```

### Verify Configuration

```bash
# Print effective configuration
docker-compose config
```

### Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# Frontend (should return HTML)
curl http://localhost:3000
```

---

## Clean Up

### Remove Everything

```bash
# Stop and remove containers, networks, volumes
docker-compose down -v

# Remove images
docker-compose down --rmi all

# Remove all Docker data (CAUTION: affects all projects)
docker system prune -a
```

---

## Summary

✅ **Installation**: 5 minutes (Docker + dependencies)
✅ **Configuration**: 2 minutes (`.env` file)
✅ **First Run**: 2 minutes (build + start)
✅ **First Task**: 1 minute (register + create)

**Total Time to Productive**: ~10 minutes

**Ready to develop!** 🚀
