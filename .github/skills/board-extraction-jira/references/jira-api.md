# Jira API Reference

Reference for Jira data extraction. The **preferred method** is the Atlassian MCP server; the REST API calls below are the **fallback** when MCP is not available.

---

## Preferred: Atlassian MCP Server

When the Atlassian MCP server is configured and available, use its tools instead of manual curl commands. The MCP server handles authentication automatically and provides structured responses.

**Typical MCP tool names** (exact names depend on the MCP server configuration):

| Operation | MCP Tool | Equivalent REST API |
|---|---|---|
| List boards | `mcp_atlassian_jira_get_boards` | `GET /rest/agile/1.0/board?projectKeyOrId=...` |
| Board configuration | `mcp_atlassian_jira_get_board_configuration` | `GET /rest/agile/1.0/board/{id}/configuration` |
| List sprints | `mcp_atlassian_jira_get_sprints` | `GET /rest/agile/1.0/board/{id}/sprint` |
| Sprint issues | `mcp_atlassian_jira_get_sprint_issues` | `GET /rest/agile/1.0/board/{id}/sprint/{sprintId}/issue` |
| Search issues (JQL) | `mcp_atlassian_jira_search` | `GET /rest/api/3/search?jql=...` |
| Get issue details | `mcp_atlassian_jira_get_issue` | `GET /rest/api/3/issue/{key}` |
| List fields | `mcp_atlassian_jira_get_fields` | `GET /rest/api/3/field` |
| Project statuses | `mcp_atlassian_jira_get_project_statuses` | `GET /rest/api/3/project/{key}/statuses` |

> **Note:** MCP tool names may vary by server version. Use tool discovery to find the exact names available in your session.

When using MCP, record `data-source: atlassian-mcp` in the output contract.

---

## Fallback: REST API (curl)

Use the REST API calls below only when Atlassian MCP is not available. All calls use Basic Auth (`email:api-token`). Replace placeholder values before running.

---

## Prerequisites

| Variable | Description |
|---|---|
| `JIRA_BASE_URL` | e.g. `https://company.atlassian.net` |
| `JIRA_PROJECT_KEY` | e.g. `PROJ` |
| `JIRA_BOARD_ID` | Numeric board ID (find via the board list call) |
| `JIRA_SPRINT_ID` | Numeric sprint ID (find via the sprint list call) |
| `JIRA_USER_EMAIL` | Email address associated with the API token |
| `JIRA_API_TOKEN` | Personal API token — never log or commit this |

---

## Authentication

```sh
# Verify authentication and retrieve current user
curl -u "$JIRA_USER_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/api/3/myself" \
  -H "Accept: application/json"
```

---

## Boards

```sh
# List all boards for a project
curl -u "$JIRA_USER_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/agile/1.0/board?projectKeyOrId=$JIRA_PROJECT_KEY" \
  -H "Accept: application/json"

# Get board configuration (columns, statuses per column, swimlanes)
curl -u "$JIRA_USER_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/agile/1.0/board/$JIRA_BOARD_ID/configuration" \
  -H "Accept: application/json"
```

**What to extract:**
- Board ID and type (`scrum` / `kanban`)
- Column names in flow order
- Which workflow statuses map to each column
- Swimlane configuration

---

## Sprints

```sh
# List all sprints for a board
curl -u "$JIRA_USER_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/agile/1.0/board/$JIRA_BOARD_ID/sprint" \
  -H "Accept: application/json"

# Get only the active sprint
curl -u "$JIRA_USER_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/agile/1.0/board/$JIRA_BOARD_ID/sprint?state=active" \
  -H "Accept: application/json"
```

---

## Issues

```sh
# Issues in a specific sprint
curl -u "$JIRA_USER_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/agile/1.0/board/$JIRA_BOARD_ID/sprint/$JIRA_SPRINT_ID/issue?maxResults=100&fields=summary,status,assignee,priority,customfield_10016,labels" \
  -H "Accept: application/json"

# JQL search — recent issues for field consistency check
curl -u "$JIRA_USER_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/api/3/search?jql=project=$JIRA_PROJECT_KEY+ORDER+BY+updated+DESC&maxResults=50&fields=summary,priority,customfield_10016,description,labels,assignee" \
  -H "Accept: application/json"

# Security and NFR issues
curl -u "$JIRA_USER_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/api/3/search?jql=project=$JIRA_PROJECT_KEY+AND+labels+in+(Security,Performance,Accessibility,NFR)&maxResults=50&fields=summary,status,priority,labels" \
  -H "Accept: application/json"

# Issues related to QA/test infrastructure (keyword search)
curl -u "$JIRA_USER_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/api/3/search?jql=project=$JIRA_PROJECT_KEY+AND+text+~+%22test+automation+OR+CI+OR+pipeline+OR+DoD+OR+DoR%22&maxResults=50&fields=summary,status,labels" \
  -H "Accept: application/json"
```

**Common custom field IDs:**

| Field | Default custom field ID | Notes |
|---|---|---|
| Story Points | `customfield_10016` | May vary — confirm via field metadata |
| Sprint | `customfield_10020` | May vary |
| Acceptance Criteria | `customfield_10014` or in description | Team-dependent |

To discover custom field IDs for a specific instance:

```sh
# List all fields (includes custom fields with their IDs)
curl -u "$JIRA_USER_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/api/3/field" \
  -H "Accept: application/json"
```

---

## Workflow Statuses

```sh
# All statuses in the project
curl -u "$JIRA_USER_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/api/3/project/$JIRA_PROJECT_KEY/statuses" \
  -H "Accept: application/json"
```

---

## Fallback: Static Exports

If API access is unavailable, look for these files in `.github/quality-queen/input-data/`:

| File pattern | Contents |
|---|---|
| `*Board*.tsv` / `*Board*.csv` | Full board export (all statuses) |
| `*Backlog*.tsv` / `*Backlog*.csv` | Backlog items |
| `*iteration*.tsv` / `*sprint*.tsv` | Current sprint items |

When using static exports, note the export date and treat all data as potentially stale.
