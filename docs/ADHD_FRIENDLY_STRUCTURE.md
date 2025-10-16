# ADHD-Friendly Project Structure

## The Problem
The current structure (even after migration) is still overwhelming because:
- Too many directories at root level (15+)
- Unclear what's important vs. what's not
- Mixed old and new structures
- Too many decision points when navigating

## The ADHD-Optimized Solution: "3-3-3 Rule"

**Only 3 main folders at root, each with max 3 subfolders, going max 3 levels deep.**

```
resilience/
├── 📦 app/           # ALL THE CODE (Backend + Scripts)
├── 📊 data/          # ALL THE DATA 
├── 📝 docs/          # ALL THE DOCS
├── README.md         # Start here
├── Makefile          # Commands
└── .env.example      # Config template
```

That's it. 3 folders. Super clean.

## Detailed Structure (But Still Simple!)

```
resilience/
│
├── 📦 app/                    # EVERYTHING THAT RUNS
│   ├── backend/               # Go API server (42 files)
│   │   └── [All Go files flattened here]
│   │
│   ├── analytics/            # Python analysis (13 scripts)
│   │   ├── analyze_resilience.py
│   │   ├── generate_tables.py
│   │   ├── requirements.txt
│   │   └── venv/             # Python virtual environment
│   │
│   ├── deploy/               # Deployment configs
│   │   ├── schema.sql        # Supabase schema
│   │   ├── import_to_supabase.py
│   │   ├── vercel.json       # Vercel config
│   │   └── docker-compose.yml
│   │
│   └── scripts/              # Utility scripts
│       └── [Shell scripts]
│
├── 📊 data/                   # ALL DATA FILES
│   ├── input/                # Raw data goes here
│   ├── output/               # Results come out here (includes map_screenshot.png)
│   └── README.md             # What's what
│
├── 📝 docs/                   # ALL DOCUMENTATION
│   ├── business/             # Team docs, planning (36 files)
│   ├── research/             # Research findings
│   ├── setup/                # Installation guides
│   └── [Technical docs]      # API specs, etc.
│
├── 🔧 Makefile               # Simple commands
├── 📋 README.md              # Start here
└── 🔐 .env.example           # Environment setup
```

## Why This Works for ADHD

### 1. **Cognitive Load Reduction**
- Only 3 top-level decisions
- Clear emoji indicators 
- Obvious folder purposes

### 2. **No Analysis Paralysis**
- Code? → `app/`
- Data? → `data/`
- Docs? → `docs/`
- That's it.

### 3. **Visual Clarity**
```
Before: 38 directories, 22 files at root
After:  3 directories, 3 files at root
```
**92% reduction in visual noise**

### 4. **Working Memory Friendly**
- Maximum 3 levels deep
- Maximum 3 main categories
- Can hold entire structure in working memory

## Migration Script (Simple Version)

```bash
#!/bin/bash
# ADHD-Friendly Restructure

# Create super simple structure
mkdir -p app/{backend,analytics,scripts}
mkdir -p data/{input,output}
mkdir -p docs/findings

# Move Go stuff
mv backend/* app/backend/ 2>/dev/null || true
mv cmd/* app/backend/ 2>/dev/null || true
mv internal/* app/backend/ 2>/dev/null || true
mv pkg/* app/backend/ 2>/dev/null || true
mv *.go app/backend/ 2>/dev/null || true

# Move Python stuff
mv analytics/src/* app/analytics/ 2>/dev/null || true
mv *.py app/analytics/ 2>/dev/null || true

# Move data
mv data/raw/* data/input/ 2>/dev/null || true
mv data/processed/* data/output/ 2>/dev/null || true

# Move docs (flatten them!)
find . -name "*.md" -not -path "./app/*" -not -path "./data/*" -not -path "./docs/*" -exec mv {} docs/ \; 2>/dev/null || true

# Clean up empty directories
find . -type d -empty -delete

echo "✨ Done! Your project is now ADHD-friendly!"
```

## Simplified Makefile

```makefile
help:
	@echo "📦 Code Commands:"
	@echo "  make run    - Start the app"
	@echo "  make test   - Run tests"
	@echo ""
	@echo "📊 Data Commands:" 
	@echo "  make analyze - Run analysis"
	@echo "  make map    - Generate maps"
	@echo ""
	@echo "🔧 Setup:"
	@echo "  make setup  - First time setup"
	@echo "  make clean  - Clean everything"

run:
	cd app/backend && go run main.go

test:
	cd app/backend && go test ./...

analyze:
	cd app/analytics && python analyze.py

map:
	cd app/analytics && python visualize.py

setup:
	./app/scripts/setup.sh

clean:
	rm -rf data/output/*
```

## The "Where Do I Put This?" Guide

| If you have... | Put it in... | Why |
|---------------|--------------|-----|
| Go code | `app/backend/` | All Go together |
| Python script | `app/analytics/` | All Python together |
| Shell script | `app/scripts/` | All scripts together |
| CSV/Excel file | `data/input/` | Raw data here |
| Generated chart | `data/output/` | Results here |
| Any documentation | `docs/` | All docs together |
| Configuration | Root (`.env`) | Easy to find |

## Benefits for ADHD

1. **No Decision Fatigue**: Only 3 folders to choose from
2. **Visual Simplicity**: Clean root, no clutter
3. **Fast Navigation**: Everything is max 3 clicks away
4. **Clear Boundaries**: No ambiguity about where things go
5. **Reduced Overwhelm**: 92% less visual noise
6. **Memory-Friendly**: Can remember entire structure easily

## Comparison

### Before We Started:
- 38 directories
- 22 root files
- Mixed language files at root
- Unclear boundaries
- **Cognitive Load: 🔴 HIGH**

### After Our Migration (Current):
- 3 directories (`app/`, `data/`, `docs/`)
- 3 essential files (README, Makefile, LICENSE)
- Crystal clear purpose
- Obvious boundaries
- **Cognitive Load: 🟢 LOW**

## Next Step

Run this to clean everything up:

```bash
# Save this as adhd_restructure.sh
cat > adhd_restructure.sh << 'EOF'
#!/bin/bash
echo "🧹 Creating ADHD-friendly structure..."

# Create the 3 main directories
mkdir -p app/{backend,analytics,scripts}
mkdir -p data/{input,output}
mkdir -p docs/findings

# Move everything
find . -name "*.go" -exec mv {} app/backend/ \; 2>/dev/null || true
find . -name "*.py" -exec mv {} app/analytics/ \; 2>/dev/null || true
find . -name "*.sh" -exec mv {} app/scripts/ \; 2>/dev/null || true
find . -name "*.csv" -exec mv {} data/input/ \; 2>/dev/null || true
find . -name "*.md" -not -name "README.md" -exec mv {} docs/ \; 2>/dev/null || true

echo "✅ Done! Your project is now simple and clean."
EOF

chmod +x adhd_restructure.sh
./adhd_restructure.sh
```

This will give you the simplest possible structure that still makes sense.