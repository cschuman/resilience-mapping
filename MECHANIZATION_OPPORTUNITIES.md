# Mechanization Opportunities

*Synthesized from four parallel analyst subagents (skills, hooks, playbooks, prompts) reviewing `PROJECT_STORY.md` and the source docs that grounded it. The filter for inclusion was strict: this project must have **actually paid the cost** of the missing mechanism — a failure happened, was painful, and a tool would have caught it, prevented it, or accelerated the recovery. Theoretical "would be nice" patterns were rejected.*

---

## TL;DR — Top picks across all artifact types

Ranked by `(historical pain × recurrence likelihood) / build cost`. Build top-down:

| # | Artifact | Type | Why it tops the list |
|---|---|---|---|
| 1 | **`circularity-audit`** (skill) + **`/circularity-check`** (prompt) | Skill + companion prompt | Killed Paper 5 the day it shipped; threatens live Papers 4 / 4B per the story's open question #1. Highest blast radius. No existing skill covers it. |
| 2 | **`adversarial-peer-review`** (skill) | Skill | The single most productive mechanism in the project — fired 4+ times in 72 hours, produced the "this is how peer review is supposed to work" line. `expert-panel` does product, not academic methodology. |
| 3 | **`/vision-gap`** (prompt) + **`vision-vs-shipped`** (skill) | Prompt + companion skill | The original 65/100 doc predicted *every* failure that hit 12 months later. Generalizes beyond odds.health to any project with a vision doc. |
| 4 | **`ai-cliche-color-blocker`** (hook) | Hook | Sharp, deterministic, low FP risk, cheap (~30 LOC). Project burned a full v1→v2→v3 color cycle writing this rule down; Claude would otherwise re-produce slate-800/900 every component. |
| 5 | **`defensive-publication-pack`** (playbook) + **`/defensive-framing`** (prompt) | Playbook + invocation prompt | Built reactively on Dec 31 for every live paper; Paper 5 V2 shipped without it and was archived 6 hours later. Needed for every future paper. |
| 6 | **`methodology-retraction`** (playbook) | Playbook | Executed 5+ times in 72 hours; the story's open question #1 exists because step 5 (sweep dependent claims) was skipped on Paper 5 V2. |
| 7 | **`long-silence-resumption`** (playbook) + **`/state-of-union`** (prompt) | Playbook + invocation prompt | Pattern recurred 2x and the project is currently 4 months into its longest silence yet. Active need. |
| 8 | **`places-as-dependent-variable-warn`** (hook) | Hook | The cheapest mechanical guard against the project's #1 risk surface. Warns, doesn't block — preserves Papers 1/2 use-case. |

Everything below is genuinely useful but secondary. Stop at the cost-line you can afford.

---

## The shape of what we're mechanizing

The four analysts converged on **four thematic clusters**, each with multiple artifact-type expressions. Reading across clusters makes the system legible:

### Cluster A — Methodological rigor in observational research

The project's defining failure mode: building findings on data whose construction the project doesn't fully control (CDC PLACES MRP estimates), then publishing claims whose statistical artifact-vs-signal distinction is unclear. Five mechanisms address this:

- `circularity-audit` (skill) — provenance graph of predictors vs. outcome's generative inputs
- `adversarial-peer-review` (skill) — 4-reviewer panel with discipline-specific personas
- `data-leakage-check` (skill) — temporal/spatial/target-encoding leak detection
- `places-as-dependent-variable-warn` (hook) — mechanical guard at edit time
- `unsupported-numeric-claim-flag` (hook) — fabricated-precision scanner
- `/circularity-check` (prompt) — quick one-shot version
- `/methodology-grade` (prompt) — B+/C- scorecard
- `methodology-retraction` (playbook) — when something collapses

### Cluster B — Vision-vs-reality accountability

The project's most successful early audit (`implementation-vs-vision-analysis.md`, 65/100) predicted every failure that came after. The vision/reality gap then widened dramatically and was only re-audited in `PROJECT_STORY.md` (May 2026, ~16 months later). The mechanisms keep this audit cheap and repeatable:

- `vision-vs-shipped` (skill) — scored reckoning table generator
- `/vision-gap` (prompt) — lightweight version
- `/state-of-union` (prompt) — dated stocktaking doc
- `long-silence-state-of-the-union` (hook) — SessionStart prompt after N days quiet
- `long-silence-resumption` (playbook) — coalesce off-repo work into staged commits
- `architecture-pivot` (playbook) — maximalist → simpler-alternative ADR shape

### Cluster C — Publication defense

The project's response to its own caveat ("findings must not justify disinvestment") evolved from a single sentence into a full UX layer of equity/misuse warnings, audience-tailored pages, and plain-language summaries. Built reactively for every paper on Dec 31, 2025. The mechanisms make it proactive:

- `equity-warning-layer` (skill) — defensive component generator
- `defensive-publication-pack` (playbook) — pre-publish checklist with retraction-readiness as final gate
- `/defensive-framing` (prompt) — one-shot generator

### Cluster D — Design taste / repo hygiene

The project explicitly catalogued AI-default design defaults (slate-800/900) and supersession patterns (archive headers, deprecated docs, throwaway "reference architecture"). Cheap mechanical hooks catch these:

- `ai-cliche-color-blocker` (hook) — block forbidden hex/Tailwind tokens in design files
- `superseded-doc-edit-warn` (hook) — prevent reviving archived docs
- `csv-precommit-lfs-gate` (hook) — Git LFS routing for large data files
- `/ai-cliche-check` (prompt) — broader taste audit including typography/copy/components

---

## By artifact type

The full proposals from each analyst, lightly edited for cross-reference.

### Skills (rich packaged capabilities, invokable on demand)

#### S1. `circularity-audit`

**Pattern**: *"CDC PLACES health data are modeled estimates using multilevel regression with poststratification (MRP) that incorporates tract-level demographics. Our baseline model used the same demographics to predict health burden. Therefore: the 'unexplained health burden' we identified is indistinguishable from CDC model prediction error."*

Given a study design (data sources, predictors, outcome variable, baseline model), traces the provenance of every variable and flags constructs where a predictor was used — directly or via a model — to *generate* the outcome. Emits a "circularity ledger" with per-path verdicts (clean / suspect / fatal).

The reference catalog is the load-bearing artifact: a mapping of common MRP/modeled datasets (PLACES → ACS race/age/sex/poverty; SAIPE → IRS+ACS; SVI → ACS) to the demographics they ingest. Built once, reused on every future study.

**Differentiation**: `rigor` audits code; `expert-panel` workshops product problems; `holistic-review` correlates runtime errors. None know what CDC PLACES is.

**Build cost**: medium (catalog is the work). **Pain history**: 2 papers killed; threatens 2 live papers.

#### S2. `adversarial-peer-review`

**Pattern**: *"4 elite reviewers (IQ 175+) conducted brutal assessment. Identified fabricated claims, tautological constructs, missing citations."* Methodology grade B+ → C-.

Runs a 4-reviewer simulated panel on a research artifact. Each reviewer is a named persona with a discipline (epi / biostats / health-geography / policy-evaluation), modeled on the actual Voss / Asante / Chen-Ramirez / Thornton panel. Pipeline: independent scans → flagged failure modes (fabricated precision, uncited claims, tautological constructs, terminology appropriation) → cross-corroboration → per-reviewer review + consolidated retraction list + suggested rewrites with citations.

**Differentiation**: `expert-panel` is product-problem framing with 6 generalist personas (PM, designer, engineer). Different domain, different reviewer kit.

**Build cost**: medium. **Pain history**: 4+ documented retractions in 72 hours.

#### S3. `vision-vs-shipped`

**Pattern**: The `implementation-vs-vision-analysis.md` 65/100 audit predicted exactly the failures that hit 12 months later. The gap has only widened since.

Compares a vision/grand-plan doc against shipped reality (deployed app + git log + actual file tree) and produces a scored reckoning table — categories, current grade, "what would close the gap" actions. Uses the project's own document template.

**Differentiation**: `holistic-review` looks at runtime errors; `rigor` audits code quality; `sdlc` builds features. None reconcile vision-as-written vs. shipped-as-deployed.

**Build cost**: low-medium (format is templated). **Pain history**: pattern recurred at 16-month gap; vision delta grew unobserved between audits.

#### S4. `equity-warning-layer`

**Pattern**: *"The project explicitly armors itself against misuse — the original 'do not justify disinvestment' caveat from January 2025 has become an entire UX layer."*

For a research finding touching race / ethnicity / geography / community-level outcomes, generates: plain-language summary, equity warning, misuse warning, audience-tailored framings (journalist / policy / researcher). Reference doc ships a misuse taxonomy (deficit-framing, individual-responsibility, disinvestment justification, fixed-group-difference reading, savior framing).

**Differentiation**: `design-brief` produces UI mockup spec, not equity scaffolding for empirical claims.

**Build cost**: low (templates exist in the project). **Pain history**: Each of Papers 1, 2, 4, 4B, 5 needed this; built reactively.

#### S5. `data-leakage-check`

**Pattern**: The spatial-contagion retraction 20 minutes after publishing supplements. `neighbor_avg_change` used contemporaneous year-T data. Importance ratio 16.7× → 1.12×.

Given a prediction pipeline, checks for temporal, spatial, and target-derived leakage. Three parallel checkers; per-feature flag with leak path and lag/exclusion that closes it.

**Differentiation**: Distinct from `circularity-audit` (which is about generative provenance of the *outcome*); leakage is about predictor-target timing/spatial overlap within a clean outcome.

**Build cost**: low-medium. **Pain history**: caused the most public retraction in project history.

---

### Hooks (automated event-triggered guards)

The bar for hooks is high — they fire on every matching event and need to be cheap, deterministic, and high-precision. Each below clears that bar.

#### H1. `ai-cliche-color-blocker`

- **Event**: `PreToolUse` on Edit / Write / MultiEdit, files matching `\.(svelte|css|scss|html|ts|tsx|jsx|vue)$` under `app/web/`
- **Action**: grep `tool_input.new_string` for `#0f172a`, `#1e293b`, `#020617`, `slate-(800|900|950)`, `bg-slate-[89]00`, `from-slate-[89]00`. If matched, exit 2 with feedback naming `COLOR_SYSTEM.md` and the Charred Hinoki replacement (`#0C0A08` / `#1C1410`).
- **Behavior**: block with override path (magic comment `/* color-system-override: <reason> */`)
- **FP risk**: low (catch list enumerated in project policy; legitimate quoting of the doc itself is path-excluded)
- **Build**: ~30 lines of jq + grep

#### H2. `places-as-dependent-variable-warn`

- **Event**: `PostToolUse` on Write / Edit / MultiEdit for `analysis/.*\.py$`, `app/web/python/.*\.py$`, or new `.py`/`.R` files under `data/` or `analysis/`
- **Action**: detect co-occurrence of PLACES variable tokens (`PLACES`, `CHBI`, `chbi_score`, `health_burden`, `resilience_score`, `residual`) used as `y` / `target` / left-hand-side of regression formula. Inject context citing `RESEARCH_VISION_2026.md` Tier 1 + Paper 5 V2 archive header.
- **Behavior**: warn, never block (Papers 1/2 are explicitly about PLACES failing — a valid use)
- **FP risk**: medium; mitigated by warn-only + explicit citation of project's own decision
- **Build**: ~80 lines (regex against pandas / statsmodels / sklearn idioms)

#### H3. `unsupported-numeric-claim-flag`

- **Event**: `PostToolUse` on Edit / Write / MultiEdit for `docs/research/.*\.md$` and `app/web/src/routes/\(research\)/.*\.(svelte|md)$`
- **Action**: extract added lines; regex-match `\b\d+(\.\d+)?\s*(years?|%|percent|×|x more|fold|standard deviations?|SD)\b`. For each match, check ±3 surrounding lines for citation pattern (`et al\.|\[\d+\]|\(\d{4}\)|JAMA|NEJM|Lancet|doi:|https?://`). Inject any unsupported claims as `additionalContext`.
- **Behavior**: observe + warn (never blocks)
- **FP risk**: medium. Mitigations: scope to research paths only; skip fenced code and table headers; tune unit list to causal-claim units
- **Build**: ~60 lines

#### H4. `superseded-doc-edit-warn`

- **Event**: `PreToolUse` on Edit / Write / MultiEdit for `docs/`, `app/web/`, root `*.md`
- **Action**: read first 30 lines of target file; grep for `ARCHIVED|SUPERSEDED|DEPRECATED|replaced by|⚠️.*archived|fatal methodology flaw`. If matched, exit 2 quoting the archive header back.
- **Behavior**: block with explicit re-run override
- **FP risk**: low (file must self-declare)
- **Build**: ~25 lines

#### H5. `csv-precommit-lfs-gate`

- **Event**: `PreToolUse` on Bash for commands matching `git add` / `git commit`
- **Action**: `git diff --cached --name-only --diff-filter=A` and check any staged `*.csv` / `*.parquet` / `*.geojson` / `*.pmtiles` > 10 MB without LFS filter. If found, exit 2 with `git lfs track` instructions.
- **Behavior**: block
- **FP risk**: low (deterministic on file size and LFS filter)
- **Build**: ~20 lines

#### H6. `long-silence-state-of-the-union`

- **Event**: `SessionStart`, self-gated to fire at most weekly via `.claude/.last-silence-warning` stamp file
- **Action**: compute days since last main commit. If > 14, emit `additionalContext`: "Last commit on main was N days ago. Project pattern is multi-week off-repo work returning as large commits — consider asking the user for a state-of-the-union before editing."
- **Behavior**: inject context
- **FP risk**: low (self-gated weekly; observe-only)
- **Build**: ~15 lines

---

### Playbooks (structured multi-step procedures with gates)

#### P1. `methodology-retraction`

**When to invoke**: A finding, claim, or feature has been proven wrong after publication / public commit.

**Steps**:
1. **Identify scope** — list every artifact that asserts the broken claim (commits, papers, UI copy, OG images, press releases, dependent papers). **Gate**: scope checklist file before any edits.
2. **Write the corrected narrative** — what was claimed, the mechanism of the error, the corrected finding, one sentence on detection. **Gate**: mechanism explicitly named.
3. **Apply archive header in place** (don't delete; Paper 5 V2's header is the load-bearing artifact). Status badge + fatal-flaw summary + redirect to replacement scope. **Gate**: header includes specific reproduction mechanism.
4. **Sweep dependent claims** — grep the canonical phrase ("16.7×", "1,059", "spatial contagion") across repo. **Gate**: zero references in live copy.
5. **Update research log** — what survives, what falls; address dependent live papers (the story's open question #1 exists because this step was skipped for Paper 5 V2). **Gate**: dependent papers explicitly addressed.

**Artifacts**: archive header, retraction commit, updated research log, scope-checklist file.
**Form**: markdown templates + multi-step skill for the sweep.

#### P2. `data-quality-blocker-sprint` (Phase 0)

**When to invoke**: Before any major release; when a leadership audit flags data integrity concerns; when ingesting a new external dataset whose population frame may not match the analytic frame.

**Steps**:
1. State-of-the-union: current dataset, current top-10, would-this-embarrass-us check. **Gate**: top-N manually inspected for face-validity (the "is this a prison?" question).
2. Population-frame audit — group quarters %, temporal alignment, measurement artifacts (e.g., MRP circularity). **Gate**: every flagged issue has a documented filter or accepted-risk note.
3. Fix in place: filter, re-run, regenerate. **Gate**: old vs new comparison table.
4. Research-team sign-off (simulated reviewer panel). **Gate**: explicit checkbox.
5. Site copy + metadata reflects corrected N. **Gate**: grep for old N returns zero hits before merge.

**Form**: markdown reference doc + checklist skill.

#### P3. `architecture-pivot` (maximalist → honest)

**When to invoke**: Architectural decision feels off; planned stack hasn't been built; commit body contains "we'll replace this later."

**Steps**:
1. Document the maximalist version. **Gate**: written, not implied.
2. Cost analysis: team = N, time = M, what survives if one person is doing this? **Gate**: explicit headcount in the doc.
3. Propose simpler alternative with comparison table (SvelteKit doc's table is the template). **Gate**: trade-offs accepted, not just wins.
4. ADR with APPROVED / SUPERSEDED status. **Gate**: explicit supersession + link to prior doc.
5. Migration plan with "is anything in production?" check.
6. **Sweep**: delete truly-throwaway code. **Gate**: don't leave dead stacks as "reference architecture" indefinitely.

**Form**: markdown reference doc; ADR is the artifact.

#### P4. `defensive-publication-pack`

**When to invoke**: Before any research paper goes public — must run before press release / OG image / homepage update.

**Steps**:
1. Plain-language summary (200 words). **Gate**: non-researcher can summarize back.
2. Equity warning — who could be harmed if misread? **Gate**: harm scenarios listed.
3. Misuse warning — who would weaponize this? **Gate**: at least one named misuse + counter-framing.
4. Audience pages (journalists / policy / researchers). **Gate**: each answers "what should I do with this?"
5. Press / OG / homepage copy reviewed against warnings. **Gate**: copy cannot contradict warnings.
6. **Retraction-readiness test**: if this collapses tomorrow, what's the shortest clean retraction path? **Gate**: artifact list ready for `methodology-retraction` playbook.

**Form**: markdown templates + multi-step skill walking the checklist.

#### P5. `long-silence-resumption`

**When to invoke**: Returning to a repo after weeks/months of off-repo work, before first commit to main.

**Steps**:
1. State-of-the-union doc lands as commit #1, before code. **Gate**: dated, blunt, no corporate optimism.
2. Stage off-repo work into logical commit chunks. **Gate**: no single commit > N files unless explicit restructure with justifying doc.
3. Run `methodology-retraction` for any findings that shifted while silent.
4. Run `architecture-pivot` for any stack changes that happened off-repo.
5. Re-establish vision-vs-reality scorecard. **Gate**: explicit table updated.

**Form**: markdown reference doc + state-of-the-union template.

---

### Prompts / slash-commands (single-shot reusable templates)

Lightweight versions of the above, for when full skill scaffolding is overkill. The full prompt bodies are in the source analyst report — these are the headers.

#### C1. `/circularity-check <model-or-paper-path>`
Verdict-per-predictor (CLEAN / SUSPECT / FATAL) + overall paper verdict + "what would make this paper survive its own framework's critique?" Differentiated from skill S1 by being one-shot text vs. cataloged-knowledge-base.

#### C2. `/vision-gap [vision-doc] [reality-doc-or-glob]`
Two-column promised/shipped table + per-row classification (SHIPPED / PARTIAL / NOT BUILT / SUPERSEDED / CONTESTED) + 100-point score (Scope 40 / Rigor 40 / Polish 20) + close-the-gap section + retire-the-promise section.

#### C3. `/methodology-grade <paper-path>`
Letter grade across 6 axes (construct validity, causal honesty, uncertainty, data quality controls, citation integrity, reproducibility), overall = MIN of the six. Publish / Revise / Retract verdict.

#### C4. `/state-of-union [project-root]`
Generates `STATE_OF_THE_UNION_YYYY-MM-DD.md` with: where we actually are; what shipped since last; what's been retracted or killed; open questions; the single next most important thing. Tone constraint: honest, slightly weary, allergic to corporate optimism, no emoji, quote real commit hashes.

#### C5. `/defensive-framing <paper-path>`
4-part packet: plain-language summary + equity warning + misuse warning + three audience-tailored summaries (journalist / policymaker / researcher). Lightweight one-shot version of playbook P4.

#### C6. `/ai-cliche-check <css-or-design-doc>`
Audits for AI-default tells: colors (slate-800/900, indigo-500, gradient-from-purple-to-pink), typography (Inter-only, no display face), copy ("Elevate", "Unlock", "Seamlessly"), components (rounded-2xl + shadow-xl + backdrop-blur stacks). Each tell → line number + one-sentence reason + replacement grounded in existing design system.

---

## Patterns deliberately rejected (cross-section)

The four analysts each had a "rejected" section. The most instructive rejections:

- **Fictional 8-person team as a roleplay skill** — `expert-panel` already does multi-persona problem framing. The personas demonstrably worked for odds.health as a design-attribution device, but proposing a near-duplicate with health-equity flavoring would duplicate existing capability. Better: add personas to a project memory or `expert-panel` config.
- **Maximalist-then-honest cycle detector** — the failure mode is a human decision ("ship the maximalist version anyway"), not something a skill prevents. A hook flagging "production-ready" + "planned to simplify" in the same commit would catch it faster than a skill could.
- **Cognitive-load auditor (3-3-3 / ADHD-friendly)** — one-shot work per project; once a repo is at 3-3-3 it stays there. Not enough recurrence to justify a skill.
- **Large-deletion-without-explanation flagger** — every one of this project's large deletions was intentional and well-messaged. The flagger would fire on healthy events and train the user to ignore it.
- **Data-leakage hook (vs. skill)** — detecting `neighbor_avg_change` at year T predicting year T requires understanding pandas semantics across multiple lines. Mechanical regex would miss subtle cases or fire on every legitimate `df['neighbor_avg']`. Belongs to a skill that reads the full pipeline.
- **Research-paper birth-to-publication playbook** — `sdlc` and `sdlc-light` already encode "phase + gate + review" orchestration. The differentiated value is concentrated in `defensive-publication-pack` (P4).
- **`/pivot-tell`** — the human knows they're about to pivot. They don't need Claude to tell them.
- **`/retraction <finding>`** — multi-step with checkpoints = playbook (P1), not slash command.

---

## Build sequence recommendation

If building one at a time, in order of marginal value per hour:

1. **`ai-cliche-color-blocker`** (H1) — 1 hour, immediate daily payoff, zero risk.
2. **`/state-of-union`** (C4) — 30 minutes (just a prompt template). Use it now, write the May 2026 SOTU, ship before the next push.
3. **`/circularity-check`** (C2) — 30 minutes. Run it on Papers 4 and 4B *today* to resolve open question #1.
4. **`/vision-gap`** (C2) — 30 minutes. Run on `GRAND_VISION.md` + current `app/web/`. The result will likely set the next quarter's roadmap.
5. **`places-as-dependent-variable-warn`** (H2) — 2 hours. The cheapest mechanical guard against the #1 risk surface.
6. **`adversarial-peer-review`** (S2) — half a day. Reusable across every future paper.
7. **`circularity-audit`** (S1) — full day (the reference catalog is the work). Highest blast-radius prevention.
8. **`methodology-retraction`** (P1) — half a day to template; then keep it on hand for next retraction.
9. **`defensive-publication-pack`** (P4) — full day. Required for any next paper.
10. **Everything else** as needed.

### Stop conditions

If after building #1–#4 you find the patterns aren't recurring (e.g., the project goes truly dormant), stop. Don't build #5+ on theoretical recurrence.

---

## Meta: the workflow that produced this doc is itself mechanizable

This document was produced by:
1. `PROJECT_STORY.md` reconstruction (git historian + research archaeologist + app archaeologist, parallel) → synthesis
2. This mechanization analysis (4 parallel analysts: skills/hooks/playbooks/prompts) → synthesis

That's a `/post-mortem-mechanization` skill: given a project root, produce a chronological story + a mechanization opportunities doc. Reusable across any sufficiently-documented project. Worth scoping after the first few items in the build sequence above pay off — proves the meta-pattern by using it.

---

## Source analyst reports

The four full analyst reports (cap ~1500 words each) live in the conversation context but were not written to disk. Re-runnable from `PROJECT_STORY.md` if needed.
