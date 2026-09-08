---
name: board-extraction-github
description: "Extract board structure, issues, PR check suites, and branch protection from a GitHub project using the GitHub CLI. Produces structured board data consumed by project-structure-analysis. Triggers: GitHub board, GitHub issues, PR checks, branch protection, gh CLI, GitHub project."
argument-hint: "Provide the GitHub owner (org or user). Optionally provide the project number if known."
---

# Board Extraction — GitHub

Extracts board structure, issues, PR check suites, and branch protection from a GitHub repository and project board. Produces structured output consumed by the `project-structure-analysis` skill (Steps 2 and 6).

## When to Use

- When `project-structure-analysis` detects the board source is GitHub Issues
- When auditing GitHub issue quality, board column flow, or PR gate enforcement standalone
- When the existing board data in the project structure document is stale

## Output Contract

This skill produces a structured summary block that `project-structure-analysis` stores and uses to fill its output document. Record the following fields:

| Field | Content |
|---|---|
| `data-source` | `gh-cli` or `static-export` |
| `board-access-status` | `accessible` / `inaccessible` / `no-board-detected` / `unknown` |
| `board-access-reason` | Exact reason when access is unavailable; do not infer absence from an access error |
| `board-columns` | Ordered list of column names as they appear on the board, or `not verifiable` when inaccessible |
| `custom-fields` | Fields in use (Priority, Size, Sprint, etc.) and consistency rating, or `not verifiable` when inaccessible |
| `dor-dod-status` | `documented` / `informal` / `not-defined` / `not-verifiable` |
| `issues-in-progress` | List of active board items (number, title, status, owner) |
| `issues-security-nfr` | Issues labelled Security, Performance, Accessibility, NFR |
| `issues-process-qa` | Issues related to templates, test tooling, environments, DoR/DoD |
| `pr-check-suites` | Table: check suite app, required-to-merge, typical conclusion, notes |
| `branch-protection` | Summary of `main` protection rules |

See [gh-commands.md](./references/gh-commands.md) for every `gh` command used in this skill.

---

## Step A — Verify GitHub CLI Access

```sh
gh auth status
gh repo view
```

- If both repository checks succeed, use `gh` for repository data and record `data-source: gh-cli`.
- Attempt `gh project list --owner <org-or-user>` separately from repository access. If it succeeds with one or more projects, record `board-access-status: accessible` and continue with board extraction.
- If the project query succeeds with zero projects, record `board-access-status: no-board-detected`; this is different from an access failure.
- If the project query fails because of a missing scope, permission, authentication, network, or API error, record `board-access-status: inaccessible` and the exact error. Do not claim that no board exists and do not fabricate columns, fields, or DoR/DoD status.
- If repository access fails, fall back to static exports in `.github/quality-queen/input-data/` (`.tsv`, `.csv`) when present. Record `data-source: static-export` and note the export date.

---

## Step B — Query Issues

```sh
# All issues with labels, assignees, milestone
gh issue list --state all --limit 200 --json number,title,state,labels,assignees,milestone,createdAt,updatedAt

# Filter by label
gh issue list --state all --label "Security" --json number,title,state,labels,assignees
gh issue list --state all --label "QA" --json number,title,state,labels,assignees
gh issue list --state all --label "Bug" --json number,title,state,labels,assignees
```

Categorize issues into four groups:

### In Progress / Ready for Work
Issues currently active on the board. Record: number, title, status, owner.

### Security & Non-Functional
Issues labelled `Security`, `Performance`, `Accessibility`, `NFR`, or similar. Note if previously completed but no longer enforced in CI.

### Process / QA Infrastructure
Issues related to templates, test tooling, environments, DoR/DoD, monitoring, or error handling.

### Recently Closed Patterns
Closed issues that reveal quality trends: regressions reopened quickly, security work done but not maintained, recurring bug labels.

---

## Step C — Query Project Board

Only run the project-item and field queries when `board-access-status` is `accessible`. When status is `inaccessible`, record the reason and skip board queries; continue with Steps B and D and return an explicit not-verifiable board section.

```sh
# List all projects for the org/user
gh project list --owner <org-or-user>

# List items on a specific project board (replace 181 with the project number)
gh project item-list 181 --owner <org-or-user> --limit 200 --format json
```

Extract:
- Column names (Status field values = workflow states) in flow order
- Custom fields in use (Priority, Size, Sprint, Estimate, etc.)
- Distribution of items across columns (backlog size, in-progress count, blocked items)
- Items with no Priority or Size set (field consistency check)
- Any DoR/DoD wording in column titles, column descriptions, or board field descriptions

---

## Step D — Query PR Check Suites and Branch Protection

Workflow YAML shows what *should* run. PR check suites show what *actually* runs and whether it blocks merges. These often diverge.

```sh
# Recent merged PRs — obtain PR numbers and commit SHAs
gh pr list --state merged --limit 10 --json number,title,headRefOid,mergedAt

# Check summary for a specific PR
gh pr checks <PR_NUMBER>

# Detailed check runs for a commit SHA
gh api repos/{owner}/{repo}/commits/{sha}/check-runs \
  --jq '.check_runs[] | {name: .name, app: .app.slug, status: .status, conclusion: .conclusion}'

# Required status checks on main (what must pass before merge)
gh api repos/{owner}/{repo}/branches/main/protection/required_status_checks \
  --jq '{strict: .strict, contexts: .contexts, checks: .checks}'

# Branch protection rules
gh api repos/{owner}/{repo}/branches/main/protection
```

**Workflow:**
1. Run `gh pr list --state merged --limit 5` to get recent SHAs.
2. For 2–3 PRs, run the check-runs query to capture which app slugs registered checks.
3. Cross-reference slugs against the required status checks list.

Produce a check suite table:

| Check suite / app | Required to merge? | Typical conclusion | Notes |
|---|---|---|---|
| e.g. `snyk` | Yes / No | passing / failing / skipped | Dependency + code vulnerability scan |
| e.g. `github-actions` | Yes | passing | Build + test pipeline |
| e.g. `codecov` | No | passing | Coverage reporting only |

Flag explicitly:
- Security scanners present but **not required** — findings visible but bypass is possible
- Security scanners **absent entirely**
- Check suites with consistent failures not blocking merges
- Mismatch between checks listed in workflow YAML and checks appearing on actual PRs

---

## Step E — Return Structured Summary

After completing Steps A–D, compile the output contract fields defined at the top of this document. Include the board access status and exact reason whenever the board was not inspected. The calling skill (`project-structure-analysis`) stores this summary and uses it to fill the data-source note and board/issue sections of the output document without converting an access failure into a no-board claim.




