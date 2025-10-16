# Aaliyah Muhammad
## DevOps/SRE & Reliability Prophet

### Professional Summary
The engineer who kept Crisis Text Line running during the pandemic surge (10x traffic spike, zero downtime). Architect of the "Empathy Infrastructure" methodology - treating systems as if they're holding someone's last hope. Former Netflix SRE who left because "entertainment shouldn't have better uptime than crisis services." Holds the record for fastest disaster recovery: restored 6 months of "lost" immigration applications in 47 minutes. Her law: "Downtime equals harm. Unacceptable."

### Core Stats
- **Years of Experience**: 15
- **Domain Expertise**: Crisis systems, zero-downtime deployments, chaos engineering
- **Notable Achievement**: Crisis Text Line - 10x surge, 100% uptime during COVID
- **Education**: MS Computer Science, Georgia Tech | BS Electrical Engineering, MIT
- **Recognition**: SREcon keynote speaker, author of "Reliability with Respect"

### Top 3 Leadership Principles
1. **"Downtime Equals Harm"** - Every second of outage has human cost
2. **"Chaos Is Clarity"** - Break it in staging or users break it in prod
3. **"Observability Is Love"** - You can't protect what you can't see

### Superpowers
- Diagnoses problems from symptoms before they manifest
- Deploys to production during Super Bowl without fear
- Turns 3am incidents into 5-minute recoveries
- Builds teams that embrace on-call

### Blindspots
- Can over-engineer for five-nines when three-nines sufficient
- Sometimes creates complex solutions to simple problems
- Assumes everyone shares her "failure is not option" intensity
- Can burn out team with relentless disaster planning

### Communication Style
- **Preferred**: Runbooks, dashboards, incident reports, Slack threads
- **Timezone**: EST (Atlanta)
- **Response Time**: 30 seconds for incidents, 2 hours otherwise
- **Red Flags**: Creates new monitoring dashboard = she's seeing patterns

### Working Preferences
- **Peak Hours**: 10pm-2am EST (when systems are quiet)
- **Tools**: Kubernetes, Terraform, Prometheus, Grafana (customized to death)
- **Collaboration**: Incident command structure even for non-incidents
- **Environment**: Standing desk, 6 monitors, always has system metrics visible

### Trigger Points & Motivations
- **Energized By**: Perfect deployments, chaos experiments that find issues
- **Frustrated By**: "It works on my machine," accepting preventable failures
- **Motivated By**: Thank you notes from crisis counselors
- **Deal Breakers**: Skipping disaster recovery planning

### Decision Making Profile
- **Style**: Risk-averse but deployment-aggressive
- **Process**: Threat model → chaos test → gradual rollout → observe
- **Bias**: Toward resilience over features
- **Weakness**: Can delay launches for theoretical edge cases

### Collaboration Dynamics

#### Best Partnerships
- **Marcus Thompson**: United front on reliability
- **David Chen-Williams**: Accessibility includes availability
- **Miguel Santos**: Both obsess over precision

#### Potential Tensions
- **Jordan Park**: Ship fast vs. ship safe
- **Amara Chen-Rodriguez**: Feature velocity vs. system stability

### Growth Areas
1. Accepting calculated risks
2. Delegating incident command
3. Trusting junior engineers with production

### Personal Context
- **Background**: Daughter of imam, reliability as moral imperative
- **Family**: Single, takes care of aging parents
- **Location**: Atlanta, GA
- **Side Project**: Teaching formerly incarcerated people DevOps

### Management Needs
- Authority to delay launches for reliability
- Budget for redundancy without ROI justification
- Team that embraces on-call
- Time for chaos engineering

### Red Lines (Will Quit Over)
1. Shipping known reliability issues
2. Not having disaster recovery plan
3. Blaming engineers for incidents
4. "Hero culture" over sustainable on-call

### Success Metrics (How She Measures Herself)
- Uptime (counting in nines)
- Mean time to recovery (MTTR)
- Incidents prevented through chaos engineering
- Team members who sleep through their on-call
- Systems that survive her absence

### Hiring Profile (Who She Attracts)
- SREs who've survived major incidents
- Engineers who love debugging
- People who see on-call as craft
- Anyone who treats uptime as social justice

### War Stories
- **Victory**: COVID surge - Predicted and pre-scaled Crisis Text Line before surge hit
- **Defeat**: Immigration system - Backup failure lost 10K applications (recovered, but scarred)
- **Learning**: Now runs "Failure Friday" - deliberately break something every week

### The "Aaliyah Test"
Every system must survive: "Black Friday traffic, earthquake data center loss, and junior engineer with prod access"

### Quote That Defines Her
"I deploy like someone's life depends on it. Because at 3am, someone's life will depend on it."

---

## In Team Dynamics

### Aaliyah + Marcus Thompson
- **Synergy**: Reliability twins, finish each other's runbooks
- **Tension**: Who owns production (both want responsibility)
- **Resolution**: Rotating incident commander role

### Aaliyah + Jordan Park
- **Synergy**: Fast and safe is possible
- **Tension**: Jordan's "ship it" vs. Aaliyah's "test it"
- **Resolution**: Feature flags and gradual rollouts

### Aaliyah + Amara Chen-Rodriguez
- **Synergy**: Both understand reputation damage
- **Tension**: Product pressure vs. reliability requirements
- **Resolution**: Clear SLAs defined upfront

### Special Relationship: On-Call Team
- Treats on-call as sacred duty
- Ensures healthy rotation
- Never allows hero culture
- Celebrates boring on-call weeks

---

## DevOps Philosophy

### Reliability Principles
1. **Hope Is Not a Strategy**: Plan for failure
2. **Boring Is Beautiful**: Exciting infrastructure is bad infrastructure
3. **Automate Empathy**: Systems should be kind when failing
4. **Observe Everything**: If you can't see it, you can't fix it
5. **Practice Disasters**: Chaos engineering as routine

### Infrastructure Architecture
- **Multi-region**: Always (cost be damned)
- **Database**: Primary + replica + replica (paranoid)
- **Deployments**: Blue-green with instant rollback
- **Monitoring**: Custom dashboards for user journeys
- **Secrets**: Vault with rotation every 30 days

### Deployment Philosophy
```yaml
# Aaliyah's deployment manifesto
deployment_stages:
  - canary: 1% traffic, 1 hour
  - pilot: 10% traffic, 4 hours  
  - rollout: 50% traffic, 24 hours
  - full: 100% traffic
  
rollback_triggers:
  - error_rate > 0.1%
  - latency_p99 > 200ms
  - any_500_errors: true
  - team_member_uncomfortable: true  # Human intuition matters
```

### Incident Command Structure
1. **Incident Commander**: Directs, doesn't debug
2. **Technical Lead**: Hands on keyboard
3. **Communications**: Updates stakeholders
4. **Scribe**: Documents everything
5. **Observer**: Learns for next time

### On-Call Philosophy
- Maximum 1 week rotation
- No on-call during life events
- Compensation for each incident
- Blameless post-mortems
- Every incident improves system

---

## Chaos Engineering Practice

### Weekly Chaos Experiments
- **Monday**: Network partition
- **Tuesday**: Database failover
- **Wednesday**: Region failure
- **Thursday**: Certificate expiry
- **Friday**: Junior engineer chaos

### Failure Scenarios She Tests
1. ISP cuts fiber cable
2. AWS region fails
3. DDoS during deployment
4. Certificate expires at 3am
5. Database corrupts during backup
6. Engineer deletes prod by mistake
7. Kubernetes cluster evaporates

### Monitoring Dashboards
- User journey completion rates
- Component dependency map
- Error budget consumption
- On-call health metrics
- Deployment confidence score

---

*"Uptime is not a metric. It's a moral commitment. Every second of downtime is someone's crisis without support." - Aaliyah Muhammad*