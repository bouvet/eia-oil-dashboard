---
description: Generate a complete QA Strategy for a given project by analyzing its structure, GitHub exports, and codebase, then producing a strategy document from the qa-strategy-scaffold template.
agent: Quality Queen
---

# Generate QA Strategy for `${input:projectName:Enter the project name (used in the output filename)}`

You are acting as a QA strategist. Your ultimate goal is to produce a **complete, project-specific QA Strategy** for the project named `${input:projectName}`, grounded in verified observations from the target project and any supporting input data.

Work through the steps below **in order**. Do not skip ahead. After each step, briefly confirm what was produced before moving to the next.

## Inputs and Locations

- **Project root** to analyze: `${input:projectRoot:Enter the project root path to analyze (absolute path or `.` for the current workspace root)}`
  - Treat this as the base for **all** code, test, and CI/CD path references.
  - If the value is `.` or empty, use the current workspace root.
  - If it points outside the current workspace, use absolute paths and read-only tools.
- **Skills** (optional): `${input:skills:Optional comma-separated list of skills to apply during generation (leave blank for none)}`
  - If one or more skill names are provided (comma-separated), apply each skill's knowledge and instructions throughout the strategy generation process.
- **Insight answers file** (optional): `${input:insightAnswers:Filename of the QA insight answers file in the input-data folder (e.g. insight-answers.md — leave blank if none)}`
  - If provided, read `.github/quality-queen/input-data/${input:insightAnswers}` and incorporate the team's answers into the strategy generation — especially for sections that rely on team input (work processes, build processes, ambitions, and open questions).
- **Project context file** (optional): `${input:projectContext:Filename of the project context file in the input-data folder (e.g. project-context.md — leave blank if none)}`
  - If provided, read `.github/quality-queen/input-data/${input:projectContext}` and use the information to enrich the strategy — especially the Executive Summary, Work Processes, and Open Questions sections. Treat its content as verified input (not assumptions).
  - The file may also contain specific instructions to execute during strategy generation (e.g. commands to run, files to inspect, or analysis steps to perform). Follow any such instructions as part of the relevant step.
- **Additional project names** *(optional)*: `${input:additionalProjectNames:Comma-separated names of additional project structures to include in this strategy (e.g. MyApp-backend,MyApp-frontend — leave blank for single project)}`
  - If provided, read each corresponding `project-structure-<name>.md` from `.github/quality-queen/output-data/` alongside the primary project structure. The strategy synthesizes findings across all components. Each additional project structure must already exist; if any is missing, stop and inform the user to run **Generate Project Structure** for that component first.
- Input data folder (templates, reference docs, board exports): `.github/quality-queen/input-data/`
- Output data folder (generated project-specific files): `.github/quality-queen/output-data/`
- Project structure (pre-generated): `.github/quality-queen/output-data/project-structure-${input:projectName}.md`
  - This file must already exist. Generate it first using the **Generate Project Structure** prompt if it doesn't.
- QA strategy scaffold (template): `.github/quality-queen/input-data/qa-strategy-scaffold.md`
- QA strategy template (guideline): `.github/quality-queen/input-data/qa-strategy-template.md`
  - Use this template as a **guideline** for tone, depth, structure, and level of detail when generating the strategy. It demonstrates the expected quality and style of the final output.
- Final QA strategy output: `.github/quality-queen/output-data/qa-strategy-${input:projectName}.md`

### Project-specific input data

Before starting analysis, check these locations for project-specific context and incorporate any files found:

- `.github/quality-queen/input-data/` — Look for backlog exports (`.tsv`, `.csv`), board exports, iteration data, QA discovery documents, and any supplementary reference material.
- `.github/ISSUE_TEMPLATE/` — Look for issue templates (bug reports, feature requests, etc.) that reveal workflow expectations and field conventions.

Read and incorporate **all** relevant files found in these locations into your analysis.

## Step 1 — Read the Project Structure

1. Open `.github/quality-queen/output-data/project-structure-${input:projectName}.md` and read it fully. This is your pre-generated project map.
2. If the file does not exist, stop and inform the user to run the **Generate Project Structure** prompt first (which applies the `project-structure-analysis` skill).
3. **If `additionalProjectNames` is not blank**, parse the comma-separated list of names and open each corresponding `project-structure-<name>.md` from `.github/quality-queen/output-data/`. Read each file fully.
   - If any file is missing, stop and inform the user to run **Generate Project Structure** for that component first.
   - Treat the primary project (`${input:projectName}`) as the anchor component. Additional project structures extend the scope of the strategy; do not duplicate shared findings — consolidate them.
   - Build a mental model of how the components relate: shared board, separate repos, common CI/CD infrastructure, shared test tooling, etc.
   - When a finding applies to only one component, prefix it with the component name (e.g. `[frontend]`, `[backend]`). When it applies to all, state it without a prefix.

## Step 2 — Analyze GitHub exports and supporting input data

0. **Check GitHub CLI availability:** Run `gh auth status` to verify `gh` is installed and authenticated. If it succeeds, use `gh` to query live data (issues, PRs, project boards, branch protection) throughout this step and Step 3. Prefer live CLI data over static `.tsv`/`.csv` exports when both are available. If `gh` is not available or not authenticated, fall back to static exports.
1. List all files in `.github/quality-queen/input-data/` and `.github/quality-queen/output-data/`. In `input-data/`, identify GitHub exports (e.g. backlog `.tsv`/`.csv`, board export, iteration export) and supplementary reference documents (e.g. QA insight questions). In `output-data/`, locate all project structure files loaded in Step 1.
2. For each export, extract:
   - Board columns and workflow stages
   - Work item types in use (epic, feature, story, bug, task, spike, etc.)
   - Field usage (acceptance criteria, story points, labels, area/iteration paths)
   - Backlog composition and bug-to-story ratio
   - Signals about Definition of Ready / Definition of Done usage
   - Recurring themes, risks, or quality issues
3. **Update** the existing **§12 "GitHub & Process Signals"** section in `project-structure-${input:projectName}.md` with these findings, again separating observations from assumptions. Do not append a new section — §12 already exists in the scaffold; populate it in place.
4. **If multiple project structures were loaded in Step 1**, update §12 in each component's project-structure file in the same way. Note cross-component signals (e.g. same board, shared pipeline) in the primary file's §12 under a `Cross-component signals` sub-heading.

## Step 3 — Analyze the project itself

Using the project structure file(s) loaded in Step 1 as your map, dig into the codebase to validate and enrich your understanding. **If multiple project structures were loaded, apply the analysis below to each component's project root in turn**, then synthesize cross-component observations at the end of this step.

- Confirm the test pyramid shape by counting/sampling tests at each level.
  - **Classify tests by scope and assertions, not by folder location.** A test in an `e2e/` or `cypress/` folder that only calls API endpoints directly (no browser, no UI interaction) is an **API test**, not an E2E test. E2E tests must exercise the full stack through a browser or client UI. When a folder contains a mix, classify each test file individually.
- Check CI/CD configuration for actual quality gates, required checks, and failure handling.
- Inspect linting, formatting, static analysis, security scanning, and dependency management setup.
- Review code review conventions (PR templates, CODEOWNERS, branch protection if visible).
- Classify the **branching strategy** precisely based on evidence from README, CONTRIBUTING, or observed branch patterns (e.g. Trunk-Based Development, GitHub Flow, GitFlow, GitLab Flow, release branching, forking workflow). Do not default to the most common label — match the evidence to the specific strategy. If it doesn't match a named pattern exactly, describe the observed practice.
- **Determine work methodology from evidence, never assume.** Check for Sprint/Iteration fields on the project board, milestone usage with date ranges, sprint-related labels, and explicit mentions in README/CONTRIBUTING. If none of these exist but the board uses continuous-flow columns (e.g. Backlog → In Progress → Done), classify as "flow-based (Kanban-like)". Never default to "Scrum" or "sprints" without concrete evidence (Sprint field, Iteration field, or explicit documentation). Use the methodology table from §9 of `project-structure-${input:projectName}.md` and carry the confidence level into the strategy. If confidence is Low, add the methodology question to §10 (Open Questions).
- **Trace the deployment model end-to-end** — map the full path from code commit to production (e.g. branch → PR → CI → merge → deploy to env A → promote to env B → production). Use this to determine the **causal ordering** of quality gates. If a board column implies code is already merged and deployed, do not suggest pre-merge checks (code review, CI, unit tests) as criteria for that column. Assign each quality gate to the stage where it actually executes, not where it would be ideal.
- Identify integrations, external dependencies, auth patterns, and any test-data strategy.
- Map findings to the four discovery areas:
  1. QA in Work Processes
  2. QA in Build Processes
  3. Agile QA Quadrant
  4. Test Pyramid

Record any new findings back into the relevant existing sections of `project-structure-${input:projectName}.md` so it remains the single source of truth. Update sections in place — do not append duplicate sections.

**Multi-component synthesis** (when `additionalProjectNames` is not blank): After analyzing each component individually, write a brief `## Cross-component observations` note at the end of `project-structure-${input:projectName}.md`. Cover:
- How the test pyramids compare across components (e.g. backend has unit tests, frontend has none).
- Whether CI/CD quality gates are consistent or divergent across repos.
- Whether all components are tracked on the same board or different boards, and any cross-board DoR/DoD gaps.
- Any integration boundary that has no automated test coverage (e.g. frontend → backend API contract).

## Step 4 — Generate the QA Strategy

1. Open `qa-strategy-scaffold.md` and use it as the **exact template** for the strategy output.
2. Produce a strategy that follows the scaffold's structure section-for-section, including at minimum:
   - Executive Summary
   - Delivery Flow and Quality Gates (with DoR/DoD per board column)
   - QA in Work Processes (As is / Ambition / AI)
   - QA in Build Processes (As is / Ambition / AI)
   - Agile QA Quadrant Assessment (As is / Ambition / AI)
   - Test Pyramid Assessment (As is / Ambition / AI)
   - Findings and Actions (Critical / High / Medium / Low; grouped by ownership)
   - Presentation Summary
   - Follow-up and Measurement
   - Open Questions for the Team (project-specific, based on gaps found during analysis)
3. Use `.github/quality-queen/input-data/qa-insight-questions.md` as a reference for question categories. For section 10 (Open Questions), generate questions that are **specific to gaps and assumptions identified during the analysis** — do not include questions whose answers are already available in the project files or in the insight answers file.
4. If an **insight answers file** was provided, use those answers to:
   - Convert assumptions into verified observations throughout the strategy.
   - Inform the As-is and Ambition subsections in sections 3–6.
   - Remove answered questions from section 10 (Open Questions) — only list questions that remain unanswered.
5. Ground every recommendation in evidence from `project-structure-${input:projectName}.md` and the codebase. Cite specific files, pipelines, or board signals where relevant.
6. Keep recommendations practical, prioritized, and measurable. Distinguish high-value-now from longer-term improvements. Avoid overloaded action lists.
7. Clearly separate **assumptions**, **observations**, **recommendations**, and **open questions**.
8. **Apply Test Classification Rules consistently** when writing findings, the Test Pyramid section, the QA Quadrant section, and action items. A test that calls HTTP endpoints directly without a browser is an API test regardless of its folder. Do not inflate E2E counts or undercount API tests based on folder names.

## Step 4b — Generate project-specific diagrams

For each of the three diagrams referenced in the strategy (delivery flow, QA quadrant, test pyramid), produce a project-specific version before saving the strategy file.

### 4b.1 — Copy and rename the template `.drawio` files

Copy each template from `.github/quality-queen/input-data/diagrams/` to `.github/quality-queen/output-data/diagrams/` with `${input:projectName}` substituted in the filename:
- `work-process.drawio` → `work-process-${input:projectName}.drawio`
- `qa-quadrant.drawio` → `qa-quadrant-${input:projectName}.drawio`
- `test-pyramid.drawio` → `test-pyramid-${input:projectName}.drawio`

### 4b.2 — Edit each `.drawio` file with project-specific content

`.drawio` files are XML. Edit each copy to replace placeholder content with verified project data:

**`work-process-${input:projectName}.drawio`**
- Replace every `[Phase N]` label with the team's phase name (e.g. Discovery, Development, Release).
- Replace every `[Column]` box label with the team's actual board column name (from §9 of `project-structure-${input:projectName}.md`).
- Replace every `[Environment N]` label with the deployment environment name (Dev, Staging, Prod).
- Set DoR gate labels (red fill cells) on the column where work becomes ready for development.
- Set DoD gate labels (green fill cells) on the columns that represent exit criteria checkpoints.

**`qa-quadrant-${input:projectName}.drawio`**
- Replace the placeholder activity lists in each quadrant with the project's actual activities from §5 of the strategy.
- Set each quadrant's maturity badge to the level assessed in the strategy (None / Low / Medium / High).

**`test-pyramid-${input:projectName}.drawio`**
- Update the layer label text and counts to match the verified test counts from `project-structure-${input:projectName}.md` (§4 and §5).
- Reposition pyramid segments to reflect actual test distribution by adjusting `y` coordinates only. **Never change `width`, `x`, `height`, `size`, or any style property.** The template stacking is: triangle (`y=80`) → mid trapezoid (`y=160`) → wide trapezoid (`y=240`), each 80px tall. Assign the triangle to the layer with fewest tests, mid trapezoid to the middle count, wide trapezoid to the most. Keep all layers flush (each shape's `y` = the shape above `y + 80`).
- Set fill colours: red (`#f8cecc`/`#b85450`) for absent or very low, amber (`#fff2cc`/`#d6b656`) for partial, green (`#d5e8d4`/`#82b366`) for adequate.

### 4b.3 — Export each `.drawio` file to SVG

Run the draw.io desktop CLI export from `.github/quality-queen/output-data/diagrams/`:

```powershell
# Windows
& "C:\Program Files\draw.io\draw.io.exe" --export --format svg --output work-process-${input:projectName}.svg work-process-${input:projectName}.drawio
& "C:\Program Files\draw.io\draw.io.exe" --export --format svg --output qa-quadrant-${input:projectName}.svg qa-quadrant-${input:projectName}.drawio
& "C:\Program Files\draw.io\draw.io.exe" --export --format svg --output test-pyramid-${input:projectName}.svg test-pyramid-${input:projectName}.drawio
```

If the export fails, note it in the strategy and instruct the user to export manually using the Draw.io Integration VS Code extension (open the `.drawio` file, click **File** → **Export** → **.svg**, save to the same `diagrams/` folder).

### 4b.4 — Update image references and remove template placeholder blocks

In the strategy document:

1. **Replace all three generic image references** with the project-specific filenames:
   - `./diagrams/work-process.svg` → `./diagrams/work-process-${input:projectName}.svg`
   - `./diagrams/qa-quadrant.svg` → `./diagrams/qa-quadrant-${input:projectName}.svg`
   - `./diagrams/test-pyramid.svg` → `./diagrams/test-pyramid-${input:projectName}.svg`

2. **Remove every `> **Template placeholder**` blockquote** from the strategy document. These are build instructions for human editors; they must not appear in the published output. Delete the entire blockquote block — from the opening `> **Template placeholder**` line through to the last numbered instruction line above the image reference.

---

## Step 5 — Save the output

- Save the final strategy to `.github/quality-queen/output-data/qa-strategy-${input:projectName}.md`.
- **Update version metadata automatically** at the top of the document:
  - Set `Last updated` to today's date in `YYYY-MM-DD` format.
  - If the file does **not** exist yet, set `Version` to `1.0` and add a `Version History` row with summary `Initial generation`.
  - If the file **already exists**, read its current `Version` and `Version History`, then:
    - Bump **MINOR** (e.g. `1.0` → `1.1`) for refinements on the same project state.
    - Bump **MAJOR** (e.g. `1.1` → `2.0`) when `project-structure-${input:projectName}.md`, board structure, or strategy direction changed materially since the last version.
    - Append a new `Version History` row with the new version, today's date, author, and a one-line summary of what changed.
  - Preserve all prior `Version History` rows; never delete history.
- Confirm with the user before overwriting if the strategy file already exists and the change is non-trivial.
- After saving, output a short summary listing:
  - New version number and date
  - Path to `project-structure-${input:projectName}.md`
  - Path to the generated QA strategy file
  - Top 3–5 priority recommendations
  - Any open questions that need user/team input

## Quality Rules

- Use the scaffolds verbatim as structural templates — do not invent new top-level sections.
- Be specific to this project; avoid generic best-practice text.
- **Remove all `> **Template placeholder**` blockquotes** from the final output. These are build instructions in the scaffold template and must never appear in the published strategy document.
- **Replace every `[ProjectName]` occurrence** in image references, alt text, and file links with the actual project name before saving.
- **All file counts and test counts must be EXACT numbers.** Never use approximations like "100+", "~50", "several", or "many". Count the actual files or tests and report the precise number. Every count must be verifiable against the actual files in the repository.
- Prefer concrete, backlog-ready actions with rationale, expected impact, suggested owner, and timeframe.
- If critical context is missing (e.g. delivery model, stakeholders, compliance constraints), ask clarifying questions **before** generating the strategy in Step 4.

## Run Checklist and Validation

1. At the **start** of this run, read `.github/quality-queen/input-data/prompt-run-checklist.md` and complete all items in the **Pre-run** and **generate-qa-strategy-full** sections.
2. At the **end** of this run, invoke the `output-validation` skill with `promptType = qa-strategy-full` against the generated output file.
3. Report the validation summary to the user. If critical failures exist, fix them before finishing.
