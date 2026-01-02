# Research Vision & Future Directions

**Created:** January 1, 2026
**Purpose:** Capture the full research frontier for the Community Health Resilience project

---

## Current Foundation

We have built a system that identifies 2,767 census tracts with unexpectedly good health outcomes despite limited food access. The methodology is peer-reviewed (Paper 2: 4/4 Accept), and the core finding is robust.

**Core insight:** Some communities thrive where they "shouldn't." Understanding why is the research frontier.

---

## Research Directions: Zero New Data Required

These studies can begin immediately using existing data:

### 1. The Paradox Study (Inverse Cases)

**Question:** Which tracts have EXCELLENT food access but TERRIBLE health outcomes?

**Method:** Analyze positive residuals in non-LILA tracts. Same regression, opposite tail.

**Hypothesis:** High-income suburbs with abundant grocery stores may suffer from social isolation, car-dependent lifestyles, or over-consumption patterns.

**Effort:** Days (re-analysis of existing model outputs)

**Paper potential:** Strong. Flips the narrative. "Why Whole Foods Won't Save You."

---

### 2. Trajectory Analysis (4-Year Velocity)

**Question:** Which tracts are becoming more/less resilient over time?

**Method:** Harmonize PLACES 2020-2025 releases, compute year-over-year resilience change.

**Data:** Already downloaded (places_harmonized_2020.csv through places_harmonized_2025.csv)

**Key outputs:**
- Velocity scores (rate of change)
- Stability classification (persistent vs. volatile)
- Early warning indicators for declining resilience

**Effort:** Weeks

**Paper potential:** Strong. Predictive value for policy targeting.

---

### 3. Neighbor Effects (Spatial Contagion)

**Question:** Do resilient tracts cluster? Is resilience "contagious"?

**Method:** Spatial autocorrelation (Moran's I), local clustering (LISA), spatial lag models.

**Data:** TIGER boundaries + existing resilience scores

**Key outputs:**
- Cluster maps
- Spillover coefficients
- Border analysis (what happens at resilient/vulnerable boundaries)

**Effort:** Weeks

**Paper potential:** Strong. Builds on Paper 1's spatial synchrony finding.

---

### 4. Matched Pair Analysis (The "Why Not Them?" Study)

**Question:** What distinguishes a resilient tract from its demographic twin?

**Method:** Propensity score matching. For each resilient tract, find the most similar vulnerable tract. Analyze residual differences.

**Data:** ACS demographics + resilience scores

**Key outputs:**
- Matched pair dataset
- Distinguishing features between twins
- Hypothesis generation for causal mechanisms

**Effort:** Weeks

**Paper potential:** High. Closest we can get to causation without intervention.

---

### 5. Feature Interaction Mining

**Question:** Which combinations of factors predict resilience?

**Method:** SHAP interaction values, decision tree splits, non-linear term exploration.

**Data:** Trained model + features

**Key outputs:**
- Interaction heatmaps
- Threshold effects (tipping points)
- Subgroup-specific patterns

**Effort:** Weeks

**Paper potential:** Moderate. Technical but publishable in methods journals.

---

### 6. Demographic Stratification

**Question:** Does resilience manifest differently across racial, age, or urban/rural groups?

**Method:** Run separate models by subgroup. Compare coefficients, residual distributions, and top performers.

**Data:** ACS demographics + resilience model

**Key outputs:**
- Subgroup-specific resilience mechanisms
- Equity analysis of model performance
- Distinct "types" of resilience

**Effort:** Weeks

**Paper potential:** High. Addresses Paper 4 (equity) questions directly.

---

### 7. Stability Analysis (Real vs. Artifact)

**Question:** Which resilient tracts are persistently resilient across years?

**Method:** Track resilience classification across 2020-2025. Flag volatile vs. stable tracts. Weight by confidence interval width.

**Data:** Multi-year PLACES (already harmonized)

**Key outputs:**
- Confidence-weighted resilience scores
- Stable resilient tract list (higher confidence)
- Artifact identification (small-N noise)

**Effort:** Weeks

**Paper potential:** Moderate. Methodological contribution.

---

### 8. The Disappearing Resilience Study

**Question:** Which tracts were resilient in 2020 but aren't anymore?

**Method:** Longitudinal comparison. Identify classification changers. Correlate with external shocks (COVID, economic change).

**Data:** Multi-year PLACES + external event data

**Key outputs:**
- List of "fallen" resilient tracts
- Common characteristics of decline
- Policy failure indicators

**Effort:** Weeks

**Paper potential:** High. "What destroys resilience" is actionable.

---

## Research Directions: New Data Required

These require acquiring additional (but freely available) data sources:

### 9. Social Infrastructure Census

**Question:** Do resilient tracts have denser social infrastructure (churches, community centers, mutual aid networks)?

**Data needed:**
- Church/congregation databases
- Community center locations
- 211 service registrations
- Mutual aid network mapping

**Hypothesis:** Social infrastructure substitutes for formal food access.

**Effort:** Months (data acquisition + geocoding)

---

### 10. The 100-Year Lookback (Historical Epidemiology)

**Question:** What historical events (redlining, highway construction, urban renewal) shaped current resilience?

**Data needed:**
- HOLC redlining maps (digitized, available)
- Historical highway routing
- Urban renewal project records
- Sanborn maps

**Hypothesis:** Resilient tracts have institutional memory from surviving previous crises.

**Effort:** Months to years

---

### 11. Wealth Drain Analysis

**Question:** Do resilient tracts retain more wealth locally?

**Data needed:**
- HMDA mortgage data (public)
- Business ownership records
- Court fine/fee data
- Bank branch vs. payday lender locations

**Hypothesis:** Lower wealth extraction → higher resilience.

**Effort:** Months

---

### 12. Local Narrative Corpus (Computational Ethnography)

**Question:** Do resilient tracts have different narrative signatures?

**Data needed:**
- Local newspaper archives
- City council transcripts
- Social media geotags
- Google/Yelp reviews

**Method:** NLP sentiment, topic modeling, collective vs. individual language.

**Hypothesis:** Resilient communities talk differently about themselves.

**Effort:** Months

---

### 13. The Exposome Mapping Project

**Question:** Do resilient tracts have hidden environmental advantages?

**Data needed:**
- Hyperlocal air quality (not just EPA monitors)
- Water quality testing
- Soil contamination maps
- Green space quality assessments

**Hypothesis:** Some "food deserts" have environmental health advantages.

**Effort:** Months to years (may require primary data collection)

---

### 14. Kinship Geography Study

**Question:** Are resilient tract residents embedded in healthy kinship networks?

**Data needed:**
- Survey of family geography
- Emergency contact analysis
- Holiday travel patterns

**Hypothesis:** Tract boundaries are meaningless; kinship networks are real.

**Effort:** Years (requires primary research, IRB)

---

### 15. Global Resilience Comparison

**Question:** Do similar patterns exist internationally?

**Data needed:**
- Cuban health data
- Kerala health outcomes
- Costa Rica Blue Zone data
- Indigenous community health (Canada, Australia, NZ)

**Hypothesis:** Resilience mechanisms are universal but context-specific.

**Effort:** Years (international partnerships)

---

### 16. Manufactured Vulnerability Study

**Question:** Which "vulnerable" tracts were made vulnerable by deliberate policy?

**Data needed:**
- Hospital closure records
- Grocery store acquisition/closure data
- Public housing demolition records
- Environmental hazard siting decisions

**Hypothesis:** Vulnerability is often produced, not inherent.

**Effort:** Months (investigative approach)

---

## Feature Ideas (Product, Not Research)

These emerged from product/engineering brainstorming:

### Community-Defined Metrics
Let communities define what "resilience" means to them. Participatory indicator design.

### Tract Matchmaking
"LinkedIn for census tracts." Connect struggling tracts with similar-but-resilient tracts. Facilitate peer learning.

### Intervention Simulator
"What if we added a grocery store here?" Predictive policy planning tool.

### Community Annotation Layer
Let residents add context the data misses: informal food sources, mutual aid networks, hidden assets.

### Alternative Geographies
Re-aggregate data by school district, hospital catchment, or transit isochrone instead of census tracts.

### Explainable AI Interface
Show users *why* the model thinks a tract is resilient. Feature importance as UX.

---

## Tensions to Navigate

1. **Top-down vs. bottom-up:** Are we scoring communities or listening to them?
2. **Prediction vs. explanation:** Should we forecast or understand?
3. **Digital vs. physical:** Is the next step code or fieldwork?
4. **Researcher-facing vs. community-facing:** Who's the primary user?
5. **Speed vs. rigor:** Can we publish faster or do we need more validation?

---

## Priority Ranking (Research Team Recommendation)

### Tier 1: Start Immediately
1. ~~**Paradox Study**~~ - **ABANDONED** (CDC PLACES circularity - see PAPER-5-PARADOX-STUDY-V2.md)
2. **Wealth Drain Analysis** - Economic outcomes, no PLACES dependency (see STUDY-11-WEALTH-DRAIN-SCOPE.md)

### Tier 2: Requires Methodology Reframe
These studies use CDC PLACES and have the same circularity problem unless reframed:
- **Trajectory Analysis** - Could reframe as "PLACES model stability analysis"
- **Matched Pair Analysis** - Same circularity issue
- **Neighbor Effects** - Could work as "spatial clustering of model error"

### Tier 3: Requires New Data
- **Social Infrastructure Census** - Use economic outcomes instead of health
- **Historical Lookback** - Focus on wealth/housing trajectories

### CRITICAL NOTE (January 2026)
Any study using CDC PLACES health outcomes as the dependent variable has a fundamental circularity problem: PLACES estimates are modeled from demographics, so "unexplained" residuals may just be model prediction error. See the abandoned Paper 5 for detailed explanation.

---

## Paper Pipeline

| Paper | Status | Next Step |
|-------|--------|-----------|
| Paper 1: Spatial Synchrony | Complete | Submit to Epidemiology |
| Paper 2: RTM in Small-Area Estimates | Peer-reviewed (4/4 Accept) | Submit to AJE |
| Paper 3: CHBI Validation | Scoped | Obtain external validation data |
| Paper 4: Health Equity | Scoped | Run equity analyses |
| Paper 4B: Expert Panel Methodology | Manuscript complete | Submit to qual methods journal |
| Paper 5: Paradox Study | **ABANDONED** | CDC PLACES circularity (fatal flaw) |
| Paper 6: Trajectory & Velocity | On hold | Requires reframe (PLACES circularity) |
| Paper 7: Spatial Clustering | On hold | Could reframe as model error clustering |
| **Paper 11: Wealth Drain** | **SCOPED** | Download HMDA + FDIC data |

---

## Success Metrics

- **Research impact:** Citations, policy briefs citing our work, replication studies
- **Community impact:** Number of communities using findings, CAB engagement
- **Media impact:** Coverage in outlets that reach affected communities
- **Policy impact:** Funding decisions, program designs influenced by findings

---

## Team Notes

This document captures the January 1, 2026 brainstorming session with leadership, policy, product, and academic teams. The full team agreed that:

1. The research foundation is strong (peer-reviewed, rigorous)
2. The immediate opportunity is in re-analysis of existing data
3. The Paradox Study should start first
4. We should not wait for new data to publish what we already have
5. Community ownership must grow alongside research output

---

*Last updated: January 1, 2026*
