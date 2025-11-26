# Neon Database Setup with Netlify

## Overview

Neon provides serverless Postgres that works perfectly with Netlify deployments. You've already set up Neon through Netlify's extension - great choice!

## Step 1: Get Your Neon Connection String

1. In your Netlify dashboard, go to your site
2. Click on "Integrations" or "Add-ons"
3. Find your Neon database
4. Copy the connection string (it looks like):
   ```
   postgresql://user:password@ep-xxx-xxx.us-east-2.aws.neon.tech/dbname?sslmode=require
   ```

## Step 2: Configure Backend (Railway/Render)

When deploying your backend to Railway or Render, use the Neon connection string:

### Environment Variables for Backend:

```
DATABASE_URL=postgresql://user:password@ep-xxx-xxx.us-east-2.aws.neon.tech/dbname?sslmode=require
GEMINI_API_KEY=AIzaSyCOAkSEl7XABiVLe_vS2oEp8DZC8sLzlu8
ORS_API_KEY=your_ors_key_here
CORS_ORIGINS=https://your-netlify-site.netlify.app
ENVIRONMENT=production
```

**Important**: Neon requires `?sslmode=require` in the connection string for secure connections.

## Step 3: Initialize Database

After deploying backend, initialize the database:

### Option A: Using Railway/Render Shell
1. Open terminal/shell in your backend service
2. Run:
   ```bash
   python init_db.py
   python seed_data.py
   ```

### Option B: Using Local Connection
1. Install PostgreSQL client or use Neon's web SQL editor
2. Connect using your Neon connection string
3. Run the SQL from `init_db.py` manually

### Option C: Using Python Script (Local)
1. Set `DATABASE_URL` in your local `.env` to Neon connection string
2. Run:
   ```bash
   cd backend
   python init_db.py
   python seed_data.py
   ```

## Step 4: Verify Connection

Test your database connection:

```bash
# In backend directory
python -c "from database import engine; from sqlalchemy import text; conn = engine.connect(); print('Connected!')"
```

## Neon-Specific Configuration

### Connection Pooling

Neon supports connection pooling. Update `backend/database.py` if needed:

```python
# For Neon, you might want to use connection pooling
from sqlalchemy.pool import NullPool

if DATABASE_URL.startswith("postgresql"):
    engine = create_engine(
        DATABASE_URL,
        poolclass=NullPool,  # Neon handles pooling
        connect_args={"sslmode": "require"}
    )
```

### SSL Mode

Neon requires SSL. The connection string should include `?sslmode=require`.

If your connection string doesn't have it, add it:
```
postgresql://user:pass@host/db?sslmode=require
```

## Benefits of Neon

✅ **Serverless**: Scales automatically  
✅ **Free Tier**: Generous free tier for development  
✅ **Fast**: Low latency connections  
✅ **Secure**: Built-in SSL/TLS  
✅ **Netlify Integration**: Works seamlessly with Netlify  

## Troubleshooting

### Connection Timeout
- Check that `sslmode=require` is in connection string
- Verify firewall/network settings
- Ensure IP is not blocked

### SSL Error
- Make sure connection string includes `?sslmode=require`
- Check that you're using the correct connection string format

### Authentication Failed
- Verify username and password in connection string
- Check that database user has proper permissions

## Quick Reference

**Neon Connection String Format:**
```
postgresql://[user]:[password]@[host]/[database]?sslmode=require
```

**Example:**
```
postgresql://myuser:mypass@ep-cool-name-123456.us-east-2.aws.neon.tech/food_rescue?sslmode=require
```

## Next Steps

1. ✅ Neon database created (done via Netlify extension)
2. ⏭️ Deploy backend to Railway/Render with Neon connection string
3. ⏭️ Initialize database tables
4. ⏭️ Deploy frontend to Netlify
5. ⏭️ Test full application

Your Neon database is ready to use! Just make sure your backend uses the connection string from Netlify.

