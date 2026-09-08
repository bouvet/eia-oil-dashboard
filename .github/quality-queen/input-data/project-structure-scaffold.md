# Project Structure — [Project Name]

> Purpose: Quick-reference for QA strategy analysis. Covers project overview, repo structure, test inventory, CI/CD, and known gaps.

> **Data accuracy rule:** All file counts and test counts must be EXACT numbers. Never use approximations ("100+", "~50", "several", "many"). Count the actual files or tests and report the precise number. Every count must be verifiable against the actual files in the repository.

## Project Root

| Field | Value |
|---|---|
| **Project root** | `[absolute or workspace-relative path to the project root, e.g. `c:\Git\MyProject` or `.`]` |
| **Path convention** | All paths in this document are relative to **Project root** above, unless explicitly absolute. |

> To re-target this template at a different repository or sub-folder, change only the **Project root** value above. All other path references (test folders, workflow files, etc.) should be expressed relative to it so the document remains portable.

---

## 1. Project Overview

| Field | Value |
|---|---|
| Name | [Project name] |
| Description | [Short description of what the product does and who uses it] |
| Product Owner | [Name] |
| Active team (GitHub/other) | [GitHub handles or names, with roles where known, e.g. Name (QA), Name (Backend)] |
| Repo | [URL and visibility, e.g. https://github.com/org/repo (private)] |
| Project board | [URL and board number/ID] |
| Communication | [Slack channel, Teams channel, or other] |
| Production URL | [https://...] |

---

## 2. Tech Stack

### Backend
| Item | Detail |
|---|---|
| Framework | [e.g. .NET 10 / Node.js / Python / Java] |
| Runtime | [e.g. Azure Container Apps, AWS Lambda, on-prem] |
| Storage | [e.g. Azure Table Storage, PostgreSQL, Redis] |
| Identity / Auth | [e.g. Azure AD / MSAL / OAuth2 / JWT] |
| Config / Secrets | [e.g. Azure Key Vault, env variables, Vault] |
| API docs | [e.g. Swagger, OpenAPI, GraphQL schema] |
| Deprecated components | [Any legacy code still in repo; note if still referenced by tests] |
| Shared libraries | [Any cross-project shared code] |

### Frontend
| Item | Detail |
|---|---|
| Framework | [e.g. React 18, Angular, Vue, Blazor] |
| State management | [e.g. Redux Toolkit, MobX, Zustand, none] |
| UI library | [e.g. MUI, Ant Design, Tailwind] |
| Auth | [e.g. MSAL, Auth0, custom] |
| i18n | [e.g. i18next, none] |
| Routing | [e.g. react-router-dom v6] |
| Build / serve | [e.g. Vite, Webpack, Azure Web App, S3] |
| Language | [e.g. TypeScript / JavaScript; note any pending migration] |

### Other
| Item | Detail |
|---|---|
| [Mobile / desktop / BFF / etc.] | [Details if applicable] |

---

## 3. Repository Structure (QA-relevant)

> Generate this section on a per-project basis by analysing the actual repository. Annotate each folder with its QA relevance (tested/untested, active/stale, mock infrastructure, etc.).

---

## 4. Backend Test Inventory (`[path to test project]`)

> Generate this section on a per-project basis.

**Framework:** [test framework + mocking library]  
**Target runtime:** [runtime and version]  
**Run command:** [command and working directory]

### Active Tests

| File | Class | Tests | What is tested |
|---|---|---|---|
| `[path/TestFile]` | `[ClassName]` | [n] | [Scenarios covered] |

**Total active backend tests: [n]**

### Stale / Commented-Out / Skipped Tests

| File | Notes |
|---|---|
| `[path/StaleTest]` | [Reason] |

**Note:** [Describe structural gaps — e.g. which layers or controllers have no tests, deprecated code still referenced.]

### Mock / Test Infrastructure
- [Key mock classes or helpers and what they substitute]

---

## 5. Frontend Test Inventory (`[path to frontend]`)

> Generate this section on a per-project basis.

**Framework:** [test framework + assertion library]  
**Environment:** [test environment]  
**Run command:** [command and working directory]

### Test File Summary by Category

| Category | Files | Test cases | Pattern |
|---|---|---|---|
| **[Category]** | [n] files | [n] | [Test pattern] |

**Total test files: [n]. Total test cases: [n].**

### Snapshot Files
[Note location and stale snapshot risk if applicable.]

### Untested Frontend Areas

> Cover **every** directory under `src/` — including `models/`, `constants/`, `styles/`, `assets/`, and any other subdirectory. Add a row even when risk is Low; do not silently omit directories.

| Area | Path | Risk |
|---|---|---|
| [Area] | `[path]` | [High / Medium / Low — reason] |

### Test Helpers
- [Shared test utilities, provider wrappers, fixture factories, auth mocks and what they do]

---

## 6. E2E Test Inventory (`[path to e2e folder]`)

> Generate this section on a per-project basis.

| File | Test(s) | Assertions |
|---|---|---|
| `[path/test.cy.js]` | [Test description] | [What is asserted, or "None"] |

**Total E2E tests: [n]. [Note authentication coverage, user journey coverage, and missing flows.]**

- `[support/commands file]` — [empty / custom commands defined]
- `[config file]` — [baseUrl, structurePattern, auth strategy, env config status]
- [Note any E2E authentication blockers]

---

## 6b. Manual Testing and Test Management

> Generate this section on a per-project basis. If the team has no manual test suites or test management tool, state that explicitly.

| Field | Value |
|---|---|
| Test management tool | [e.g. Azure Test Plans, TestRail, Zephyr Scale, Xray, spreadsheet, none] |
| Manual test suite location | [URL, path, or "not centralized"] |
| Approximate test case count | [n or "unknown"] |
| Ownership | [Role or person responsible for maintaining manual test cases] |
| Execution cadence | [e.g. every sprint, before release, ad-hoc, regression cycle] |
| Last known execution | [Date or "unknown"] |
| Coverage focus | [e.g. smoke tests, regression, UAT, accessibility, specific user flows] |
| Relationship to automated tests | [e.g. manual tests cover gaps not yet automated, duplicates exist, fully separate] |

**Observations:** [Note strengths and gaps — e.g. test cases are up to date vs. stale, traceability to requirements, pass/fail history tracked or not.]

---

## 7. CI/CD Pipelines (`[path to workflows]`)

> Generate this section on a per-project basis.

### CI Workflows (run on PR / branch push)

| File | Trigger | Steps | Issues / Gaps |
|---|---|---|---|
| `[ci-file]` | [Trigger and path filter] | [Step 1 → Step 2 → Step 3] | [Issues or gaps] |

### Deploy Workflows

| File | Trigger | Target | Notes |
|---|---|---|---|
| `[deploy-file]` | [Trigger] | [Environment(s) and order] | [Automated or gated; build steps] |

**Key gaps:**
- [Gap 1]
- [Gap 2]

---

## 8. Key Issues / Work Items (QA-Relevant)

> Generate this section on a per-project basis from board exports or issue tracker.

### In Progress / Ready for Work
| Issue / Item | Title | Status | Owner |
|---|---|---|---|
| [#n](link) | [Title] | [Status] | [Owner — from assignees field; use `—` only if truly unassigned] |

### Known Bugs (open, by severity)
| Issue / Item | Title | Labels | Owner |
|---|---|---|---|
| [#n](link) | [Title] | [Bug, Top priority, etc.] | [Owner or `—`] |

### Security & Non-Functional (Backlog / unscheduled)
| Issue / Item | Title |
|---|---|
| [#n](link) | [Title — note if previously completed but no longer visible in CI] |

### Process / QA Infrastructure
| Issue / Item | Title | Status |
|---|---|---|
| [#n](link) | [Title] | [Status] |

### Open Pull Requests (team-authored)

> List all open, non-Dependabot PRs with review status and age.

| PR | Title | Review status | Created |
|---|---|---|---|
| [#n](link) | [Title] | [APPROVED / REVIEW_REQUIRED / CHANGES_REQUESTED] | [Date] |

### Dependabot PRs

> Record total count and oldest creation date. Any count > 0 with oldest PR older than 4 weeks is a **High** gap.

**Open Dependabot PRs:** [n]  
**Oldest PR:** [date or "n/a"]

---

## 9. Board Structure

**Board access status:** [accessible / inaccessible / no-board-detected / unknown - include the exact reason when not accessible]

**Columns / workflow states:**
```
[Column 1] → [Column 2] → [Column 3] → [Column 4] → [Column 5] → [Column 6]
                                                                ↑
                                                    [parallel state if any]
```

**Fields in use:** [e.g. Priority (P1/P2), Size (S/M/L/XL), Sprint, Estimate] — *note if consistently applied or not*

**Labels / tags in use:** [Full list from `gh label list` if available, otherwise from live issue data. Format: `Label1`, `Label2`, ...]

**DoR/DoD status:** [Documented / Informal / Not defined / Not verifiable - use Not verifiable when board access is unavailable, and include the reason]

### Work Methodology
 
> Determine the team's actual work methodology from evidence — never assume Scrum or any specific framework without proof. Check these signals in order:
 
| Signal | Where to check | What it indicates |
|---|---|---|
| Sprint / Iteration field on board | Board fields (`gh project field-list`) | Scrum or timeboxed iterations |
| Milestone with date ranges | `gh api repos/{owner}/{repo}/milestones` | Timeboxed planning |
| Sprint-related labels | Label list | Sprint-aware workflow |
| README / CONTRIBUTING mentions | Repository docs | Explicitly stated methodology |
| Continuous-flow columns without iteration boundaries | Board columns | Kanban / flow-based |
| No sprint/iteration/milestone evidence | Absence of above | Default: "flow-based (Kanban-like)" |
 
**Observed methodology:** [Scrum / Kanban / Scrumban / SAFe / Flow-based / Unknown — state evidence]  
**Evidence:** [List the concrete signals found or not found, e.g. "No Sprint field on board, no Milestone with dates, continuous-flow columns observed"]  
**Confidence:** [High — explicitly documented / Medium — inferred from strong signals / Low — assumption, needs team confirmation]

---

## 10. Issue Templates (`[path to ISSUE_TEMPLATE/]`)

> Generate this section on a per-project basis.

| Template | Type | Required fields | QA-relevant gaps |
|---|---|---|---|
| `[template.yml]` | [Epic / Feature / Story / Task / Bug / Spike / Chore] | [Field 1, Field 2] | [Missing severity, no AC field, legacy duplicate, etc.] |

**Observations:** [Note strengths (e.g. Given/When/Then AC) and gaps (e.g. no Severity field, legacy .md templates still present, optional fields that should be required).]

---

## 11. Known QA Gaps

> Synthesize all gaps found above. Every row must reference a concrete location. Include missing DoR/DoD as **Critical** only when the board was successfully inspected; when board access is unavailable, record the limitation and use **Not verifiable** instead.

| Severity | Gap | Location |
|---|---|---|
| **Critical** | [One-sentence problem statement] | [File path / workflow name / board column / issue #] |
| **High** | [One-sentence problem statement] | [Location] |
| **Medium** | [One-sentence problem statement] | [Location] |
| **Low** | [One-sentence problem statement] | [Location] |

---

## 12. GitHub & Process Signals

> Summarize delivery health signals from live gh data. [verified YYYY-MM-DD]

**Issue tracker signals:**
- [Open issue count, open bug count, top-priority bugs]
- [QA / security ownership — single point of failure?]
- [% of issues predating structured templates — mixed quality?]

**PR signals:**
- [Approved but unmerged PRs — merge queue gap?]
- [Long-lived open PRs with no review SLA]
- [Dependabot review cadence — are security updates being actioned?]

**Delivery signals:**
- [Recent CI workflow run status — any persistent failures?]
- [Last backend / frontend CI run date]
- [Architectural changes in flight with no visible test coverage plan]