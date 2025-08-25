# Health Resilience Mapping Platform - Development Makefile
# Created: January 31, 2025
# Team: 27 developers building for 1,000+ communities

SHELL := /bin/bash
.DEFAULT_GOAL := help

# ============================================================================
# CONFIGURATION VARIABLES
# ============================================================================

# Project Configuration
PROJECT_NAME := resilience-mapping
GO_VERSION := 1.21
NODE_VERSION := 18

# Service Ports
API_PORT := 8080
FRONTEND_PORT := 3000
RESEARCH_PORT := 3001
POLICY_PORT := 3002
POSTGRES_PORT := 5432
REDIS_PORT := 6379
ELASTICSEARCH_PORT := 9200
MAILHOG_PORT := 8025

# Docker Configuration
DOCKER_REGISTRY := resilience
DOCKER_TAG := latest
COMPOSE_FILE := docker-compose.yml
COMPOSE_FILE_PROD := docker-compose.prod.yml

# Build Configuration
BUILD_DIR := bin
COVERAGE_DIR := coverage
LOGS_DIR := logs

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
PURPLE := \033[0;35m
CYAN := \033[0;36m
WHITE := \033[0;37m
NC := \033[0m # No Color

# ============================================================================
# HELP COMMAND (DEFAULT)
# ============================================================================

.PHONY: help
help: ## Show this help message
	@echo "$(BLUE)Health Resilience Mapping Platform - Development Commands$(NC)"
	@echo "$(CYAN)Building technology that serves 1,000+ communities with dignity$(NC)"
	@echo ""
	@echo "$(YELLOW)Quick Start:$(NC)"
	@echo "  make dev-up        # Start all development services"
	@echo "  make dev-start     # Start development servers"
	@echo "  make test-quick    # Run quick test suite"
	@echo ""
	@echo "$(YELLOW)Available Commands:$(NC)"
	@awk 'BEGIN {FS = ":.*##"; printf ""} /^[a-zA-Z_0-9-]+:.*##/ {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(CYAN)For detailed setup instructions, see: DEVELOPMENT_SETUP.md$(NC)"

# ============================================================================
# DEVELOPMENT ENVIRONMENT
# ============================================================================

.PHONY: dev-up dev-down dev-restart dev-status dev-reset dev-start dev-stop
dev-up: ## Start all development services (databases, cache, search)
	@echo "$(BLUE)Starting development services...$(NC)"
	@docker-compose up -d
	@echo "$(GREEN)✓ Development services started$(NC)"
	@make dev-status

dev-down: ## Stop all development services
	@echo "$(YELLOW)Stopping development services...$(NC)"
	@docker-compose down
	@echo "$(GREEN)✓ Development services stopped$(NC)"

dev-restart: ## Restart all development services
	@make dev-down
	@make dev-up

dev-status: ## Show status of development services
	@echo "$(BLUE)Development Services Status:$(NC)"
	@docker-compose ps
	@echo ""
	@echo "$(BLUE)Service URLs:$(NC)"
	@echo "  API Server:        http://localhost:$(API_PORT)"
	@echo "  Stories Site:      http://localhost:$(FRONTEND_PORT)"
	@echo "  Research Site:     http://localhost:$(RESEARCH_PORT)"
	@echo "  Policy Site:       http://localhost:$(POLICY_PORT)"
	@echo "  MailHog:          http://localhost:$(MAILHOG_PORT)"
	@echo "  Elasticsearch:    http://localhost:$(ELASTICSEARCH_PORT)"

dev-reset: ## Reset entire development environment (WARNING: destroys data)
	@echo "$(RED)WARNING: This will destroy all local data!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; echo; if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker-compose down -v; \
		docker system prune -f; \
		docker volume prune -f; \
		rm -rf $(BUILD_DIR) $(COVERAGE_DIR) $(LOGS_DIR); \
		echo "$(GREEN)✓ Development environment reset$(NC)"; \
	else \
		echo "$(YELLOW)Reset cancelled$(NC)"; \
	fi

dev-start: ## Start development servers (API + Frontend)
	@echo "$(BLUE)Starting development servers...$(NC)"
	@make -j4 api-dev frontend-dev research-dev policy-dev

dev-stop: ## Stop development servers
	@echo "$(YELLOW)Stopping development servers...$(NC)"
	@pkill -f "air.*server" || true
	@pkill -f "npm.*dev" || true
	@echo "$(GREEN)✓ Development servers stopped$(NC)"

# ============================================================================
# DATABASE MANAGEMENT
# ============================================================================

.PHONY: db-migrate db-rollback db-seed db-reset db-shell db-test-connection db-sample-data
db-migrate: ## Run database migrations
	@echo "$(BLUE)Running database migrations...$(NC)"
	@go run ./cmd/migrate up
	@echo "$(GREEN)✓ Database migrations completed$(NC)"

db-rollback: ## Rollback last database migration
	@echo "$(YELLOW)Rolling back database migration...$(NC)"
	@go run ./cmd/migrate down 1
	@echo "$(GREEN)✓ Database rollback completed$(NC)"

db-seed: ## Seed database with development data
	@echo "$(BLUE)Seeding database with development data...$(NC)"
	@go run ./cmd/seed
	@echo "$(GREEN)✓ Database seeded$(NC)"

db-reset: ## Reset database (WARNING: destroys data)
	@echo "$(RED)WARNING: This will destroy all database data!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; echo; if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker-compose exec db psql -U resilience -d postgres -c "DROP DATABASE IF EXISTS resilience_dev;"; \
		docker-compose exec db psql -U resilience -d postgres -c "CREATE DATABASE resilience_dev;"; \
		make db-migrate; \
		make db-seed; \
		echo "$(GREEN)✓ Database reset completed$(NC)"; \
	else \
		echo "$(YELLOW)Database reset cancelled$(NC)"; \
	fi

db-shell: ## Connect to database shell
	@echo "$(BLUE)Connecting to database...$(NC)"
	@docker-compose exec db psql -U resilience -d resilience_dev

db-test-connection: ## Test database connection
	@echo "$(BLUE)Testing database connection...$(NC)"
	@go run ./cmd/db-test || (echo "$(RED)✗ Database connection failed$(NC)" && exit 1)
	@echo "$(GREEN)✓ Database connection successful$(NC)"

db-sample-data: ## Load sample community data for development
	@echo "$(BLUE)Loading sample community data...$(NC)"
	@go run ./cmd/resilience data
	@go run ./cmd/resilience model
	@echo "$(GREEN)✓ Sample data loaded$(NC)"

# ============================================================================
# API SERVER DEVELOPMENT
# ============================================================================

.PHONY: api-build api-dev api-test api-lint api-fmt api-clean debug-api
api-build: ## Build API server binary
	@echo "$(BLUE)Building API server...$(NC)"
	@mkdir -p $(BUILD_DIR)
	@go build -o $(BUILD_DIR)/server ./cmd/server
	@echo "$(GREEN)✓ API server built$(NC)"

api-dev: ## Start API server with hot reload
	@echo "$(BLUE)Starting API server with hot reload...$(NC)"
	@air -c .air.toml

api-test: ## Run API tests
	@echo "$(BLUE)Running API tests...$(NC)"
	@go test -v ./internal/...
	@echo "$(GREEN)✓ API tests completed$(NC)"

api-lint: ## Lint Go code
	@echo "$(BLUE)Linting Go code...$(NC)"
	@golangci-lint run
	@echo "$(GREEN)✓ Go code linting completed$(NC)"

api-fmt: ## Format Go code
	@echo "$(BLUE)Formatting Go code...$(NC)"
	@go fmt ./...
	@goimports -w .
	@echo "$(GREEN)✓ Go code formatted$(NC)"

api-clean: ## Clean API build artifacts
	@echo "$(YELLOW)Cleaning API build artifacts...$(NC)"
	@rm -rf $(BUILD_DIR)/server
	@go clean -cache
	@echo "$(GREEN)✓ API artifacts cleaned$(NC)"

debug-api: ## Start API server with debugger
	@echo "$(BLUE)Starting API server with debugger...$(NC)"
	@dlv debug ./cmd/server --headless --listen=:2345 --api-version=2 --accept-multiclient

# ============================================================================
# FRONTEND DEVELOPMENT
# ============================================================================

.PHONY: frontend-install frontend-dev frontend-build frontend-test frontend-lint frontend-fmt
frontend-install: ## Install frontend dependencies
	@echo "$(BLUE)Installing frontend dependencies...$(NC)"
	@cd frontend && npm install
	@cd frontend-research && npm install
	@cd frontend-policy && npm install
	@cd packages/design-system && npm install
	@echo "$(GREEN)✓ Frontend dependencies installed$(NC)"

frontend-dev: ## Start all frontend development servers
	@echo "$(BLUE)Starting frontend development servers...$(NC)"
	@make -j3 stories-dev research-dev policy-dev

stories-dev: ## Start Stories site development server
	@echo "$(PURPLE)Starting Stories site (port $(FRONTEND_PORT))...$(NC)"
	@cd frontend && npm run dev

research-dev: ## Start Research site development server  
	@echo "$(PURPLE)Starting Research site (port $(RESEARCH_PORT))...$(NC)"
	@cd frontend-research && npm run dev

policy-dev: ## Start Policy site development server
	@echo "$(PURPLE)Starting Policy site (port $(POLICY_PORT))...$(NC)"
	@cd frontend-policy && npm run dev

frontend-build: ## Build all frontend applications for production
	@echo "$(BLUE)Building frontend applications...$(NC)"
	@cd packages/design-system && npm run build
	@cd frontend && npm run build
	@cd frontend-research && npm run build
	@cd frontend-policy && npm run build
	@echo "$(GREEN)✓ Frontend applications built$(NC)"

frontend-test: ## Run frontend tests
	@echo "$(BLUE)Running frontend tests...$(NC)"
	@cd packages/design-system && npm run test
	@cd frontend && npm run test
	@cd frontend-research && npm run test
	@cd frontend-policy && npm run test
	@echo "$(GREEN)✓ Frontend tests completed$(NC)"

frontend-lint: ## Lint frontend code
	@echo "$(BLUE)Linting frontend code...$(NC)"
	@cd packages/design-system && npm run lint
	@cd frontend && npm run lint
	@cd frontend-research && npm run lint
	@cd frontend-policy && npm run lint
	@echo "$(GREEN)✓ Frontend code linting completed$(NC)"

frontend-fmt: ## Format frontend code
	@echo "$(BLUE)Formatting frontend code...$(NC)"
	@cd packages/design-system && npm run fmt
	@cd frontend && npm run fmt
	@cd frontend-research && npm run fmt
	@cd frontend-policy && npm run fmt
	@echo "$(GREEN)✓ Frontend code formatted$(NC)"

# ============================================================================
# TESTING
# ============================================================================

.PHONY: test-all test-quick test-go test-js test-integration test-e2e test-a11y test-coverage test-watch
test-all: ## Run complete test suite
	@echo "$(BLUE)Running complete test suite...$(NC)"
	@make test-go
	@make test-js
	@make test-integration
	@echo "$(GREEN)✓ All tests completed$(NC)"

test-quick: ## Run quick test suite (unit tests only)
	@echo "$(BLUE)Running quick test suite...$(NC)"
	@make test-go-unit
	@make test-js-unit
	@echo "$(GREEN)✓ Quick tests completed$(NC)"

test-go: ## Run all Go tests
	@echo "$(BLUE)Running Go tests...$(NC)"
	@go test -v -race ./...
	@echo "$(GREEN)✓ Go tests completed$(NC)"

test-go-unit: ## Run Go unit tests only
	@echo "$(BLUE)Running Go unit tests...$(NC)"
	@go test -v -short ./...
	@echo "$(GREEN)✓ Go unit tests completed$(NC)"

test-js: ## Run all JavaScript tests
	@echo "$(BLUE)Running JavaScript tests...$(NC)"
	@make frontend-test
	@echo "$(GREEN)✓ JavaScript tests completed$(NC)"

test-js-unit: ## Run JavaScript unit tests only
	@echo "$(BLUE)Running JavaScript unit tests...$(NC)"
	@cd packages/design-system && npm run test:unit
	@cd frontend && npm run test:unit
	@cd frontend-research && npm run test:unit
	@cd frontend-policy && npm run test:unit
	@echo "$(GREEN)✓ JavaScript unit tests completed$(NC)"

test-integration: ## Run integration tests
	@echo "$(BLUE)Running integration tests...$(NC)"
	@go test -v -tags=integration ./tests/integration/...
	@echo "$(GREEN)✓ Integration tests completed$(NC)"

test-e2e: ## Run end-to-end tests
	@echo "$(BLUE)Running end-to-end tests...$(NC)"
	@cd tests/e2e && npm run test
	@echo "$(GREEN)✓ End-to-end tests completed$(NC)"

test-e2e-headed: ## Run end-to-end tests in headed mode
	@echo "$(BLUE)Running end-to-end tests (headed)...$(NC)"
	@cd tests/e2e && npm run test:headed

test-a11y: ## Run accessibility tests
	@echo "$(BLUE)Running accessibility tests...$(NC)"
	@cd tests/e2e && npm run test:a11y
	@echo "$(GREEN)✓ Accessibility tests completed$(NC)"

test-coverage: ## Generate test coverage report
	@echo "$(BLUE)Generating test coverage report...$(NC)"
	@mkdir -p $(COVERAGE_DIR)
	@go test -coverprofile=$(COVERAGE_DIR)/coverage.out ./...
	@go tool cover -html=$(COVERAGE_DIR)/coverage.out -o $(COVERAGE_DIR)/coverage.html
	@echo "$(GREEN)✓ Coverage report generated: $(COVERAGE_DIR)/coverage.html$(NC)"

test-watch: ## Run tests in watch mode
	@echo "$(BLUE)Running tests in watch mode...$(NC)"
	@echo "$(YELLOW)Press Ctrl+C to stop$(NC)"
	@find . -name "*.go" | entr -r make test-go-unit

# ============================================================================
# CODE QUALITY
# ============================================================================

.PHONY: lint-all lint-go lint-js lint-fix fmt-all fmt-go fmt-js type-check
lint-all: ## Run all linters
	@echo "$(BLUE)Running all linters...$(NC)"
	@make lint-go
	@make lint-js
	@echo "$(GREEN)✓ All linting completed$(NC)"

lint-go: ## Lint Go code
	@make api-lint

lint-js: ## Lint JavaScript/TypeScript code
	@make frontend-lint

lint-fix: ## Fix linting issues automatically
	@echo "$(BLUE)Fixing linting issues...$(NC)"
	@golangci-lint run --fix
	@cd packages/design-system && npm run lint:fix
	@cd frontend && npm run lint:fix
	@cd frontend-research && npm run lint:fix
	@cd frontend-policy && npm run lint:fix
	@echo "$(GREEN)✓ Linting issues fixed$(NC)"

fmt-all: ## Format all code
	@echo "$(BLUE)Formatting all code...$(NC)"
	@make fmt-go
	@make fmt-js
	@echo "$(GREEN)✓ All code formatted$(NC)"

fmt-go: ## Format Go code
	@make api-fmt

fmt-js: ## Format JavaScript/TypeScript code
	@make frontend-fmt

type-check: ## Run TypeScript type checking
	@echo "$(BLUE)Running TypeScript type checking...$(NC)"
	@cd packages/design-system && npx tsc --noEmit
	@cd frontend && npx tsc --noEmit
	@cd frontend-research && npx tsc --noEmit
	@cd frontend-policy && npx tsc --noEmit
	@echo "$(GREEN)✓ TypeScript type checking completed$(NC)"

# ============================================================================
# BUILD & DEPLOYMENT
# ============================================================================

.PHONY: build-all build-prod build-docker deploy-staging deploy-prod
build-all: ## Build all applications
	@echo "$(BLUE)Building all applications...$(NC)"
	@make api-build
	@make frontend-build
	@echo "$(GREEN)✓ All applications built$(NC)"

build-prod: ## Build production versions
	@echo "$(BLUE)Building production versions...$(NC)"
	@CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o $(BUILD_DIR)/server ./cmd/server
	@make frontend-build
	@echo "$(GREEN)✓ Production builds completed$(NC)"

build-docker: ## Build Docker images
	@echo "$(BLUE)Building Docker images...$(NC)"
	@docker build -t $(DOCKER_REGISTRY)/api-server:$(DOCKER_TAG) -f deployments/docker/api.Dockerfile .
	@docker build -t $(DOCKER_REGISTRY)/frontend:$(DOCKER_TAG) -f deployments/docker/frontend.Dockerfile .
	@echo "$(GREEN)✓ Docker images built$(NC)"

serve-prod: ## Serve production build locally
	@echo "$(BLUE)Serving production build locally...$(NC)"
	@docker-compose -f $(COMPOSE_FILE_PROD) up

deploy-staging: ## Deploy to staging environment
	@echo "$(BLUE)Deploying to staging...$(NC)"
	@echo "$(YELLOW)This would trigger staging deployment$(NC)"
	@echo "$(CYAN)Implement with your deployment tool (Kubernetes, etc.)$(NC)"

deploy-prod: ## Deploy to production environment
	@echo "$(RED)WARNING: Production deployment!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; echo; if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		echo "$(BLUE)Deploying to production...$(NC)"; \
		echo "$(YELLOW)This would trigger production deployment$(NC)"; \
		echo "$(CYAN)Implement with your deployment tool (Kubernetes, etc.)$(NC)"; \
	else \
		echo "$(YELLOW)Production deployment cancelled$(NC)"; \
	fi

# ============================================================================
# MONITORING & DEBUGGING
# ============================================================================

.PHONY: logs-all logs-api logs-db logs-redis logs-elasticsearch logs-service monitor-resources health-check
logs-all: ## View logs from all services
	@echo "$(BLUE)Viewing logs from all services...$(NC)"
	@docker-compose logs -f

logs-api: ## View API server logs
	@echo "$(BLUE)Viewing API server logs...$(NC)"
	@docker-compose logs -f api

logs-db: ## View database logs
	@echo "$(BLUE)Viewing database logs...$(NC)"
	@docker-compose logs -f db

logs-redis: ## View Redis logs
	@echo "$(BLUE)Viewing Redis logs...$(NC)"
	@docker-compose logs -f redis

logs-elasticsearch: ## View Elasticsearch logs
	@echo "$(BLUE)Viewing Elasticsearch logs...$(NC)"
	@docker-compose logs -f elasticsearch

logs-service: ## View logs from specific service (usage: make logs-service service=api)
	@echo "$(BLUE)Viewing logs from $(service)...$(NC)"
	@docker-compose logs -f $(service)

monitor-resources: ## Monitor system resources
	@echo "$(BLUE)Monitoring system resources...$(NC)"
	@docker stats

health-check: ## Check health of all services
	@echo "$(BLUE)Checking health of all services...$(NC)"
	@echo "$(CYAN)API Server:$(NC)"
	@curl -s http://localhost:$(API_PORT)/health || echo "$(RED)✗ API Server unhealthy$(NC)"
	@echo "$(CYAN)PostgreSQL:$(NC)"
	@docker-compose exec -T db pg_isready -U resilience || echo "$(RED)✗ PostgreSQL unhealthy$(NC)"
	@echo "$(CYAN)Redis:$(NC)"
	@docker-compose exec -T redis redis-cli ping || echo "$(RED)✗ Redis unhealthy$(NC)"
	@echo "$(CYAN)Elasticsearch:$(NC)"
	@curl -s http://localhost:$(ELASTICSEARCH_PORT)/_health || echo "$(RED)✗ Elasticsearch unhealthy$(NC)"
	@echo "$(GREEN)✓ Health check completed$(NC)"

# ============================================================================
# DOCUMENTATION
# ============================================================================

.PHONY: docs-serve docs-api docs-update docs-generate
docs-serve: ## Serve documentation locally
	@echo "$(BLUE)Serving documentation...$(NC)"
	@cd docs && python3 -m http.server 8000
	@echo "$(CYAN)Documentation available at: http://localhost:8000$(NC)"

docs-api: ## Generate API documentation
	@echo "$(BLUE)Generating API documentation...$(NC)"
	@swag init -g cmd/server/main.go -o docs/api
	@echo "$(GREEN)✓ API documentation generated$(NC)"

docs-update: ## Update all documentation
	@echo "$(BLUE)Updating documentation...$(NC)"
	@make docs-api
	@echo "$(GREEN)✓ Documentation updated$(NC)"

docs-generate: ## Generate project documentation
	@echo "$(BLUE)Generating project documentation...$(NC)"
	@godoc -http=:6060 &
	@echo "$(CYAN)Go documentation available at: http://localhost:6060$(NC)"

# ============================================================================
# UTILITIES & MAINTENANCE
# ============================================================================

.PHONY: clean-all clean-docker clean-cache deps-update security-scan version-info
clean-all: ## Clean all build artifacts and caches
	@echo "$(YELLOW)Cleaning all build artifacts and caches...$(NC)"
	@make api-clean
	@rm -rf $(BUILD_DIR) $(COVERAGE_DIR) $(LOGS_DIR)
	@rm -rf frontend/node_modules frontend/.next
	@rm -rf frontend-research/node_modules frontend-research/.next
	@rm -rf frontend-policy/node_modules frontend-policy/.next
	@rm -rf packages/design-system/node_modules packages/design-system/dist
	@go clean -cache -modcache
	@echo "$(GREEN)✓ Cleanup completed$(NC)"

clean-docker: ## Clean Docker resources
	@echo "$(YELLOW)Cleaning Docker resources...$(NC)"
	@docker system prune -f
	@docker volume prune -f
	@echo "$(GREEN)✓ Docker cleanup completed$(NC)"

clean-cache: ## Clean development caches
	@echo "$(YELLOW)Cleaning development caches...$(NC)"
	@go clean -cache
	@rm -rf frontend/.next/cache
	@rm -rf frontend-research/.next/cache
	@rm -rf frontend-policy/.next/cache
	@echo "$(GREEN)✓ Cache cleanup completed$(NC)"

deps-update: ## Update all dependencies
	@echo "$(BLUE)Updating dependencies...$(NC)"
	@go get -u ./...
	@go mod tidy
	@cd packages/design-system && npm update
	@cd frontend && npm update
	@cd frontend-research && npm update
	@cd frontend-policy && npm update
	@echo "$(GREEN)✓ Dependencies updated$(NC)"

security-scan: ## Run security vulnerability scans
	@echo "$(BLUE)Running security scans...$(NC)"
	@gosec ./...
	@cd packages/design-system && npm audit
	@cd frontend && npm audit
	@cd frontend-research && npm audit
	@cd frontend-policy && npm audit
	@echo "$(GREEN)✓ Security scans completed$(NC)"

version-info: ## Show version information
	@echo "$(BLUE)Version Information:$(NC)"
	@echo "  Go Version:      $$(go version)"
	@echo "  Node Version:    $$(node --version)"
	@echo "  Docker Version:  $$(docker --version)"
	@echo "  Git Version:     $$(git --version)"

# ============================================================================
# ORIGINAL DATA ANALYSIS COMMANDS (PRESERVED)
# ============================================================================

.PHONY: data model map analyze
data: ## Run original data processing
	@echo "$(BLUE)Running data processing...$(NC)"
	@go run ./cmd/resilience data

model: ## Run original model analysis
	@echo "$(BLUE)Running model analysis...$(NC)"
	@go run ./cmd/resilience model

map: ## Generate original visualization
	@echo "$(BLUE)Generating map visualization...$(NC)"
	@go run ./cmd/resilience map

analyze: ## Run complete data analysis pipeline
	@echo "$(BLUE)Running complete analysis pipeline...$(NC)"
	@make clean
	@make data
	@make model
	@make map
	@echo "$(GREEN)✓ Analysis pipeline completed$(NC)"

# ============================================================================
# SPECIAL TARGETS
# ============================================================================

# Create necessary directories
$(BUILD_DIR) $(COVERAGE_DIR) $(LOGS_DIR):
	@mkdir -p $@

# Ensure dependencies are installed
deps-check:
	@command -v go >/dev/null 2>&1 || { echo "$(RED)Go is not installed$(NC)"; exit 1; }
	@command -v node >/dev/null 2>&1 || { echo "$(RED)Node.js is not installed$(NC)"; exit 1; }
	@command -v docker >/dev/null 2>&1 || { echo "$(RED)Docker is not installed$(NC)"; exit 1; }

# ============================================================================
# COMMUNITY-FOCUSED TARGETS
# ============================================================================

.PHONY: community-first dignity-check accessibility-audit
community-first: ## Remind about community-first principles
	@echo "$(PURPLE)🤝 COMMUNITY-FIRST DEVELOPMENT REMINDER 🤝$(NC)"
	@echo ""
	@echo "$(CYAN)Before you ship:$(NC)"
	@echo "  ✓ Community approval obtained"
	@echo "  ✓ Accessibility tested (WCAG AAA)"
	@echo "  ✓ Mobile performance validated"
	@echo "  ✓ Content reviewed for dignity"
	@echo "  ✓ No harm potential identified"
	@echo ""
	@echo "$(YELLOW)Building for 1,000+ communities with respect and care.$(NC)"

dignity-check: ## Check for dignity-preserving code patterns
	@echo "$(PURPLE)Checking for dignity-preserving patterns...$(NC)"
	@echo "$(YELLOW)Scanning for problematic language...$(NC)"
	@! grep -r -i "food desert\|struggling\|failing\|poor" frontend/ || echo "$(RED)Found deficit language - consider alternatives$(NC)"
	@echo "$(GREEN)✓ Dignity check completed$(NC)"

accessibility-audit: ## Run comprehensive accessibility audit
	@echo "$(BLUE)Running accessibility audit...$(NC)"
	@make test-a11y
	@echo "$(CYAN)Remember: We build for everyone, including screen reader users$(NC)"
	@echo "$(GREEN)✓ Accessibility audit completed$(NC)"

# ============================================================================
# END OF MAKEFILE
# ============================================================================

# Make sure all targets that don't create files are marked as PHONY
.PHONY: help dev-up dev-down dev-restart dev-status dev-reset dev-start dev-stop
.PHONY: db-migrate db-rollback db-seed db-reset db-shell db-test-connection db-sample-data
.PHONY: api-build api-dev api-test api-lint api-fmt api-clean debug-api
.PHONY: frontend-install frontend-dev frontend-build frontend-test frontend-lint frontend-fmt
.PHONY: stories-dev research-dev policy-dev
.PHONY: test-all test-quick test-go test-js test-integration test-e2e test-a11y test-coverage test-watch
.PHONY: test-go-unit test-js-unit
.PHONY: lint-all lint-go lint-js lint-fix fmt-all fmt-go fmt-js type-check
.PHONY: build-all build-prod build-docker serve-prod deploy-staging deploy-prod
.PHONY: logs-all logs-api logs-db logs-redis logs-elasticsearch logs-service monitor-resources health-check
.PHONY: docs-serve docs-api docs-update docs-generate
.PHONY: clean-all clean-docker clean-cache deps-update security-scan version-info
.PHONY: data model map analyze community-first dignity-check accessibility-audit