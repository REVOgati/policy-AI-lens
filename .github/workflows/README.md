# GitHub Actions Workflows

This directory contains CI/CD workflows for the Policy AI Lens project.

## Workflows

### 1. `dev-ci.yml` - Development CI
- **Trigger**: Pushes to `dev` branch, PRs to `dev` or `main`
- **Purpose**: Run linting, type checking, and tests
- **No deployment**: Only validates code quality

### 2. `production-deploy.yml` - Production Deployment
- **Trigger**: Pushes to `main` branch
- **Purpose**: Deploy backend and frontend to production
- **Deployment targets**:
  - Backend: Render/Railway
  - Frontend: Vercel

## Required GitHub Secrets

Configure these secrets in your GitHub repository settings:
**Settings → Secrets and variables → Actions → New repository secret**

### Backend Secrets
| Secret Name | Description | Example |
|------------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key for production | `AIza...` |
| `GOOGLE_SHEETS_CREDENTIALS_FILE` | Path to Google Sheets credentials in production | `/app/credentials/prod-creds.json` |
| `GOOGLE_SHEET_ID` | Production Google Sheet ID | `1a2b3c...` |
| `CORS_ORIGINS` | Allowed frontend URLs (JSON array) | `["https://your-app.vercel.app"]` |

### Frontend Secrets
| Secret Name | Description | Example |
|------------|-------------|---------|
| `VITE_API_BASE_URL` | Production backend URL | `https://your-backend.onrender.com` |
| `VERCEL_TOKEN` | Vercel deployment token | Get from Vercel dashboard |
| `VERCEL_ORG_ID` | Vercel organization ID | Get from Vercel project settings |
| `VERCEL_PROJECT_ID` | Vercel project ID | Get from Vercel project settings |

### Deployment Platform Secrets (Choose One)
#### For Railway:
| Secret Name | Description |
|------------|-------------|
| `RAILWAY_TOKEN` | Railway API token |

#### For Render:
| Secret Name | Description |
|------------|-------------|
| `RENDER_DEPLOY_HOOK_URL` | Render deploy hook URL |

## Setup Instructions

### 1. Backend Deployment (Render/Railway)

#### Option A: Render
1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure:
   - Branch: `main`
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables in Render dashboard
5. Get deploy hook URL and add to GitHub secrets as `RENDER_DEPLOY_HOOK_URL`

#### Option B: Railway
1. Create a new project on Railway
2. Connect your GitHub repository
3. Configure build and start commands
4. Add environment variables in Railway dashboard
5. Get API token and add to GitHub secrets as `RAILWAY_TOKEN`

### 2. Frontend Deployment (Vercel)

1. Create a new project on Vercel
2. Connect your GitHub repository
3. Configure:
   - Framework Preset: Vite
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
4. Add environment variables in Vercel dashboard:
   - `VITE_API_BASE_URL`: Your backend URL
   - `VITE_APP_ENV`: `production`
5. Get deployment tokens:
   - Settings → Tokens → Create token
   - Project Settings → General → Copy Project ID and Org ID
6. Add to GitHub secrets

### 3. Google Sheets Setup

1. Create a Google Cloud project
2. Enable Google Sheets API
3. Create a Service Account
4. Download credentials JSON
5. For production:
   - Upload credentials to your backend hosting (Render/Railway)
   - Note the file path
   - Add path to `GOOGLE_SHEETS_CREDENTIALS_FILE` secret
6. Create separate Google Sheets for dev and production
7. Share sheets with service account email
8. Add sheet IDs to respective environment files

## Local Development

Local development uses `.env.dev` and `.env.development` files (not tracked in git).

### Backend (.env.dev)
```bash
cd backend/envs
cp .env.example .env.dev
# Edit .env.dev with your local values
```

### Frontend (.env.development)
```bash
cd frontend
cp .env.example .env.development
# Edit .env.development with your local values
```

## Testing Workflows

1. **Test dev CI**: 
   - Create a branch from `dev`
   - Make changes and push
   - Check Actions tab for CI results

2. **Test production deployment**:
   - Merge to `main` branch
   - Check Actions tab for deployment status
   - Verify deployment on hosting platforms

## Troubleshooting

### Workflow fails with "Secret not found"
- Ensure all required secrets are added in GitHub settings
- Check secret names match exactly (case-sensitive)

### Backend deployment fails
- Check build logs in Render/Railway
- Verify all environment variables are set
- Check Python version compatibility

### Frontend deployment fails
- Check build logs in Vercel
- Verify API URL is correct
- Check Node version compatibility

## Notes

- Vercel can auto-deploy from GitHub without Actions workflow
- The workflow provides more control and sequential deployment
- You can disable automatic Vercel deployments and use workflow only
- Workflows use `ubuntu-latest` runners (free for public repos)
