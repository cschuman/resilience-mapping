# Health Resilience Mapping: Finding Communities That Defy the Odds

Identifies US census tracts with unexpectedly good health outcomes despite limited food access by analyzing 68,000+ tracts linking CDC PLACES health data with USDA Food Access Atlas.

## 🔍 Key Findings & Insights

### The Discovery
Our analysis of **68,170 census tracts** across all 50 US states reveals **1,059 communities (1.6%)** that demonstrate exceptional health resilience despite being classified as Low-Income Low-Access (LILA) areas. These "resilience hot spots" exhibit health outcomes **0.6-4.7 standard deviations better** than predicted.

### Top Resilient Communities
The most resilient LILA tracts defying expectations:
1. **Tennessee 47149041500** (Rutherford County) - Resilience Score: 4.75
2. **South Carolina 45077011202** (Pickens County) - Score: 4.41  
3. **South Carolina 45013001000** (Beaufort County) - Score: 4.32
4. **Michigan 26107981300** (Mecosta County) - Score: 4.24
5. **Kentucky 21227010400** (Warren County) - Score: 4.22

### Geographic Patterns
- **Southeast clustering**: Strong resilience patterns in rural South
- **Midwest industrial cities**: Pockets of unexpected health outcomes
- **State leaders**: Indiana, South Carolina, Tennessee show highest concentrations

### What Makes These Communities Different?
Potential protective factors identified:
- **Social capital**: Strong community bonds and support networks
- **Faith-based infrastructure**: High church density correlating with resilience
- **Alternative food systems**: Gardens, farmers markets, informal economies
- **Healthcare access**: Presence of FQHCs and mobile clinics
- **Cultural practices**: Traditional foodways and community resilience strategies

## 📊 In-Depth Analysis

For comprehensive research findings and methodology:
- **[Full Research Findings](docs/research-findings.md)** - Complete statistical analysis and results
- **[Comprehensive Report](docs/COMPREHENSIVE-FINDINGS-REPORT.md)** - Detailed findings with policy implications
- **[Top Resilient Communities Analysis](docs/top-resilient-communities.md)** - Deep dive into exemplar tracts
- **[Policy Analysis](docs/policy-analysis.md)** - Implications for health equity initiatives
- **[Research Paper Draft](docs/research-paper-draft.md)** - Academic manuscript in preparation

## 🚀 Live Application

**View the interactive map**: [resilience-mapping.fly.dev](https://resilience-mapping.fly.dev)

## 🛠️ Run Locally

### Prerequisites
- Node.js 20+
- Python 3.8+ (for analysis scripts)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/resilience-mapping.git
cd resilience-mapping

# Install dependencies and run dev server
cd app/web
npm install
npm run dev
```

### Python Analysis Scripts

```bash
cd app/analytics

# Set up Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run comprehensive analysis
python analyze_resilience.py
```

### Project Structure

```
resilience-mapping/
├── app/
│   ├── web/                 # SvelteKit application
│   │   ├── src/routes/      # Pages and API endpoints
│   │   ├── src/lib/         # Components and utilities
│   │   └── fly.toml         # Fly.io deployment
│   ├── analytics/           # Python analysis scripts
│   └── scripts/             # SQL schema and utilities
├── data/                    # Data files
│   ├── input/               # Source data (CSV)
│   └── output/              # Generated results
├── docs/                    # Research documentation
└── figures/                 # Visualizations and maps
```

### Data Sources

The analysis combines:
- **CDC PLACES 2023**: Census tract health outcomes (n=2.55M records)
- **USDA Food Access Research Atlas 2019**: Food access indicators (n=72,531)
- **Census TIGER/Line**: Tract boundary shapefiles for mapping

## 📈 Outputs

The pipeline generates:
- **CSV Rankings**: `data/processed/model_table_with_residuals.csv`
- **Interactive Map**: `figures/index.html` (Leaflet-based choropleth)
- **Statistical Tables**: Publication-ready tables in `tables/`
- **GeoJSON**: Tract geometries with resilience scores

## ⚠️ Important Caveats

- **Temporal Gap**: 4-year difference between FARA (2019) and PLACES (2023) data
- **Geographic Boundaries**: Mixed 2010/2020 census tract definitions
- **Ecological Inference**: Tract-level patterns don't imply individual behaviors
- **Model Estimates**: PLACES uses model-based estimates, not direct measurements

## 🤝 Contributing

We welcome contributions! Areas for improvement:
- Incorporating additional social determinants data
- Temporal analysis with multiple years
- Machine learning approaches for pattern detection
- Qualitative validation through community interviews

## 📚 Citation

If you use this analysis in your research:
```
@software{resilience_mapping_2025,
  title = {Health Resilience Mapping: Finding Communities That Defy the Odds},
  year = {2025},
  url = {https://github.com/yourusername/resilience-mapping}
}
```

## 📄 License

MIT License - See [LICENSE](LICENSE) file

## 🙏 Acknowledgments

This analysis builds on publicly available data from:
- Centers for Disease Control and Prevention (CDC)
- United States Department of Agriculture (USDA)
- U.S. Census Bureau

---

*For questions or collaboration: [Open an issue](https://github.com/yourusername/resilience-mapping/issues)*
