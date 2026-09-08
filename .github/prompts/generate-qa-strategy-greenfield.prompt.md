---
description: Generate a QA Foundation Strategy for a new team or greenfield project — prescribing what QA practices to implement from day one, in what order, and with what tooling.
agent: Quality Queen
---

# Generate Greenfield QA Strategy for `${input:projectName:Enter the project name (used in the output filename)}`

You are acting as a QA strategist for a **newly established team or greenfield project**. Your goal is to produce a **prescriptive QA Foundation Strategy** that tells the team what to build from the start — not what's broken in an existing system.

Work through the steps below **in order**. After each step, briefly confirm what was produced before moving to the next.

## Context Shift: Greenfield vs. Established

This prompt operates in **foundational mode**, not diagnostic mode:

- **Do not** frame findings as "gaps" or "problems" — the project is new; gaps are expected.
- **Do** prescribe practices, sequenced by priority and effort.
- **Do** frame recommendations as "implement this" not "fix this."
- **Do** provide concrete checklists the team can execute in Sprint 0.
- **Do** set realistic expectations — not everything needs to be perfect on day one.
- **Do** tailor recommendations to the team's experience level and constraints.

## Inputs and Locations

- **Project root** to analyze (if repo exists): `${input:projectRoot:Enter the project root path (absolute path, `.` for workspace root, or `none` if no repo yet)}`
- **Skills** (optional): `${input:skills:Optional comma-separated list of skills to apply during generation (leave blank for none)}`
- **Insight answers file** (optional): `${input:insightAnswers:Filename of the greenfield insight answers file in input-data (e.g. insight-answers-greenfield.md — leave blank if none)}`
- **Project context file** (optional): `${input:projectContext:Filename of the project context file in input-data (e.g. project-context.md — leave blank if none)}`
- Input data folder: `.github/quality-queen/input-data/`
- Output data folder: `.github/quality-queen/output-data/`
- Greenfield scaffold template: `.github/quality-queen/input-data/qa-strategy-greenfield-scaffold.md`
- QA Framework reference: `.github/quality-queen/input-data/qa-framework.md`
- Greenfield discovery questions: `.github/quality-queen/input-data/qa-insight-questions-greenfield.md`
- Final output: `.github/quality-queen/output-data/qa-strategy-greenfield-${input:projectName}.md`

## Step 1 — Gather Context

1. Read the QA Framework (`.github/quality-queen/input-data/qa-framework.md`) to ground your recommendations in Bouvet's four-dimension model.
2. Read the greenfield scaffold (`.github/quality-queen/input-data/qa-strategy-greenfield-scaffold.md`) — this is your output template.
3. If `insightAnswers` is provided, read `.github/quality-queen/input-data/${input:insightAnswers}` and incorporate the team's answers.
4. If `projectContext` is provided, read `.github/quality-queen/input-data/${input:projectContext}` and use it to enrich the strategy.
5. If critical context is missing (team composition, tech stack, delivery model, risk profile), **stop and ask the user** using the greenfield discovery questions (`.github/quality-queen/input-data/qa-insight-questions-greenfield.md`) as a guide. Ask only what's needed — don't treat it as a full interview.

## Step 2 — Analyze Existing Repo (if applicable)

If `projectRoot` is not `none` and a repository exists:

1. Check if a `project-structure-${input:projectName}.md` already exists in `.github/quality-queen/output-data/`. If yes, read it.
2. If no project structure exists but the repo has code, perform a lightweight analysis:
   - Identify tech stack and frameworks in use
   - Check for existing CI/CD configuration
   - Check for existing test frameworks and any tests
   - Check for linting/formatting configuration
   - Check for branch protection or PR templates
3. Note what's already in place vs. what needs to be established.

If `projectRoot` is `none`, skip this step entirely and rely on context from Step 1.

## Step 3 — Draft the Foundation Strategy

Using the greenfield scaffold as your template, produce a complete strategy document:

1. **Executive Summary:** Frame around goals, constraints, and risks — not current-state analysis.
2. **Delivery Flow:** Prescribe a recommended board structure, DoR/DoD, and issue templates appropriate for the team's delivery model.
3. **QA in Work Processes:** Define what practices to implement, sequenced by Sprint 0 → First Month → First Quarter.
4. **QA in Build Processes:** Design the pipeline stages and quality gates to set up, with the same phasing.
5. **QA Quadrant — Target State:** Define what the team should aim for in each quadrant at each phase.
6. **Test Pyramid — Target Architecture:** Recommend the test distribution, tooling, and sequencing.
7. **Foundation Checklist:** Concrete, actionable items with owners and phases. This is the most important section — make it immediately executable.
8. **Presentation Summary:** Frame the value proposition for stakeholders.
9. **Maturity Roadmap:** Define how the team grows from zero to sustainable quality practices.
10. **Open Questions:** Only include questions that genuinely need answers to proceed.

## Step 4 — Validate and Save

1. Review the strategy for:
   - Specificity: Every recommendation must be tailored to this team's context, not generic.
   - Sequencing: Is the Sprint 0 list achievable in 1–2 weeks? Is the phasing realistic?
   - Actionability: Can the team turn the Foundation Checklist into board items today?
   - Completeness: Are all four QA dimensions covered?
2. Save the final output to `.github/quality-queen/output-data/qa-strategy-greenfield-${input:projectName}.md`.
3. Summarize what was produced and suggest next steps (e.g. "Review the Sprint 0 checklist with the team and create board items for each action").

## Tone and Style

- Be prescriptive and confident — the team needs clear direction, not options analysis.
- Be realistic — acknowledge that not everything happens in Sprint 0.
- Be practical — every recommendation should be achievable with the stated team.
- Use imperative language: "Set up X" not "Consider setting up X."
- Prefer Bouvet conventions and "the Bouvet way" where relevant.
- Keep the strategy concise enough to be read in one sitting (target 8–12 pages when rendered).

## Run Checklist and Validation

1. At the **start** of this run, read `.github/quality-queen/input-data/prompt-run-checklist.md` and complete all items in the **Pre-run** and **generate-qa-strategy-full** sections (greenfield strategies follow the same checklist).
2. At the **end** of this run, invoke the `output-validation` skill with `promptType = qa-strategy-full` against the generated output file.
3. Report the validation summary to the user. If critical failures exist, fix them before finishing.
