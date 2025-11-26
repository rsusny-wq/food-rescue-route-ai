# Food Rescue Route AI

Intelligent Food Recovery & Route Optimization Platform for NYC

## Overview

Food Rescue Route AI is a web-based platform that matches food donors (restaurants, groceries, cafeterias) with food banks and shelters, and generates optimal pickup & delivery routes for volunteer drivers or low-cost courier partners.

All logic is powered by open-source NYC datasets, federal food waste metrics, Google Maps Directions API (free tier), and a lightweight AI agent for orchestration.

## Project Structure

```
.
├── backend/          # FastAPI backend
│   ├── main.py      # API endpoints
│   ├── models.py    # Database models
│   ├── schemas.py   # Pydantic schemas
│   ├── services/    # Business logic (matching, routing, impact, AI)
│   └── alembic/     # Database migrations
├── frontend/        # Next.js frontend
│   ├── app/         # Next.js app router pages
│   └── components/   # React components
├── docker-compose.yml
└── README.md
```

## Features

### Core Functionality
- **Food Donation Matching**: AI-powered matching between donors and recipients based on category, capacity, and distance
- **Route Optimization**: Intelligent route planning using Google Maps/OpenRouteService APIs
- **Impact Tracking**: Real-time metrics on CO₂e avoided, meals provided, and landfill space saved
- **Multi-User Interfaces**: Separate interfaces for donors, recipients, drivers, and admins
- **Real-Time Dashboard**: Admin dashboard with KPIs and live map visualization

### Impact Calculations
Based on EPA WARM Model and USDA factors:
- **Meals**: 1.2 lbs of food = 1 meal
- **CO₂e**: 1 lb food waste ≈ 2.5 lbs CO₂e
- **Methane**: 1 ton food waste → 0.45 tons CH₄ avoided
- **Landfill Space**: 1 cubic yard ≈ 450 lbs food waste

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy** - ORM
- **Alembic** - Database migrations
- **OpenAI API** - AI agent for classification and decisions
- **Google Maps/OpenRouteService** - Route optimization

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Leaflet.js** - Interactive maps
- **Axios** - HTTP client

## Quick Start

### Option 1: Docker (Recommended)

```bash
# Start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Manual Setup

See [SETUP.md](SETUP.md) for detailed setup instructions.

**Backend:**
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # Edit with your settings
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
cp .env.example .env.local  # Edit with API URL
npm run dev
```

## Environment Variables

### Backend (.env)
- `DATABASE_URL` - PostgreSQL connection string
- `OPENAI_API_KEY` - OpenAI API key (for AI agent)
- `GOOGLE_MAPS_API_KEY` - Google Maps API key (optional)
- `ORS_API_KEY` - OpenRouteService API key (free alternative)
- `REDIS_URL` - Redis connection (optional, for Celery)

### Frontend (.env.local)
- `NEXT_PUBLIC_API_URL` - Backend API URL

## API Documentation

Once the backend is running:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Key Endpoints

- `POST /donation` - Create a food donation
- `POST /assign_route` - Assign route to driver
- `GET /impact` - Get impact metrics
- `GET /donations` - List all donations
- `GET /routes` - List all routes

## Seeding Sample Data

```bash
cd backend
python seed_data.py
```

This creates sample donors, recipients, drivers, and donations for testing.

## Deployment

### Railway (Backend)
1. Connect GitHub repository
2. Set environment variables
3. Deploy

### Vercel (Frontend)
1. Install Vercel CLI: `npm i -g vercel`
2. Run `vercel` in frontend directory
3. Set environment variables

## Development

### Database Migrations
```bash
cd backend
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

### Testing
```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions, please open an issue on GitHub.

