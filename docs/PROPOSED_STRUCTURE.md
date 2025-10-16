# Resilience Mapping Platform - Proposed Project Structure

## Root Directory Philosophy
- Keep root clean: only essential config files
- No source code at root level
- Clear separation of concerns

```
resilience-mapping/
├── .github/                    # GitHub specific configs
│   ├── workflows/              # CI/CD pipelines
│   ├── ISSUE_TEMPLATE/
│   └── PULL_REQUEST_TEMPLATE.md
│
├── backend/                    # Go API server & core services
│   ├── cmd/                    # Application entrypoints
│   │   ├── api/               # API server main
│   │   ├── importer/          # Data import CLI
│   │   └── worker/            # Background job processors
│   │
│   ├── internal/              # Private application code
│   │   ├── api/              # HTTP layer
│   │   │   ├── handlers/     # Request handlers
│   │   │   ├── middleware/   # HTTP middleware
│   │   │   └── routes.go     # Route definitions
│   │   │
│   │   ├── domain/           # Core business logic
│   │   │   ├── community/    # Community domain
│   │   │   ├── health/       # Health metrics domain
│   │   │   └── resilience/   # Resilience scoring domain
│   │   │
│   │   ├── infrastructure/   # External services
│   │   │   ├── database/     # Database connections
│   │   │   ├── cache/        # Redis implementation
│   │   │   ├── search/       # Elasticsearch
│   │   │   └── storage/      # File/blob storage
│   │   │
│   │   └── config/           # Configuration management
│   │
│   ├── pkg/                  # Public/shared packages
│   │   ├── auth/            # Authentication utilities
│   │   ├── errors/          # Error handling
│   │   └── validation/      # Input validation
│   │
│   ├── test/                # Test utilities & fixtures
│   │   └── testdata/        # Test data files
│   │
│   ├── Dockerfile
│   ├── go.mod
│   └── go.sum
│
├── analytics/               # Python data science workspace
│   ├── src/                # Source code
│   │   ├── models/        # Statistical models
│   │   │   ├── resilience_model.py
│   │   │   └── burden_analysis.py
│   │   │
│   │   ├── processing/    # Data processing pipelines
│   │   │   ├── census_processor.py
│   │   │   ├── health_metrics.py
│   │   │   └── geo_enrichment.py
│   │   │
│   │   ├── visualization/ # Map & chart generation
│   │   │   ├── map_generator.py
│   │   │   └── table_generator.py
│   │   │
│   │   └── utils/        # Shared utilities
│   │
│   ├── notebooks/        # Jupyter notebooks for exploration
│   │   ├── 01_data_exploration.ipynb
│   │   ├── 02_model_development.ipynb
│   │   └── 03_results_analysis.ipynb
│   │
│   ├── tests/           # Python tests
│   │   ├── unit/
│   │   └── integration/
│   │
│   ├── outputs/         # Generated outputs (gitignored)
│   │   ├── figures/
│   │   ├── tables/
│   │   └── reports/
│   │
│   ├── requirements.txt
│   ├── setup.py
│   └── Dockerfile
│
├── frontend/            # Web applications (when implemented)
│   ├── apps/
│   │   ├── stories/    # Community stories site
│   │   ├── research/   # Research portal
│   │   └── policy/     # Policy dashboard
│   │
│   ├── packages/       # Shared frontend packages
│   │   ├── ui/        # Component library
│   │   ├── utils/     # Shared utilities
│   │   └── api-client/# API client library
│   │
│   ├── package.json
│   └── Dockerfile
│
├── infrastructure/      # Infrastructure as Code
│   ├── terraform/      # Cloud infrastructure
│   ├── kubernetes/     # K8s manifests
│   ├── docker/        # Docker compositions
│   │   ├── docker-compose.yml
│   │   └── docker-compose.prod.yml
│   └── scripts/       # Deployment scripts
│
├── data/               # Data storage (mostly gitignored)
│   ├── raw/           # Original data files
│   ├── interim/       # Intermediate processing
│   ├── processed/     # Clean, processed data
│   └── README.md      # Data dictionary & sources
│
├── docs/              # Technical documentation only
│   ├── api/          # API documentation
│   ├── architecture/ # System design docs
│   ├── development/  # Developer guides
│   └── deployment/   # Deployment guides
│
├── .business/         # Non-technical documents (hidden)
│   ├── planning/     # Milestones, roadmaps
│   ├── recruiting/   # Hiring documents
│   ├── operations/   # Sprint plans
│   └── research/     # Research papers, findings
│
├── scripts/          # Development & maintenance scripts
│   ├── setup.sh     # Initial setup script
│   ├── migrate.sh   # Database migrations
│   └── seed.sh      # Data seeding
│
├── .env.example      # Environment variables template
├── Makefile         # Streamlined build commands
├── README.md        # Project overview
└── LICENSE
```

## Key Improvements

### 1. **Clear Separation of Concerns**
- Backend (Go), Analytics (Python), Frontend (JS/TS) in separate directories
- Each has its own dependencies, Dockerfile, and test structure

### 2. **Domain-Driven Design in Backend**
- `/internal/domain/` contains pure business logic
- `/internal/infrastructure/` handles external dependencies
- Clean architecture with dependency inversion

### 3. **Python Analytics as First-Class Citizen**
- Proper Python package structure with `setup.py`
- Notebooks for exploration, source code for production
- Clear output directory for generated artifacts

### 4. **Hidden Business Documents**
- `.business/` directory keeps non-technical docs out of the way
- Still version controlled but not cluttering the codebase

### 5. **Proper Test Organization**
- Go: Tests live alongside code (e.g., `handlers/community_test.go`)
- Python: Separate test directory following Python conventions
- Frontend: Tests in `__tests__` directories per Jest conventions

### 6. **Infrastructure as Code**
- All deployment configs in one place
- Clear separation between local dev and production

### 7. **Data Management**
- Clear pipeline: raw → interim → processed
- Data dictionary documenting all datasets
- Most data gitignored with download scripts

## Migration Strategy

### Phase 1: Core Restructure (Week 1)
1. Create new directory structure
2. Move Go code to `backend/`
3. Consolidate Python scripts to `analytics/src/`
4. Move business docs to `.business/`

### Phase 2: Cleanup (Week 2)
1. Merge `model` and `models` directories
2. Consolidate configuration files
3. Update import paths
4. Fix Makefile targets

### Phase 3: Standardization (Week 3)
1. Add proper .gitignore patterns
2. Create .env.example
3. Write setup scripts
4. Update documentation

### Phase 4: Testing & CI/CD (Week 4)
1. Reorganize tests to follow conventions
2. Set up GitHub Actions workflows
3. Add pre-commit hooks
4. Configure linting & formatting

## Benefits of This Structure

1. **Developer Onboarding**: New devs can understand the project in 5 minutes
2. **Scalability**: Easy to add new services or components
3. **Maintainability**: Clear ownership and boundaries
4. **CI/CD Ready**: Each component can be built/deployed independently
5. **Industry Standard**: Follows conventions senior engineers expect

## Anti-Patterns We're Fixing

❌ Scripts at root level
❌ Mixed language dependencies
❌ Business docs mixed with code
❌ Inconsistent naming conventions
❌ Test isolation from source
❌ Configuration sprawl
❌ No clear build artifacts location
❌ Documentation scattered everywhere

## Next Steps

1. Review and approve this structure
2. Create migration scripts to automate the reorganization
3. Update all import paths and references
4. Test the build pipeline
5. Update developer documentation

This structure will scale from your current 1-person team to 100+ engineers without requiring another reorganization.