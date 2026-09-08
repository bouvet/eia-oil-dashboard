---
name: board-extraction-jira
description: "Extract board structure, sprints, issues, and field usage from a Jira project using the Atlassian MCP server (preferred) or Jira REST API (fallback). Produces structured board data consumed by project-structure-analysis. Triggers: Jira board, Jira issues, Jira sprint, Jira project, JQL, Atlassian, MCP."
argument-hint: "Provide the Jira base URL (e.g. https://company.atlassian.net), the project key, and the board ID if known."
---

# Board Extraction — Jira

Extracts board structure, sprint data, issue quality, and field usage from a Jira project using the **Atlassian MCP server** (preferred) or the Jira REST API (fallback). Produces structured output consumed by the `project-structure-analysis` skill (Steps 2 and 6).

## When to Use

- When `project-structure-analysis` detects the board source is Jira
- When auditing Jira issue quality, board column flow, or workflow configuration standalone
- When the existing board data in the project structure document is stale

## Output Contract

This skill produces a structured summary block that `project-structure-analysis` stores and uses to fill its output document. Record the following fields:

| Field | Content |
|---|---|
| `data-source` | `atlassian-mcp`, `jira-api`, or `static-export` |
| `board-columns` | Ordered list of column names as they appear on the board |
| `workflow-statuses` | All statuses mapped to their board column |
| `custom-fields` | Fields in use (Priority, Story Points, Labels, etc.) and consistency rating |
| `dor-dod-status` | `documented` / `informal` / `not-defined` |
| `issues-in-progress` | Active sprint issues (key, summary, status, assignee) |
| `issues-security-nfr` | Issues labelled Security, Performance, Accessibility, NFR or matching JQL filter |
| `issues-process-qa` | Issues related to test tooling, environments, DoR/DoD, QA infrastructure |
| `field-consistency` | % of issues missing Story Points, Priority, or Acceptance Criteria |

See [jira-api.md](./references/jira-api.md) for the full set of Jira API calls used in this skill.

---

## Access Method Priority

Use the following priority order when extracting Jira board data:

| Priority | Method | When to Use |
|---|---|---|
| 1 (preferred) | **Atlassian MCP server** | MCP server is configured and accessible. Provides structured access to boards, sprints, issues, and fields without manual curl/auth setup. |
| 2 (fallback) | **Jira REST API** (curl) | MCP server is not available. Requires manual API token setup. |
| 3 (last resort) | **Static exports** | Neither MCP nor API access is available. Use `.tsv`/`.csv` files from `.github/quality-queen/input-data/`. |

### Detecting Atlassian MCP Availability

Before falling back to REST API calls, check if the Atlassian MCP server is available:

1. Check if MCP tools prefixed with `atlassian` or `jira` are available (e.g. `mcp_atlassian_jira_get_board`, `mcp_atlassian_jira_search_issues`).
2. If MCP tools are available, use them for all board, sprint, and issue queries. Record `data-source: atlassian-mcp`.
3. If MCP tools are not available, proceed to Step A (REST API authentication).

### Using Atlassian MCP

When the Atlassian MCP server is available, use its tools to:

- **Get boards:** Query boards for the project to find the board ID and type (Scrum/Kanban)
- **Get board configuration:** Retrieve column names, workflow statuses per column, and swimlanes
- **Get sprints:** List sprints and identify the active one
- **Get issues:** Query issues in the active sprint or by JQL, with fields (summary, status, assignee, priority, story points, labels, description)
- **Search issues:** Use JQL to find security/NFR issues and QA/process issues

Map the MCP responses to the same output contract fields defined above. The data structure may differ from raw REST API responses, but the extracted information should be identical.

---

## Step A — Verify Jira API Access (REST API Fallback)

> **Skip this step if using Atlassian MCP.** Only proceed here if MCP tools are not available.

Confirm the following inputs are available before proceeding. First check `.github/quality-queen/input-data/project-secrets.env` for pre-filled values; only ask the user for inputs that are still missing.

| Input | Source |
|---|---|
| `JIRA_BASE_URL` | e.g. `https://company.atlassian.net` |
| `JIRA_PROJECT_KEY` | e.g. `PROJ`, `BA`, `QA` |
| `JIRA_API_TOKEN` | Personal API token (never log or store this) |
| `JIRA_USER_EMAIL` | Email address associated with the token |

```sh
# Verify connectivity and authentication
curl -u "$JIRA_USER_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/api/3/myself" \
  -H "Accept: application/json"
```

- If this returns a 200 with a user object → proceed with API calls. Record `data-source: jira-api`.
- If this fails → fall back to static exports in `.github/quality-queen/input-data/` (`.tsv`, `.csv`). Record `data-source: static-export` and note the export date.

---

## Step B — Query Board Structure

```sh
# List all boards for the project
curl -u "$JIRA_USER_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/agile/1.0/board?projectKeyOrId=$JIRA_PROJECT_KEY" \
  -H "Accept: application/json"

# Get board configuration (columns, statuses per column)
curl -u "$JIRA_USER_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/agile/1.0/board/$JIRA_BOARD_ID/configuration" \
  -H "Accept: application/json"
```

Extract:
- Column names in flow order (e.g. Backlog → To Do → In Progress → Review → Done)
- Which workflow statuses map to each column
- Any sub-columns or swimlanes in use
- Any DoR/DoD wording in column descriptions or board configuration notes

---

## Step C — Query Active Sprint and Issues

```sh
# Get the active sprint
curl -u "$JIRA_USER_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/agile/1.0/board/$JIRA_BOARD_ID/sprint?state=active" \
  -H "Accept: application/json"

# Issues in active sprint
curl -u "$JIRA_USER_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/agile/1.0/board/$JIRA_BOARD_ID/sprint/$JIRA_SPRINT_ID/issue?maxResults=100&fields=summary,status,assignee,priority,story_points,labels,customfield_10016" \
  -H "Accept: application/json"
```

Categorize active sprint issues into:

### In Progress / Ready for Work
Issues with status In Progress, In Review, or equivalent active column status.

### Security & Non-Functional
Issues with labels or issue types matching: Security, Performance, Accessibility, NFR, Technical Debt. Use JQL:

```sh
# JQL via search API
curl -u "$JIRA_USER_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/api/3/search?jql=project=$JIRA_PROJECT_KEY+AND+labels+in+(Security,Performance,Accessibility,NFR)&maxResults=50&fields=summary,status,priority,labels" \
  -H "Accept: application/json"
```

### Process / QA Infrastructure
Issues related to test tooling, environments, issue templates, DoR/DoD, monitoring:

```sh
curl -u "$JIRA_USER_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/api/3/search?jql=project=$JIRA_PROJECT_KEY+AND+text+~+%22test+automation+OR+CI+OR+pipeline+OR+DoD+OR+DoR+OR+monitoring%22&maxResults=50&fields=summary,status,labels" \
  -H "Accept: application/json"
```

---

## Step D — Assess Issue Field Usage

Sample the 50 most recently updated issues and check field consistency:

```sh
curl -u "$JIRA_USER_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/api/3/search?jql=project=$JIRA_PROJECT_KEY+ORDER+BY+updated+DESC&maxResults=50&fields=summary,priority,story_points,customfield_10016,description,labels,assignee" \
  -H "Accept: application/json"
```

For each issue record whether the following fields are populated:

| Field | Jira field name | QA relevance |
|---|---|---|
| Story Points | `customfield_10016` (or `story_points`) | Estimation completeness |
| Priority | `priority` | Triage and risk visibility |
| Acceptance Criteria | In description body or custom field | Readiness for development |
| Labels | `labels` | Classification and filtering |
| Assignee | `assignee` | Ownership clarity |

Calculate and record:
- `% issues missing Story Points`
- `% issues missing Priority`
- `% stories with no acceptance criteria text in description`

Flag issues where the description is empty or shorter than 50 characters — these typically lack acceptance criteria.

---

## Step E — Return Structured Summary

After completing Steps A–D, compile the output contract fields defined at the top of this document. The calling skill (`project-structure-analysis`) stores this summary and uses it to fill Sections 2 (data source note) and 6 (board and issue data) of the output document.
