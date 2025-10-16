# What This Dataset CAN and CANNOT Answer

## 🟢 QUESTIONS THIS DATASET CAN ANSWER

### Geographic Patterns (We have coordinates for all 1,059 tracts!)
✅ **Where exactly are resilient vs vulnerable food deserts?**
- Yes! We have lat/lon for all tracts, can map precisely

✅ **Is there geographic clustering of resilience?**
- Yes! We can run spatial autocorrelation, identify hot spots

✅ **Which states/counties have the most disparate outcomes?**
- Yes! Texas has both 130 resilient AND 119 vulnerable tracts

✅ **Do resilient/vulnerable tracts follow historical redlining patterns?**
- Partially - would need to overlay historical HOLC maps

### Demographic Correlations
✅ **What's the relationship between poverty and resilience?**
- Yes! We have poverty rates for all tracts
- Finding: Some 60% poverty tracts thrive, some 7% poverty fail

✅ **Are rural or urban food deserts more resilient?**
- Yes! We have Urban/Rural flags
- Finding: 97.6% of resilient are urban, 95.1% of vulnerable are urban

✅ **What's the income difference between resilient/vulnerable?**
- Yes! Median family income available
- Finding: $56,184 (resilient) vs $31,944 (vulnerable)

### Statistical Patterns
✅ **How extreme are the outliers?**
- Yes! We can calculate exact standard deviations
- Finding: 9.72 SD between best and worst

✅ **What percentage are likely college towns or military bases?**
- Partially - we identified 134 likely special populations (12.7%)

✅ **Is resilience randomly distributed or clustered?**
- Yes! Can test with Moran's I and other spatial statistics

### Model-Based Insights
✅ **Which food access variables predict health outcomes?**
- Yes! We have LILA status, distance thresholds
- R² = 0.42 (moderate predictive power)

✅ **How much variance is unexplained?**
- Yes! 58% of variance unexplained by current model

---

## 🔴 QUESTIONS THIS DATASET CANNOT ANSWER

### The Causal Questions
❌ **WHY do some food deserts thrive?**
- We can identify correlations, not causes

❌ **What makes Rutherford County TN exceptional?**
- We know it scores 4.75 but not WHY

❌ **Do universities CREATE health halos?**
- Can't establish causation from cross-sectional data

### The Invisible Variables
❌ **Where are the grandmothers?**
- No multigenerational household data

❌ **Where are the churches?**
- No religious institution data

❌ **Where are the gardens?**
- No urban agriculture data

❌ **Where are mutual aid networks?**
- No social capital measurements

❌ **What is the role of trauma/historical harm?**
- No historical redlining, displacement, violence data

### The Temporal Questions
❌ **How did COVID change these communities?**
- 4-year gap makes this impossible to answer

❌ **Which tracts gentrified 2019-2023?**
- No longitudinal data

❌ **Are these patterns stable or changing?**
- Single time point only

❌ **What happens to college towns in summer?**
- No seasonal variation data

### The Lived Experience Questions
❌ **Where do people ACTUALLY shop?**
- We have store locations, not shopping behavior

❌ **What do people ACTUALLY eat?**
- No dietary/nutritional data

❌ **How do people without cars get food?**
- No transit/transportation behavior data

❌ **What would residents say about our findings?**
- No qualitative/interview data

❌ **How do social networks share food?**
- No network/relationship data

### The "What If" Questions
❌ **Would cash transfers work better than supermarkets?**
- Can't test interventions with observational data

❌ **Do food delivery apps eliminate food deserts?**
- No app usage/digital access data

❌ **Would community kitchens help?**
- Can't test hypothetical interventions

### The Critical Questions
❌ **Who profits from maintaining food deserts?**
- No corporate/economic actor data

❌ **Are we measuring the wrong thing entirely?**
- Can't test alternative frameworks with same data

❌ **Is "food desert" a meaningful concept?**
- Would need different theoretical approach

---

## 🟡 QUESTIONS WE COULD PARTIALLY ANSWER WITH ADDITIONAL DATA

### With Historical Data
🔶 **Were today's vulnerable tracts once thriving?**
- Need historical census/health data

🔶 **Do communities cycle through resilience?**
- Need longitudinal panel data

### With Additional Geographic Data
🔶 **Distance to hospitals, schools, parks?**
- Could geocode and calculate

🔶 **Presence of alternative food sources?**
- Could scrape farmers markets, food pantries

🔶 **Transit accessibility?**
- Could add GTFS transit data

### With Census/ACS Data
🔶 **Role of immigration, language, culture?**
- Could merge with ACS demographic data

🔶 **Educational attainment effects?**
- Available in ACS

🔶 **Housing stability, rent burden?**
- Available in ACS

### With Health System Data
🔶 **Presence of FQHCs, clinics?**
- HRSA data available

🔶 **Medicaid expansion effects?**
- Could code by state policy

---

## 📊 THE BRUTAL TRUTH

### What This Dataset Is Good For:
1. **Identifying WHERE** resilient/vulnerable food deserts are
2. **Describing WHO** lives there (basic demographics)
3. **Quantifying HOW DIFFERENT** outcomes are
4. **Finding PATTERNS** in geographic distribution
5. **Generating HYPOTHESES** for further research

### What This Dataset Is Terrible For:
1. **Explaining WHY** differences exist
2. **Understanding MECHANISMS** of resilience
3. **Capturing LIVED EXPERIENCE**
4. **Testing INTERVENTIONS**
5. **Establishing CAUSATION**

### The Most Honest Answer:
**This dataset can tell us WHAT IS, but not WHY IT IS or WHAT TO DO ABOUT IT.**

---

## 🎯 THE QUESTIONS WE SHOULD FOCUS ON

Given our data limitations, here are the MOST ANSWERABLE and IMPACTFUL questions:

### Immediately Answerable:
1. **After removing colleges/military, which communities are truly resilient?**
2. **What percentage of "food deserts" are actually well-served by non-supermarket food sources?**
3. **Which specific census tracts should be prioritized for intervention?**
4. **How does resilience correlate with state policy environments?**
5. **Are there "twins" - similar tracts with opposite outcomes?**

### Answerable with Minimal Additional Data:
6. **Do resilient tracts have more churches? (Google Places API)**
7. **Are vulnerable tracts transit deserts too? (GTFS data)**
8. **Did resilient tracts gentrify 2019-2023? (ACS updates)**
9. **Are resilient tracts near hospitals/clinics? (HRSA data)**
10. **Do state SNAP policies correlate with resilience patterns?**

### The Meta-Question This Dataset Answers Best:
**"How badly are we mismeasuring community health when we use administrative data without ground-truthing?"**

Answer: VERY BADLY. We mistook college dining halls for food deserts and called them "resilient."

---

## 💡 THE REAL INSIGHT

This dataset's greatest value isn't in answering questions about food deserts.

It's in revealing how our measurement systems create false narratives that could misdirect millions in funding toward college towns while actual suffering communities remain invisible.

**The dataset's most important finding:**
Not that 1,059 communities are resilient, but that our entire framework for understanding food access and health might be fundamentally flawed.

**The question this dataset truly answers:**
*"What happens when we make policy based on administrative data without ever talking to the humans who live in these places?"*

Answer: We celebrate college students' health while 874 communities suffer in silence.