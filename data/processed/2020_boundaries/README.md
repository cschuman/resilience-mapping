# Resilience Data - 2020 Census Boundaries

Last updated: 2025-12-29

## Overview

This dataset uses 2020 Census tract boundaries consistently across all data sources.

## Data Sources

| Source | Year | Census Vintage | Description |
|--------|------|----------------|-------------|
| CDC PLACES | 2024 | 2020 | Health outcomes (BRFSS 2022) - 48 states + DC |
| CDC PLACES | 2023 | 2020 | Health outcomes (BRFSS 2021) - KY & PA only |
| USDA FARA | 2019 | 2010→2020* | Food access indicators |
| Census Bureau | 2020 | 2020 | Population data |

*FARA data crosswalked from 2010 to 2020 boundaries using Census Bureau relationship file.

### Why Two PLACES Releases?

Kentucky and Pennsylvania are missing from CDC PLACES 2024/2025 because they
couldn't collect enough BRFSS data in 2023 to meet CDC's quality thresholds.
PLACES 2023 (using BRFSS 2021 data collected before these issues) has complete
health outcome data for these states, so we use that as a fallback.

## Coverage

- **Total tracts**: 83,117
- **States covered**: 50 states + DC
- **Population covered**: 330+ million

## Known Limitations

### Kentucky & Pennsylvania Data Vintage

Kentucky (1,106 tracts) and Pennsylvania (3,196 tracts) use PLACES 2023 data
(BRFSS 2021) instead of PLACES 2024 data (BRFSS 2022). This means their health
outcome data is approximately one year older than other states.

**Reason**: These states couldn't collect enough BRFSS data in 2023 to be
included in PLACES 2024/2025. CDC only provides screening measures for these
states in recent releases.

### FARA Crosswalk

The USDA Food Access Research Atlas (FARA) 2019 data uses 2010 Census tract
boundaries. We crosswalk this data to 2020 boundaries using the Census Bureau's
2020 Comparability Relationship File with area-weighted interpolation.

**Impact**: ~25 of 72,531 FARA tracts (0.03%) could not be matched to 2020
boundaries.

## Files

- `model_table_2020.csv` - Main model output with resilience scores
- `../crosswalks/tab20_tract20_tract10_natl.txt` - Census tract relationship file

## Methodology

1. **Burden Score**: Mean of z-scored health outcomes (obesity, diabetes,
   hypertension, CHD, low physical activity)

2. **Resilience Score**: Negative residual from regression of burden on
   LILA (Low Income, Low Access) status. Positive scores indicate communities
   performing better than expected given their food access environment.

## Data Quality

- All tracts have population data (100% coverage)
- All tracts have complete health outcome data
- Florida now included (5,077 tracts) - previously missing due to CDC data issues
