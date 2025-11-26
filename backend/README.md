# Food Rescue Route AI - Backend

FastAPI backend for the Food Rescue Route AI platform.

## Features

- RESTful API for donations, routes, and impact tracking
- Intelligent matching algorithm for donors and recipients
- Route optimization using Google Maps/OpenRouteService
- AI agent for food classification and assignment decisions
- Impact calculations based on EPA WARM Model

## API Endpoints

### Donations
- `POST /donation` - Create a new donation
- `GET /donations` - List all donations (optional status filter)

### Routes
- `POST /assign_route` - Assign a route to a driver
- `GET /routes` - List all routes (optional status filter)
- `PATCH /route/{route_id}/status` - Update route status

### Impact
- `GET /impact` - Get cumulative impact metrics

### Entities
- `POST /donor` - Create a donor
- `POST /recipient` - Create a recipient
- `POST /driver` - Create a driver

## Running the Server

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your settings

# Run migrations (if using Alembic)
alembic upgrade head

# Seed sample data (optional)
python seed_data.py

# Start the server
uvicorn main:app --reload
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Environment Variables

See `.env.example` for required environment variables.

## Database

The application uses PostgreSQL. Tables are created automatically on first run, or use Alembic migrations:

```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

