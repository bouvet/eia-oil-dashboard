# Prompt Run Checklist

This checklist defines mandatory steps that every Quality Queen prompt must complete. The agent reads this file at the start of each run and verifies all applicable items before finishing.

---

## Pre-run (all prompts)

- [ ] Read `.github/quality-queen/input-data/project-secrets.env` if it exists; load non-empty values as inputs
- [ ] Attempt authentication for the board platform; if access is unavailable, record `board-access-status: inaccessible` and continue with repository-only and fallback evidence
- [ ] Verify the output target path is correct and will not overwrite without user consent

---

## generate-project-structure

- [ ] Project root is resolved and all paths are relative to it
- [ ] All 9 exploration steps in the `project-structure-analysis` skill are completed
- [ ] Board extraction was attempted for the specified platform, or `no-board-detected` was established; record the status and exact reason
- [ ] §4/§5 test inventories have exact counts (no approximations)
- [ ] §6b Manual Testing and Test Management is populated (or explicitly states "none")
- [ ] §7 CI/CD has every workflow file accounted for
- [ ] §8 Key Issues are populated from available live tracker data; inaccessible sources are identified and not presented as assumptions
- [ ] §11 Known QA Gaps has at least one entry with concrete location references
- [ ] No scaffold placeholder text remains in the output
- [ ] Board status, data source, and timestamp are recorded

---

## generate-qa-strategy-full

- [ ] `project-structure-<name>.md` exists and was read before starting
- [ ] All six main sections (1–6) are populated from verified evidence
- [ ] §5 Agile QA Quadrant includes Q3 manual testing assessment
- [ ] §6 Test Pyramid includes manual testing subsection
- [ ] §7 Findings have severity ratings and concrete evidence references
- [ ] §7 Actions are backlog-ready with owner, timeframe, and expected impact
- [ ] Diagram `.drawio` files are created in `output-data/diagrams/`
- [ ] All `[ProjectName]` placeholders are replaced with the actual project name
- [ ] All `> **Template placeholder**` blockquotes are removed
- [ ] No scaffold placeholder text remains in the output

---

## generate-qa-strategy-lite

- [ ] Full strategy file exists and was read
- [ ] Output is ≤2 pages equivalent in length
- [ ] Top risks, priority actions, and measurement guidance are preserved
- [ ] No new findings are invented (summary only)

---

## create-issues-from-strategy

- [ ] Strategy file exists and has a §7 Findings and Actions section
- [ ] Findings were filtered by the specified severity threshold
- [ ] User confirmed which findings to create work items for
- [ ] Duplicate check was performed before creating each item
- [ ] Created items have QA label and severity label where applicable

---

## Post-run validation (all prompts)

- [ ] Run the `output-validation` skill against the generated output
- [ ] All critical validation errors are resolved before finishing
- [ ] Summary of completed checklist items is reported to the user
