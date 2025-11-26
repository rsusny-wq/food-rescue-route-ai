# Food Rescue Route AI - Frontend

Next.js frontend for the Food Rescue Route AI platform.

## Features

- Donor interface for posting food donations
- Recipient interface for viewing and accepting donations
- Driver interface for accepting and managing routes
- Admin dashboard with real-time metrics and map visualization
- Impact tracking and reporting

## Getting Started

```bash
# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with your API URL

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Pages

- `/` - Homepage with impact metrics
- `/donor` - Donor interface for posting donations
- `/recipient` - Recipient interface for viewing donations
- `/driver` - Driver interface for accepting routes
- `/admin` - Admin dashboard with KPIs
- `/admin/map` - Real-time map visualization

## Tech Stack

- Next.js 14 (App Router)
- React 18
- TypeScript
- Tailwind CSS
- Leaflet.js (maps)
- Axios (API client)

## Building for Production

```bash
npm run build
npm start
```

## Environment Variables

- `NEXT_PUBLIC_API_URL` - Backend API URL (default: http://localhost:8000)

