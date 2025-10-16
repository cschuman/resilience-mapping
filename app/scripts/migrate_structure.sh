#!/bin/bash
# Resilience Mapping Project Structure Migration Script
# WARNING: This script will reorganize your entire project structure
# Make sure you have committed all changes before running

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Resilience Mapping Structure Migration ===${NC}"
echo -e "${YELLOW}This script will reorganize your project to follow best practices${NC}"
echo -e "${RED}WARNING: Make sure all changes are committed first!${NC}"
read -p "Continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Migration cancelled"
    exit 1
fi

# Create backup
echo -e "${BLUE}Creating backup...${NC}"
BACKUP_DIR="../resilience-backup-$(date +%Y%m%d-%H%M%S)"
cp -r . "$BACKUP_DIR"
echo -e "${GREEN}Backup created at: $BACKUP_DIR${NC}"

# Create new directory structure
echo -e "${BLUE}Creating new directory structure...${NC}"

# Backend structure
mkdir -p backend/{cmd/{api,importer,worker},internal/{api/{handlers,middleware},domain/{community,health,resilience},infrastructure/{database,cache,search,storage},config},pkg/{auth,errors,validation},test/testdata}

# Analytics structure  
mkdir -p analytics/{src/{models,processing,visualization,utils},notebooks,tests/{unit,integration},outputs/{figures,tables,reports}}

# Frontend structure (placeholder)
mkdir -p frontend/{apps/{stories,research,policy},packages/{ui,utils,api-client}}

# Infrastructure structure
mkdir -p infrastructure/{terraform,kubernetes,docker,scripts}

# Documentation structure
mkdir -p docs/{api,architecture,development,deployment}

# Business documents (hidden)
mkdir -p .business/{planning,recruiting,operations,research}

# Scripts directory
mkdir -p scripts

echo -e "${GREEN}✓ Directory structure created${NC}"

# Move Go backend files
echo -e "${BLUE}Migrating Go backend files...${NC}"

# Move cmd files
[ -d "cmd/server" ] && mv cmd/server/* backend/cmd/api/ 2>/dev/null || true
[ -d "cmd/importer" ] && mv cmd/importer/* backend/cmd/importer/ 2>/dev/null || true
[ -d "cmd/resilience" ] && mv cmd/resilience/* backend/cmd/worker/ 2>/dev/null || true

# Move internal files
[ -d "internal/api" ] && mv internal/api/* backend/internal/api/ 2>/dev/null || true
[ -d "internal/handlers" ] && mv internal/handlers/* backend/internal/api/handlers/ 2>/dev/null || true
[ -d "internal/middleware" ] && mv internal/middleware/* backend/internal/api/middleware/ 2>/dev/null || true

# Move domain logic
[ -d "internal/models" ] && mv internal/models/* backend/internal/domain/community/ 2>/dev/null || true
[ -d "internal/model" ] && mv internal/model/* backend/internal/domain/resilience/ 2>/dev/null || true
[ -d "internal/feature" ] && mv internal/feature/* backend/internal/domain/health/ 2>/dev/null || true

# Move infrastructure
[ -d "internal/database" ] && mv internal/database/* backend/internal/infrastructure/database/ 2>/dev/null || true
[ -d "internal/cache" ] && mv internal/cache/* backend/internal/infrastructure/cache/ 2>/dev/null || true
[ -d "internal/search" ] && mv internal/search/* backend/internal/infrastructure/search/ 2>/dev/null || true

# Move config
[ -d "internal/config" ] && mv internal/config/* backend/internal/config/ 2>/dev/null || true
[ -f "config/default.yml" ] && mv config/default.yml backend/internal/config/ 2>/dev/null || true

# Move pkg files
[ -d "pkg" ] && cp -r pkg/* backend/pkg/ 2>/dev/null || true

# Move test files
[ -d "test" ] && cp -r test/* backend/test/ 2>/dev/null || true

# Move Go module files
[ -f "go.mod" ] && mv go.mod backend/ 2>/dev/null || true
[ -f "go.sum" ] && mv go.sum backend/ 2>/dev/null || true

echo -e "${GREEN}✓ Go backend migrated${NC}"

# Move Python analytics files
echo -e "${BLUE}Migrating Python analytics files...${NC}"

# Create analytics module structure
cat > analytics/setup.py << 'EOF'
from setuptools import setup, find_packages

setup(
    name="resilience-analytics",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas>=1.5.0",
        "numpy>=1.23.0",
        "scipy>=1.9.0",
        "scikit-learn>=1.1.0",
        "matplotlib>=3.5.0",
        "seaborn>=0.12.0",
        "geopandas>=0.12.0",
        "folium>=0.14.0",
        "statsmodels>=0.13.0",
    ],
)
EOF

# Move Python scripts to appropriate locations
PYTHON_SCRIPTS=(
    "analyze_resilience.py:processing/analyze_resilience.py"
    "analyze_least_resilient.py:processing/analyze_least_resilient.py"
    "extract_all_resilient.py:processing/extract_all_resilient.py"
    "investigate_anomalies.py:processing/investigate_anomalies.py"
    "get_cities_census.py:processing/get_cities_census.py"
    "get_cities_tiger.py:processing/get_cities_tiger.py"
    "get_cities_tiger_full.py:processing/get_cities_tiger_full.py"
    "generate_tables.py:visualization/generate_tables.py"
    "serve_map.py:visualization/serve_map.py"
    "screenshot.py:visualization/screenshot.py"
    "screenshot_simple.py:visualization/screenshot_simple.py"
)

for mapping in "${PYTHON_SCRIPTS[@]}"; do
    IFS=':' read -r source dest <<< "$mapping"
    [ -f "$source" ] && mv "$source" "analytics/src/$dest" 2>/dev/null || true
done

# Move requirements.txt
[ -f "requirements.txt" ] && mv requirements.txt analytics/ 2>/dev/null || true

# Move tables output
[ -d "tables" ] && mv tables/* analytics/outputs/tables/ 2>/dev/null || true

# Move figures
[ -d "figures" ] && mv figures/* analytics/outputs/figures/ 2>/dev/null || true

echo -e "${GREEN}✓ Python analytics migrated${NC}"

# Move infrastructure files
echo -e "${BLUE}Migrating infrastructure files...${NC}"

[ -f "docker-compose.yml" ] && mv docker-compose.yml infrastructure/docker/ 2>/dev/null || true
[ -f "docker-compose.prod.yml" ] && mv docker-compose.prod.yml infrastructure/docker/ 2>/dev/null || true
[ -f "Dockerfile" ] && mv Dockerfile backend/ 2>/dev/null || true

# Move Supabase files
[ -d "supabase" ] && mv supabase/* infrastructure/docker/ 2>/dev/null || true

echo -e "${GREEN}✓ Infrastructure files migrated${NC}"

# Move documentation
echo -e "${BLUE}Organizing documentation...${NC}"

# Technical docs
[ -d "architecture" ] && mv architecture/* docs/architecture/ 2>/dev/null || true
[ -f "DEVELOPMENT_SETUP.md" ] && mv DEVELOPMENT_SETUP.md docs/development/ 2>/dev/null || true
[ -f "ROADMAP.md" ] && mv ROADMAP.md docs/development/ 2>/dev/null || true

# Move business documents to hidden directory
BUSINESS_DOCS=(
    "docs/dream-team-assembly-playbook.md:.business/recruiting/"
    "docs/implementation-dream-team.md:.business/recruiting/"
    "docs/nyt-editor-requirements.md:.business/research/"
    "docs/paper-checklist.md:.business/research/"
    "docs/passionate-research-questions.md:.business/research/"
    "docs/policy-analysis.md:.business/research/"
    "docs/press-release.md:.business/operations/"
    "docs/press-release-short.md:.business/operations/"
    "docs/research-findings.md:.business/research/"
    "docs/research-paper-draft.md:.business/research/"
    "docs/slide-outline.md:.business/planning/"
    "docs/team-composition-strategy.md:.business/recruiting/"
    "docs/top-resilient-communities.md:.business/research/"
    "docs/webpage-audience-analysis.md:.business/planning/"
    "docs/website-design-workshop.md:.business/planning/"
    "docs/website-implementation-plan.md:.business/planning/"
    "docs/COMPREHENSIVE-FINDINGS-REPORT.md:.business/research/"
)

for mapping in "${BUSINESS_DOCS[@]}"; do
    IFS=':' read -r source dest <<< "$mapping"
    [ -f "$source" ] && mv "$source" "$dest" 2>/dev/null || true
done

# Move other business directories
[ -d "milestones" ] && mv milestones/* .business/planning/ 2>/dev/null || true
[ -d "operations" ] && mv operations/* .business/operations/ 2>/dev/null || true
[ -d "recruiting" ] && mv recruiting/* .business/recruiting/ 2>/dev/null || true
[ -d "team" ] && mv team/* .business/recruiting/ 2>/dev/null || true
[ -d "ux" ] && mv ux/* .business/planning/ 2>/dev/null || true

echo -e "${GREEN}✓ Documentation organized${NC}"

# Move scripts
echo -e "${BLUE}Moving utility scripts...${NC}"

[ -f "scripts/import_sample_data.sh" ] && mv scripts/import_sample_data.sh scripts/seed.sh 2>/dev/null || true

echo -e "${GREEN}✓ Scripts organized${NC}"

# Create improved Makefile
echo -e "${BLUE}Creating improved Makefile...${NC}"

cat > Makefile << 'EOF'
# Resilience Mapping Platform - Makefile
.DEFAULT_GOAL := help

# Service directories
BACKEND_DIR := backend
ANALYTICS_DIR := analytics
FRONTEND_DIR := frontend
INFRA_DIR := infrastructure

.PHONY: help
help: ## Show this help message
	@echo "Resilience Mapping Platform - Build Commands"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf ""} /^[a-zA-Z_-]+:.*##/ {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Backend commands
.PHONY: backend-build backend-test backend-run
backend-build: ## Build Go backend
	cd $(BACKEND_DIR) && go build -o bin/api ./cmd/api

backend-test: ## Test Go backend
	cd $(BACKEND_DIR) && go test -v ./...

backend-run: ## Run Go backend
	cd $(BACKEND_DIR) && go run ./cmd/api

# Analytics commands
.PHONY: analytics-setup analytics-test analytics-notebook
analytics-setup: ## Setup Python analytics environment
	cd $(ANALYTICS_DIR) && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt

analytics-test: ## Test Python analytics
	cd $(ANALYTICS_DIR) && python -m pytest tests/

analytics-notebook: ## Start Jupyter notebook server
	cd $(ANALYTICS_DIR) && jupyter notebook

# Docker commands
.PHONY: docker-up docker-down docker-build
docker-up: ## Start all services with Docker Compose
	cd $(INFRA_DIR)/docker && docker-compose up -d

docker-down: ## Stop all Docker services
	cd $(INFRA_DIR)/docker && docker-compose down

docker-build: ## Build all Docker images
	docker build -t resilience-backend $(BACKEND_DIR)
	docker build -t resilience-analytics $(ANALYTICS_DIR)

# Development
.PHONY: dev clean
dev: ## Start development environment
	make docker-up
	make backend-run

clean: ## Clean build artifacts
	rm -rf $(BACKEND_DIR)/bin
	rm -rf $(ANALYTICS_DIR)/outputs/*
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

.PHONY: install
install: ## Install all dependencies
	cd $(BACKEND_DIR) && go mod download
	make analytics-setup
EOF

echo -e "${GREEN}✓ Makefile created${NC}"

# Create .gitignore
echo -e "${BLUE}Creating comprehensive .gitignore...${NC}"

cat > .gitignore << 'EOF'
# Environment
.env
.env.local
.env.*.local
venv/
*.pyc
__pycache__/

# Data files (too large for git)
data/raw/*
data/interim/*
data/processed/*
!data/raw/.gitkeep
!data/interim/.gitkeep
!data/processed/.gitkeep
!data/README.md

# Analytics outputs
analytics/outputs/figures/*
analytics/outputs/tables/*
analytics/outputs/reports/*
!analytics/outputs/figures/.gitkeep
!analytics/outputs/tables/.gitkeep
!analytics/outputs/reports/.gitkeep

# Build artifacts
backend/bin/
backend/vendor/
*.exe
*.dll
*.so
*.dylib

# Test coverage
*.coverprofile
coverage/
.coverage
htmlcov/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Node (for future frontend)
node_modules/
dist/
.next/
*.log

# Terraform
*.tfstate
*.tfstate.*
.terraform/

# Kubernetes
*.secret.yaml
EOF

echo -e "${GREEN}✓ .gitignore created${NC}"

# Create .env.example
echo -e "${BLUE}Creating .env.example...${NC}"

cat > .env.example << 'EOF'
# API Configuration
API_PORT=8080
API_HOST=localhost
API_ENV=development

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/resilience
DATABASE_MAX_CONNECTIONS=25
DATABASE_IDLE_CONNECTIONS=5

# Redis Cache
REDIS_URL=redis://localhost:6379
REDIS_DB=0

# Elasticsearch
ELASTICSEARCH_URL=http://localhost:9200
ELASTICSEARCH_INDEX=resilience

# Supabase (if using)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key

# AWS (for data storage)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
S3_BUCKET=resilience-data

# Monitoring
SENTRY_DSN=
LOG_LEVEL=info

# Security
JWT_SECRET=change-this-in-production
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
EOF

echo -e "${GREEN}✓ .env.example created${NC}"

# Clean up empty old directories
echo -e "${BLUE}Cleaning up old directories...${NC}"
find . -type d -empty -delete 2>/dev/null || true

# Create .gitkeep files for empty directories that should be preserved
touch data/raw/.gitkeep
touch data/interim/.gitkeep  
touch data/processed/.gitkeep
touch analytics/outputs/figures/.gitkeep
touch analytics/outputs/tables/.gitkeep
touch analytics/outputs/reports/.gitkeep

echo -e "${GREEN}✓ Cleanup complete${NC}"

# Final summary
echo -e "${GREEN}===============================================${NC}"
echo -e "${GREEN}✓ Migration completed successfully!${NC}"
echo -e "${GREEN}===============================================${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Review the new structure"
echo "2. Update import paths in Go files"
echo "3. Test the build with: make backend-build"
echo "4. Commit the changes"
echo ""
echo -e "${BLUE}Backup saved at: $BACKUP_DIR${NC}"
echo -e "${YELLOW}Run 'make help' to see available commands${NC}"