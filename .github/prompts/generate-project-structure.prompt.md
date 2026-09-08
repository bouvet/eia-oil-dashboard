---
agent: Quality Queen
description: Analyze a project's file structure, tech stack, tests, CI/CD, and environments, then produce a project-structure-<name>.md from the scaffold template.
---

# Generate Project Structure for `${input:projectName:Enter the project name}`

You are acting as a technical analyst. Your goal is to produce a **complete, verified Project Structure document** for the project named `${input:projectName}` by exploring its codebase and filling in the scaffold template.

> **Skill:** Apply the `project-structure-analysis` skill throughout this prompt. It defines the step-by-step procedure, test classification rules, and gap severity criteria used to produce this document. Based on the board platform input below, the skill will invoke `board-extraction-github`, `board-extraction-azdo`, or `board-extraction-jira` — no separate invocation is needed.

## Inputs and Locations

- **Project root** to analyze: `${input:projectRoot:Enter the project root path to analyze (absolute path or `.` for the current workspace root)}`
  - Treat this as the base for **all** path references.
  - If the value is `.` or empty, use the current workspace root.
  - If it points outside the current workspace, use absolute paths and read-only tools.
- **Board platform:** `${input:boardPlatform:Which board platform does the team use? (GitHub / Azure DevOps / Jira / None / Unknown)}`
  - This determines which board-extraction skill is invoked and how §9 Board Structure is populated. Choose `None` to skip board extraction or `Unknown` when the platform cannot be identified.
- **Board URL** *(optional)*: `${input:boardUrl:Enter a verified board URL, or leave blank when unavailable or unused}`
  - Record the URL only when supplied and verified. If access is unavailable, record `not accessible` and the reason; do not infer that no board exists.
- **Board access** *(optional)*: `${input:boardAccess:Choose accessible, inaccessible, no-board-detected, or unknown; leave blank to detect}`
  - Treat `inaccessible` and `no-board-detected` as different outcomes. Continue the analysis when access is unavailable.
- **Additional repositories** *(optional)*: `${input:additionalRepos:Comma-separated list of additional repo root paths to include (e.g. C:\Git\MyApp\frontend,C:\Git\MyApp\infra — leave blank for single repo)}`
  - If provided, each additional root is analyzed and documented as a separate component sub-section under §2 (Repository Layout) in the **same** output file. Use the folder name of each root as the component label.
- **Additional boards** *(optional)*: `${input:additionalBoards:Comma-separated additional boards in format Platform|URL (e.g. Jira|https://company.atlassian.net — leave blank for single board)}`
  - If provided, each additional board is extracted using the matching skill and appended to §9 (Board Structure) under its own sub-section labeled by platform. The primary board appears first.
- **Test management tool** *(optional)*: `${input:testManagementTool:Test management tool and URL if the team uses one (e.g. TestRail|https://company.testrail.io or Azure Test Plans — leave blank if none or unknown)}`
  - If provided, record in §6b (Manual Testing and Test Management). If blank, the skill will look for evidence in the repo and ask the caller if none is found.
- Project structure scaffold (template): `.github/quality-queen/input-data/project-structure-scaffold.md`
- Project structure output: `.github/quality-queen/output-data/project-structure-${input:projectName}.md`

## Instructions

1. Explore the structure of the **Project root** above (folders, key config files, solution/project files, frontend/backend layout, test projects, CI/CD pipelines, infra, scripts). Do not analyze unrelated folders outside the project root.
2. Open `project-structure-scaffold.md` and use it as the **exact template** for the output.
3. In the generated `project-structure-${input:projectName}.md`, set the **Project root** field at the top to the value provided above. Express every path elsewhere in the document as **relative to that project root** so the spec stays portable.
4. Fill every section of the scaffold with verified facts from the project:
   - **§1 Project Overview:** Populate every row — Product Owner, Active team (GitHub handles + roles), Repo URL, Project board URL, communication channel, production URL. Record the **Board URL** only when it is a verified URL; otherwise use `Not available` and record board access status separately. Use the **Board platform** input for the board type. Source remaining fields from README, CODEOWNERS, package.json, or issue/PR author patterns. Do not leave any row as `[Name]` or `[URL]` placeholder.
   - Tech stack and frameworks
   - Repository layout
   - Test inventory (unit, API, component, E2E, performance, security, accessibility)
   - CI/CD pipelines and quality gates
   - Environments and test data
   - Known QA gaps observed in the code or tooling
   - **§9 Board Structure:** board access status and reason; columns/workflow states, fields in use, full label list, and **DoR/DoD status** only when the board was successfully inspected. Use **Not verifiable** for inaccessible board data.
   - Open PRs (team-authored and Dependabot) in §8
   - Issue templates in §10
   - GitHub & Process Signals in §12
5. Clearly mark **assumptions** vs **verified observations**.
6. **DoR/DoD enforcement:** If the board was successfully inspected and DoR/DoD is not formally documented in board column settings or a linked document, add it to the Known QA Gaps table (§11) as a **Critical** gap with location `Board / process`. If board access is unavailable, record the access limitation and mark DoR/DoD as **Not verifiable**; do not claim that DoR/DoD is absent.
7. Save the result to `.github/quality-queen/output-data/project-structure-${input:projectName}.md` (overwrite if it exists, but preserve the scaffold's section structure).

### Multi-repository analysis

If `additionalRepos` is not blank, parse the comma-separated list of paths. For each additional repo:

1. Explore its structure using the same rules as for the primary project root (folders, config files, test projects, CI/CD, scripts).
2. Add a dedicated sub-section under **§2 Repository Layout** in the output file, headed by the folder name of that repo (e.g. `#### Component: frontend`). Do not create a separate output file per repo — all components are documented in the single `project-structure-${input:projectName}.md`.
3. Extend the **§4 Test Inventory** and **§5 CI/CD Pipelines** tables to include rows for each component, adding a `Component` column if more than one repo is covered.
4. Include a short **Cross-repo observations** note at the end of **§11 Known QA Gaps**, flagging any inconsistencies across components (e.g. different test frameworks, one component with no CI, divergent dependency versions).

### Multi-board analysis

If `additionalBoards` is not blank, parse the comma-separated list of `Platform|URL` entries. For each additional board:

1. Determine the platform from the entry prefix (`GitHub`, `Azure DevOps`, or `Jira`).
2. Call the corresponding board-extraction skill using the URL from the entry.
3. Append the results to **§9 Board Structure** under a clearly labeled sub-section, e.g. `#### Board 2: Jira (https://company.atlassian.net)`. The primary board remains the first sub-section.
4. After all boards are recorded, add a **Cross-board observations** note summarizing: whether work flows across boards (e.g. PM backlog in Jira, dev tasks in GitHub), any duplicated work item types, and whether DoR/DoD is defined consistently across boards.

## Exploration Rules

- Use workspace search and file-listing tools (file_search, list_dir, read_file) to explore the project structure. Do not use terminal commands like `Get-ChildItem`, `find`, or `ls` for directory exploration.
- **GitHub CLI (`gh`):** Before exploring issues, PRs, or CI data, check if `gh` is available and authenticated by running `gh auth status`. If it succeeds and the repository is reachable (`gh repo view` works), use `gh` to query:
  - Issues: `gh issue list --state all --limit 200 --json number,title,state,labels,assignees,milestone,createdAt,updatedAt`
  - Issues filtered by label (run separately for each): `gh issue list --state open --label "Security" --json number,title,state,assignees` and `gh issue list --state open --label "QA" --json number,title,state,assignees` — use to populate Security and QA subsections in §8
  - Team-authored open PRs: `gh pr list --state open --json number,title,reviewDecision,createdAt,author` (exclude Dependabot)
  - Dependabot PRs: `gh pr list --state open --author app/dependabot --json number,title,createdAt,reviewDecision --limit 50` — record total count and the oldest `createdAt` date; any count > 0 with oldest PR older than 4 weeks is a **High** gap
  - All PRs (merged sample): `gh pr list --state merged --limit 10 --json number,title,statusCheckRollup` — for PR check suite inspection
  - Labels: `gh label list --json name --limit 100` — use for the full label list in §9
  - Recent CI runs: `gh run list --limit 10 --json status,conclusion,name,updatedAt` — record pass/fail pattern and most recent run date per workflow
  - Branch protection: `gh api repos/{owner}/{repo}/branches/main/protection` (if accessible)
- Prefer `gh` over static `.tsv`/`.csv` exports when both are available, as CLI data is live and current.
- If `gh` is not available or not authenticated, fall back to any static exports in `.github/quality-queen/input-data/`. Generated project-specific files are stored in `.github/quality-queen/output-data/`.

### Board Data Extraction Rules

**Only use `gh` CLI for project board data when the Board platform input is explicitly `GitHub`.** For other platforms, use the corresponding board-extraction skill. The routing logic is:

| Board Platform (input) | Extraction Method |
|---|---|
| **GitHub** | `gh project item-list` (if project number is known) or `gh api graphql` for project board fields, columns, and items. |
| **Azure DevOps** | Use the `board-extraction-azdo` skill with the Board URL. Do NOT use `gh` CLI. |
| **Jira** | Use the `board-extraction-jira` skill with the Board URL. **Preferred:** Use the Atlassian MCP server if available (provides structured access without manual auth setup). **Fallback:** Jira REST API via curl. Do NOT use `gh` CLI. |
| **None** | Record `board-access-status: no-board-detected` and skip board extraction. |
| **Unknown** | Ask the user for the platform before making board claims; if it remains unknown, record `board-access-status: unknown`. |

- If the Board platform input is blank or `Unknown`, **ask the user** which platform the board is on before making board claims. If no platform can be identified, record `board-access-status: unknown`. If the platform is `None`, skip board extraction and record `board-access-status: no-board-detected`. If the platform is known but cannot be accessed, continue with repository analysis and record it as **inaccessible**, including the exact access error and any fallback source used.
- The `gh` CLI may still be used for GitHub-hosted repo data (issues, PRs, CI runs, labels, branch protection) regardless of where the project board lives — the restriction above applies **only to project board queries**.

## Test Classification Rules

- **Classify tests by scope and assertions, not by folder location.** A test that lives in an `e2e/` or `cypress/` folder but only calls API endpoints directly (no browser, no UI interaction) is an **API test**, not an E2E test.
- **E2E tests** must exercise the full stack through a browser or client UI — they simulate real user interaction.
- **API tests** call HTTP endpoints directly (e.g. via `cy.request()`, `supertest`, `HttpClient`, REST client) and assert on response status/body — they do not launch a browser.
- When a test folder contains a mix, count and classify each test file individually based on what it actually does.
- For any frontend directory containing auth, API, or configuration logic: list **each file individually** in the Untested Areas table — do not group files with distinct risk profiles (e.g. auth service, API client, feature flag config) into a single row.
- **All src/ subdirectories must be accounted for in the Untested Areas table.** For every subdirectory under the frontend `src/` root, confirm whether test files exist. If no tests exist for that directory, add a row — including `models/`, `constants/`, `styles/`, `assets/`, and any other directory regardless of perceived risk. Do not silently omit directories with low logic risk.

## Quality Rules

- Use the scaffold verbatim as the structural template — do not invent new top-level sections.
- Be specific to this project; avoid generic filler text.
- **All file counts and test counts must be EXACT numbers.** Never use approximations like "100+", "~50", "several", or "many". Count the actual files or tests and report the precise number. Every count must be verifiable against the actual files in the repository.
- Clearly separate **assumptions** from **verified observations**.
- **Record a live data timestamp** on the data source note in §8: `[verified YYYY-MM-DD]` using today's date. Apply the same annotation to any section where gh CLI data was used.
- **Issue assignees:** When populating the Owner column in §8 tables, always use the `assignees` field from the gh CLI data. Never default to `—` when assignee data is available for a given issue.
- **Open team PRs:** List **every** non-Dependabot open PR in the team-authored PR table — do not truncate or omit any. Include number, title, review decision, author, and creation date for each.
- **E2E config:** Read the full E2E config file (e.g. `cypress.config.js`, `playwright.config.ts`). Note any auth indicators such as `experimentalModifyObstructiveThirdPartyCode`, `authStrategy`, stored credentials, or env-based tokens, and state whether SSO / auth is a blocker for meaningful E2E coverage.
- **Test data directories:** In §3, annotate any `Data/`, `fixtures/`, or `testdata/` directories found under a test project with their QA relevance (e.g. JSON fixtures, seed data).

## Run Checklist and Validation

1. At the **start** of this run, read `.github/quality-queen/input-data/prompt-run-checklist.md` and complete all items in the **Pre-run** and **generate-project-structure** sections.
2. At the **end** of this run, invoke the `output-validation` skill with `promptType = project-structure` against the generated output file.
3. Report the validation summary to the user. If critical failures exist, fix them before finishing.
