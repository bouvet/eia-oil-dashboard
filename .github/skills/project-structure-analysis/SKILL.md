---
name: project-structure-analysis
description: "Analyze a software project's repository, GitHub issues, issue templates, CI/CD pipelines, and board structure to produce a verified Project Structure document. Use when generating a QA strategy, onboarding to a new project, or auditing test coverage and quality gates. Triggers: project structure, repo analysis, test inventory, CI/CD audit, board structure, GitHub issues, QA gaps."
argument-hint: "Provide the project name and project root path (absolute or `.` for workspace root)."
---

# Project Structure Analysis

Produces a complete, verified Project Structure document by systematically exploring the repository, GitHub data, and CI/CD configuration. The output is the primary input for QA strategy generation.

## When to Use

- Before generating a QA strategy (prerequisite step)
- When onboarding as QA on an existing project
- When auditing the current state of test coverage or CI/CD quality gates
- When the existing Project Structure document is stale and needs regeneration

## Output

Save to: `.github/quality-queen/output-data/project-structure-<projectName>.md`  
Template: `.github/quality-queen/input-data/project-structure-scaffold.md`

All paths in the output must be **relative to the project root** so the document is portable.

---

## Step 1 — Establish the Project Root

- Accept the project root from the caller (absolute path or `.` for workspace root).
- If `.` or empty, resolve to the current workspace root.
- Record this as the **Project root** field at the top of the output document.
- All subsequent path references must be relative to this root.

---

## Step 2 — Identify Board Source and Extract Board Data

Determine which board tool the project uses, then call the appropriate extraction skill when the board source is known. Board discovery and board access are separate outcomes; never treat an access failure as evidence that no board exists.

### Board access outcomes

Record one of these outcomes in the structured summary and in §9 of the output:

- **accessible** — the board query succeeded and columns, fields, and items may be reported as verified.
- **inaccessible** — a board platform was identified, but authentication, permission, scope, network, or API errors prevented inspection. Record the exact reason, do not invent columns or fields, and continue the repository, issue, PR, and CI analysis using the available fallback data.
- **no-board-detected** — board discovery completed successfully and no board was found, or the caller explicitly confirms that no board is used. Do not use this status when access was denied.
- **unknown** — the platform cannot be identified from repository evidence or caller input; ask the caller before making board claims.

### Detect the board source

Before checking environment variables or config files, read `.github/quality-queen/input-data/project-secrets.env` (if it exists) and load any non-empty values as inputs for board detection and authentication.

Apply these signals in order — stop at the first match:

1. **Explicit caller input** — honor GitHub, Jira, Azure DevOps, or None before repository heuristics. For None, record `no-board-detected` and skip extraction.
2. **Jira** — a `JIRA_BASE_URL` input or environment variable, or a Jira URL (`.atlassian.net`) in README or CI config.
3. **Azure DevOps** — an `ADO_ORG_URL` input or environment variable, or an Azure DevOps URL (`dev.azure.com` or `visualstudio.com`) in README or CI config.
4. **GitHub Issues** — `.github/` exists and no Jira or Azure DevOps signal is present.
5. **Unknown** — ask the caller before making board claims; record `unknown` if the platform remains unidentified.

### Multiple boards

Some teams track work on more than one platform simultaneously (e.g. a GitHub project board for dev issues and a Jira board for PM-level backlog). If the caller provides an `additionalBoards` list, or if detection signals point to more than one platform, treat each platform as a separate board:

- Call the extraction skill for each board in turn.
- Store each board's structured summary with a label (e.g. `Board 1: GitHub`, `Board 2: Jira`).
- In Step 6, write each board's data into a separate sub-section under §9 (Board Structure), labeled by platform and URL.
- Add a **Cross-board observations** note at the end of §9 summarizing: whether work items flow between boards, whether DoR/DoD is defined consistently, and any gaps in coverage between boards.

### Call the appropriate extraction skill

| Board source | Skill to invoke |
|---|---|
| GitHub Issues | `board-extraction-github` |
| Jira | `board-extraction-jira` |
| Azure DevOps | `board-extraction-azdo` |

Store the structured summary returned by the skill. It will be used in Step 6.

Record the board source, `board-access-status`, access reason, and data source (e.g. `gh-cli`, `jira-api`, `static-export`) as observation notes in the output document. If access is **inaccessible**, label board columns, fields, item status, and DoR/DoD as **not verifiable** rather than **not defined**. Continue the run with repository-only evidence and any accessible issue, PR, or static-export data.

### Multiple repositories

If the caller provides additional repository roots (via `additionalRepos`):

- Treat each additional root as a named component. Derive the component label from the folder name of each path.
- Apply Steps 3–5 to each component's root. Scope file counts, test counts, and CI/CD findings to that component.
- Collect all components' findings into the **single** output file. Use sub-headings within §2 (Repository Layout), §4 (Test Inventory), and §5 (CI/CD Pipelines) to clearly separate per-component data.
- At the end of §11 (Known QA Gaps), add a `Cross-repo observations` row for any gaps that span components (e.g. no shared integration test, divergent CI tooling, inconsistent dependency management).

---

## Step 3 — Explore the Repository Structure

Use workspace file tools (`list_dir`, `file_search`, `read_file`) — **not terminal commands** like `Get-ChildItem`, `find`, or `ls`.

Explore and annotate:

1. **Top-level layout** — identify monorepo vs. single-project; locate backend, frontend, infra, scripts, test projects.
2. **Backend** — solution/project files, framework config, Dockerfile(s), shared libraries, deprecated code.
3. **Frontend** — `package.json` (dependencies, scripts, devDependencies), build config, asset folders.
4. **Test projects** — locate all test folders; read framework config files (`jest.config.*`, `*.csproj`, `pytest.ini`, `vitest.config.*`, `cypress.config.*`, etc.).
5. **CI/CD** — read every file in `.github/workflows/` (or equivalent). Record trigger, steps, and gaps for each.
6. **Configuration and secrets** — `appsettings.json`, `.env.example`, Key Vault references, environment variable usage.
7. **Issue templates** — read all files in `.github/ISSUE_TEMPLATE/`. Note required fields and what they reveal about workflow expectations.
8. **Work methodology** — determine the team's methodology from evidence, not assumptions. Check: (a) board fields for Sprint/Iteration, (b) milestones with date ranges, (c) sprint-related labels, (d) README/CONTRIBUTING for explicit methodology statements. If continuous-flow columns exist without iteration boundaries, record as "flow-based (Kanban-like)". Never default to "Scrum" without concrete evidence. Record findings in the §9 "Work Methodology" subsection with confidence level.
9. **Manual testing and test management** — look for references to test management tools (e.g. Azure Test Plans, TestRail, Zephyr Scale, Xray) in README, docs, CI config, or board issues. Check for manual test case files (spreadsheets, markdown checklists, wiki links). Ask the caller if no evidence is found. Record findings in §6b of the output document.

For each folder annotate QA relevance: tested / untested / active / stale / mock infrastructure.

---

## Step 4 — Inventory All Tests

Apply the classification rules in [test-classification.md](./references/test-classification.md) to every test file found.

### Counting rules

- **All counts must be EXACT integers.** Never write "~50", "100+", "several", or "many".
- Count `[Fact]`, `[Theory]`, `it(`, `test(`, `describe(` blocks and similar test declarations — not test files alone.
- For `[Theory]` / `@pytest.mark.parametrize` / `.each` — count each data row as one test case.
- Record commented-out or skipped tests separately in a **Stale** table.

### Per test layer, capture

| Field | What to record |
|---|---|
| Framework | Test framework + assertion/mocking libraries |
| Run command | Exact command and working directory |
| File count | Exact number of test files |
| Test case count | Exact number of test cases (not files) |
| Coverage | Reported % if available; otherwise "not configured" |
| Gaps | Which layers, controllers, services, or pages have zero test files |

---

## Step 5 — Inventory CI/CD Pipelines

For every workflow file:

| Field | What to record |
|---|---|
| Trigger | Event + branch/path filter |
| Steps | Ordered list of what the workflow does |
| Quality gates | Lint, format, test, coverage threshold, security scan — and whether failures are enforced or suppressed |
| Gaps | Missing gates, suppressed failures (`|| true`), no approval between environments |

Flag critical gaps explicitly:
- Lint/format failures silently suppressed
- No test coverage collection or threshold
- No manual approval gate between staging and production
- No smoke test or health check post-deploy

### PR Check Suites (GitHub only)

If the board source is GitHub, the PR check suite table and branch protection summary are produced by `board-extraction-github` (Step 2). Carry those findings forward into the gap table (Step 8) — do not re-query them here.

---

## Step 6 — Record Board Data

Use the structured summary produced by the board extraction skill in Step 2. Do not re-query the board source here.

Record in the output document:

### Board Structure
- Board access status and reason (`accessible`, `inaccessible`, `no-board-detected`, or `unknown`)
- Column names and flow order (from `board-columns` field) only when access is verified
- Custom fields in use and consistency (from `custom-fields` field) only when access is verified
- Labels in use
- DoR/DoD status: Documented / Informal / Not defined only after successful inspection; otherwise Not verifiable with the access reason

### Issues
- In Progress / Ready for Work (from `issues-in-progress`)
- Security & Non-Functional (from `issues-security-nfr`)
- Process / QA Infrastructure (from `issues-process-qa`)

### PR Check Suites (GitHub only)
Copy the check suite table from the `board-extraction-github` summary (`pr-check-suites` field). If board source is Jira, omit this sub-section.

---

## Step 7 — Read Issue Templates

Read every file under `.github/ISSUE_TEMPLATE/` (and root-level `ISSUE_TEMPLATE.md` if present).

For each template record:
- Template name and type (bug report, feature request, etc.)
- Required fields
- What the fields reveal about expected workflow (e.g. does the bug template require steps to reproduce, environment, expected vs. actual?)
- Gaps: missing fields that would aid QA (e.g. no severity, no reproduction steps, no acceptance criteria)

---

## Step 8 — Compile Known QA Gaps

Synthesize a gap table from all observations above. Assign severity using these criteria:

| Severity | Meaning |
|---|---|
| **Critical** | Blocks release safety, hides defects, or creates production risk |
| **High** | Slows delivery, erodes confidence, or represents unaddressed security/compliance risk |
| **Medium** | Reduces quality visibility or increases maintenance cost |
| **Low** | Minor friction, technical debt, or inconsistency |

Each gap must reference a concrete location (file path, workflow name, board column, issue number).

---

## Step 9 — Write the Output Document

1. Open `.github/quality-queen/input-data/project-structure-scaffold.md` — use it as the exact structural template.
2. Fill every section with verified facts from the steps above.
3. Mark each data point as either **[verified]** (directly observed) or **[assumed]** (inferred).
4. Save to `.github/quality-queen/output-data/project-structure-<projectName>.md`.

**Do not invent sections.** Do not add top-level headings not in the scaffold.  
**Do not use approximations.** Every number must be exact.

---

## Quality Checklist

Before saving, verify:

- [ ] All test counts are exact integers
- [ ] Every CI/CD workflow file is accounted for
- [ ] Every gap has a concrete location reference
- [ ] Issue template fields are documented
- [ ] Board access status and reason are recorded; if accessible, the column flow is recorded, and if inaccessible or absent, the distinction is explicit
- [ ] Data source (gh CLI / static export) is noted
- [ ] All paths are relative to the project root
- [ ] No placeholder text from the scaffold remains in the output






