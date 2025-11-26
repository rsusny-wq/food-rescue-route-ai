# Deployment Guide - Food Rescue Route AI

## Deployment Architecture

This application has two components:
1. **Frontend** (Next.js) - Deploy to Netlify
2. **Backend** (FastAPI) - Deploy to Railway/Render/Heroku

## Option 1: Netlify (Frontend) + Railway (Backend) - Recommended

### Step 1: Deploy Backend to Railway

1. **Sign up at Railway**: https://railway.app
2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository: `rsusny-wq/food-rescue-route-ai`
   - Select the `backend` directory as root

3. **Configure Environment Variables**:
   ```
   DATABASE_URL=postgresql://... (Railway provides this)
   GEMINI_API_KEY=AIzaSyCOAkSEl7XABiVLe_vS2oEp8DZC8sLzlu8
   ORS_API_KEY=your_ors_key_here
   ENVIRONMENT=production
   ```

4. **Add PostgreSQL Database**:
   - In Railway dashboard, click "New" → "Database" → "PostgreSQL"
   - Railway will provide the DATABASE_URL automatically

5. **Deploy**:
   - Railway will auto-detect Python and deploy
   - Note the deployment URL (e.g., `https://your-app.railway.app`)

6. **Initialize Database**:
   - In Railway, open a shell/terminal
   - Run: `python init_db.py`
   - Run: `python seed_data.py`

### Step 2: Deploy Frontend to Netlify

1. **Sign up at Netlify**: https://netlify.com

2. **Deploy from GitHub**:
   - Click "Add new site" → "Import an existing project"
   - Connect to GitHub
   - Select repository: `rsusny-wq/food-rescue-route-ai`
   - Configure:
     - **Base directory**: `frontend`
     - **Build command**: `npm install && npm run build`
     - **Publish directory**: `.next`

3. **Set Environment Variables**:
   - Go to Site settings → Environment variables
   - Add:
     ```
     NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
     ```

4. **Deploy**:
   - Click "Deploy site"
   - Netlify will build and deploy your frontend

5. **Update CORS in Backend**:
   - In your backend `.env` or Railway environment variables, add:
     ```
     CORS_ORIGINS=https://your-netlify-site.netlify.app
     ```
   - Update `backend/main.py` CORS settings to include your Netlify URL

## Option 2: Netlify (Frontend) + Render (Backend)

### Deploy Backend to Render

1. **Sign up at Render**: https://render.com
2. **Create New Web Service**:
   - Connect GitHub repository
   - Select `backend` directory
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
3. **Add PostgreSQL Database** (free tier available)
4. **Set environment variables** (same as Railway)
5. **Deploy**

Then follow Step 2 from Option 1 for Netlify frontend deployment.

## Option 3: Vercel (Full Stack) - Alternative

Vercel supports Next.js natively and can host API routes.

1. **Sign up at Vercel**: https://vercel.com
2. **Import GitHub repository**
3. **Configure**:
   - Root directory: `frontend`
   - Framework: Next.js
4. **Deploy backend separately** (Railway/Render) and set `NEXT_PUBLIC_API_URL`

## Quick Deploy Commands

### Railway (Backend)
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize
railway init

# Deploy
railway up
```

### Netlify (Frontend)
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Deploy
cd frontend
netlify deploy --prod
```

## Post-Deployment Checklist

- [ ] Backend is accessible (test: `https://your-backend.railway.app/docs`)
- [ ] Frontend can connect to backend (check browser console)
- [ ] Environment variables are set correctly
- [ ] Database is initialized
- [ ] CORS is configured properly
- [ ] API endpoints are working
- [ ] Map tiles are loading (OpenStreetMap)

## Troubleshooting

### Netlify "Page not found" Error

**Issue**: Netlify shows 404 for all routes

**Solution**:
1. Ensure `netlify.toml` is in the `frontend` directory
2. Check build command: `npm run build`
3. Verify publish directory: `.next`
4. Add `_redirects` file in `frontend/public/`

### CORS Errors

**Issue**: Frontend can't connect to backend

**Solution**:
1. Update backend CORS to include Netlify URL
2. Check `NEXT_PUBLIC_API_URL` environment variable
3. Verify backend is accessible

### Build Failures

**Issue**: Netlify build fails

**Solution**:
1. Check Node version (should be 18+)
2. Verify all dependencies in `package.json`
3. Check build logs in Netlify dashboard
4. Ensure `next.config.js` is properly configured

## Environment Variables Reference

### Backend (Railway/Render)
```
DATABASE_URL=postgresql://...
GEMINI_API_KEY=your_key
ORS_API_KEY=your_key
CORS_ORIGINS=https://your-netlify-site.netlify.app
ENVIRONMENT=production
```

### Frontend (Netlify)
```
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

## Support

If you encounter issues:
1. Check deployment logs
2. Verify environment variables
3. Test API endpoints directly
4. Check browser console for errors

