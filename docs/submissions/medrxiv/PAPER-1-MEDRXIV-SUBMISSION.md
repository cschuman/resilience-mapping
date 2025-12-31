# medRxiv Submission Package: Paper 1

## Manuscript: Spatial Synchrony, Not Contagion

**Status:** Ready for submission
**Target:** medRxiv (Health Informatics / Epidemiology)
**Follow-up:** American Journal of Epidemiology

---

## Pre-Submission Checklist

- [x] Title finalized
- [x] Abstract within 300 words (current: ~250)
- [x] Keywords selected (6 keywords)
- [x] Author information complete
- [x] Conflict of interest statement prepared
- [x] Data availability statement included
- [x] Code availability statement included
- [x] Supplementary materials prepared
- [ ] ORCID verified
- [ ] Funding statement (if applicable)

---

## Manuscript Information

**Title:** Spatial Synchrony, Not Contagion: A Methodological Correction in Community Health Trajectory Prediction

**Running Title:** Spatial Synchrony in Community Health

**Article Type:** Original Research

**Word Count:** ~3,200 (within AJE limit of 3,500)

**Keywords:**
1. Spatial epidemiology
2. Temporal data leakage
3. Health trajectories
4. Methodological correction
5. CDC PLACES
6. Spatial synchrony

---

## Author Information

**Author 1:**
- Name: Corey Schuman
- Affiliation: Independent Researcher / odds.health
- Email: [to be filled]
- ORCID: [to be filled]
- Role: Conceptualization, Methodology, Software, Formal Analysis, Writing

**Corresponding Author:** Corey Schuman

---

## Abstract (250 words)

**Background:** Recent claims of "spatial contagion" in community health—where health trajectory changes purportedly propagate across geographic boundaries—require careful methodological scrutiny. Initial analyses suggested neighbor health trajectories were 3.8 times more predictive than a community's own historical trend.

**Objective:** To rigorously test whether neighboring community health trajectories genuinely predict focal community trajectories, using temporally appropriate feature construction to avoid data leakage.

**Methods:** We analyzed 189,566 tract-year observations from 72,161 U.S. census tracts using CDC PLACES data (2020-2024). We compared two spatial feature specifications: (1) contemporaneous neighbor change (year T-1 to T, same period as outcome), and (2) properly lagged neighbor change (year T-2 to T-1, prior to outcome period). We evaluated predictive contribution using permutation importance on temporal holdout data with bootstrap confidence intervals.

**Results:** With contemporaneous (leaked) neighbor features, neighbor_avg_change showed 16.7x higher permutation importance than CHBI_change_1yr (0.039 vs. 0.002, non-overlapping 95% CIs). After correcting to properly lagged features, importance dropped to 0.001 for both variables (ratio: 1.12x, overlapping CIs). Ablation experiments showed spatial features contributed -0.4% to model performance when properly lagged, versus +18.2% when contemporaneous data was leaked.

**Conclusions:** The apparent "spatial contagion" in community health trajectories was an artifact of temporal data leakage, not genuine predictive signal. Communities exhibit spatial synchrony—they change together at the same time—but prior neighbor trajectories do not predict future focal trajectories. This finding has important implications for spatial health modeling.

---

## Conflict of Interest Statement

The author declares no conflicts of interest. This research was conducted independently without external funding.

---

## Data Availability Statement

The CDC PLACES dataset is publicly available from the Centers for Disease Control and Prevention at https://www.cdc.gov/places/. Census tract boundary geometries are available from the U.S. Census Bureau TIGER/Line program. Processed datasets supporting this analysis are available from the corresponding author upon reasonable request.

---

## Code Availability Statement

All code for data processing, feature engineering, model training, and analysis is available at: https://github.com/[repository-to-be-created]

---

## Funding Statement

This research received no external funding.

---

## Ethics Statement

This study used only publicly available, de-identified aggregate data at the census tract level. No individual-level data were accessed. IRB review was not required.

---

## Submission Steps

### Step 1: Create medRxiv Account
1. Go to https://www.medrxiv.org/submit-a-manuscript
2. Create account (or log in)
3. Verify ORCID

### Step 2: Prepare Files
1. **Main manuscript:** Convert SPATIAL-CONTAGION-PAPER-REVISED.md to Word/PDF
2. **Supplementary materials:** SUPPLEMENTARY-MATERIALS.md as separate file
3. **Figures:** Extract from figures/paper/ directory

### Step 3: Submit
1. Select article type: "Original Research"
2. Select subject area: "Epidemiology" or "Health Informatics"
3. Upload manuscript and supplementary files
4. Enter metadata (title, abstract, keywords)
5. Confirm declarations
6. Submit

### Step 4: Post-Submission
1. Expect 2-3 day screening period
2. Once posted, note the medRxiv DOI
3. Immediately submit to AJE with medRxiv link

---

## Cover Letter Template (for AJE submission)

Dear Editors,

We submit for your consideration our manuscript titled "Spatial Synchrony, Not Contagion: A Methodological Correction in Community Health Trajectory Prediction."

This manuscript makes three important contributions:

1. **Methodological correction:** We identify temporal data leakage as the source of apparent "spatial contagion" findings in community health research, a methodological issue that may affect other spatial epidemiology studies.

2. **Rigorous demonstration:** Using 189,566 tract-year observations, permutation importance with bootstrap confidence intervals, and ablation experiments, we show that properly lagged spatial features contribute nothing to prediction.

3. **Policy relevance:** The distinction between spatial synchrony (communities changing together) and spatial contagion (changes spreading between communities) has direct implications for intervention design.

This work exemplifies the self-correcting nature of science—we identified and corrected our own methodological error through rigorous peer review, fundamentally changing our conclusions. We believe this transparency strengthens rather than weakens the contribution.

A pre-print version is available on medRxiv [DOI to be added].

The manuscript has not been published previously and is not under consideration elsewhere.

Sincerely,
Corey Schuman

---

## Timeline

| Date | Action |
|------|--------|
| Day 0 | Submit to medRxiv |
| Day 3-5 | medRxiv posts manuscript |
| Day 5 | Publish on odds.health |
| Day 7 | Submit to AJE |
| Month 3-6 | AJE decision expected |
