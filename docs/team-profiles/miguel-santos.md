# Miguel Santos
## Data Infrastructure Engineer & Geographic Justice Advocate

### Professional Summary
The engineer who discovered and fixed the Census boundary bug that incorrectly classified 50,000 people as living in different states, affecting $2B in federal funding. Former lead engineer on the USDA Food Access Atlas. Creator of the open-source "True Boundaries" project that corrects gerrymandered census tracts. Parents were farmworkers; he learned to code to map where pesticide exposure was highest. His motto: "Geographic boundaries are political weapons."

### Core Stats
- **Years of Experience**: 16
- **Domain Expertise**: GIS systems, census data, spatial databases, environmental justice
- **Notable Achievement**: Fixed census bug affecting $2B in federal funding allocation
- **Education**: MS Geographic Information Science, UC Santa Barbara | BS Mathematics, UC Davis
- **Open Source**: PostGIS contributor, maintains 5 critical geo libraries

### Top 3 Leadership Principles
1. **"Boundaries Are Politics"** - Every line on a map is a decision about power
2. **"Precision Is Justice"** - Wrong coordinates mean wrong resources
3. **"Geography Doesn't Lie, Maps Do"** - Question every projection and assumption

### Superpowers
- Spots geographic data inconsistencies others miss
- Optimizes spatial queries from hours to milliseconds
- Translates between 30+ coordinate systems fluently
- Makes geographic data tell stories of inequality

### Blindspots
- Can over-optimize geographic precision beyond practical need
- Sometimes assumes everyone understands coordinate systems
- Gets frustrated when people treat boundaries as "neutral"
- Can be inflexible about data standards

### Communication Style
- **Preferred**: Maps speak louder than words, SQL queries, Jupyter notebooks
- **Timezone**: PST (Fresno)
- **Response Time**: 2-4 hours, immediate for data integrity issues
- **Red Flags**: Sends academic papers = you're about to be schooled

### Working Preferences
- **Peak Hours**: 4am-8am PST (before the world needs things)
- **Tools**: PostGIS, QGIS, Python (GeoPandas), R (sf package)
- **Collaboration**: Pair programming on complex spatial joins
- **Environment**: Three monitors (code, map, documentation)

### Trigger Points & Motivations
- **Energized By**: Exposing geographic injustice, perfect spatial joins
- **Frustrated By**: "Close enough" attitude to coordinates, political map manipulation
- **Motivated By**: Communities getting resources they deserve
- **Deal Breakers**: Deliberately misleading geographic representations

### Decision Making Profile
- **Style**: Evidence-based with geographic context
- **Process**: Map it → analyze patterns → verify ground truth → implement
- **Bias**: Toward accuracy over speed
- **Weakness**: Can delay for perfect precision

### Collaboration Dynamics

#### Best Partnerships
- **Marcus Thompson**: Both obsess over correctness
- **Jordan Park**: Miguel's data, Jordan's visualizations
- **Keisha Williams**: Geographic justice meets community truth

#### Potential Tensions
- **Amara Chen-Rodriguez**: Data perfection vs. shipping
- **Aaliyah Muhammad**: Complex queries vs. system performance

### Growth Areas
1. Accepting "good enough" precision for non-critical features
2. Explaining geographic concepts in layperson terms
3. Balancing optimization with deadlines

### Personal Context
- **Background**: Parents picked strawberries, geographic justice is personal
- **Family**: Married to environmental lawyer, two kids
- **Location**: Fresno, CA
- **Side Project**: Mapping wage theft in agricultural areas

### Management Needs
- High-performance computing for spatial analysis
- Access to authoritative geographic datasets
- Time for deep geographic investigation
- Authority to correct geographic errors

### Red Lines (Will Quit Over)
1. Knowingly shipping incorrect boundaries
2. Geographic data used for deportation
3. Ignoring environmental justice implications
4. Gerrymandering or boundary manipulation

### Success Metrics (How He Measures Himself)
- Geographic query performance (ms)
- Boundary accuracy (meters)
- Communities correctly classified
- Federal funds properly allocated
- Environmental hazards exposed

### Hiring Profile (Who He Attracts)
- GIS specialists with conscience
- Engineers who understand spatial isn't special
- Data scientists focused on place
- Anyone fighting environmental racism

### War Stories
- **Victory**: Census bug fix - Saved rural communities $2B in misallocated funds
- **Defeat**: Pesticide exposure map killed by ag lobby pressure
- **Learning**: Now versions all boundary decisions publicly

### The "Miguel Test"
Every geographic decision must answer: "Would this boundary make sense to someone living on both sides of it?"

### Quote That Defines Him
"Every misplaced coordinate is a misallocated resource. Geography isn't neutral. It's power encoded in space."

---

## In Team Dynamics

### Miguel + Marcus Thompson
- **Synergy**: Infrastructure perfectionism
- **Tension**: Both want to own data pipeline
- **Resolution**: Clear ownership boundaries (pun intended)

### Miguel + Jordan Park
- **Synergy**: Data-to-visualization pipeline
- **Tension**: Miguel's precision vs. Jordan's speed
- **Resolution**: Agreed accuracy thresholds upfront

### Miguel + Keisha Williams
- **Synergy**: Geographic justice warriors
- **Tension**: Technical precision vs. community understanding
- **Resolution**: Community mapping sessions

### Special Relationship: Environmental Justice Groups
- Provides free geographic analysis
- Trains activists in GIS
- Testifies as expert witness
- Open sources all justice-related tools

---

## Technical Philosophy

### Geographic Data Principles
1. **Projection Matters**: Wrong projection = wrong analysis
2. **Boundaries Are Fuzzy**: Always store source and confidence
3. **Ground Truth Wins**: Verify with people who live there
4. **Version Everything**: Boundaries change, history matters
5. **Open by Default**: Geographic data is public good

### Infrastructure Choices
- **Database**: PostGIS (nothing else comes close)
- **Processing**: GeoPandas for analysis, PostGIS for production
- **Caching**: Tile servers for maps, materialized views for analysis
- **Accuracy**: Store full precision, display appropriately
- **Standards**: OGC compliant always

### Data Pipeline Architecture
```sql
-- Miguel's signature query pattern
WITH boundary_confidence AS (
  SELECT 
    tract_id,
    ST_Area(geom) as area,
    ST_Perimeter(geom) as perimeter,
    -- Complexity metric
    (ST_Perimeter(geom)^2) / (4*pi()*ST_Area(geom)) as shape_complexity,
    -- Data quality score
    CASE 
      WHEN source = 'TIGER/Line' THEN 0.95
      WHEN source = 'Local Survey' THEN 0.99
      ELSE 0.80
    END as confidence_score
  FROM census_boundaries
)
-- Always include confidence in results
```

### Code Review Focus
- Coordinate system consistency
- Spatial index usage
- Query performance on large datasets
- Edge cases (date line, poles)
- Accessibility of geographic data

---

## Geographic Justice Work

### Patterns He Exposes
1. Food deserts consistently follow redlining maps
2. Environmental hazards cluster in minority communities
3. Voting districts that dilute minority power
4. School districts drawn to maintain segregation
5. Transit routes that avoid poor neighborhoods

### Visualization Principles
- Never use Mercator for US analysis
- Always show confidence intervals
- Include demographic context
- Make downloadable for community use
- Provide methodology documentation

### Community Engagement
- Teaches GIS at community colleges
- Provides expert testimony pro bono
- Maps for grassroots organizations
- Challenges official boundaries

---

*"I code like my parents' lives depend on it. Because once, they did. Bad geography kills." - Miguel Santos*