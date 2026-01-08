# Health Resilience Mapping: Finding Communities That Defy the Odds

[![CI/CD Pipeline](https://github.com/cschuman/resilience-mapping/actions/workflows/ci.yml/badge.svg)](https://github.com/cschuman/resilience-mapping/actions/workflows/ci.yml)
[![Deploy](https://github.com/cschuman/resilience-mapping/actions/workflows/deploy.yml/badge.svg)](https://github.com/cschuman/resilience-mapping/actions/workflows/deploy.yml)
[![codecov](https://codecov.io/gh/cschuman/resilience-mapping/branch/main/graph/badge.svg)](https://codecov.io/gh/cschuman/resilience-mapping)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen)](https://resilience-mapping.fly.dev)

[![SvelteKit](https://img.shields.io/badge/SvelteKit-5.x-FF3E00?logo=svelte&logoColor=white)](https://kit.svelte.dev/)
[![Go](https://img.shields.io/badge/Go-1.21-00ADD8?logo=go&logoColor=white)](https://golang.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-PostGIS-336791?logo=postgresql&logoColor=white)](https://postgis.net/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://python.org/)

> Identifies US census tracts with unexpectedly good health outcomes despite limited food access by analyzing 68,000+ tracts linking CDC PLACES health data with USDA Food Access Atlas.

<p align="center">
  <a href="https://resilience-mapping.fly.dev">
    <img src="data/output/figures/resilience_analysis.png" alt="Health Resilience Analysis" width="700">
  </a>
</p>

## Table of Contents

- [Key Findings](#key-findings)
- [Live Demo](#live-demo)
- [Documentation](#documentation)
- [Quick Start](#quick-start)
- [Data Sources](#data-sources)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [Citation](#citation)
- [License](#license)

## Key Findings

### The Discovery

Our analysis of **68,170 census tracts** across all 50 US states reveals **1,059 communities (1.6%)** that demonstrate exceptional health resilience despite being classified as Low-Income Low-Access (LILA) areas. These "resilience hot spots" exhibit health outcomes **0.6-4.7 standard deviations better** than predicted.

### Top Resilient Communities

| Rank | Location | County | Resilience Score |
|------|----------|--------|------------------|
| 1 | Tennessee 47149041500 | Rutherford | 4.75 |
| 2 | South Carolina 45077011202 | Pickens | 4.41 |
| 3 | South Carolina 45013001000 | Beaufort | 4.32 |
| 4 | Michigan 26107981300 | Mecosta | 4.24 |
| 5 | Kentucky 21227010400 | Warren | 4.22 |

### Geographic Patterns

- **Southeast clustering**: Strong resilience patterns in rural South
- **Midwest industrial cities**: Pockets of unexpected health outcomes
- **State leaders**: Indiana, South Carolina, Tennessee show highest concentrations

### Potential Protective Factors

| Factor | Description |
|--------|-------------|
| Social Capital | Strong community bonds and support networks |
| Faith-Based Infrastructure | High church density correlating with resilience |
| Alternative Food Systems | Gardens, farmers markets, informal economies |
| Healthcare Access | Presence of FQHCs and mobile clinics |
| Cultural Practices | Traditional foodways and community resilience strategies |

## Live Demo

**[View the Interactive Map](https://resilience-mapping.fly.dev)** - Explore all 68,170 census tracts with filtering, search, and detailed community profiles.

## Documentation

### Research

| Document | Description |
|----------|-------------|
| [Research Findings](docs/research/research-findings.md) | Complete statistical analysis and results |
| [Research Paper](docs/research/research-paper-draft.md) | Academic manuscript in preparation |
| [Policy Analysis](docs/research/policy-analysis.md) | Implications for health equity initiatives |
| [Methodology](docs/reports/methodology-report.md) | Detailed methodology and validation |

### Development

| Document | Description |
|----------|-------------|
| [Technical Architecture](docs/architecture/technical-architecture.md) | System design and infrastructure |
| [Development Setup](docs/development/DEVELOPMENT_SETUP.md) | Local development guide |
| [Roadmap](docs/development/ROADMAP.md) | Planned features and improvements |

## Quick Start

### Prerequisites

- Node.js 20+
- Python 3.8+ (for analysis scripts)
- Go 1.21+ (for API development)

### Web Application

```bash
# Clone the repository
git clone https://github.com/cschuman/resilience-mapping.git
cd resilience-mapping

# Install dependencies and run dev server
cd app/web
npm install
npm run dev
```

### Python Analysis

```bash
cd app/analytics

# Set up Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run comprehensive analysis
python analyze_resilience.py
```

## Data Sources

| Source | Year | Records | Description |
|--------|------|---------|-------------|
| [CDC PLACES](https://www.cdc.gov/places/) | 2023 | 2.55M | Census tract health outcomes |
| [USDA FARA](https://www.ers.usda.gov/data-products/food-access-research-atlas/) | 2019 | 72,531 | Food access indicators |
| [Census TIGER/Line](https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html) | 2020 | - | Tract boundary shapefiles |

### Important Caveats

- **Temporal Gap**: 4-year difference between FARA (2019) and PLACES (2023) data
- **Geographic Boundaries**: Mixed 2010/2020 census tract definitions
- **Ecological Inference**: Tract-level patterns don't imply individual behaviors
- **Model Estimates**: PLACES uses model-based estimates, not direct measurements

## Project Structure

```
resilience-mapping/
├── app/
│   ├── web/                 # SvelteKit application
│   │   ├── src/routes/      # Pages and API endpoints
│   │   ├── src/lib/         # Components and utilities
│   │   └── fly.toml         # Fly.io deployment config
│   ├── analytics/           # Python analysis scripts
│   └── scripts/             # SQL schema and utilities
├── data/
│   ├── input/               # Source data (CSV, shapefiles)
│   └── output/              # Generated results and figures
├── docs/                    # Research and development documentation
│   ├── research/            # Research papers and findings
│   ├── architecture/        # Technical documentation
│   └── development/         # Development guides
└── .github/                 # CI/CD workflows and templates
```

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Areas for Contribution

- Incorporating additional social determinants data
- Temporal analysis with multiple years
- Machine learning approaches for pattern detection
- Qualitative validation through community interviews
- Accessibility improvements

## Citation

If you use this analysis in your research:

```bibtex
@software{resilience_mapping_2025,
  author       = {Schuman, Corey},
  title        = {Health Resilience Mapping: Finding Communities That Defy the Odds},
  year         = {2025},
  publisher    = {GitHub},
  url          = {https://github.com/cschuman/resilience-mapping},
  note         = {Analysis of 68,170 US census tracts identifying 1,059 communities
                  with exceptional health resilience despite limited food access}
}
```

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Acknowledgments

This analysis builds on publicly available data from:

- [Centers for Disease Control and Prevention (CDC)](https://www.cdc.gov/)
- [United States Department of Agriculture (USDA)](https://www.usda.gov/)
- [U.S. Census Bureau](https://www.census.gov/)

---

<p align="center">
  <a href="https://github.com/cschuman/resilience-mapping/issues">Report Bug</a>
  ·
  <a href="https://github.com/cschuman/resilience-mapping/issues">Request Feature</a>
  ·
  <a href="https://github.com/cschuman/resilience-mapping/discussions">Discussions</a>
</p>
