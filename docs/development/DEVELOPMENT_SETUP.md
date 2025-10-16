# 🛠 DEVELOPMENT ENVIRONMENT SETUP
## Health Resilience Mapping Platform

**Created**: January 31, 2025  
**Version**: 1.0  
**For**: Development Team Onboarding

---

## 🎯 QUICK START

New to the project? Follow this path:
1. **Prerequisites** → Install required tools
2. **Clone & Setup** → Get the code running locally
3. **Verify Installation** → Run tests and see the site
4. **Development Workflow** → Understand our process
5. **First Contribution** → Make your first PR

**Estimated setup time**: 30-60 minutes

---

## 📋 PREREQUISITES

### **Required Software**

#### **Core Development Tools**
```bash
# Go (backend API and data processing)
Go 1.21+ 
Download: https://golang.org/dl/

# Node.js (frontend applications)
Node.js 18+ with npm/yarn
Download: https://nodejs.org/

# Docker (local development environment)
Docker Desktop
Download: https://www.docker.com/products/docker-desktop/

# Git (version control)
Git 2.30+
Download: https://git-scm.com/
```

#### **Database Tools**
```bash
# PostgreSQL Client (optional - Docker handles the server)
psql (PostgreSQL) 14+

# Redis CLI (optional - for debugging cache)
redis-cli

# PostGIS (for geographic data - included in Docker)
PostGIS 3.2+
```

#### **Development Utilities**
```bash
# Make (for running development commands)
make (usually pre-installed on macOS/Linux)

# Air (for Go hot reload during development)
go install github.com/air-verse/air@latest

# golangci-lint (for code linting)
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
```

### **Recommended Tools**

#### **Code Editors**
- **VS Code** with Go and React extensions
- **Vim/Neovim** with appropriate language plugins
- **GoLand** (JetBrains IDE)

#### **API Testing**
- **Postman** or **Insomnia** for API testing
- **curl** for command-line API testing

#### **Database Tools**
- **pgAdmin** or **TablePlus** for PostgreSQL GUI
- **Redis Desktop Manager** for Redis GUI

---

## 🚀 LOCAL DEVELOPMENT SETUP

### **1. Clone the Repository**
```bash
# Clone the main repository
git clone https://github.com/your-org/resilience-mapping-go.git
cd resilience-mapping-go

# Check out the development branch
git checkout develop
git pull origin develop
```

### **2. Environment Configuration**
```bash
# Copy environment template
cp .env.example .env.local

# Edit environment variables
nano .env.local
```

**Required Environment Variables:**
```bash
# Database Configuration
DATABASE_URL=postgres://resilience:resilience_password@localhost:5432/resilience_dev
REDIS_URL=redis://localhost:6379
ELASTICSEARCH_URL=http://localhost:9200

# API Configuration
API_PORT=8080
API_HOST=localhost
JWT_SECRET=your-super-secret-jwt-key-for-development-only

# Frontend Configuration
NEXT_PUBLIC_API_URL=http://localhost:8080
NEXT_PUBLIC_SITE_URL=http://localhost:3000

# External Services (optional for local dev)
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
S3_BUCKET_NAME=resilience-mapping-dev

# Email Configuration (optional)
SMTP_HOST=localhost
SMTP_PORT=1025
SMTP_USER=test@example.com
SMTP_PASSWORD=password
```

### **3. Start Development Services**
```bash
# Start all services with Docker Compose
make dev-up

# Alternative: start services individually
docker-compose up -d db redis elasticsearch

# Check services are running
make dev-status
```

**Docker Compose Services:**
- **PostgreSQL** (port 5432) - Main database with PostGIS
- **Redis** (port 6379) - Caching and sessions
- **Elasticsearch** (port 9200) - Search functionality
- **MailHog** (port 1025/8025) - Email testing

### **4. Database Setup**
```bash
# Run database migrations
make db-migrate

# Seed development data
make db-seed

# Load sample communities (optional)
make db-sample-data

# Verify database setup
make db-test-connection
```

### **5. Backend Setup (Go API)**
```bash
# Install Go dependencies
go mod download

# Build the API server
make api-build

# Run the API server with hot reload
make api-dev

# Verify API is running
curl http://localhost:8080/health
```

### **6. Frontend Setup (React/Next.js)**
```bash
# Install Node.js dependencies
cd frontend
npm install

# Start the development server
npm run dev

# In another terminal, start the other sites
cd ../frontend-research
npm install && npm run dev

cd ../frontend-policy  
npm install && npm run dev
```

### **7. Verify Installation**
```bash
# Run all tests
make test-all

# Check code quality
make lint-all

# Verify all services
make health-check

# Open development sites
open http://localhost:3000  # Stories site
open http://localhost:3001  # Research site
open http://localhost:3002  # Policy site
open http://localhost:8080  # API documentation
```

---

## 📁 PROJECT STRUCTURE

### **Repository Organization**
```
resilience-mapping-go/
├── README.md                    # Project overview
├── TEAM_CHARTER.md             # Team values and processes
├── DEVELOPMENT_SETUP.md        # This file
├── docker-compose.yml          # Local development services
├── Makefile                    # Development commands
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── .golangci.yml              # Go linting configuration
│
├── cmd/                       # Go application entry points
│   ├── server/                # API server main
│   │   └── main.go           
│   ├── workers/               # Background workers
│   │   ├── etl/              # Data processing
│   │   ├── notifications/    # Email/alerts
│   │   └── analytics/        # Usage analytics
│   └── cli/                   # Command-line tools
│       └── main.go           
│
├── internal/                  # Private Go packages
│   ├── api/                  # HTTP handlers and routes
│   │   ├── communities/      # Community endpoints
│   │   ├── stories/          # Story endpoints
│   │   ├── research/         # Research endpoints
│   │   ├── policy/           # Policy endpoints
│   │   └── search/           # Search endpoints
│   ├── services/             # Business logic
│   ├── repositories/         # Data access layer
│   ├── models/               # Data structures
│   └── middleware/           # HTTP middleware
│
├── frontend/                  # Stories site (Next.js)
│   ├── pages/                # Next.js pages
│   ├── components/           # React components
│   ├── lib/                  # Utility functions
│   ├── styles/               # CSS/styling
│   ├── public/               # Static assets
│   └── package.json          
│
├── frontend-research/         # Research site (Next.js)
├── frontend-policy/          # Policy site (Next.js)
│
├── packages/                 # Shared packages
│   ├── design-system/        # Shared UI components
│   ├── api-client/           # API client library
│   └── utils/                # Shared utilities
│
├── migrations/               # Database migrations
├── seeds/                    # Database seed data
├── docs/                     # Documentation
├── scripts/                  # Development scripts
├── tests/                    # Test files
│   ├── api/                  # API tests
│   ├── frontend/             # Frontend tests
│   └── integration/          # Integration tests
└── deployments/              # Deployment configurations
    ├── docker/               # Docker files
    ├── kubernetes/           # K8s manifests
    └── terraform/            # Infrastructure as code
```

### **Key Configuration Files**
```
# Go Configuration
├── go.mod                    # Go module definition
├── go.sum                    # Go dependency checksums
├── .golangci.yml            # Go linting rules

# Frontend Configuration
├── frontend/package.json     # Node.js dependencies
├── frontend/next.config.js   # Next.js configuration
├── frontend/tailwind.config.js # Tailwind CSS config
├── frontend/tsconfig.json    # TypeScript config

# Development Tools
├── docker-compose.yml        # Local development services
├── Makefile                  # Development commands
├── .github/workflows/        # CI/CD pipelines
└── .vscode/                  # VS Code settings
```

---

## 🔧 DEVELOPMENT WORKFLOW

### **Daily Development Process**

#### **1. Start Your Day**
```bash
# Get latest changes
git checkout develop
git pull origin develop

# Start development environment
make dev-up

# Run tests to ensure everything works
make test-quick
```

#### **2. Create Feature Branch**
```bash
# Create feature branch from develop
git checkout -b feature/your-feature-name

# Start development servers
make dev-start
```

#### **3. Development Loop**
```bash
# Make changes to code

# Run tests frequently
make test-watch

# Check code quality
make lint-fix

# Commit changes frequently
git add .
git commit -m "feat: add community search functionality"
```

#### **4. Before Creating PR**
```bash
# Run full test suite
make test-all

# Check code quality
make lint-all

# Build production versions
make build-all

# Update documentation if needed
make docs-update
```

### **Git Workflow**

#### **Branch Naming Convention**
```
feature/short-description     # New features
bugfix/issue-description     # Bug fixes  
hotfix/critical-fix          # Emergency fixes
chore/maintenance-task       # Maintenance work
docs/documentation-update    # Documentation changes
```

#### **Commit Message Format**
```
type(scope): short description

feat(api): add community search endpoint
fix(frontend): resolve mobile navigation bug  
docs(readme): update installation instructions
test(api): add integration tests for search
chore(deps): update Go dependencies
```

#### **Pull Request Process**
1. **Create PR** against `develop` branch
2. **Add description** explaining changes and why
3. **Link issues** that are resolved
4. **Request reviews** from relevant team members
5. **Address feedback** and update PR
6. **Merge** after approval and passing tests

---

## 🧪 TESTING STRATEGY

### **Test Types and Commands**

#### **Unit Tests**
```bash
# Run Go unit tests
make test-go-unit

# Run JavaScript unit tests  
make test-js-unit

# Run tests with coverage
make test-coverage

# Watch mode for development
make test-watch
```

#### **Integration Tests**
```bash
# Run API integration tests
make test-api-integration

# Run database integration tests
make test-db-integration

# Run full integration suite
make test-integration
```

#### **End-to-End Tests**
```bash
# Run Playwright e2e tests
make test-e2e

# Run e2e tests in headed mode
make test-e2e-headed

# Run specific e2e test suite
make test-e2e-stories
```

#### **Accessibility Tests**
```bash
# Run accessibility tests
make test-a11y

# Generate accessibility report
make test-a11y-report
```

### **Writing Tests**

#### **Go Unit Test Example**
```go
// internal/services/community_test.go
package services

import (
    "testing"
    "github.com/stretchr/testify/assert"
)

func TestCommunityService_FindSimilar(t *testing.T) {
    service := NewCommunityService(mockRepo)
    
    similar, err := service.FindSimilar("community-id", 5)
    
    assert.NoError(t, err)
    assert.Len(t, similar, 5)
    assert.Equal(t, "expected-id", similar[0].ID)
}
```

#### **React Component Test Example**
```javascript
// frontend/components/CommunityCard.test.tsx
import { render, screen } from '@testing-library/react'
import { CommunityCard } from './CommunityCard'

describe('CommunityCard', () => {
  it('displays community information correctly', () => {
    const community = {
      name: 'Test Community',
      state: 'TX',
      population: 5000
    }
    
    render(<CommunityCard community={community} />)
    
    expect(screen.getByText('Test Community')).toBeInTheDocument()
    expect(screen.getByText('TX')).toBeInTheDocument()
    expect(screen.getByText('5,000')).toBeInTheDocument()
  })
})
```

---

## 🐛 DEBUGGING TOOLS

### **Backend Debugging**

#### **Go Debugging**
```bash
# Run with debugger
make debug-api

# Use delve debugger
dlv debug ./cmd/server

# Debug with VS Code
# Add breakpoints and press F5
```

#### **Database Debugging**
```bash
# Connect to database
make db-shell

# View logs
make logs-db

# Query performance analysis
make db-analyze-queries
```

#### **API Debugging**
```bash
# View API logs
make logs-api

# Test API endpoints
make api-test-endpoints

# Monitor API performance
make api-monitor
```

### **Frontend Debugging**

#### **React DevTools**
- Install React Developer Tools browser extension
- Use React Profiler for performance analysis
- Debug component state and props

#### **Next.js Debugging**
```bash
# Debug with Node.js inspector
npm run dev:debug

# Enable Next.js debugging
DEBUG=next:* npm run dev
```

### **Full Stack Debugging**
```bash
# View all service logs
make logs-all

# Debug specific service
make logs-service service=api

# Monitor system resources
make monitor-resources
```

---

## 📏 CODE STANDARDS

### **Go Code Standards**

#### **Formatting and Linting**
```bash
# Format code
make fmt-go

# Run linter
make lint-go

# Fix linting issues automatically
make lint-go-fix
```

#### **Go Style Guidelines**
- Follow [Effective Go](https://golang.org/doc/effective_go.html)
- Use `gofmt` for formatting
- Write comprehensive tests
- Use meaningful variable names
- Add comments for exported functions
- Handle errors explicitly

#### **Go Example**
```go
// Package community provides community-related business logic.
package community

import (
    "context"
    "fmt"
)

// Service handles community operations.
type Service struct {
    repo Repository
}

// FindSimilar returns communities similar to the given community.
func (s *Service) FindSimilar(ctx context.Context, communityID string, limit int) ([]Community, error) {
    if communityID == "" {
        return nil, fmt.Errorf("community ID cannot be empty")
    }
    
    communities, err := s.repo.FindSimilar(ctx, communityID, limit)
    if err != nil {
        return nil, fmt.Errorf("finding similar communities: %w", err)
    }
    
    return communities, nil
}
```

### **JavaScript/TypeScript Standards**

#### **Formatting and Linting**
```bash
# Format code
make fmt-js

# Run ESLint
make lint-js

# Fix linting issues
make lint-js-fix

# Type check TypeScript
make type-check
```

#### **JavaScript/TypeScript Guidelines**
- Use TypeScript for type safety
- Follow React best practices
- Write unit tests for components
- Use meaningful component and variable names
- Implement proper error boundaries
- Follow accessibility guidelines

#### **React Component Example**
```typescript
// components/CommunityCard.tsx
import { FC } from 'react'

interface Community {
  id: string
  name: string
  state: string
  population: number
  resilienceScore: number
}

interface CommunityCardProps {
  community: Community
  onSelect?: (id: string) => void
  className?: string
}

export const CommunityCard: FC<CommunityCardProps> = ({
  community,
  onSelect,
  className = ''
}) => {
  const handleClick = () => {
    onSelect?.(community.id)
  }
  
  return (
    <div 
      className={`community-card ${className}`}
      onClick={handleClick}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => e.key === 'Enter' && handleClick()}
    >
      <h3>{community.name}</h3>
      <p>{community.state}</p>
      <p>Population: {community.population.toLocaleString()}</p>
      <p>Resilience Score: {community.resilienceScore}</p>
    </div>
  )
}
```

### **CSS/Styling Standards**
```bash
# Use Tailwind CSS for styling
# Follow mobile-first approach
# Ensure accessibility compliance
# Use semantic class names
```

---

## 📚 DOCUMENTATION

### **Code Documentation**

#### **Go Documentation**
```go
// Use Go doc comments for exported functions
// Run: go doc ./internal/services

// Package documentation
// Service provides community-related operations.

// Function documentation  
// FindSimilar returns up to 'limit' communities similar to the given community.
// It uses demographic and geographic similarity algorithms.
```

#### **JavaScript Documentation**
```javascript
/**
 * Community card component for displaying community information
 * @param community - The community data to display
 * @param onSelect - Callback when community is selected
 * @param className - Additional CSS classes
 */
```

### **API Documentation**
```bash
# Generate API documentation
make docs-api

# Serve documentation locally
make docs-serve

# Update OpenAPI specification
make docs-update-api
```

### **Architecture Documentation**
- Keep `docs/` folder updated with architectural decisions
- Document major design decisions in ADRs (Architecture Decision Records)
- Update README files when changing setup processes

---

## 🚀 DEPLOYMENT

### **Local Testing**
```bash
# Build production versions
make build-prod

# Test production build locally
make serve-prod

# Run production smoke tests
make test-prod
```

### **Staging Deployment**
```bash
# Deploy to staging (auto from develop branch)
git push origin develop

# Manual staging deployment
make deploy-staging

# Run staging tests
make test-staging
```

### **Production Deployment**
```bash
# Create release branch
git checkout -b release/v1.2.0

# Update version numbers
make version-update

# Deploy to production (auto from main branch)
git checkout main
git merge release/v1.2.0
git push origin main

# Monitor deployment
make monitor-prod
```

---

## 🔍 TROUBLESHOOTING

### **Common Issues**

#### **Docker Issues**
```bash
# Problem: Services won't start
# Solution: Reset Docker environment
make dev-reset
docker system prune -f
make dev-up

# Problem: Port already in use
# Solution: Check what's using the port
lsof -i :8080
kill -9 [PID]
```

#### **Database Issues**
```bash
# Problem: Database connection failed
# Solution: Restart database service
docker-compose restart db
make db-test-connection

# Problem: Migration failed
# Solution: Reset database
make db-reset
make db-migrate
```

#### **Frontend Issues**
```bash
# Problem: Node modules issues
# Solution: Clean install
rm -rf node_modules package-lock.json
npm install

# Problem: Build failures
# Solution: Clear Next.js cache
npm run clean
npm run build
```

#### **API Issues**
```bash
# Problem: API not responding
# Solution: Check logs and restart
make logs-api
make restart-api

# Problem: Tests failing
# Solution: Check test database
make test-db-reset
make test-all
```

### **Getting Help**

#### **Internal Resources**
- **Team Chat**: Slack #resilience-dev channel
- **Documentation**: `docs/` folder in repository
- **Issue Tracking**: GitHub Issues
- **Code Review**: GitHub Pull Requests

#### **External Resources**
- **Go Documentation**: https://golang.org/doc/
- **React Documentation**: https://reactjs.org/docs/
- **Next.js Documentation**: https://nextjs.org/docs
- **PostgreSQL Documentation**: https://www.postgresql.org/docs/

### **Debugging Checklist**
1. **Check service status**: `make dev-status`
2. **Review recent logs**: `make logs-all`
3. **Verify environment**: Check `.env.local` file
4. **Test database**: `make db-test-connection`
5. **Clear caches**: `make clean-all`
6. **Restart services**: `make dev-restart`
7. **Ask for help**: Post in team chat with error details

---

## 🎯 DEVELOPMENT COMMANDS REFERENCE

### **Most Used Commands**
```bash
# Start development
make dev-up              # Start all services
make dev-start           # Start development servers
make dev-status          # Check service status

# Testing
make test-quick          # Fast test suite
make test-all           # Complete test suite  
make test-watch         # Watch mode testing

# Code quality
make lint-all           # Run all linters
make fmt-all            # Format all code
make type-check         # TypeScript type checking

# Database
make db-migrate         # Run migrations
make db-seed            # Seed development data
make db-reset           # Reset database

# Debugging
make logs-all           # View all logs
make logs-api           # View API logs
make debug-api          # Debug API server

# Cleanup
make clean-all          # Clean build artifacts
make dev-reset          # Reset development environment
```

### **Complete Makefile Reference**
```bash
# View all available commands
make help

# Or check the Makefile directly
cat Makefile
```

---

## 🎉 WELCOME TO THE TEAM!

You're now ready to contribute to the Health Resilience Mapping Platform! Remember:

1. **Community First**: Everything we build serves communities
2. **Quality Matters**: Take time to write good code and tests
3. **Ask Questions**: Better to ask than make incorrect assumptions
4. **Documentation**: Keep docs updated as you work
5. **Collaboration**: Work together, review each other's code

**Ready to make your first contribution?**
1. Pick an issue labeled `good-first-issue`
2. Follow the workflow above
3. Create your first PR
4. Celebrate! 🎉

**Questions?** Ask in #resilience-dev Slack channel or create a GitHub issue.

---

**Happy Coding!** 🚀

*Last updated: January 31, 2025*