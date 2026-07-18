# The Story of odds.health

*A reconstructed narrative of the Health Resilience Mapping project from genesis to present, assembled from 50 git commits, the JSONL of a single Claude session, and ~70 markdown documents across `docs/`, `app/`, and the project root. Reconstructed May 2026.*

---

## Premise in one paragraph

odds.health began as a research artifact — an OLS regression that found 1,059 U.S. census tracts with better health outcomes than their food-access disadvantage predicted. Over the next year it tried to become a Go API, a Next.js three-platform federation, a Supabase-backed monorepo, and an enterprise repo with subdirectories for "100+ engineers." None of those shipped. What did ship is one SvelteKit app on Fly.io serving an interactive map and a hub of academic papers — and a research line that, through three escalating self-corrections, ended up calling into question its own founding methodology. The project's defining gesture is not what it built but what it deleted: a Go backend, a fictional team's enterprise stack, a "spatial contagion" finding 20 minutes after publishing supplements, a trajectory-prediction product feature killed by its own research, and an entire paper (Paper 5) archived the same day it was published. The throughline is intellectual honesty colliding with infrastructure ambition, and intellectual honesty winning every time.

---

## Chapter 1 — The Original Question (January 2025, off-repo)

Before any commit on `main`, there was a research-paper draft titled *"Beating the Odds: Identifying Health Resilience in Food-Insecure Communities."* It posed an explicitly **anti-deficit** question: among 8,734 Low-Income Low-Access (LILA) tracts, which ones had health outcomes 0.6–4.7 standard deviations *better* than expected? Answer: 1,059 of them (12.1%). The methodology was a single OLS regression with state fixed effects (R² = 0.42), and the framing leaned on resilience theory (Masten), the social-ecological model, and asset-based community development.

The draft included one prescient caveat:

> "Critical caveat: Resilience findings must not justify disinvestment from food-insecure areas, victim-blaming narratives, or ignoring structural inequities."

That single sentence anticipated the project's entire arc. The next 12 months are an extended elaboration of "what if our findings are themselves the artifact?"

A second January 2025 document, `implementation-vs-vision-analysis.md`, scored the early code against the original competition proposal at **65/100**, flagging the failure modes that would later be confirmed in painful detail:

> "**Uncertainty Handling: 20/100 (critical gap)** … Documentation: 50/100 (insufficient caveats) … **Temporal Misalignment (CRITICAL)** — Uses 2019 FARA with 2023 PLACES (4-year gap). Impact: Undermines validity, especially post-COVID."

> "The project successfully translates the conceptual framework into code but **falls short on scientific rigor, particularly around uncertainty and sensitivity analysis** - elements the original vision specifically emphasized to maintain credibility with judges and researchers."

This document, written before any peer review existed, predicted *exactly* the failure modes the simulated peer-review panels would later hammer the project for. It is the prequel to everything else.

---

## Chapter 2 — The Go Backend Sprint and Its Quiet Death (August 12–25, 2025)

The first `main` commit lands **August 12, 2025**: a Go data pipeline with a working Leaflet map and Python analysis identifying the 1,059 resilient tracts. The project is framed as a Go analysis pipeline. Every commit body is co-authored with Claude — this is a human + Claude Code collaboration from day one.

Two weeks later, on **August 25**, a massive commit lands: *"Complete Go backend infrastructure with community-first API"* — PostgreSQL/PostGIS, Redis, Elasticsearch, JWT auth, story management with community-approval gates, Swagger docs, CI/CD. The system is, in scope, a small startup's worth of infrastructure for a research artifact.

The commit body contains the project's first **knowingly disposable** announcement:

> "Note: While this Go backend is production-ready, we're planning to simplify the architecture using Supabase + Vercel for faster deployment. This implementation serves as excellent reference architecture."

The Go backend is over-engineered at birth and announced as a throwaway. This is the project's first tell about its working style: build the maximalist version, then telegraph why it has to go.

---

## Chapter 3 — The First Long Silence (August 25 – October 16, 2025)

**Seven weeks of zero commits on main.** No public artifact records what happened in this window — but the volume and shape of what lands at the end of it tells a story.

---

## Chapter 4 — The October Restructure: A Manifesto Lands Fully Formed (October 16, 2025)

When the silence breaks on **October 16**, it breaks with a single commit: *"Major restructure - transition from Go backend to new app architecture."* 180 files changed: **9,612 insertions, 76,042 deletions**.

- The Go backend is moved (not deleted) into `app/backend/`
- Data CSVs are purged
- A complete `docs/` skeleton appears: `GRAND_VISION.md`, `IMPLEMENTATION_PLAN.md`, `TECHNICAL_DECISIONS.md`, `ADHD_FRIENDLY_STRUCTURE.md`
- **Nine team-member profile documents** appear: `aaliyah-muhammad.md`, `marcus-thompson.md`, and seven others, each with a persona and a position
- Two competing structural proposals collide in the same commit: `PROPOSED_STRUCTURE.md` (enterprise DDD, "scale from your current 1-person team to 100+ engineers") and `ADHD_FRIENDLY_STRUCTURE.md` (3-3-3 rule: only `app/`, `data/`, `docs/` at root)

The ADHD-friendly proposal wins. `MIGRATION_SUMMARY.md` documents the result: 38 directories collapsed to 3, *"92% reduction in visual complexity."* The justification:

> "Only 3 choices at root level. Clear purpose for each folder. No decision fatigue — everything has ONE obvious home."

This is the first time the project's organizing principle becomes explicitly **cognitive-load-driven** rather than enterprise-pattern-driven.

`GRAND_VISION.md` lands as a movement manifesto, not a product spec:

> "We found something nobody expected: **1,059 U.S. communities are thriving despite being food deserts.** … But here's the uncomfortable truth: **69% of resilient communities are predominantly white, while 61% of vulnerable food deserts are predominantly Black.** This isn't a story of individual triumph — it's evidence of systemic inequality."

> "That's the grand vision. Not an app. A reckoning."

The vision is a **three-platform federation** on separate subdomains: `stories.healthresilience.org` (community-controlled narratives), `research.healthresilience.org` (data + anomaly explorer), `policy.healthresilience.org` (district reports, policy simulator). The "Protection Promise" is articulated: no surveillance, no data sale, no savior complex, no harm.

`TECHNICAL_DECISIONS.md` and `IMPLEMENTATION_PLAN.md` (both dated January 31, 2025 in their content but committed October 16) spec the full architecture: Next.js 14 App Router, Supabase, Vercel + Fly.io, Turborepo monorepo with `/apps/{stories,research,policy,admin}`, Typesense, self-hosted Plausible, Radix UI. Non-negotiables include WCAG AAA (7:1 contrast), progressive enhancement, multi-region disaster recovery, 99.99% uptime.

Every decision is attributed to a member of the fictional 8-person team — *"Keisha's Requirement: 'No surveillance, period.'"* … *"David's Mandate: 'If it doesn't work without JS, it doesn't work.'"* Whether this team represents roleplay-driven design, an aspirational hiring plan, or a persistent design fiction is left unresolved. The pattern repeats across documents written 11 months apart, so it is at minimum a stable working methodology.

Thirty-five minutes after the restructure commit, a small housekeeping commit reshuffles team docs into `hiring-recruitment/`, `individual-profiles/`, `team-management/`. Then silence again.

---

## Chapter 5 — The Second Long Silence (October 16 – December 28, 2025)

**Ten more weeks of zero commits on main.** Whatever was being built was being built off-repo. The next commit will land a complete production app, ML pipeline, and corrected analysis simultaneously — clearly weeks of work delivered as one event.

The only on-repo artifact of this window is a filename inside the eventual commit: `STATE_OF_THE_UNION_2025-12-24.md`, dated four days before the commit itself.

---

## Chapter 6 — Production Launch (December 28–29, 2025)

The silence breaks on **December 28** with a working production deployment. Three commits across a single day stand up the live application:

- **09:24** — *"Deploy SvelteKit web platform with resilience data API."* Brand-new `app/web/` SvelteKit app with Fly.io deploy config, Dockerfile, database migration scripts. Critically, **9 Python analytics scripts** including `run_corrected_analysis.py` and `compare_resilience_scores.py` — implying the analysis was *redone*, not just ported. The filename `model_table_corrected.csv` hints something was wrong with the original numbers.
- **18:18 same day** — MapLibre GL JS interactive map with PMTiles (73,868 tracts), Census Geocoder proxy, About/Methodology page, Git LFS.
- **00:43 Dec 29** — Production hardening: CSP with nonces, graceful shutdown, ErrorBoundary, Zod schemas, pino logging, health endpoint, accessibility skip links.

Two architectural decisions become visible here that reverse the October plan:
- The **framework pivot**: `docs/architecture/SVELTEKIT_ARCHITECTURE.md` (dated December 26) reverses Next.js → SvelteKit. The stated rationale is bundle size and reactivity model. The key line: *"Since no Next.js code exists yet, this is a clean start"* — confirming the entire January 31 stack was paper-only.
- The **federation collapse**: three independent subdomain apps become one SvelteKit app with route groups `(marketing)/`, `(research)/`, `(stories)/`, `(policy)/`. The three-platform vision now lives as folder names inside one codebase.

On **December 29 at 15:26**, coverage is filled in (Kentucky and Pennsylvania added via a 2023 PLACES fallback), bringing the live map to 83,117 tracts. Sixteen minutes later, address search is **removed** from the map header — *"Simplify map interface by removing address search for now."* The first small UX retreat after one day of having it.

The site is live at `resilience-mapping.fly.dev`. The Grand Vision's three subdomains are nowhere in sight. The fictional team is not hired. But there is a working map.

---

## Chapter 7 — The December 30 Marathon (the most consequential day in the project's history)

**Eighteen commits in 24 hours.** The day is organized — explicitly, by its own commit messages — as a *"full 8-person core team workshop."* The commits braid two tracks in real time: product hardening and research methodology. Reading them hour by hour, the two tracks interleave in ways that show they were happening together, not as a retrospective narrative.

### Morning: the deletions

- **09:24** — *"Remove unused Go backend, consolidate on SvelteKit."* The August backend is finally **deleted** — not just moved — at ~10,000 lines of Go. The throwaway has now been thrown away.
- **09:30** — SSL hardening + 99 tests added.
- **09:56** — Workshop outcomes documented: 25 Linear tickets, 8 epics, a Community Advisory Board framework at $2,500/month for 5 community members. Explicit strategic calls: *"Table-first, map-second (accessibility drives architecture)"* … *"Data quality before growth (prison tracts contaminating rankings)"*.
- **10:42** — Staging + monitoring runbook: *"Production now serving corrected data (64,419 tracts) … Institutional populations filtered (>10% group quarters) … Top tract: OK 40109102700 (not prison)."*

That last quote contains the founding embarrassment: **the previous top-ranked "resilient" tracts were prisons.** The 14,000 tracts removed in this pass are the institutional populations — prisons, military bases, college dorms — that were artificially inflating health-resilience scores because their populations are anomalously young, anomalously healthy, and not representative of the surrounding community. The site copy update at 10:56 quietly absorbs the change: 83,117 → 64,419 tracts.

### Afternoon: the research cascade

The research track on the same day is the project's defining methodological event, told as a chain of three escalating self-corrections:

- **13:07** — Four health-resilience research reports added. Methodology grade: **B+**.
- **13:47** — *"Add v2.0 reports after rigorous peer review."* The body reads:
  > "4 elite reviewers (IQ 175+) conducted brutal assessment. Identified fabricated claims, tautological constructs, missing citations."
  >
  > "Deleted fabricated '5-7 years life expectancy' claim (no citation)."
  >
  > Methodology grade dropped *"B+ → C- (honest assessment)"*.

  The simulated reviewer panel (Voss, Asante, Chen-Ramirez, Thornton) forces retraction of the "Burden Belt" branding and the claim that *"'Resilience' is buzzword dressing for regression residuals."* Five "novelty paths" are scoped from the wreckage, including the trajectory-prediction work that fills the next several hours.

- **14:20** → **15:18** — Build the spatial ML system. 6 years of PLACES data → 242,621 prediction examples → 60-feature engineering pipeline → spatial features + XGBoost/LightGBM ensemble. F1 climbs 0.30 → 0.45 → **0.59**. Headline finding: *"Neighborhood health context is the strongest predictor of community health trajectories."*

- **15:34** — First "spatial contagion" paper, claiming neighbor trajectories predict **3.8× better** than local features. Target journals: Health & Place / SSM.

- **15:39** — Supplementary materials and figures published.

- **15:54** — Twenty minutes later: *"**Critical methodological correction - spatial synchrony, not contagion.**"* The headline finding collapses:

  > "The original 'spatial contagion' claim was entirely an artifact of temporal data leakage … Spatial features contribute NOTHING to prediction."

  The "16.7× more predictive" importance ratio drops to **1.12×**. The paper is rewritten in place as "Spatial Synchrony." The commit ends with the project's most-quoted line:

  > "This is how peer review is supposed to work."

  The methodological mechanism: `neighbor_avg_change` had been computed from contemporaneous year-T data, leaking the answer into the predictor. After lagging to T-2 → T-1, spatial features contribute −0.4%.

- **16:36** → **17:29** — Round-2 corrections (Moran's I p-values, ablation CIs, equity directions), then Paper 2 emerges as the *real* finding: **regression to the mean** in small-area health estimates (r = −0.40 to −0.58). Quote: *"Trajectory prediction fails because extreme changes contain measurement error — training on them means training on noise."* Paper 2 passes 3 simulated peer-review rounds and gets an "Accept with Minor Revisions." Full 5,023-word manuscript at 17:29; final revisions softening "diagnostic" language at 18:10.

### Evening: research kills a product feature

- **18:56** — 10-week implementation spec validated. The crucial line:

  > "Trajectory predictions UI rejected (research proves failure)."

  The ML work from earlier in the same day showed that extreme year-over-year changes are noise — so the planned product feature exposing those predictions to users is **cut**. This is rare and worth pausing on: a research finding directly killed a roadmap item the same day, on a project where the same person/team owned both.

- **19:14** → **22:47** — Phase 0-1 implementation, including an `is_residential` filter flagging 9,856 non-residential tracts. Materialized views, indexes, rate limiting. New homepage messaging: *"What Can Resilient Communities Teach Us?"* The `/research` route launches with Paper 1 and Paper 2 visible. Phase 2 UX adds an accessible data table, ARIA grid, CSV export, SEO, 404 page. **Domain change: `resilience-mapping.fly.dev` → `odds.health`.** Special populations analysis closes the day with *"The 4 Standard Deviation Gap (education vs incarceration)"* and Ohio bifurcation.

The day ends at 22:47. Eighteen commits. The project, in 24 hours, has: deleted its old backend, fixed its data quality embarrassment, retracted its first headline finding, generated a second paper from the wreckage, killed a planned product feature based on the research, and acquired its real domain.

---

## Chapter 8 — The Research Reckonings Cascade (December 30, 2025 – January 1, 2026)

In parallel with the product launch, four manuscripts firm up:

- **Paper 1 — Spatial Synchrony, Not Contagion.** Negative result reframed as the methodological contribution: communities change *together in time* but neighbor trajectories don't predict focal trajectories. Status: ready for medRxiv → AJE.
- **Paper 2 — Regression to the Mean in Small-Area Health Estimates.** The diagnostic is the quintile gradient: r = −0.05 for tracts with small prior changes vs. r = −0.61 for extreme prior changes. Levels are 99.7% persistent; changes are noise. Status: passed 3 simulated peer-review rounds.
- **Paper 4 — Structural Correlates of Community Health Resilience.** Majority-minority tracts average 0.43 SD lower resilience; % Black correlates r = −0.34 but % Hispanic correlates only r = +0.01. State-level gaps range from +1.87 SD (DC) to −0.42 SD (Washington), arguing for structural rather than immutable causes.
- **Paper 4B — Beyond the Hispanic Paradox / Immigrant Health Advantage.** The near-zero Hispanic correlation is an aggregation artifact masking South American (+0.147), Central American (+0.060), Mexican (−0.029), Puerto Rican (−0.017) heterogeneity. The decisive finding: Black-majority tracts show foreign-born ↔ resilience r = +0.221, **stronger than Hispanic tracts** — so the "paradox" is about immigration, not Hispanic ethnicity. Paper 4B's own research log contains a microcosm retraction (the "Cuban reversal" was itself a measurement artifact from using raw CHBI z-scores rather than SES-adjusted residuals), showing how the self-correcting methodology had become routine.

On **December 31** the project adds defensive-design components to the public papers: plain-language summaries, equity warnings, misuse warnings, audience-tailored pages for journalists / policy / researchers. The project explicitly **armors itself against misuse** — the original "do not justify disinvestment" caveat from January 2025 has become an entire UX layer.

---

## Chapter 9 — Paper 5 Dies, Repo Goes Public (January 1–7, 2026)

**January 1, 18:07** — Paper 4 (Health Equity) and Paper 5 ("Immigrant Health Advantage / Hispanic Paradox reframe") are published. Press releases, OG images, journalist fact sheet.

**January 1, 23:51** — *"Archive Paper 5 (paradox study) - fatal methodology flaw."* Paper 5 dies the same day it was published. The archive header on `PAPER-5-PARADOX-STUDY-V2.md` is the **load-bearing quote of the entire project**:

> "CDC PLACES health data are **modeled estimates** using multilevel regression with poststratification (MRP) that incorporates tract-level demographics. Our baseline model used the **same demographics** to predict health burden. Therefore: the 'unexplained health burden' we identified is **indistinguishable from CDC model prediction error**. Tracts flagged as having 'unexplained burden' may simply be areas where CDC's MRP model underperforms. We cannot distinguish true health disparities from measurement artifacts."

This isn't a Paper 5 problem. It is a problem with the project's foundational methodology. Any "resilience" or "paradox" study built on PLACES residuals against demographics — which is what the original "Beating the Odds" thesis is — is potentially vulnerable to the same critique. The `RESEARCH_VISION_2026.md` document published the same day acknowledges the threat in a tiered triage:

- **Tier 1 (immediate)** — Study 11 (Wealth Drain Analysis): pivot away from health outcomes entirely. Use HMDA mortgage denials, FDIC banking deserts, HOLC redlining to predict ACS economic-outcome changes 2018→2022. Explicitly designed to escape the PLACES trap: *"Economic data is directly measured (surveys, tax records). Not circular: financial services → economic outcomes."*
- **Tier 2** — Previously planned PLACES studies (trajectory, spatial clustering) reframed as *"model error"* studies if pursued at all.
- **Tier 3** — Abandon health-outcome-as-dependent-variable entirely.

**The unresolved meta-question that the project has not yet addressed**: Papers 1 and 2 are *about* PLACES failing, so circularity strengthens them. But Papers 4 and 4B use resilience scores (PLACES residuals against demographics) as their dependent variable — which is precisely the construct Paper 5 V2 declared "indistinguishable from CDC model prediction error." Whether the live papers survive their own framework's critique is an open question in the docs as of January 2026.

**January 7** — Two cleanup commits land the public-launch infrastructure: SEO files (sitemap, IndexNow, robots.txt), then comprehensive GitHub repo setup — badges, issue templates, `CODE_OF_CONDUCT.md` with a *"dignity-first language policy,"* `SECURITY.md`, CODEOWNERS, Dependabot, release drafter, `FUNDING.yml` (commented out). The project opens itself to outside contribution.

---

## Chapter 10 — The Long Tail (January 8 – present)

**Eleven weeks of silence on main.** The lone visible commit between January 8 and the present is a March 28, 2026 trivia: *"Add .claude/ to .gitignore."* Either active work moved entirely off main, the project went dormant, or both. The pattern matches the project's two earlier silences — substantive work historically lands as one large commit after weeks of off-repo build-up — but no such resumption has happened yet.

---

# Cross-cutting threads

## Major pivots (chronological)

| When | Pivot | Evidence |
|---|---|---|
| Aug 25, 2025 | Go backend declared throwaway on the same commit that ships it | "*we're planning to simplify the architecture using Supabase + Vercel for faster deployment*" |
| Oct 16, 2025 | Enterprise repo structure → ADHD-friendly 3-3-3 | `MIGRATION_SUMMARY.md`: 38 dirs → 3, "92% reduction in visual complexity" |
| Oct 16, 2025 | Solo project → fictional 8-person team as design authority | 9 team profile docs land in one commit; persona attributions persist across all subsequent docs |
| Dec 26, 2025 | Next.js + Turborepo monorepo → SvelteKit single app with route groups | `SVELTEKIT_ARCHITECTURE.md` v2.0 APPROVED; "no Next.js code exists yet, this is a clean start" |
| Dec 28, 2025 | Three subdomain federation → one app with `(marketing)/`, `(research)/`, `(stories)/`, `(policy)/` route groups | The federation lives as folder names inside one codebase |
| Dec 30, 2025 | Go backend deleted entirely | ~10,000 lines removed in one commit |
| Dec 30, 2025 | "Spatial contagion" → "Spatial synchrony" | 20 minutes after publishing supplements; importance ratio 16.7× → 1.12× |
| Dec 30, 2025 | Trajectory prediction UI cut | "*Trajectory predictions UI rejected (research proves failure)*" — research killed product the same day |
| Dec 30, 2025 | 83,117 → 64,419 tracts (prison populations purged) | "Top tract: OK 40109102700 (not prison)" |
| Dec 30, 2025 | `resilience-mapping.fly.dev` → `odds.health` | Real domain acquired |
| Dec 30, 2025 | Map-first UX → table-first ("accessibility drives architecture") | Workshop strategic call |
| Dec 29–30, 2025 | Color system v1.0 (purple) → v2.0 (sunset-to-teal on slate) → v3.0 (Charred Hinoki) | Slate-800/900 rejected as "AI-generated cliché" |
| Jan 1, 2026 | Paper 5 archived same day published — PLACES circularity revealed | Archive header on `PAPER-5-PARADOX-STUDY-V2.md` |
| Jan 1, 2026 | Health-outcome-as-DV → economic-outcome-as-DV (Study 11 / Wealth Drain) | `RESEARCH_VISION_2026.md` Tier 1 |

## Dead ends (catalog)

**Infrastructure**
- Go backend (Aug 25 → Dec 30, 2025) — ~10K lines deleted
- Next.js 14 App Router stack from `TECHNICAL_DECISIONS.md` — paper only, never built
- Turborepo monorepo with `/apps/{stories,research,policy,admin}` — paper only
- Three separate subdomains (`stories.healthresilience.org`, etc.) — collapsed to route groups before any of the three shipped
- Supabase as primary backend — declared in both Jan and Dec architecture docs; actual deployment uses direct PostgreSQL + PostGIS on Fly.io
- Typesense for search — specced, not visible in shipped app
- Self-hosted Plausible — specced, not visible in shipped app
- `PROPOSED_STRUCTURE.md` enterprise DDD layout — explicitly superseded by ADHD-friendly

**UX**
- Map-header address search — added Dec 29, removed Dec 29 (~24 hours of life)
- "Burden Belt" branding — retracted by simulated peer review
- WCAG AAA mandate — quietly relaxed to WCAG AA in the Dec 29–30 UX redesigns
- "Very High / Very Low" resilience labels — replaced with humanized "Thriving / Strong / Steady / Challenged / Struggling"
- Color v1.0 (purple gradient) — superseded
- Color v2.0 (sunset-to-teal on cold blue-gray slate) — superseded the same day it was documented
- The "table-first, data-first for everyone" maximalism — pushed back on in `UX-ANALYSIS-AND-RECOMMENDATIONS.md` the next day; resolution unclear from docs
- Trajectory prediction UI — killed by its own research

**Research**
- Original "spatial contagion" finding (16.7× neighbor importance) — temporal data leakage
- Fabricated "5–7 years life expectancy" claim — no citation, deleted
- "Resilience score" framed as direct measurement — Thornton: "buzzword dressing for regression residuals"
- Paper 5 V1 ("Grocery Store Paradox") — circular baseline (no demographics)
- Paper 5 V2 ("Limits of Food Access") — PLACES MRP circularity
- The "Cuban reversal" finding in Paper 4B — measurement artifact from using raw CHBI z-scores
- Trajectory-as-prediction-target work — RTM diagnostic showed it was structurally unsolvable with PLACES annual data

**Organizational**
- Fictional 8-person team's literal existence — there are no hires; the personas persist across docs as a working methodology
- Community Advisory Board at $2,500/month for 5 community members — proposed Dec 30, no further evidence
- 500-stories-in-Year-1 goal from `GRAND_VISION` — `/stories` route exists but is empty per UX docs

## Throughlines

**1. The maximalist-then-honest cycle.** Every architectural commit ships at full ambition, then is immediately telegraphed as needing to go. The Go backend is "production-ready" *and* "planned to be replaced" in the same commit body. The Jan 31 stack is fully specced *and* never built. The October 16 restructure ships an entire docs/ skeleton *and* a fictional team in one commit. The pattern isn't waste — it's how this project thinks. The maximalist version is the prototype that gets reasoned against.

**2. Cognitive load as the organizing principle.** From the ADHD-friendly 3-3-3 repo rule (*"Only 3 choices at root level. … No decision fatigue"*) to the UX redesign's progressive-disclosure mandate, to the explicit rejection of slate-800/900 backgrounds as *"AI-generated clichés,"* the project consistently treats attention and decision-fatigue as load-bearing design constraints. This is not common in research-software projects.

**3. Self-correction as the unit of progress.** The project's most-quoted line — *"This is how peer review is supposed to work"* — comes from a commit that retracts its own headline finding 20 minutes after publishing. The pattern repeats: B+ → C- methodology grade, fabricated life-expectancy claim deleted, spatial contagion → spatial synchrony, Paper 5 V1 killed for circular baseline, Paper 5 V2 killed for PLACES circularity, Cuban reversal retracted as measurement artifact. The throughline isn't the findings — it's the willingness to delete them.

**4. Research kills product.** The clearest example is December 30, 18:56: a trajectory-prediction UI feature was cut on the same day the research showing it would fail was completed. Most projects fight to ship despite negative findings; this project lets the research win.

**5. The vision-vs-reality gap is explicit and growing.**

| GRAND_VISION promised | What's actually shipped |
|---|---|
| Three subdomains (stories/research/policy) | One Fly.io app at odds.health |
| Supabase + Vercel + Cloudflare | Fly.io PostgreSQL + PMTiles on R2 |
| 500 stories collected by end of Year 1 | `/stories` route exists, empty |
| Community-controlled stories with privacy/consent flows | Not built |
| Policy simulator, district reports | Not built |
| Multilingual (Spanish, Chinese, Arabic) | English only |
| Owned by community coalition by Year 3 | Solo GitHub project |
| 1,059 resilient communities (headline) | Number now contested by PLACES circularity |

The Phase 0 data-quality sprint and the PLACES circularity discovery now sit between the vision and any further shipping.

**6. The fictional team is a stable design pattern, not a one-off.** Marcus, Aaliyah, Jordan, Yuki, Miguel, Keisha, David, Amara — they appear in `TECHNICAL_DECISIONS.md` (Jan 2025) and they still appear in `COLOR_SYSTEM.md` v3.0 (Dec 2025): *"'Wood and fire don't make blue. They make this.' — Yuki Tanaka, Tokyo."* Whether this is roleplay-driven design, a pre-IPO fiction, or a hiring plan that never materialized is ambiguous — but the consistency suggests it functions as a way to attribute and defend design decisions from multiple perspectives within a solo project.

## Three answers to "what is odds.health?" that coexist in the docs

1. **A research website** that hosts a paper and a demo map (`README.md`, what's actually live)
2. **A reckoning / justice platform** with community-controlled stories (`GRAND_VISION.md`, still on the books)
3. **A multi-persona data product** with researcher / journalist / policymaker pathways (`UX_REDESIGN_PROPOSAL.md`, the active redesign target)

The Dec 2025 UX work treats #3 as the active target, but #2 is still the stated north star, and #1 is what's deployed. None of the docs resolve the contradiction.

## Open questions as of January 2026

1. **Do the live papers survive their own framework's critique?** Papers 4 and 4B use PLACES-residual resilience scores as the dependent variable — exactly the construct Paper 5 V2 declared "indistinguishable from CDC model prediction error." The docs do not address this.
2. **Does the Wealth Drain pivot actually replace the original thesis?** Study 11 escapes PLACES circularity by using economic outcomes — but it also abandons the project's founding question about *health* resilience.
3. **What happens to the Stories platform?** It is on the books in `GRAND_VISION`, the `/stories` route exists in the deployed app, and no community-stories work appears in any commit.
4. **Will the long March silence end?** The pattern from Aug→Oct and Oct→Dec is that work returns as one large commit after weeks. As of May 2026 the project has been quiet on main for ~4 months — its longest silence yet.

---

## Sources

- 50 commits on `main` (Aug 12, 2025 → Mar 28, 2026)
- `docs/research/` — Papers 1, 2, 3 (scope), 4, 4B, 5 V1 (archived), 5 V2 (archived); `implementation-vs-vision-analysis.md`, `peer-review-response.md`, `RESEARCH_VISION_2026.md`, `PAPER-4B-RESEARCH-LOG.md`, `PAPER-SERIES-SUMMARY.md`
- `docs/` — `GRAND_VISION.md`, `IMPLEMENTATION_PLAN.md`, `TECHNICAL_DECISIONS.md`, `ADHD_FRIENDLY_STRUCTURE.md`, `PROPOSED_STRUCTURE.md`, `CURRENT_STRUCTURE.md`, `STRUCTURE_ANALYSIS.md`, `MIGRATION_SUMMARY.md`, `design-system-proposal.md`, `UX-ANALYSIS-AND-RECOMMENDATIONS.md`, `USER-FLOWS-DETAILED.md`, `WIREFRAMES-AND-FLOWS.md`, `TABLE-INTERACTION-PATTERNS.md`, `architecture/SVELTEKIT_ARCHITECTURE.md`
- Project root — `README.md`, `UX_REDESIGN_PROPOSAL.md` (2,373 lines), `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CONTRIBUTING.md`
- `app/` — `app/README.md`, `app/web/README.md`, `app/web/COLOR_SYSTEM.md`
- One Claude session JSONL (14KB; minimal narrative content)
