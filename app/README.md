# 📦 App Directory

All executable code lives here in 4 simple folders:

## Structure

```
app/
├── analytics/     # Python analysis scripts
├── backend/       # Go API server (reference)
├── deploy/        # Deployment configs
└── scripts/       # Shell utilities & SQL
```

## Quick Start

### Import to Supabase (Primary Path)
```bash
cd analytics

# Create .env file with your credentials:
echo "SUPABASE_URL=https://YOUR_PROJECT.supabase.co" > .env
echo "SUPABASE_ANON_KEY=YOUR_ANON_KEY" >> .env

# Install dependencies
pip install pandas python-dotenv supabase

# Run import
python import_to_supabase.py
```

### Run Python Analysis
```bash
cd analytics
python analyze_resilience.py      # Main analysis
python generate_tables.py         # Create tables
python serve_map.py               # Interactive map
```

### Setup Database (Supabase)
```bash
# 1. Go to Supabase SQL Editor
# 2. Copy contents of scripts/schema.sql
# 3. Run the SQL
```

### Legacy Go Backend (Reference Only)
```bash
cd backend && go run main.go
```

## Key Files

### Analytics (Python)
- `import_to_supabase.py` - Import 1,059 communities
- `analyze_resilience.py` - Main resilience analysis
- `generate_tables.py` - Statistical tables
- `serve_map.py` - Interactive maps

### Scripts
- `schema.sql` - Supabase database schema
- `seed.sh` - Database seeding
- `migrate_structure.sh` - Structure migration

### Deploy
- `vercel.json` - Vercel config
- `docker-compose.yml` - Docker setup

## Architecture Note

We're using a simplified stack:
- **Supabase** for backend/database/auth
- **Vercel** for hosting
- **Next.js** for frontend (coming soon)

The Go backend remains as reference architecture but is not needed for deployment.
