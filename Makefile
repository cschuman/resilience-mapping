# Resilience Mapping - SvelteKit + Fly.io
.DEFAULT_GOAL := help

help: ## Show this help
	@echo "RESILIENCE MAPPING COMMANDS"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

dev: ## Run SvelteKit dev server
	cd app/web && npm run dev

build: ## Build for production
	cd app/web && npm run build

preview: ## Preview production build
	cd app/web && npm run preview

test: ## Run tests
	cd app/web && npm run test:run

check: ## Run type checking and linting
	cd app/web && npm run check

analyze: ## Run Python analysis
	cd app/analytics && python analyze_resilience.py

setup: ## Initial project setup
	@echo "Installing web dependencies..."
	cd app/web && npm install
	@echo "Installing Python dependencies..."
	cd app/analytics && pip install -r requirements.txt

deploy: ## Deploy to Fly.io
	cd app/web && fly deploy

clean: ## Clean generated files
	rm -rf app/web/.svelte-kit
	rm -rf app/web/build
	rm -rf data/output/*
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -delete

.PHONY: help dev build preview test check analyze setup deploy clean
