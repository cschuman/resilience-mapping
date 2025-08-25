# 👥 USER PERSONAS & STORIES
## Health Resilience Mapping Platform

**Created**: January 31, 2025  
**Version**: 1.0  
**For**: Dev/Creative Team Startup

---

## 🎯 PRIMARY PERSONAS

### **PERSONA 1: Maria - Community Health Worker**
**Demographics**: 34, Latina, Birmingham AL, CHW for 8 years  
**Tech Level**: Moderate (smartphone, basic apps)  
**Context**: Works with 200+ families, knows food desert challenges intimately  

**Goals**:
- Find successful strategies from similar communities
- Show families they're not alone in their struggles
- Access resources that actually work in food deserts
- Build hope and community pride

**Pain Points**:
- Tired of being told her community is "failing"
- Needs proof that solutions work in similar places
- Limited time between home visits
- Unreliable internet connection

**User Stories**:
```
As Maria, I want to:
- Search by similar demographics so I can find relevant success stories
- Save resources offline so I can share them during home visits
- See photos of real families so my clients know these are authentic
- Get quick facts to share in 2-minute conversations
- Access content in Spanish and English
```

---

### **PERSONA 2: Dr. James - Public Health Researcher**
**Demographics**: 42, Black, Atlanta GA, PhD Epidemiology  
**Tech Level**: Expert (research databases, statistical software)  
**Context**: Studies health disparities, writes policy recommendations  

**Goals**:
- Access clean, analyzable data for research
- Identify patterns across successful communities
- Build evidence base for policy recommendations
- Publish findings in peer-reviewed journals

**Pain Points**:
- Data often incomplete or unreliable
- Can't replicate other researchers' findings
- Pressure to show immediate policy impact
- Difficulty getting community buy-in for studies

**User Stories**:
```
As Dr. James, I want to:
- Download datasets in standard formats (CSV, JSON)
- See methodology and data collection details
- Filter by demographic variables for analysis
- Cite data properly in academic papers
- Contact communities for follow-up research
```

---

### **PERSONA 3: Councilwoman Sarah - Local Policymaker**
**Demographics**: 51, White, Rural Kansas, City Council 6 years  
**Tech Level**: Basic (email, Facebook, simple websites)  
**Context**: Represents agricultural district with limited grocery access  

**Goals**:
- Find proven solutions for her constituents
- Get political cover for controversial decisions
- Understand what works without academic jargon
- Build coalitions with other rural leaders

**Pain Points**:
- Overwhelmed by academic research
- Needs simple talking points for town halls
- Limited budget for new programs
- Political pressure from multiple sides

**User Stories**:
```
As Councilwoman Sarah, I want to:
- See 1-page summaries of what works
- Find examples from similar rural communities
- Get contact info for successful community leaders
- Download maps showing geographic patterns
- Share success stories at public meetings
```

---

### **PERSONA 4: Keisha - Community Resident & Mom**
**Demographics**: 29, Black, Detroit MI, 3 kids under 12  
**Tech Level**: Mobile-first (all internet via phone)  
**Context**: Lives in identified "resilient" community, curious about the designation  

**Goals**:
- Understand what makes her community special
- Find resources for her family
- Connect with neighbors doing good work
- Feel proud of where she lives

**Pain Points**:
- Tired of negative portrayals of her neighborhood
- Limited data on mobile
- Suspicious of outside research
- Needs info that helps today, not just understanding

**User Stories**:
```
As Keisha, I want to:
- See my community represented authentically
- Find local resources and programs nearby
- Read success stories from people like me
- Share positive news about my neighborhood
- Control how my story is used
```

---

### **PERSONA 5: Miguel - Nonprofit Program Director**
**Demographics**: 37, Latino, Phoenix AZ, runs food access programs  
**Tech Level**: Intermediate (CRM systems, grant databases)  
**Context**: Manages $2M budget, serves 15 communities  

**Goals**:
- Identify which programs have biggest impact
- Find evidence for grant applications
- Scale successful interventions
- Demonstrate ROI to funders

**Pain Points**:
- Hard to prove impact of complex interventions
- Funders want simple metrics
- Competition for limited resources
- Difficulty measuring community-level change

**User Stories**:
```
As Miguel, I want to:
- Filter by intervention type to find what works
- See cost data for successful programs
- Get contact info for program leaders
- Export data for grant applications
- Track changes over time in communities
```

---

## 🎯 SECONDARY PERSONAS

### **Graduate Student Emma** (Research Assistant)
- Needs: Thesis data, methodology examples, citation formats
- Tech: Advanced, works in R/Python
- Goals: Academic publication, career advancement

### **Journalist Marcus** (Health Reporter)
- Needs: Human interest stories, expert sources, data visualizations
- Tech: Intermediate, deadline-driven
- Goals: Compelling stories, source verification

### **Federal Program Manager Lisa** (USDA/HHS)
- Needs: National patterns, program effectiveness, policy impact
- Tech: Government systems, security-conscious
- Goals: Evidence-based policy, program improvement

---

## 📱 USER JOURNEY MAPS

### **Journey 1: Maria's Weekly Resource Hunt**

**Monday Morning**: Preparing for home visits
1. **Opens app** → needs quick load on slow connection
2. **Searches** "single mom + diabetes + Birmingham" 
3. **Finds stories** → wants to save 3-4 for offline
4. **Downloads resources** → needs Spanish versions
5. **Shares with clients** → during home visits all week

**Emotional Journey**: Hopeful → Focused → Confident → Proud

---

### **Journey 2: Dr. James's Research Process**

**Grant Deadline Approaching**: Need data for proposal
1. **Searches literature** → finds reference to platform
2. **Explores site** → evaluates data quality
3. **Downloads dataset** → runs preliminary analysis
4. **Contacts communities** → seeks collaboration
5. **Cites in proposal** → gets funding approved

**Emotional Journey**: Skeptical → Curious → Excited → Grateful

---

### **Journey 3: Keisha's Discovery**

**Neighbor mentions**: "Our neighborhood is on some website"
1. **Google searches** → finds resilience platform
2. **Looks up address** → sees her community listed
3. **Reads description** → feels proud, curious
4. **Shares with friends** → spreads positive news
5. **Contacts site** → wants to add her story

**Emotional Journey**: Curious → Surprised → Proud → Engaged

---

## 🎯 USER STORY EPICS

### **EPIC 1: Discovery & Search**
```
As a user, I want to find communities like mine so I can learn from their success.

Stories:
- Search by demographics (age, race, income, location)
- Filter by challenges (food access, health outcomes)  
- Sort by similarity to my community
- Save interesting communities for later
- Get notifications about similar communities
```

### **EPIC 2: Story Consumption**
```
As a user, I want to understand what makes communities successful so I can apply lessons.

Stories:
- Read community success stories
- Watch video testimonials from residents
- See before/after data visualizations
- Download resource lists and contact info
- Share stories on social media
```

### **EPIC 3: Data Access**
```
As a researcher, I want to analyze patterns across communities so I can publish findings.

Stories:
- Download clean datasets in multiple formats
- Access methodology and data dictionary
- Filter data by multiple variables
- Export custom analysis subsets
- Cite data with persistent identifiers
```

### **EPIC 4: Community Control**
```
As a community member, I want to control how my story is told so I maintain dignity.

Stories:
- Review how my community is portrayed
- Request changes to descriptions
- Add my own story or photos
- Remove my content anytime
- See who has accessed my community's data
```

### **EPIC 5: Resource Connection**
```
As a practitioner, I want to connect with successful programs so I can replicate them.

Stories:
- Contact community leaders directly
- Find programs similar to what I run
- Get implementation guides and resources
- Track outcomes over time
- Build networks with peer organizations
```

---

## 🎯 ACCEPTANCE CRITERIA EXAMPLES

### **User Story**: Search by demographics
```
Given I am a community health worker
When I search for "Latino families" + "diabetes" + "rural"
Then I should see communities ranked by similarity
And each result shows key demographics
And I can save up to 10 communities for offline viewing
And search works on 2G connections within 5 seconds
```

### **User Story**: Community story control
```
Given I am a community resident
When I find my community on the platform
Then I can see exactly what data is shown
And I can request corrections through a simple form
And I receive email confirmation within 24 hours
And changes appear on the site within 48 hours
```

### **User Story**: Research data download
```
Given I am a public health researcher  
When I download a dataset
Then I get CSV + metadata + methodology documentation
And all personally identifiable information is removed
And I can reproduce any analysis shown on the site
And the data includes proper citation information
```

---

## 🎯 EDGE CASES & ACCESSIBILITY

### **Low-bandwidth Users** (Maria, Keisha)
- Offline-first design
- Image optimization
- Progressive loading
- Essential content first

### **Screen Reader Users** (All personas)
- Semantic HTML structure
- Alt text for all images
- Keyboard navigation
- Clear heading hierarchy

### **Mobile-only Users** (Keisha, many CHWs)
- Touch-friendly interfaces
- Thumb-reachable navigation
- Minimal text input
- Voice search capability

### **Low-literacy Users** (Some community members)
- Simple language (6th grade level)
- Visual instructions
- Audio narration options
- Icon-based navigation

---

## 🎯 SUCCESS METRICS BY PERSONA

### **Maria (CHW)**
- Time to find relevant story: <2 minutes
- Offline usage: 70% of sessions
- Stories shared: 5+ per month
- Return visits: Weekly

### **Dr. James (Researcher)**  
- Data download completion: 95%
- Citation rate in publications: Growing
- Community contact success: 60%
- Platform recommendation: 90%

### **Councilwoman Sarah (Policymaker)**
- Policy brief downloads: 50+ per month
- Town hall usage: 3+ examples per meeting
- Colleague referrals: 20+ per year
- Implementation attempts: 2+ per year

### **Keisha (Community Member)**
- Story sharing: 10+ friends/family
- Pride increase: Measured via survey
- Community engagement: Sustained
- Platform recommendations: High

### **Miguel (Nonprofit Director)**
- Grant success rate: Improved
- Program replication: 2+ per year
- Network connections: 10+ new contacts
- ROI demonstration: Quantified

---

## 🎯 DESIGN PRINCIPLES FROM USER RESEARCH

### **Dignity First**
- No deficit language ("food desert" → "limited access")
- Strength-based framing
- Community-controlled narratives
- Beautiful, professional design

### **Mobile Reality**
- 60% of users are mobile-only
- Slow connections common
- Thumb-friendly interactions
- Essential content prioritized

### **Trust Building**
- Transparent about data sources
- Clear privacy controls
- Community contact information verified
- Regular updates to maintain accuracy

### **Inclusive Access**
- Multiple languages
- Various literacy levels
- Assistive technology support
- Cultural responsiveness

---

**Next Steps**: Create wireframes based on these personas and user stories.

**Review Date**: February 5, 2025 (after initial user testing)