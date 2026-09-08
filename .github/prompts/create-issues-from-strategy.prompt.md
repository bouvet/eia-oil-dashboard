---
description: Extract findings and actions from a QA strategy and create work items on the team's chosen platform.
agent: Quality Queen
---

# Create Work Items from QA Strategy Findings

You are acting as a QA automation assistant. Your goal is to read the QA strategy document, extract the findings and actions, present them to the user for selection, and create work items on the team's chosen platform.

## Inputs

- **Strategy file:** `.github/quality-queen/output-data/qa-strategy-${input:projectName:Enter the project name (must match the strategy filename)}.md`
- **Severity threshold:** `${input:severityThreshold:Minimum severity to include (Critical / High / Medium / Low)}`
- **Platform:** `${input:platform:Work item platform (github / jira / azdevops)}`

## Instructions

### Step 1 — Extract findings and actions

1. Open the strategy file above.
2. Locate **§7 Findings and Actions** (or equivalent section containing the findings table and action list).
3. Extract all findings at or above the specified severity threshold.
4. For each finding, capture:
   - Severity (Critical / High / Medium / Low)
   - Finding description (one sentence)
   - Evidence / location reference
   - Linked action (if one exists in the actions table)
   - Proposed owner role (from the action table, if available)

### Step 2 — Present findings for selection

Present the extracted findings as a numbered list to the user, grouped by severity. For each finding, show:

```
[n] [Severity] — Finding description
    Location: evidence/path
    Action: proposed action (or "No action defined")
    Owner: role (or "Unassigned")
```

Then ask the user: **"Which findings should I create work items for? Enter the numbers (e.g. 1,3,5-7) or 'all'."**

Wait for the user's response before proceeding.

### Step 3 — Confirm work item details

For each selected finding, propose the work item that will be created:

| Field | Value |
|---|---|
| Title | `[Chore] <action title or finding summary>` |
| Labels / Tags | `QA`, `<severity as label if it exists>` |
| Body / Description | Structured body (see template below) |

Present all proposed work items in a table and ask: **"Shall I create these work items? (yes / no / edit)"**

If the user says "edit", ask which item to modify and what to change.

### Step 4 — Create work items

Use the body template below for every work item regardless of platform:

```markdown
## Summary

<One-sentence finding description>

## Evidence

<Location / file path / metric from the strategy>

## Proposed Action

<Action from the strategy, or "Define action during refinement">

## Expected Impact

<Expected impact from the action table, or "To be defined">

## Source

This work item was generated from the QA strategy: `.github/quality-queen/output-data/qa-strategy-<projectName>.md`
Severity: **<severity>**
```

#### GitHub

```sh
gh issue create --title "<title>" --label "QA" --body "<body>"
```

After creating each issue, report the issue number and URL.

#### Jira

```sh
curl -s -X POST "https://<domain>.atlassian.net/rest/api/3/issue" \
  -H "Authorization: Basic <base64 email:token>" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "project": {"key": "<PROJECT_KEY>"},
      "summary": "<title>",
      "description": <ADF body>,
      "issuetype": {"name": "Task"},
      "labels": ["QA", "<severity>"]
    }
  }'
```

Before creating Jira issues, ask the user for:
- Jira domain (e.g. `myteam.atlassian.net`)
- Project key (e.g. `PROJ`)
- Authentication method — suggest using a `.env` file or environment variable (`JIRA_AUTH`) for the Base64-encoded `email:api-token`. **Never hardcode credentials.**

After creating each issue, report the issue key and URL.

#### Azure DevOps

```sh
az boards work-item create \
  --title "<title>" \
  --type "Task" \
  --description "<body as HTML>" \
  --org "https://dev.azure.com/<org>" \
  --project "<project>" \
  --fields "System.Tags=QA;<severity>"
```

Before creating Azure DevOps work items, ask the user for:
- Organization URL (e.g. `https://dev.azure.com/myorg`)
- Project name
- Work item type (default: `Task`)

Verify the user is logged in with `az account show`. If not, instruct them to run `az login`.

After creating each work item, report the work item ID and URL.

### Step 5 — Optional: Add to project board

After all work items are created, ask: **"Would you like to add these items to a project board?"**

#### GitHub

1. Check if `gh` has `project` scope: run `gh auth status` and look for `project` in scopes.
2. If scope is missing, inform the user they need to run `gh auth refresh -s project` and authenticate in the browser, then retry.
3. If scope is available, add each issue to the board:
   ```sh
   gh project item-add <project-number> --owner <org> --url <issue-url>
   ```

#### Jira

Jira issues are automatically visible on the board for their project. If the user wants a specific sprint or board placement, ask for the sprint name/ID and move the issue:
```sh
curl -s -X POST "https://<domain>.atlassian.net/rest/agile/1.0/sprint/<sprintId>/issue" \
  -H "Authorization: Basic <JIRA_AUTH>" \
  -H "Content-Type: application/json" \
  -d '{"issues": ["<issueKey>"]}'
```

#### Azure DevOps

Azure DevOps work items appear on the board based on their area path and iteration. If the user wants a specific iteration:
```sh
az boards work-item update --id <id> --org "<org-url>" --project "<project>" \
  --fields "System.IterationPath=<project>\\<iteration>"
```

Report which items were successfully added or moved.

## Rules

- Never create issues without explicit user confirmation.
- If the strategy file does not exist or has no findings section, inform the user and stop.
- If `gh` is not authenticated, inform the user and stop.
- Do not create duplicate issues — before creating, search for existing issues with similar titles using `gh issue list --search "<keywords>" --json number,title`.
- Apply the `QA` label to all created issues. If a severity label exists in the repo (e.g. `Top priority`), apply it for Critical findings.
- Keep issue titles concise (max 80 characters) and action-oriented.

## Run Checklist and Validation

1. At the **start** of this run, read `.github/quality-queen/input-data/prompt-run-checklist.md` and complete all items in the **Pre-run** and **create-issues-from-strategy** sections.
2. At the **end** of this run, invoke the `output-validation` skill with `promptType = create-issues` against the work items created.
3. Report the validation summary to the user. If critical failures exist, fix them before finishing.
