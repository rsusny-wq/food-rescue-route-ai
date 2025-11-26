# Neon Database Quick Start

## ✅ You've Already Set Up Neon!

Great! You've added Neon through Netlify's extension. Now you just need to connect your backend to it.

## Get Your Connection String

1. **Netlify Dashboard** → Your site
2. **Integrations** or **Add-ons** → Find **Neon**
3. **Copy connection string** (looks like):
   ```
   postgresql://user:password@ep-xxx-xxx.us-east-2.aws.neon.tech/food_rescue?sslmode=require
   ```

## Use It in Backend Deployment

When deploying backend to Railway or Render, use this connection string:

### Railway Example:
1. Railway dashboard → Your service → Variables
2. Add: `DATABASE_URL` = `[your Neon connection string]`
3. Make sure it includes `?sslmode=require` at the end

### Render Example:
1. Render dashboard → Your service → Environment
2. Add: `DATABASE_URL` = `[your Neon connection string]`

## Initialize Database

After backend is deployed:

1. Open terminal/shell in Railway or Render
2. Run:
   ```bash
   python init_db.py
   python seed_data.py
   ```

That's it! Your Neon database is now connected and ready.

## Benefits of Neon

- ✅ **Serverless**: No server management
- ✅ **Free Tier**: Perfect for development
- ✅ **Fast**: Low latency
- ✅ **Secure**: Built-in SSL
- ✅ **Netlify Integration**: Works seamlessly

## Need Help?

See `NEON_SETUP.md` for detailed instructions.

