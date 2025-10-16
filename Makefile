# Simple Commands for Simple Structure
.DEFAULT_GOAL := help

help: ## Show this help
	@echo "📦 RESILIENCE MAPPING COMMANDS"
	@echo ""
	@echo "Quick Actions:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

run: ## Run the Go backend
	cd app/backend && go run *.go

analyze: ## Run Python analysis
	cd app/analytics && python analyze_resilience.py

test: ## Run tests
	cd app/backend && go test ./...

setup: ## Initial project setup
	@echo "Installing Go dependencies..."
	cd app/backend && go mod init resilience 2>/dev/null || go mod download
	@echo "Installing Python dependencies..."
	cd app/analytics && pip install -r requirements.txt

clean: ## Clean generated files
	rm -rf data/output/*
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -delete

data: ## Download required data files
	@echo "📊 Data download instructions:"
	@echo "1. Download CDC PLACES data"
	@echo "2. Place in data/input/"
	@echo "See docs/setup/data-download.md for details"

.PHONY: help run analyze test setup clean data
