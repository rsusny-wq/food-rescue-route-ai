# Netlify Deployment Setup Guide

## Quick Fix for "Page not found" Error

The issue is that Netlify needs proper Next.js configuration. Follow these steps:

## Step-by-Step Deployment

### 1. Install Netlify Next.js Plugin

In your Netlify dashboard:
1. Go to your site settings
2. Click "Plugins" → "Add plugin"
3. Search for "@netlify/plugin-nextjs"
4. Install it

OR add it to your `package.json`:

```bash
cd frontend
npm install @netlify/plugin-nextjs --save-dev
```

### 2. Configure Netlify Build Settings

In Netlify dashboard → Site settings → Build & deploy:

**Build settings:**
- **Base directory**: `frontend`
- **Build command**: `npm install && npm run build`
- **Publish directory**: `.next`

**Environment variables:**
- `NEXT_PUBLIC_API_URL` = `https://your-backend-url.railway.app` (or your backend URL)

### 3. Deploy Backend First (Required!)

Netlify only hosts the frontend. You MUST deploy the backend separately:

#### Option A: Railway (Easiest)
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repo
5. Set root directory to `backend`
6. Add PostgreSQL database
7. Set environment variables:
   - `GEMINI_API_KEY=AIzaSyCOAkSEl7XABiVLe_vS2oEp8DZC8sLzlu8`
   - `DATABASE_URL` (auto-provided by Railway)
   - `CORS_ORIGINS=https://your-netlify-site.netlify.app`
8. Note your Railway URL (e.g., `https://food-rescue-api.railway.app`)

#### Option B: Render (Free Tier)
1. Go to https://render.com
2. Sign up with GitHub
3. Create "New Web Service"
4. Connect your GitHub repo
5. Set root directory to `backend`
6. Build: `pip install -r requirements.txt`
7. Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
8. Add PostgreSQL database
9. Set environment variables (same as Railway)

### 4. Update Frontend Environment Variable

In Netlify dashboard:
1. Go to Site settings → Environment variables
2. Add/Update:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
   ```
3. Redeploy the site

### 5. Update Backend CORS

In your backend environment variables (Railway/Render), add:
```
CORS_ORIGINS=https://your-netlify-site.netlify.app
```

Or update `backend/main.py` to include your Netlify URL.

### 6. Redeploy

1. In Netlify, go to "Deploys"
2. Click "Trigger deploy" → "Clear cache and deploy site"

## Verification Checklist

After deployment, verify:

- [ ] Backend is accessible: `https://your-backend.railway.app/docs`
- [ ] Frontend loads: `https://your-netlify-site.netlify.app`
- [ ] API calls work (check browser console)
- [ ] No CORS errors
- [ ] Maps load correctly

## Common Issues & Solutions

### Issue: "Page not found" on all routes

**Solution:**
1. Ensure `@netlify/plugin-nextjs` is installed
2. Check build command: `npm install && npm run build`
3. Verify publish directory: `.next`
4. Make sure `netlify.toml` is in `frontend/` directory

### Issue: API calls fail

**Solution:**
1. Check `NEXT_PUBLIC_API_URL` is set correctly
2. Verify backend is running and accessible
3. Check CORS settings in backend
4. Test backend URL directly: `https://your-backend.railway.app/health`

### Issue: Build fails

**Solution:**
1. Check Node version (should be 18+)
2. Review build logs in Netlify dashboard
3. Ensure all dependencies are in `package.json`
4. Try clearing cache and redeploying

## Alternative: Use Vercel Instead

Vercel has better Next.js support:

1. Go to https://vercel.com
2. Import your GitHub repository
3. Set root directory to `frontend`
4. Add environment variable: `NEXT_PUBLIC_API_URL`
5. Deploy (automatic)

Vercel handles Next.js routing automatically!

## Quick Deploy Commands

### Using Netlify CLI:
```bash
cd frontend
npm install -g netlify-cli
netlify login
netlify deploy --prod
```

### Using Railway CLI (Backend):
```bash
cd backend
npm install -g @railway/cli
railway login
railway up
```

## Need Help?

1. Check deployment logs in Netlify dashboard
2. Verify environment variables are set
3. Test backend API directly
4. Check browser console for errors
5. Review `DEPLOYMENT.md` for detailed instructions

