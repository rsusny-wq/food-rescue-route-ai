# Quick Netlify Fix - Step by Step

## The Problem
Netlify shows "Page not found" because Next.js needs special configuration on Netlify.

## The Solution (5 Minutes)

### Step 1: Deploy Backend to Railway (2 min)
1. Go to https://railway.app → Sign up with GitHub
2. Click "New Project" → "Deploy from GitHub repo"
3. Select repo: `rsusny-wq/food-rescue-route-ai`
4. Set root directory: `backend`
5. Add PostgreSQL database (click "New" → "Database")
6. Add environment variables:
   - `GEMINI_API_KEY=AIzaSyCOAkSEl7XABiVLe_vS2oEp8DZC8sLzlu8`
   - `CORS_ORIGINS=https://your-netlify-site.netlify.app`
7. Copy your Railway URL (e.g., `https://food-rescue-api.railway.app`)

### Step 2: Fix Netlify Configuration (2 min)
1. In Netlify dashboard → Your site → "Site settings"
2. Go to "Plugins" → "Add plugin"
3. Search: `@netlify/plugin-nextjs` → Install
4. Go to "Build & deploy" settings:
   - Base directory: `frontend`
   - Build command: `npm install && npm run build`
   - Publish directory: `.next`
5. Go to "Environment variables":
   - Add: `NEXT_PUBLIC_API_URL` = `https://your-railway-url.railway.app`
6. Click "Deploy site" → "Trigger deploy" → "Clear cache and deploy"

### Step 3: Update Backend CORS (1 min)
1. In Railway dashboard → Your service → "Variables"
2. Add: `CORS_ORIGINS` = `https://your-netlify-site.netlify.app`
3. Service will auto-redeploy

## That's It!

Your site should now work at: `https://your-site.netlify.app`

## Still Not Working?

1. **Check build logs** in Netlify dashboard
2. **Verify backend** is accessible: `https://your-railway-url.railway.app/docs`
3. **Test API** in browser console
4. **Check environment variables** are set correctly

## Alternative: Use Vercel (Easier for Next.js)

Vercel is made for Next.js and works out of the box:

1. Go to https://vercel.com
2. Import GitHub repo
3. Set root: `frontend`
4. Add env var: `NEXT_PUBLIC_API_URL`
5. Deploy (automatic!)

Vercel handles Next.js routing automatically - no plugins needed!

