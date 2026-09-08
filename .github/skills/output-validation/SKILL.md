---
name: output-validation
description: Validate generated Quality Queen outputs against prompt checklists and structural requirements.
argument-hint: Provide the output file path and prompt type.
---

# Output Validation

Validates Quality Queen prompt outputs against the run checklist and structural requirements.

---

## When to invoke

Every prompt calls this skill as its **final step** before reporting completion to the user. Do not skip validation even if the output appears correct.

---

## Inputs

| Input | Source |
|---|---|
| `outputFile` | Path to the generated output file |
| `promptType` | One of: `project-structure`, `qa-strategy-full`, `qa-strategy-lite`, `qa-strategy-greenfield`, `qa-strategy-greenfield-lite`, `create-issues` |
| `checklist` | `.github/quality-queen/input-data/prompt-run-checklist.md` |

---

## Validation Steps

### Step 1 — Load the checklist

Read `.github/quality-queen/input-data/prompt-run-checklist.md`. Identify the section matching `promptType` plus the "Post-run validation" and "Pre-run" sections.

### Step 2 — Structural validation

Check the output file against these rules:

| Check | Applies to | Rule |
|---|---|---|
| No placeholder text | all | No `[Project Name]`, `[Current state]`, `[n]`, `[Gap 1]`, or other scaffold placeholders remain |
| ProjectName replacement | `qa-strategy-full`, `qa-strategy-greenfield` | No literal `[ProjectName]` remains in image refs, headings, or file links |
| No template blockquotes | `qa-strategy-full`, `qa-strategy-greenfield` | No `> **Template placeholder**` lines remain |
| Exact counts | `project-structure`, `qa-strategy-full` | All numeric counts are integers — no `~`, `+`, `several`, `many` |
| Section completeness | all | Every required top-level section from the scaffold has content (not empty or placeholder-only) |
| Evidence references | `qa-strategy-full`, `qa-strategy-greenfield` | Every finding in §7 references a concrete location (file path, workflow, board column, issue #) |
| Cross-reference integrity | `qa-strategy-full`, `qa-strategy-greenfield` | §1 risks and recommendations reference valid finding/action IDs from §7 |
| Action table completeness | `qa-strategy-full`, `qa-strategy-greenfield` | Every action row has all 7 columns filled (Action, Finding, Rationale, Impact, Owner, Timeframe, Effort) |
| Manual testing coverage | `qa-strategy-full`, `qa-strategy-greenfield` | §5 Q3 and §6 manual testing subsection are both populated |
| Image references | `qa-strategy-full`, `qa-strategy-greenfield` | All `![...]` references point to files that exist (or will exist after SVG export) |
| Diagram files created | `qa-strategy-full`, `qa-strategy-greenfield` | `.drawio` files exist in `output-data/diagrams/` |
| QA Quadrant legend | `qa-strategy-full`, `qa-strategy-greenfield` | §5 contains the maturity levels legend table (None/Low/Medium/High) |
| QA Quadrant colors | `qa-strategy-full`, `qa-strategy-greenfield` | Quadrant `.drawio` background colors are unchanged from template (Q1=`#dae8fc`, Q2=`#d5e8d4`, Q3=`#fff2cc`, Q4=`#f8cecc`) |
| Data source noted | `project-structure` | A `[verified YYYY-MM-DD]` timestamp is present |
| Board access status | `project-structure` | §9 explicitly distinguishes `accessible`, `inaccessible`, `no-board-detected`, or `unknown`; inaccessible board data is marked `not verifiable` and includes the reason |
| Lite length constraint | `qa-strategy-lite`, `qa-strategy-greenfield-lite` | Output does not exceed ~2 pages equivalent (roughly 80–100 lines of content) |
| No invented findings | `qa-strategy-lite`, `qa-strategy-greenfield-lite` | All findings and actions trace back to the source strategy — no new items added |

### Step 3 — Checklist verification

For each checkbox in the applicable checklist sections:
1. Verify the item is satisfied by inspecting the output file and any generated artifacts.
2. Mark as PASS or FAIL.
3. For FAIL items, record a one-line reason.

### Step 4 — Report results

Produce a validation summary in this format:

```
## Validation Results — [promptType]

**Output file:** [path]
**Status:** [PASS / FAIL (n issues)]

### Passed
- [item 1]
- [item 2]
- ...

### Failed
| # | Check | Reason |
|---|---|---|
| 1 | [check name] | [one-line reason] |

### Recommended fixes
- [fix 1]
- [fix 2]
```

### Step 5 — Resolution

- If all checks PASS → report success and finish.
- If any checks FAIL with severity **Critical** (missing sections, placeholder text, invented findings) → fix them automatically and re-validate.
- If checks FAIL with severity **Non-critical** (minor wording, optional fields) → report them to the user as warnings but do not block completion.

---

## Severity classification for failures

| Severity | Examples |
|---|---|
| **Critical** | Scaffold placeholders in output, missing required sections, approximate counts, findings without evidence |
| **Non-critical** | Optional subsection left as "unknown", diagram not yet exported to SVG, minor formatting |
