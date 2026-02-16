# Environment Setup Guide

This document explains the environment configuration for both **development** (dev branch) and **production** (main branch).

## Overview

- **Development (dev branch)**: Local development using `.env.dev` and `.env.development`
- **Production (main branch)**: Deployed using GitHub secrets and hosting platform environment variables

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Development (dev)                        │
├─────────────────────────────────────────────────────────────┤
│  Backend: localhost:8000 (.env.dev)                         │
│  Frontend: localhost:5173 (.env.development)                │
│  Google Sheets: Dev sheet                                    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    Production (main)                         │
├─────────────────────────────────────────────────────────────┤
│  Backend: Render/Railway (.env.prod + GitHub Secrets)       │
│  Frontend: Vercel (GitHub Secrets)                          │
│  Google Sheets: Production sheet                            │
│  Deployment: Automatic via GitHub Actions                   │
└─────────────────────────────────────────────────────────────┘
```

## Files Created

### Backend
- ✅ `backend/envs/.env.dev` - Development environment (not tracked)
- ✅ `backend/envs/.env.prod` - Production template (not tracked)
- ✅ `backend/envs/.env.example` - Template for both environments
- ✅ `backend/app/config.py` - Updated to load correct env file based on `APP_ENV`

### Frontend
- ✅ `frontend/.env.development` - Development environment (not tracked)
- ✅ `frontend/.env.production` - Production template (not tracked)
- ✅ `frontend/.env.example` - Template for both environments
- ✅ `frontend/src/services/apiConfig.ts` - Centralized API configuration
- ✅ Updated all components to use `apiConfig` instead of hardcoded URLs

### CI/CD
- ✅ `.github/workflows/dev-ci.yml` - CI checks for dev branch
- ✅ `.github/workflows/production-deploy.yml` - Deployment for main branch
- ✅ `.github/workflows/README.md` - Workflow documentation
- ✅ `.gitignore` - Updated to exclude env files but keep examples

## Current Configuration Status

### Backend Environment Variables

| Variable | Dev (.env.dev) | Production (.env.prod) | Source |
|----------|----------------|------------------------|--------|
| `GEMINI_API_KEY` | ✅ Set | ⏳ To be filled | Local / GitHub Secret |
| `APP_ENV` | `development` | `production` | Environment file |
| `DEBUG` | `True` | `False` | Environment file |
| `GOOGLE_SHEET_ID` | `your_dev_sheet_id_here` | ⏳ To be filled | Local / GitHub Secret |
| `GOOGLE_SHEETS_CREDENTIALS_FILE` | `path/to/credentials.json` | ⏳ To be filled | Local / GitHub Secret |
| `CORS_ORIGINS` | `["http://localhost:5173","http://localhost:3000"]` | ⏳ To be filled | GitHub Secret |

### Frontend Environment Variables

| Variable | Dev (.env.development) | Production (.env.production) | Source |
|----------|------------------------|------------------------------|--------|
| `VITE_API_BASE_URL` | `http://localhost:8000` | ⏳ To be filled | Local / Vercel Dashboard |
| `VITE_APP_ENV` | `development` | `production` | Environment file |

## How It Works

### Development Workflow (dev branch)

1. **Backend**: Reads `backend/envs/.env.dev` automatically
   - `config.py` checks `os.getenv("APP_ENV", "development")` → defaults to "development"
   - Loads `envs/.env.development`

2. **Frontend**: Vite automatically reads `.env.development` in dev mode
   - Components use `apiConfig.endpoints.upload`, `apiConfig.endpoints.extract()`, etc.
   - Points to `http://localhost:8000`

3. **No CI/CD**: Just local development, manual testing

### Production Workflow (main branch)

1. **Push to main** triggers `.github/workflows/production-deploy.yml`

2. **Backend Deployment**:
   - GitHub Actions creates `.env.prod` from GitHub Secrets
   - Deploys to Render/Railway
   - Platform sets `APP_ENV=production` → loads `.env.prod`

3. **Frontend Deployment**:
   - GitHub Actions builds with production env vars from secrets
   - Deploys to Vercel
   - Vercel environment variables override `.env.production`

4. **Environment Variables**: Sourced from:
   - GitHub Secrets (for GitHub Actions)
   - Hosting platform environment settings (Render/Railway/Vercel)

## Setup Instructions

### 1. Local Development Setup

#### Backend
```bash
cd backend/envs
# .env.dev already exists with your API key
# Update Google Sheets values when ready:
# GOOGLE_SHEET_ID=your_dev_sheet_id
# GOOGLE_SHEETS_CREDENTIALS_FILE=path/to/dev-credentials.json
```

#### Frontend
```bash
cd frontend
# .env.development already exists with localhost:8000
# No changes needed for now
```

### 2. Production Setup (Do Later)

#### A. Create GitHub Secrets
Go to: **GitHub Repo → Settings → Secrets and variables → Actions**

Add these secrets:

**Backend:**
- `GEMINI_API_KEY` - Your production Gemini API key
- `GOOGLE_SHEET_ID` - Production Google Sheet ID
- `GOOGLE_SHEETS_CREDENTIALS_FILE` - Path like `/app/credentials/prod-creds.json`
- `CORS_ORIGINS` - `["https://your-vercel-app.vercel.app"]`

**Frontend:**
- `VITE_API_BASE_URL` - Your backend URL (e.g., `https://your-backend.onrender.com`)
- `VERCEL_TOKEN` - From Vercel dashboard
- `VERCEL_ORG_ID` - From Vercel project settings
- `VERCEL_PROJECT_ID` - From Vercel project settings

**Deployment Platform (choose one):**
- `RAILWAY_TOKEN` or `RENDER_DEPLOY_HOOK_URL`

#### B. Backend Hosting (Render/Railway)

**Option 1: Render**
1. Create Web Service, connect GitHub
2. Settings:
   - Branch: `main`
   - Root: `backend`
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. Add all env vars in Render dashboard
4. Get deploy hook URL → add to GitHub secrets

**Option 2: Railway**
1. Create project, connect GitHub
2. Configure similar to Render
3. Add env vars in Railway dashboard
4. Get API token → add to GitHub secrets

#### C. Frontend Hosting (Vercel)

1. Create project, connect GitHub
2. Settings:
   - Framework: Vite
   - Root: `frontend`
   - Build: `npm run build`
   - Output: `dist`
3. Add env vars in Vercel:
   - `VITE_API_BASE_URL`
   - `VITE_APP_ENV=production`
4. Get tokens:
   - Settings → Tokens → Create
   - Project Settings → Copy IDs
5. Add to GitHub secrets

## Next Steps

You indicated these next steps:

✅ **Set up Google Sheets API & credentials** - Next
✅ **Implement Google Sheets storage in code** - After API setup
✅ **Create Dockerfile for backend** - For deployment
✅ **Deploy backend to Render/Railway** - When ready
✅ **Deploy frontend to Vercel** - When ready

## Testing

### Test Local Development
```bash
# Terminal 1: Backend
cd backend
python -m uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

### Test Production Configuration (locally)
```bash
# Backend with production env (don't commit .env.prod with real values)
export APP_ENV=production  # or $env:APP_ENV="production" in PowerShell
cd backend
python -m uvicorn app.main:app --reload

# Frontend production build
cd frontend
npm run build
npm run preview
```

### Test GitHub Actions
1. **Dev branch**: Push changes → check CI passes
2. **Main branch**: Merge to main → check deployment succeeds

## Important Notes

1. **Never commit actual .env files** - They contain secrets
2. **Only .env.example should be in git** - Templates only
3. **GitHub Secrets are encrypted** - Safe for production secrets
4. **Hosting platforms have their own env vars** - Can override .env files
5. **APP_ENV determines which .env file loads** - development vs production

## Troubleshooting

### Backend won't start
- Check `APP_ENV` environment variable
- Verify correct `.env.{APP_ENV}` file exists
- Check all required variables are set

### Frontend can't connect to backend
- Check `VITE_API_BASE_URL` in relevant .env file
- Verify backend CORS allows your frontend URL
- Check network/firewall settings

### Deployment fails
- Check GitHub Actions logs
- Verify all secrets are set correctly
- Check hosting platform logs

## Summary

✅ **Environment separation complete**
- Dev uses `.env.dev` and `.env.development`
- Production uses GitHub Secrets and hosting platform env vars
- Config automatically loads correct environment

✅ **CI/CD workflows ready**
- Dev branch: Runs CI checks only
- Main branch: Deploys to production

✅ **All placeholder values ready**
- Fill in production values when ready to deploy
- Local development works now with existing values

**Ready to proceed with Google Sheets integration!** 🚀
