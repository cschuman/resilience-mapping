# App Directory

All executable code lives here:

## Structure

```
app/
├── web/           # SvelteKit application (frontend + API)
├── analytics/     # Python analysis scripts
├── deploy/        # Deployment configs (Docker, etc.)
└── scripts/       # Shell utilities & SQL schema
```

## Architecture

```
SvelteKit (Fly.io)
├── Server routes     → SSR data loading
├── API routes        → REST endpoints (/api/*)
└── Direct PostgreSQL → No separate backend needed

PostgreSQL + PostGIS (Fly.io)
└── Resilience data for 68,170 census tracts

PMTiles (Cloudflare R2)
└── Vector tiles for map visualization
```

## Quick Start

### Run Development Server
```bash
cd web
npm install
npm run dev
```

### Run Python Analysis
```bash
cd analytics
pip install -r requirements.txt
python analyze_resilience.py      # Main analysis
python generate_tables.py         # Create tables
```

### Deploy to Fly.io
```bash
cd web
fly deploy
```

## Key Files

### Web (SvelteKit)
- `src/routes/` - Page routes and API endpoints
- `src/lib/server/db.ts` - PostgreSQL connection
- `src/lib/components/map/` - MapLibre visualization
- `fly.toml` - Fly.io deployment config

### Analytics (Python)
- `analyze_resilience.py` - Main resilience analysis
- `generate_tables.py` - Statistical tables

### Scripts
- `schema.sql` - Database schema with PostGIS

### Deploy
- `docker-compose.yml` - Local development stack
