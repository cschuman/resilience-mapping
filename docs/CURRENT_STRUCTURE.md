# Current Project Structure (As Built)

*Last Updated: August 25, 2024*

## Actual Structure Right Now

```
resilience/
├── 📦 app/                    
│   ├── backend/              # 42 Go files (all flattened)
│   ├── analytics/            # 13 Python scripts + venv
│   ├── deploy/               # Deployment configs
│   │   ├── schema.sql        # Supabase database schema
│   │   ├── import_to_supabase.py
│   │   ├── vercel.json       # Vercel deployment config
│   │   ├── docker-compose.yml
│   │   └── docker-compose.prod.yml
│   └── scripts/              # Shell utilities
│
├── 📊 data/
│   ├── input/                # Raw data files (CSVs, etc.)
│   ├── output/               # Generated results
│   │   └── map_screenshot.png # Example output
│   └── [legacy dirs]         # census_gazetteer, external, etc.
│
├── 📝 docs/
│   ├── business/             # 36 business/team documents
│   ├── research/             # Research findings
│   ├── setup/                # Installation guides
│   ├── architecture/         # Technical architecture docs
│   ├── development/          # Developer guides
│   ├── MIGRATION_SUMMARY.md  # What we did today
│   ├── ADHD_FRIENDLY_STRUCTURE.md
│   ├── STRUCTURE_ANALYSIS.md
│   └── [API specs]           # swagger.json, swagger.yaml
│
├── LICENSE
├── Makefile                  # Simple commands
└── README.md                 # Project overview
```

## File Counts

- **Root level:** 6 visible items (3 folders, 3 files)
- **app/backend:** 42 Go files
- **app/analytics:** 13 Python scripts
- **app/deploy:** 5 deployment configs
- **docs/business:** 36 business documents
- **Total root files:** 3 (down from 22)

## What Lives Where

| Content Type | Location | Example |
|-------------|----------|---------|
| Go API code | `app/backend/` | `community_handler.go` |
| Python analysis | `app/analytics/` | `analyze_resilience.py` |
| Python environment | `app/analytics/venv/` | Virtual environment |
| Supabase schema | `app/deploy/` | `schema.sql` |
| Vercel config | `app/deploy/` | `vercel.json` |
| Docker configs | `app/deploy/` | `docker-compose.yml` |
| Raw data | `data/input/` | Census CSVs |
| Generated outputs | `data/output/` | Maps, tables |
| Team documents | `docs/business/` | Planning, milestones |
| Research papers | `docs/research/` | Findings, analysis |
| Setup guides | `docs/setup/` | Installation docs |

## Quick Commands

```bash
# Navigate to main areas
cd app/backend      # Go code
cd app/analytics    # Python code
cd app/deploy       # Deployment

# Common tasks (via Makefile)
make run           # Run Go backend
make analyze       # Run Python analysis
make help          # See all commands

# Python work
cd app/analytics
source venv/bin/activate
python analyze_resilience.py
```

## Migration Notes

- Migrated from 38 directories to 3 main directories
- Flattened Go package structure (all files in backend/)
- Moved Python venv from root to app/analytics/
- Consolidated all deployment configs to app/deploy/
- Moved business docs from hidden .business/ to docs/business/
- 92% reduction in root-level visual complexity

## Why This Structure?

1. **ADHD-Friendly:** Only 3 main folders to remember
2. **Clear Boundaries:** Code, Data, Docs - nothing ambiguous
3. **Flat Where Possible:** Backend has all Go files at one level
4. **Deployment Ready:** All configs in one place
5. **Clean Root:** Only essential files visible

## Future Considerations

When the project grows:
- Backend can add subdirectories when needed
- Frontend would go in app/frontend/
- More deployment targets can be added to app/deploy/
- But the 3-folder root structure stays constant