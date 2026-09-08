---
description: Generate a lite 2-page QA Foundation Plan from an existing greenfield QA strategy — suitable for team kickoffs and stakeholder communication.
agent: Quality Queen
---

# Generate Lite Greenfield QA Strategy from `${input:strategyFile:Filename of the existing greenfield QA strategy in .github/quality-queen/output-data/ (e.g. qa-strategy-greenfield-MyProject.md)}`

Produce a **lite, actionable QA Foundation Plan** based on the existing greenfield strategy document. This is a 2-page summary for team kickoffs and stakeholder buy-in.

## Inputs

- **Source strategy:** `.github/quality-queen/output-data/${input:strategyFile}`

## Output

Save to: `.github/quality-queen/output-data/qa-strategy-greenfield-lite-${input:projectName:Enter the project name}.md`

## Rules

- Maximum **2 pages** worth of content. Cut ruthlessly.
- Use bullet points and tables — no prose paragraphs.
- Every statement must be specific to this project.
- Frame everything as "what we will build" — not "what's missing."
- The Foundation Checklist is the most important section — keep it intact.

## Structure

### 1. Context (max 5 bullets)

- Project name, tech stack, team size
- Delivery model and planned release cadence
- Planned git/branching strategy
- Team's QA experience level in one sentence
- Biggest quality risk for a new project in one sentence

### 2. Recommended Quality Gates

One table: board column → DoR/DoD criteria. No explanation — just the table.

### 3. QA Foundation by Phase

For each of the four QA dimensions, provide a single table:

| Dimension | Sprint 0 | First Month | First Quarter |
|---|---|---|---|

Max 2 bullets per cell. Concrete actions only.

### 4. Foundation Checklist — Sprint 0 (max 10 items)

| # | Action | Owner | Priority |
|---|---|---|---|

These should be items the team can create as board items **today**.

### 5. Value Proposition (max 4 bullets)

Why investing in QA foundations now pays off. One sentence each, tied to concrete outcomes.

### 6. Metrics to Start Tracking

One table: metric, when to start, initial target. Max 5 rows.

### 7. Open Questions (max 5)

Only questions that block Sprint 0 actions.

## Run Checklist and Validation

1. At the **start** of this run, read `.github/quality-queen/input-data/prompt-run-checklist.md` and complete all items in the **Pre-run** and **generate-qa-strategy-lite** sections (greenfield lite follows the same checklist).
2. At the **end** of this run, invoke the `output-validation` skill with `promptType = qa-strategy-lite` against the generated output file.
3. Report the validation summary to the user. If critical failures exist, fix them before finishing.
