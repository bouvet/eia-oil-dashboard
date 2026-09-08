# GitHub CLI Commands for Board Extraction

Reference for all `gh` commands used during GitHub board extraction. Run these after confirming `gh auth status` and `gh repo view` both succeed.

---

## Prerequisites

```sh
# Verify authentication
gh auth status

# Confirm the repo is reachable and note the default branch
gh repo view
```

---

## Issues

```sh
# All issues (open + closed), with labels, assignees, milestone
gh issue list --state all --limit 200 --json number,title,state,labels,assignees,milestone,createdAt,updatedAt

# Filter to open issues only
gh issue list --state open --limit 100 --json number,title,state,labels,assignees

# Filter by label (e.g. Security, QA, Bug)
gh issue list --state all --label "Security" --json number,title,state,labels,assignees
gh issue list --state all --label "QA" --json number,title,state,labels,assignees
gh issue list --state all --label "Bug" --json number,title,state,labels,assignees
```

**What to extract:**
- Issues currently in progress or ready for work (active board items)
- Security and non-functional items (by label or keyword in title)
- Process / QA infrastructure items (bug templates, test tooling, environment access, DoR/DoD)
- Recently closed issues that reveal patterns (regressions reopened quickly, security work done but not maintained)

---

## Pull Requests

```sh
# All PRs with review status and labels
gh pr list --state all --limit 50 --json number,title,state,labels,reviewDecision,createdAt,mergedAt,author

# PRs currently open (pending review or approval)
gh pr list --state open --json number,title,state,labels,reviewDecision,author
```

**What to extract:**
- PRs without required reviews (reviewDecision: null or REVIEW_REQUIRED)
- Long-lived open PRs (high createdAt delta)
- Label patterns that reveal QA-relevant work in flight

---

## Project Board

```sh
# List all projects for the org/user
gh project list --owner <org-or-user>

# List items on a specific project board (replace 181 with the project number)
gh project item-list 181 --owner <org-or-user> --limit 200 --format json

# If project number is unknown, find it from the list output above
```

**What to extract:**
- Column names (Status field values = workflow states)
- Custom fields in use (Priority, Size, Sprint, Estimate, etc.)
- Distribution of items across columns (backlog size, in-progress count, blocked items)
- Items with no Priority or Size set (field consistency check)

---

## Branch Protection

```sh
# Check main branch protection rules
gh api repos/{owner}/{repo}/branches/main/protection

# List all branches and their protection status
gh api repos/{owner}/{repo}/branches --jq '.[] | {name: .name, protected: .protected}'
```

**What to extract:**
- Is `main` protected? (required reviews, required status checks, restrict pushes)
- Which status checks are required before merge (CI jobs that must pass)
- Whether force-push or deletion is blocked

---

## PR Check Suites

```sh
# View check summary for a specific PR (quickest overview)
gh pr checks <PR_NUMBER>

# Get detailed check runs for a commit SHA (includes app/integration name)
gh api repos/{owner}/{repo}/commits/{sha}/check-runs \
  --jq '.check_runs[] | {name: .name, app: .app.slug, status: .status, conclusion: .conclusion}'

# Get check suites grouped by app for a commit SHA
gh api repos/{owner}/{repo}/commits/{sha}/check-suites \
  --jq '.check_suites[] | {app: .app.slug, status: .status, conclusion: .conclusion}'

# Required status checks on the default branch (what must pass before merge)
gh api repos/{owner}/{repo}/branches/main/protection/required_status_checks \
  --jq '{strict: .strict, contexts: .contexts, checks: .checks}'

# Get recent merged PRs to obtain sample SHAs
gh pr list --state merged --limit 10 --json number,title,headRefOid,mergedAt
```

**Workflow:**
1. Run `gh pr list --state merged --limit 5` to get recent PR numbers and commit SHAs (`headRefOid`).
2. For 2–3 PRs, run the check-runs query to see which app slugs registered checks.
3. Cross-reference the app slugs against the required status checks from branch protection.

**Common app slugs to watch for:**

| Slug | Tool |
|---|---|
| `snyk` | Snyk dependency + code vulnerability scan |
| `github-advanced-security` | GitHub CodeQL / secret scanning |
| `sonarcloud` / `sonarqube` | SonarCloud / SonarQube code quality |
| `codecov` | Code coverage reporting |
| `dependabot` | Automated dependency updates |
| `lgtm-com` | LGTM semantic code analysis (deprecated, replaced by CodeQL) |
| `github-actions` | All GitHub Actions workflows |

**What to extract:**
- Full list of check suite apps that appeared on recent PRs
- Whether each app is in the required status checks list (i.e. can PRs merge without it passing?)
- Failure/success pattern across sampled PRs (consistent failures = gate not enforced)
- Presence/absence of security-focused scanners

---

## Repository Metadata

```sh
# General repo info (default branch, topics, visibility, language)
gh repo view --json name,description,defaultBranchRef,primaryLanguage,repositoryTopics,isPrivate

# List all workflow files
gh api repos/{owner}/{repo}/contents/.github/workflows --jq '.[].name'

# Recent workflow runs (last 20, all workflows)
gh run list --limit 20 --json workflowName,status,conclusion,createdAt,headBranch
```

**What to extract:**
- Default branch name (for correct branch protection queries)
- Recent workflow run conclusions (flaky / always-failing pipelines)
- Any workflows with repeated failures

---

## Labels

```sh
# All labels defined in the repo
gh label list --json name,description,color
```

**What to extract:**
- Full label taxonomy (compare against what's actually used on issues)
- Missing labels that would aid QA classification (e.g. no `Regression`, no `Test-coverage`)

---

## Fallback: Static Exports

If `gh` is not available or not authenticated, look for these files in `.github/quality-queen/input-data/`:

| File pattern | Contents |
|---|---|
| `*Board*.tsv` / `*Board*.csv` | Full board export (all statuses) |
| `*Backlog*.tsv` / `*Backlog*.csv` | Backlog items |
| `*iteration*.tsv` / `*iteration*.csv` | Current sprint/iteration items |

When using static exports, note the export date and treat all data as potentially stale.
