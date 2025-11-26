# Quick Start Guide

## ✅ Setup Complete!

Your Food Rescue Route AI application is now configured with:

1. **Gemini API** - Integrated for AI-powered food classification
2. **OpenRouteService** - Configured as primary routing service (open source)
3. **NYC Open Data** - Integrated for food pantries and neighborhood data
4. **SQLite Database** - Initialized with sample data

## 🚀 Running the Application

### Option 1: Use the Setup Script
```powershell
.\setup_and_run.ps1
```

### Option 2: Manual Start

**Backend (Terminal 1):**
```powershell
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend (Terminal 2):**
```powershell
cd frontend
npm run dev
```

## 🌐 Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📝 Next Steps

1. **Get OpenRouteService API Key** (Free):
   - Visit: https://openrouteservice.org/dev/#/signup
   - Sign up for free account
   - Get your API key
   - Add to `backend/.env`: `ORS_API_KEY=your_key_here`

2. **Populate NYC Data** (Optional):
   - Visit: http://localhost:8000/docs
   - Use endpoint: `POST /nyc-data/populate-recipients`
   - This will fetch real NYC food pantry data

3. **Test the Application**:
   - Go to http://localhost:3000
   - Try creating a donation as a donor
   - View available donations as a recipient
   - Accept routes as a driver
   - Check admin dashboard for metrics

## 🔧 Configuration

All configuration is in `backend/.env`:
- `GEMINI_API_KEY` - Already configured ✅
- `ORS_API_KEY` - Add your free key from openrouteservice.org
- `DATABASE_URL` - Using SQLite (change to PostgreSQL for production)

## 📊 Sample Data

The database has been seeded with:
- 3 sample donors (restaurants, grocery, cafeteria)
- 3 sample recipients (food bank, community fridge, shelter)
- 2 sample drivers (volunteers)
- 3 sample donations

## 🐛 Troubleshooting

**Backend won't start:**
- Check if port 8000 is available
- Verify Python dependencies: `pip install -r requirements.txt`

**Frontend won't start:**
- Check if port 3000 is available
- Verify Node dependencies: `npm install`

**Database issues:**
- SQLite database file: `backend/food_rescue.db`
- Delete it to reset: `del backend\food_rescue.db`
- Re-run: `python init_db.py` and `python seed_data.py`

## 🚢 Production Deployment

For production:
1. Use PostgreSQL instead of SQLite
2. Set up proper environment variables
3. Deploy backend to Railway/Heroku
4. Deploy frontend to Vercel
5. Configure CORS properly

Enjoy your Food Rescue Route AI platform! 🍎

