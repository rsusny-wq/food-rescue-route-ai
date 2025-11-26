# Food Rescue Route AI - Setup Guide

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+ (or use Docker)
- Redis (optional, for Celery)

## Quick Start with Docker

1. **Start all services:**
   ```bash
   docker-compose up -d
   ```

2. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Manual Setup

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your database URL and API keys
   ```

5. **Set up database:**
   ```bash
   # Create database
   createdb food_rescue
   
   # Run migrations (if using Alembic)
   alembic upgrade head
   ```

6. **Run the backend:**
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your API URL
   ```

4. **Run the frontend:**
   ```bash
   npm run dev
   ```

## Environment Variables

### Backend (.env)

```env
DATABASE_URL=postgresql://user:password@localhost:5432/food_rescue
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
ORS_API_KEY=your_ors_api_key_here
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your_secret_key_here
ENVIRONMENT=development
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## API Keys Setup

### OpenAI (for AI Agent)
1. Sign up at https://platform.openai.com
2. Create an API key
3. Add to backend `.env`

### Google Maps (optional)
1. Sign up at https://cloud.google.com/maps-platform
2. Enable Directions API
3. Create API key
4. Add to backend `.env`

### OpenRouteService (free alternative)
1. Sign up at https://openrouteservice.org
2. Get API key
3. Add to backend `.env`

## Database Schema

The application uses the following main tables:
- `donors` - Food donors (restaurants, groceries, etc.)
- `recipients` - Food banks, shelters, community fridges
- `donations` - Food donation listings
- `drivers` - Volunteer drivers and couriers
- `routes` - Delivery routes
- `route_stops` - Individual stops in routes

## Testing the Application

1. **Create a donor:**
   ```bash
   curl -X POST http://localhost:8000/donor \
     -H "Content-Type: application/json" \
     -d '{"name": "Test Restaurant", "email": "test@example.com", "address": "123 Broadway, NYC"}'
   ```

2. **Create a donation:**
   ```bash
   curl -X POST http://localhost:8000/donation \
     -H "Content-Type: application/json" \
     -d '{
       "donor_id": 1,
       "food_type": "Fresh vegetables",
       "quantity_lbs": 25,
       "pickup_window_start": "2025-01-10T14:00:00",
       "pickup_window_end": "2025-01-10T16:00:00",
       "address": "123 Broadway, NYC"
     }'
   ```

3. **View impact:**
   ```bash
   curl http://localhost:8000/impact
   ```

## Deployment

### Railway

1. Connect your GitHub repository
2. Railway will auto-detect the backend
3. Set environment variables in Railway dashboard
4. Deploy

### Vercel (Frontend)

1. Install Vercel CLI: `npm i -g vercel`
2. Run `vercel` in the frontend directory
3. Set environment variables in Vercel dashboard

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Verify database exists: `psql -l`

### API Key Issues
- Verify API keys are set correctly
- Check API quotas/limits
- Review API documentation for required permissions

### CORS Issues
- Ensure frontend URL is in backend CORS origins
- Check that API_URL matches backend URL

## Next Steps

1. Set up authentication (JWT tokens)
2. Add email/SMS notifications
3. Integrate with NYC Open Data APIs
4. Set up monitoring and logging
5. Add unit and integration tests

