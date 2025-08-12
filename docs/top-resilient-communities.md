# Top 10 Resilient LILA Communities - Detailed Profiles

## The Mystery Communities: America's Healthiest "Food Deserts"

### 1. 🥇 **Murfreesboro, Tennessee** (Rutherford County)
- **Census Tract:** 47149041500
- **Resilience Score:** 4.75 (highest in nation)
- **Population:** 2,966 (2010)
- **Context:** Part of Nashville metro area, home to Middle Tennessee State University (21,000 students)
- **🚨 Red Flag:** University presence - student health may skew data

### 2. 🥈 **Pickens County, South Carolina**
- **Census Tract:** 45077011202  
- **Resilience Score:** 4.41
- **Population:** 5,694 (2010)
- **Context:** Home to Clemson University
- **🚨 Red Flag:** Another college town - pattern emerging

### 3. 🥉 **Beaufort County, South Carolina**
- **Census Tract:** 45013001000
- **Resilience Score:** 4.32
- **Population:** 4,469 (2010)
- **Context:** Coastal area near Hilton Head, includes Parris Island Marine Base
- **🚨 Red Flag:** Military presence - commissaries not counted as supermarkets

### 4. **Big Rapids area, Michigan** (Mecosta County)
- **Census Tract:** 26107981300
- **Resilience Score:** 4.24
- **Population:** 2,216 (2010)
- **Context:** Home to Ferris State University
- **🚨 Red Flag:** Yet another university town

### 5. **Bowling Green, Kentucky** (Warren County)
- **Census Tract:** 21227010400
- **Resilience Score:** 4.22
- **Population:** 4,822 (2010)
- **Context:** Home to Western Kentucky University
- **🚨 Red Flag:** University pattern continues

### 6. **Oakland County, Michigan** (Detroit suburbs)
- **Census Tract:** 26125192800
- **Resilience Score:** 4.19
- **Population:** 2,200 (2010)
- **Context:** Wealthy Detroit suburb (Pontiac/Auburn Hills area)
- **🚨 Red Flag:** May have gentrified significantly since 2010

### 7. **Oxford, Mississippi** (Lafayette County)
- **Census Tract:** 28071950301
- **Resilience Score:** 4.19
- **Population:** 5,801 (2010)
- **Context:** Home to University of Mississippi
- **🚨 Red Flag:** Another college town

### 8. **San Angelo, Texas** (Tom Green County)
- **Census Tract:** 48451001500
- **Resilience Score:** 4.14
- **Population:** 2,249 (2010)
- **Context:** Home to Angelo State University, Goodfellow Air Force Base
- **🚨 Red Flag:** University AND military base

### 9. **Ann Arbor area, Michigan** (Washtenaw County)
- **Census Tract:** 26161402200
- **Resilience Score:** 4.08
- **Population:** 4,749 (2010)
- **Context:** University of Michigan area
- **🚨 Red Flag:** Elite university town

### 10. **Fort Wayne, Indiana** (Allen County)
- **Census Tract:** 18003980001
- **Resilience Score:** 4.05
- **Population:** 664 (2010)
- **Context:** Small population tract in Indiana's second-largest city
- **Note:** Unusually small population for urban tract

---

## 🔴 CRITICAL PATTERN DISCOVERED

**7 out of 10 "most resilient food deserts" are college towns or military bases!**

This suggests the findings may be artifacts of:
1. **Young, healthy student populations** temporarily residing in tracts
2. **University dining halls** not counted as food retail
3. **Military commissaries** not included in supermarket counts
4. **Transient populations** that don't reflect permanent residents

## Where to Find 2023 Food Access Data

### Official Sources (Limited Updates)

1. **USDA Food Access Research Atlas**
   - Latest version: Still 2019 (as of January 2025)
   - URL: https://www.ers.usda.gov/data-products/food-access-research-atlas/
   - **Problem:** USDA hasn't released 2023 update yet

2. **USDA Food Environment Atlas**
   - Some 2022 data available
   - URL: https://www.ers.usda.gov/data-products/food-environment-atlas/
   - Limited tract-level detail

3. **CDC PLACES**
   - Has 2023 health data but NO food access measures
   - They removed food environment variables

### Alternative 2023 Data Sources

4. **Private Sector Data** (Would need to purchase/request)
   - **Nielsen TDLinx** - Commercial database of all food retailers
   - **InfoUSA/Data Axle** - Business listings including grocery
   - **SafeGraph** - Foot traffic data showing where people actually shop
   - **Google Places API** - Current grocery store locations

5. **Crowdsourced/Tech Options**
   - **OpenStreetMap** - Community-mapped grocery stores
   - **Yelp/Google Reviews** - API access to current businesses
   - **SNAP Retailer Database** - Updated quarterly by USDA
   - **WIC Vendor Lists** - State-by-state current vendors

6. **Academic Alternatives**
   - **National Establishment Time Series (NETS)** - Through universities
   - **Reference USA** - Library database access
   - **County Health Rankings** - Some 2022-2023 food data

### Recommended Approach for Verification

```python
# Quick verification strategy
1. Use SNAP Retailer Database (free, current)
2. Cross-reference with Google Places API
3. Compare to 2019 FARA baseline
4. Document changes in each "resilient" tract
```

### The Reality Check

Given that most "resilient" communities are **college towns or military bases**, we likely don't have a resilience story at all. We have a data artifact story about:
- How federal datasets miss special populations
- Why university/military areas appear as "food deserts"
- The danger of ecological inference

**New story angle:** "How Bad Data Could Misdirect Millions in Food Security Funding"

---

## Next Steps

1. **Verify university/military presence** in all top 100 resilient tracts
2. **Exclude special population tracts** and re-run analysis
3. **Check SNAP retailer database** for current food access
4. **Ground-truth top non-university/military tracts** if any remain

The Murfreesboro tract being #1 is the smoking gun - MTSU has 21,000 students eating in dining halls, living in a tract marked as a "food desert." This isn't resilience; it's a measurement problem.