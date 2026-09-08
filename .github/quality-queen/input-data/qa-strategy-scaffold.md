# QA Strategy — [Project Name]

> **Data accuracy rule:** All file counts and test counts must be EXACT numbers. Never use approximations ("100+", "~50", "several", "many"). Count the actual files or tests and report the precise number. Every count must be verifiable against the actual files in the repository.

**Project:** [Project name and short description]  
**Version:** [X.Y]  
**Last updated:** [YYYY-MM-DD]  
**Author:** [QA consultant name]  
**Status:** Draft — to be reviewed and refined collaboratively with the team

> **Versioning rules (managed automatically on regeneration):**
> - `Last updated` = today's date in `YYYY-MM-DD` format.
> - `Version` follows `MAJOR.MINOR`:
>   - First generation = `1.0`.
>   - Increment **MINOR** for refinements, clarifications, or new findings on the same project state.
>   - Increment **MAJOR** when the underlying `project-structure-<projectName>.md`, board structure, or strategy direction changes materially.
> - Add a row to the **Version History** table below for every regeneration.

### Version History

| Version | Date | Author | Summary of changes |
|---|---|---|---|
| [X.Y] | [YYYY-MM-DD] | [Author] | [What changed in this revision, e.g. "Initial generation", "Refreshed test pyramid section after new E2E suite", "Bumped after Project-Structure.md update"] |

**Sources used:**
- [List sources: repository code, CI/CD workflows, board exports, wiki, interviews, etc.]

**Not yet validated through:** [List what has not been validated, e.g. team interviews, retrospectives, board observation, customer/PO conversations, wiki content.]

---

## 1. Executive Summary

### Project Context

[Describe the project: what it does, who uses it, tech stack, deployment model, team composition and size, current QA situation. Include the git branching strategy used (e.g. trunk-based, GitFlow, GitHub Flow, feature-branch) and how it affects code integration and release cadence.]

### Top Quality Risks

> Reference finding IDs from §7 (e.g. C1, M2). State the business-level risk in one sentence — do not restate the evidence or location here.

1. [Risk 1 — finding ID]
2. [Risk 2 — finding ID]
3. [Risk 3 — finding ID]
4. [Risk 4 — finding ID]
5. [Risk 5 — finding ID]

### Overall QA Maturity Snapshot

Rate each area using the scale below. Base the rating on **verified evidence**, not impressions.

| Rating | Criteria |
|---|---|
| **Very Low** | Capability is absent or non-functional (0 tests, blocked tooling, no process exists) |
| **Low** | Capability exists minimally but has critical gaps (e.g. tests exist but miss key layers; process defined but not enforced) |
| **Medium** | Reasonable coverage with notable but non-critical blind spots (e.g. good component coverage but API layer untested; templates exist and are mostly followed) |
| **High** | Comprehensive coverage with few gaps; actively maintained and enforced |

| Area | Maturity | Notes |
|---|---|---|
| Unit testing (backend) | [Very Low / Low / Medium / High] | [Max 5 words] |
| Unit testing (frontend) | [Very Low / Low / Medium / High] | [Max 5 words] |
| API testing | [Very Low / Low / Medium / High] | [Max 5 words] |
| E2E testing | [Very Low / Low / Medium / High] | [Max 5 words] |
| CI/CD pipeline quality gates | [Very Low / Low / Medium / High] | [Max 5 words] |
| Documentation & process | [Very Low / Low / Medium / High] | [Max 5 words] |
| Security testing | [Very Low / Low / Medium / High] | [Max 5 words] |
| Issue prioritisation | [Very Low / Low / Medium / High] | [Max 5 words] |

### Priority Recommendations (Top 5)

> List action IDs from §7 with a one-line summary. Do not duplicate the full action table rows here.

1. [Action ID — one-line summary]
2. [Action ID — one-line summary]
3. [Action ID — one-line summary]
4. [Action ID — one-line summary]
5. [Action ID — one-line summary]

---

## 2. Delivery Flow and Quality Gates

### 2.1 As Is — Observed Board Columns

[Describe the team's actual workflow. Map the columns observed on the board. Note any gaps between the structural flow and how it is used in practice.]

> **Template placeholder** — replace with a project-specific delivery flow diagram before publishing.
> 1. Copy `work-process.drawio` from `.github/quality-queen/input-data/diagrams/` to `work-process-[ProjectName].drawio` in `.github/quality-queen/output-data/diagrams/`.
> 2. Open in draw.io. For each phase: rename `[Phase N]` to the team's phase name and `[Environment N]` to the deployment environment. Rename each `[Column]` box to the board column name. Add or remove column boxes within each phase panel as needed. Set DoR (red) and DoD (green) gate labels on the appropriate columns.
> 3. In the generated output file, update the image reference below to `./diagrams/work-process-[ProjectName].svg`.
> 4. Export the `.drawio` file to SVG (see README — Step 3).

![Delivery Flow — [ProjectName]](./diagrams/work-process.svg)

**Observations:**
- [Observation 1 — e.g. which columns are actively used]
- [Observation 2 — e.g. whether items flow consistently]
- [Observation 3 — e.g. whether DoR/DoD exist or not]

### 2.2 Recommended Quality Gates (Proposal)

Mapped onto the team's existing column structure:

| Column | Gate | Suggested Criteria (to validate with team) |
|---|---|---|
| **[Column 1]** | — | [Criteria or "no further criteria"] |
| **[Column 2]** | DoR | [Entry criteria for development to start] |
| **[Column 3]** | — | [In-progress conventions] |
| **[Column 4]** | DoD-partial | [Code review exit criteria] |
| **[Column 5]** | DoD-partial | [Test/QA exit criteria] |
| **[Column 6]** | DoD-full | [Done criteria including deployment and sign-off] |

**Recommendation:** [How and where to codify these criteria — e.g. GitHub Issue templates, CONTRIBUTING.md, PR checks.]

---

## 3. QA in Work Processes

### As Is

[Describe how the team actually works today. Cover: Agile methodology, tooling, team composition and roles, planning practices, issue taxonomy, DoR/DoD status, release cadence, communication, and any observed quality practices. Include whether feature flags are used (system, ownership, impact on release planning and rollback) or note their absence and any resulting risk for progressive delivery. Ground each observation in a concrete source.]

### Ambition

[What improvements does the team want to make? Be specific and actionable. Where possible, reference existing backlog items.]

### AI

- **Current:** [Which AI tools are in use today, and for what? Which engine?]
- **Engine in use:** [e.g. GitHub Copilot, ChatGPT, other]
- **Opportunity:** [Where could AI streamline work responsibly?]

---

## 4. QA in Build Processes

### As Is

[Describe the CI/CD pipeline, test automation in the build, code review practices, environments, test data, deployment flow, and any security/dependency scanning. Include whether feature flags are integrated into the pipeline, how flag states are managed across environments, whether tests validate behavior under different flag states, and if there is a process for cleaning up stale flags. Reference actual pipeline files or tools where possible.]

### Ambition

[What pipeline and build process improvements are planned or recommended? Be specific.]

### AI

- **Opportunity:** [Where could AI assist in build, review, or pipeline work?]

---

## 5. Agile QA Quadrant Assessment

### As Is

> **Template placeholder** — replace with a project-specific quadrant diagram before publishing.
> 1. Copy `qa-quadrant.drawio` from `.github/quality-queen/input-data/diagrams/` to `qa-quadrant-[ProjectName].drawio` in `.github/quality-queen/output-data/diagrams/`.
> 2. Open in draw.io and fill each quadrant with ✓/⚠/✗ bullet-point activities. Set the maturity badge (top-right corner of each quadrant) to the project's level (None/Low/Medium/High — see table below).
> 3. **Do NOT change quadrant background colors.** Colors are fixed per quadrant (Q1=blue, Q2=green, Q3=amber, Q4=red) and represent the quadrant identity, not maturity. Only the small grey badge text changes to reflect maturity.
> 4. In the generated output file, update the image reference below to `./diagrams/qa-quadrant-[ProjectName].svg`.
> 5. Export the `.drawio` file to SVG (see README — Step 3).

![Agile QA Quadrant — [ProjectName]](./diagrams/qa-quadrant.svg)

| Quadrant | Description | Current State |
|---|---|---|
| **Q1 — Technology-facing, supporting the team** | Unit tests, component tests | [Current state] |
| **Q2 — Business-facing, supporting the team** | Functional tests, story tests, acceptance tests, buddy testing | [Current state] |
| **Q3 — Business-facing, critiquing the product** | Exploratory testing, usability testing, UAT, manual test suites, test management tools (e.g. Azure Test Plans, TestRail, Zephyr Scale, Xray) | [Current state — for manual testing detail, see §6] |
| **Q4 — Technology-facing, critiquing the product** | Performance testing, security testing, load testing | [Current state] |

**Maturity levels** (shown as badges in the top-right corner of each quadrant in the diagram) — **keep this legend in the final output:**

| Label | Description |
|---|---|
| **None** | No testing activities in this quadrant |
| **Low** | Testing exists but is ad-hoc and not consistently practised |
| **Medium** | Activities are defined and repeatable; partial coverage |
| **High** | Activities are well-established, measured, and continuously improved |

#### Strengths
- [Strength 1]
- [Strength 2]
- [Strength 3]

#### Gaps

> Reference §7 finding IDs where applicable.

- [Gap 1]
- [Gap 2]
- [Gap 3]

### Ambition

**High value now:**
- [Improvement 1]
- [Improvement 2]
- [Improvement 3]

**Longer term:**
- [Improvement 4]
- [Improvement 5]
- [Improvement 6]

### AI

- [Where could AI assist in testing across the quadrants?]

---

## 6. Test Pyramid Assessment

### As Is

> **Template placeholder** — replace with a project-specific pyramid diagram before publishing.
> 1. Copy `test-pyramid.drawio` from `.github/quality-queen/input-data/diagrams/` to `test-pyramid-[ProjectName].drawio` in `.github/quality-queen/output-data/diagrams/`.
> 2. Open in draw.io and fill in each layer: counts, status text, and colour (red `#f8cecc`/`#b85450`, amber `#fff2cc`/`#d6b656`, green `#d5e8d4`/`#82b366`).
> 3. **Reposition segments to reflect actual test distribution** — do NOT alter any shape's style, width, height, or x coordinate. Only the `y` coordinate may be changed to move a segment up or down:
>    - The template stacking is: triangle (E2E, `y=80`) → mid trapezoid (API, `y=160`) → wide trapezoid (Unit, `y=240`). Each layer is 80px tall, so adjacent shapes must stay flush: each shape's `y` equals the shape above it's `y + 80`.
>    - To reflect the actual distribution, assign the **triangle** (the smallest shape) to whichever layer has the fewest tests, the **mid trapezoid** to the middle count, and the **wide trapezoid** to the layer with the most tests. For example: if API tests are the scarcest, move the triangle to `y=160`; if unit tests are the scarcest (inverted pyramid), move the triangle to `y=240`. Adjust the other two shapes' `y` values accordingly, keeping all layers flush.
>    - Never change `width`, `x`, `height`, `size`, or any style property — only `y`.
> 4. In the generated output file, update the image reference below to `./diagrams/test-pyramid-[ProjectName].svg`.
> 5. Export the `.drawio` file to SVG (see README — Step 3).

![Test Pyramid — [ProjectName]](./diagrams/test-pyramid.svg)

**Current pyramid shape:** [Describe the shape and what it means for the team — e.g. over-reliant on UI tests, missing API test layer, etc.]

**Major imbalances:**
- [Imbalance 1]
- [Imbalance 2]
- [Imbalance 3]

**Estimated coverage:**
- [Frontend / layer 1]: [estimated coverage and what is covered]
- [Backend / layer 2]: [estimated coverage and what is covered]

**Manual testing:**
- **Test management tool:** [e.g. Azure Test Plans, TestRail, Zephyr Scale, Xray, spreadsheet, none]
- **Manual test case count:** [n or "unknown"]
- **Execution cadence:** [e.g. every sprint, before release, ad-hoc]
- **Relationship to automated tests:** [e.g. manual tests cover gaps not yet automated, overlap exists, fully separate]
- **Observations:** [Are manual test cases maintained, stale, traceable to requirements? Is there a plan to automate any of them?]

### Ambition

**High value now:**
1. [Improvement 1]
2. [Improvement 2]
3. [Improvement 3]

**Longer term:**
4. [Improvement 4]
5. [Improvement 5]
6. [Improvement 6]

**Authentication / environment challenges:** [Note any known blockers for automated testing, e.g. auth, test data, environment stability.]

### AI

- [Where could AI assist in test pyramid improvements?]

---

## 7. Findings and Actions

### Critical Findings

> **Critical** — Blocks release safety, hides defects, or creates an active production risk. Must be addressed before the next release or as an immediate priority.

| # | Finding | Risk | Related Board Item |
|---|---|---|---|
| C1 | [Finding] | [Risk] | [Link or —] |
| C2 | [Finding] | [Risk] | [Link or —] |
| C3 | [Finding] | [Risk] | [Link or —] |

### High

> **High** — Slows delivery, erodes confidence, or represents an unaddressed quality, security, or compliance risk. Does not block releases today but increases the likelihood of future incidents. Address within the current quarter.

| # | Finding | Risk | Related Board Item |
|---|---|---|---|
| H1 | [Finding] | [Risk] | [Link or —] |
| H2 | [Finding] | [Risk] | [Link or —] |
| H3 | [Finding] | [Risk] | [Link or —] |

### Medium

> **Medium** — Reduces quality visibility or increases maintenance cost. Worth scheduling but not urgent.

| # | Finding | Risk | Related Board Item |
|---|---|---|---|
| M1 | [Finding] | [Risk] | [Link or —] |
| M2 | [Finding] | [Risk] | [Link or —] |
| M3 | [Finding] | [Risk] | [Link or —] |

### Low

> **Low** — Minor friction, inconsistency, or technical debt. Often a quick win; pick up alongside other work.

| # | Finding | Risk | Related Board Item |
|---|---|---|---|
| L1 | [Finding] | [Risk] | [Link or —] |
| L2 | [Finding] | [Risk] | [Link or —] |
| L3 | [Finding] | [Risk] | [Link or —] |

---

### Actions QA Can Take Directly

| Action | Linked finding | Rationale | Expected impact | Owner | Timeframe | Effort |
|---|---|---|---|---|---|---|
| [Action] | [C1 / H2 / M3 / etc.] | [Why] | [Measurable outcome] | [QA / name] | [When] | S / M / L |
| [Action] | [C1 / H2 / M3 / etc.] | [Why] | [Measurable outcome] | [QA / name] | [When] | S / M / L |
| [Action] | [C1 / H2 / M3 / etc.] | [Why] | [Measurable outcome] | [QA / name] | [When] | S / M / L |

### Actions to Propose to the Team

| Action | Linked finding | Rationale | Expected impact | Owner | Timeframe | Effort |
|---|---|---|---|---|---|---|
| [Action] | [C1 / H2 / M3 / etc.] | [Why] | [Measurable outcome] | [Team / role] | [When] | S / M / L |
| [Action] | [C1 / H2 / M3 / etc.] | [Why] | [Measurable outcome] | [Team / role] | [When] | S / M / L |
| [Action] | [C1 / H2 / M3 / etc.] | [Why] | [Measurable outcome] | [Team / role] | [When] | S / M / L |

### Actions Requiring Leadership / PO / Technical Owner Alignment

| Action | Linked finding | Rationale | Expected impact | Owner | Timeframe | Effort |
|---|---|---|---|---|---|---|
| [Action] | [C1 / H2 / M3 / etc.] | [Why] | [Measurable outcome] | [PO / Tech lead] | [When] | S / M / L |
| [Action] | [C1 / H2 / M3 / etc.] | [Why] | [Measurable outcome] | [PO / Tech lead] | [When] | S / M / L |
| [Action] | [C1 / H2 / M3 / etc.] | [Why] | [Measurable outcome] | [PO / Tech lead] | [When] | S / M / L |

---

## 8. Presentation Summary

### Current Status

> Summarize §1 maturity ratings in stakeholder language — do not restate observations from §3–§6.

[2–4 sentences summarising where the team is today on quality. Highlight both strengths and gaps. Keep it factual and stakeholder-readable.]

### Why the Proposed Changes Matter

[Explain the consequences of not acting. Frame the risks in business or delivery terms, not only technical ones.]

### What Value QA Work Will Create

- [Value 1 — e.g. reduced risk of production incidents]
- [Value 2 — e.g. faster onboarding]
- [Value 3 — e.g. measurable test coverage]
- [Value 4 — e.g. better stakeholder communication]
- [Value 5 — e.g. time savings from earlier defect detection]

**Collaborative next step:** [Describe how to present this to the team and invite them to co-own the Ambition sections and actions.]

---

## 9. Follow-up and Measurement

### Suggested Metrics

| Metric | Baseline (Current) | Target (6 months) |
|---|---|---|
| Frontend test coverage | [Baseline] | [Target] |
| Backend test coverage | [Baseline] | [Target] |
| E2E test count | [Baseline] | [Target] |
| API test count | [Baseline] | [Target] |
| Escaped defects (post-release bugs) | [Baseline] | [Target] |
| Build stability (CI pass rate) | [Baseline] | [Target] |
| Lead time (ready → done) | [Baseline] | [Target] |
| Deployment frequency | [Baseline] | [Target] |
| Backlog readiness quality | [Baseline] | [Target] |
| Flaky test rate | [Baseline] | [Target] |

### Review Cadence

- **Weekly:** [What to check weekly]
- **Per sprint / bi-weekly:** [What to review each iteration]
- **Monthly:** [What to review monthly]
- **Quarterly:** [Full strategy review scope]

### Action Tracking

- [How actions will be tracked — e.g. GitHub Issues, Jira, Azure DevOps, team board]
- [Label or tag convention for QA improvement items]
- [How progress will be reviewed — e.g. retrospectives, syncs]

### Documenting Learnings

- [Where learnings are recorded — e.g. this document, wiki, retrospective notes]
- [How improvements are shared with the broader team]

---

## 10. Open Questions for the Team

To convert assumptions in this document into verified observations, the following should be confirmed with the team. These questions must be **project-specific** — generated based on gaps, assumptions, and unknowns identified during analysis. Do not repeat information already available in the project files.

Use `.github/quality-queen/input-data/qa-insight-questions.md` as a reference for question categories, but tailor every question to what is actually unknown or unverified for this project.

### Work Processes

- [Question about a specific unverified assumption from section 3]
- [Question about a specific gap in process understanding]

### Build Processes

- [Question about a specific unverified assumption from section 4]
- [Question about a specific gap in pipeline/environment understanding]

### Testing & Quality

- [Question about test ownership, coverage gaps, or tooling unknowns]
- [Question about authentication, test data, or environment blockers]

### Delivery & Stakeholders

- [Question about release cadence, PO involvement, or customer sign-off]
- [Question about compliance, security, or regulatory requirements]

### Team & Capacity

- [Question about QA capacity, handover plans, or role expectations]
- [Question about team dynamics, decision-making, or improvement appetite]

---

*This strategy is a living document. It should be reviewed and updated regularly as the team's practices evolve. The team should collaboratively fill in and refine the Ambition sections to ensure shared ownership of quality.*
