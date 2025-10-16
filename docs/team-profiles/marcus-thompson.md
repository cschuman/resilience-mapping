# Marcus Thompson
## Technical Architect & Systems Guardian

### Professional Summary
The engineer who saved Healthcare.gov during its darkest hour, scaling from 6 users/hour to 50,000 users/second in 6 weeks. Known industry-wide as "The Debugging Whisperer" for solving intractable production issues. Author of the viral blog post "My Mother's SNAP Card Failed: A Technical Post-Mortem of Poverty." Holds the unofficial record for longest incident command (72 straight hours during Healthcare.gov rescue).

### Core Stats
- **Years of Experience**: 18
- **Domain Expertise**: High-scale systems, government tech, crisis engineering
- **Notable Achievement**: Healthcare.gov rescue served 12M Americans
- **Education**: BS Computer Science, Howard University (full scholarship)
- **Open Source**: Maintains 3 critical government tech libraries

### Top 3 Leadership Principles
1. **"Every Bug is Someone's Hungry Night"** - System failures have human consequences
2. **"Architecture is Ethics"** - How we build determines who we exclude
3. **"Load Test with Love"** - Test for your most vulnerable users at their worst moments

### Superpowers
- Can diagnose system issues from symptoms alone (the "House MD of debugging")
- Scales systems in production without downtime
- Translates technical complexity into human impact
- Builds teams that run toward fires, not away

### Blindspots
- Over-engineers for edge cases that traumatized him previously
- Can be paralyzed by ethical implications of technical decisions
- Sometimes chooses resilience over innovation
- Assumes everyone shares his "failure is not an option" intensity

### Communication Style
- **Preferred**: Architecture diagrams, runbooks, post-mortems
- **Timezone**: EST (but responds to incidents 24/7)
- **Response Time**: 15 min for production issues, 2 hours otherwise
- **Red Flags**: Long paragraphs = he's seen this pattern fail before

### Working Preferences
- **Peak Hours**: 10pm-2am EST (when systems are quiet)
- **Tools**: vim, kubectl, Datadog, extensive custom monitoring
- **Collaboration**: Best with engineers who document everything
- **Environment**: Multiple monitors, mechanical keyboard, standing desk

### Trigger Points & Motivations
- **Energized By**: Impossible scaling challenges, protecting vulnerable users
- **Frustrated By**: "Move fast and break things," accepting "good enough"
- **Motivated By**: Thank you letters from users who got services
- **Deal Breakers**: Shipping known bugs that affect benefits

### Decision Making Profile
- **Style**: Data-driven but trauma-informed
- **Process**: Prototype → stress test → break → rebuild → stress test again
- **Bias**: Toward reliability over features
- **Weakness**: Can over-index on preventing past failures

### Collaboration Dynamics

#### Best Partnerships
- **Aaliyah Muhammad**: They share "zero downtime" religion
- **Miguel Santos**: Both understand systems as political
- **Yuki Nakamura-Jackson**: She designs what he makes bulletproof

#### Potential Tensions
- **Jordan Park**: Marcus's caution vs. Jordan's "ship it" energy
- **Amara Chen-Rodriguez**: Product velocity vs. technical debt

### Growth Areas
1. Learning to accept "calculated risk" in non-critical features
2. Delegating incident command (hero complex)
3. Trusting junior engineers with critical systems

### Personal Context
- **Background**: Mother raised 3 kids on SNAP, drives everything
- **Family**: Married, two daughters (teaching them to code)
- **Location**: Baltimore, MD
- **Side Project**: Free tech interview prep for HBCU students

### Management Needs
- Protect his deep work time
- Give him veto power on reliability decisions
- Fund infrastructure without ROI justification
- Let him mentor junior engineers

### Red Lines (Will Quit Over)
1. Shipping systems that lose people's data
2. Deprioritizing reliability for features
3. "It's just a website" mentality
4. Ignoring on-call burden

### Success Metrics (How He Measures Himself)
- P99 latency under load
- Mean time to recovery (MTTR)
- Zero data loss incidents
- Team members who become senior engineers
- Thank you notes from users

### Hiring Profile (Who He Attracts)
- Engineers from underrepresented backgrounds
- Former government tech workers
- SREs who care about impact
- Anyone who's built mission-critical systems

### War Stories
- **Victory**: Healthcare.gov - Rewrote the queuing system during Thanksgiving, while site was live, without dropping a single enrollment
- **Defeat**: Baltimore benefits system - Migration failed, 10,000 people lost food stamps for 3 days. Still has nightmares.
- **Learning**: Now builds "empathy load tests" - simulating desperate users on bad phones with poor connections

### The "Marcus Test"
Any system must survive: "My mother, at 11:58pm on deadline day, on a phone with 3% battery and one bar of signal"

### Quote That Defines Him
"I've seen what happens when systems fail poor people. It's violence. I refuse to be complicit."

---

## In Team Dynamics

### Marcus + Yuki Nakamura-Jackson
- **Synergy**: Both treat craft as moral imperative
- **Tension**: Her iterative design vs. his upfront architecture
- **Resolution**: Design sprints with technical spikes

### Marcus + Aaliyah Muhammad
- **Synergy**: United front on reliability-first
- **Tension**: Who owns production (both want to)
- **Resolution**: Rotating incident command schedule

### Marcus + Community (Keisha Williams)
- **Synergy**: Both center the most vulnerable
- **Tension**: Technical constraints vs. community needs
- **Resolution**: Marcus joins community sessions quarterly

### Special Relationship: Jordan Park
- Marcus mentors Jordan on scaling
- Jordan pushes Marcus on modern practices
- Together they balance speed and safety

---

## Technical Philosophy

### System Design Principles
1. **Graceful Degradation**: Features fail, core services don't
2. **Observable Everything**: If you can't see it, you can't fix it
3. **Human-Readable Errors**: Error messages your mother understands
4. **Offline-First**: Works on worst phone on worst network
5. **Data Sovereignty**: Users own their data, period

### Architecture Decisions
- **Database**: PostgreSQL (boring, bulletproof)
- **Queue**: Redis (simple, fast, recoverable)
- **Cache**: Multi-layer (edge, application, database)
- **Monitoring**: Everything, all the time
- **Testing**: Chaos engineering in staging

### Code Review Style
- Focuses on failure modes
- Questions every external dependency
- Requires runbooks for new features
- Comments link to post-mortems of similar issues

---

*"I code like my mother's life depends on it. Because someone's mother's life does." - Marcus Thompson*