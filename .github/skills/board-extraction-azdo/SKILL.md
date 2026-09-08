---
name: board-extraction-azdo
description: "Extract board structure, sprints, work items, and field usage from an Azure DevOps project using the Azure DevOps REST API. Produces structured board data consumed by project-structure-analysis. Triggers: Azure DevOps board, Azure DevOps work items, ADO sprint, ADO backlog, ADO board, VSTS, dev.azure.com."
argument-hint: "Provide the Azure DevOps organization URL (e.g. https://dev.azure.com/myorg), the project name, and the team name if known."
---

# Board Extraction — Azure DevOps

Extracts board structure, sprint data, work item quality, and field usage from an Azure DevOps project using the Azure DevOps REST API. Produces structured output consumed by the `project-structure-analysis` skill (Steps 2 and 6).

## When to Use

- When `project-structure-analysis` detects the board source is Azure DevOps
- When auditing Azure DevOps board column flow, work item quality, or sprint state standalone
- When the existing board data in the project structure document is stale

## Output Contract

This skill produces a structured summary block that `project-structure-analysis` stores and uses to fill its output document. Record the following fields:

| Field | Content |
|---|---|
| `data-source` | `azdo-api` or `static-export` |
| `board-columns` | Ordered list of column names as they appear on the board |
| `workflow-states` | All work item states mapped to their board column |
| `custom-fields` | Fields in use (Priority, Story Points, Acceptance Criteria, Area Path, etc.) and consistency rating |
| `dor-dod-status` | `documented` / `informal` / `not-defined` |
| `issues-in-progress` | Active sprint work items (ID, title, state, assigned-to) |
| `issues-security-nfr` | Work items tagged Security, Performance, Accessibility, NFR, or Technical Debt |
| `issues-process-qa` | Work items related to test tooling, environments, DoR/DoD, QA infrastructure |
| `field-consistency` | % of user stories missing Story Points, Acceptance Criteria, or Priority |

See [azdo-api.md](./references/azdo-api.md) for the full set of Azure DevOps REST API calls used in this skill.

---

## Step A — Verify Azure DevOps API Access

Confirm the following inputs are available before proceeding. First check `.github/quality-queen/input-data/project-secrets.env` for pre-filled values; only ask the user for inputs that are still missing.

| Input | Source |
|---|---|
| `ADO_ORG_URL` | e.g. `https://dev.azure.com/myorg` |
| `ADO_PROJECT` | e.g. `MyProject` |
| `ADO_TEAM` | e.g. `MyProject Team` (often `<project> Team` by default) |
| `ADO_PAT` | Personal Access Token with at minimum `Work Items (Read)` scope — never log or store this |

```sh
# Verify connectivity and authentication (base64-encode :PAT for Basic auth)
$base64 = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(":$ADO_PAT"))
Invoke-RestMethod -Uri "$ADO_ORG_URL/$ADO_PROJECT/_apis/wit/workitemtypes?api-version=7.1" `
  -Headers @{ Authorization = "Basic $base64" }
```

- If the call returns a list of work item types → proceed with API calls. Record `data-source: azdo-api`.
- If authentication fails → fall back to static exports in `.github/quality-queen/input-data/` (`.tsv`, `.csv`). Record `data-source: static-export` and note the export date.

---

## Step B — Query Board Structure

```sh
# List boards for the team
Invoke-RestMethod -Uri "$ADO_ORG_URL/$ADO_PROJECT/$ADO_TEAM/_apis/work/boards?api-version=7.1" `
  -Headers @{ Authorization = "Basic $base64" }

# Get board column configuration (columns, states, DoD rules per column)
Invoke-RestMethod -Uri "$ADO_ORG_URL/$ADO_PROJECT/$ADO_TEAM/_apis/work/boards/$BOARD_ID?api-version=7.1" `
  -Headers @{ Authorization = "Basic $base64" }
```

Extract:
- Column names in flow order (e.g. New → Active → Resolved → Closed)
- Which work item states map to each column
- Split columns (Doing / Done sub-columns within a column)
- Definition of Done rules per column — Azure DevOps boards support per-column DoD checklists. Record whether any columns have DoD rules configured.
- Any swimlanes in use

---

## Step C — Query Active Sprint and Work Items

```sh
# Get the current sprint (iteration)
Invoke-RestMethod -Uri "$ADO_ORG_URL/$ADO_PROJECT/$ADO_TEAM/_apis/work/teamsettings/iterations?`$timeframe=current&api-version=7.1" `
  -Headers @{ Authorization = "Basic $base64" }

# Work items in the current sprint (returns ID + URL only)
Invoke-RestMethod -Uri "$ADO_ORG_URL/$ADO_PROJECT/$ADO_TEAM/_apis/work/teamsettings/iterations/$ITERATION_ID/workitems?api-version=7.1" `
  -Headers @{ Authorization = "Basic $base64" }

# Batch-fetch work item details (IDs from sprint query above, max 200 per request)
$ids = "1,2,3,..."
Invoke-RestMethod -Uri "$ADO_ORG_URL/$ADO_PROJECT/_apis/wit/workitems?ids=$ids&fields=System.Id,System.Title,System.State,System.AssignedTo,System.WorkItemType,Microsoft.VSTS.Common.Priority,Microsoft.VSTS.Scheduling.StoryPoints,System.Tags,Microsoft.VSTS.Common.AcceptanceCriteria&api-version=7.1" `
  -Headers @{ Authorization = "Basic $base64" }
```

Categorize sprint work items into:

### In Progress / Ready for Work
Items with state Active, In Progress, Committed, or equivalent active column state.

### Security & Non-Functional
Items with tags or titles matching: Security, Performance, Accessibility, NFR, Technical Debt. Use WIQL:

```sh
# WIQL query for security/NFR items
$wiqlBody = '{"query": "SELECT [System.Id],[System.Title],[System.State],[System.Tags] FROM WorkItems WHERE [System.TeamProject] = \"' + $ADO_PROJECT + '\" AND ([System.Tags] CONTAINS \"Security\" OR [System.Tags] CONTAINS \"NFR\" OR [System.Tags] CONTAINS \"Performance\" OR [System.Tags] CONTAINS \"Accessibility\") ORDER BY [System.ChangedDate] DESC"}'
Invoke-RestMethod -Uri "$ADO_ORG_URL/$ADO_PROJECT/_apis/wit/wiql?api-version=7.1" `
  -Method POST -Body $wiqlBody -ContentType "application/json" `
  -Headers @{ Authorization = "Basic $base64" }
```

### Process / QA Infrastructure
Work items related to test tooling, environments, DoR/DoD, monitoring:

```sh
$wiqlBody = '{"query": "SELECT [System.Id],[System.Title],[System.State],[System.Tags] FROM WorkItems WHERE [System.TeamProject] = \"' + $ADO_PROJECT + '\" AND (CONTAINS([System.Title],\"test automation\") OR CONTAINS([System.Title],\"CI\") OR CONTAINS([System.Title],\"pipeline\") OR CONTAINS([System.Title],\"DoD\") OR CONTAINS([System.Title],\"DoR\") OR CONTAINS([System.Title],\"monitoring\")) ORDER BY [System.ChangedDate] DESC"}'
Invoke-RestMethod -Uri "$ADO_ORG_URL/$ADO_PROJECT/_apis/wit/wiql?api-version=7.1" `
  -Method POST -Body $wiqlBody -ContentType "application/json" `
  -Headers @{ Authorization = "Basic $base64" }
```

---

## Step D — Assess Work Item Field Usage

Sample the 50 most recently updated user stories and check field consistency:

```sh
$wiqlBody = '{"query": "SELECT [System.Id] FROM WorkItems WHERE [System.TeamProject] = \"' + $ADO_PROJECT + '\" AND [System.WorkItemType] = \"User Story\" ORDER BY [System.ChangedDate] DESC"}'
$result = Invoke-RestMethod -Uri "$ADO_ORG_URL/$ADO_PROJECT/_apis/wit/wiql?`$top=50&api-version=7.1" `
  -Method POST -Body $wiqlBody -ContentType "application/json" `
  -Headers @{ Authorization = "Basic $base64" }

# Batch-fetch full details for the sampled IDs
$ids = ($result.workItems | Select-Object -First 50 | ForEach-Object { $_.id }) -join ","
Invoke-RestMethod -Uri "$ADO_ORG_URL/$ADO_PROJECT/_apis/wit/workitems?ids=$ids&fields=System.Id,System.Title,Microsoft.VSTS.Scheduling.StoryPoints,Microsoft.VSTS.Common.Priority,Microsoft.VSTS.Common.AcceptanceCriteria,System.Description,System.Tags,System.AssignedTo&api-version=7.1" `
  -Headers @{ Authorization = "Basic $base64" }
```

For each sampled work item, check whether the following fields are populated:

| Field | ADO field reference | QA relevance |
|---|---|---|
| Story Points | `Microsoft.VSTS.Scheduling.StoryPoints` | Estimation completeness |
| Priority | `Microsoft.VSTS.Common.Priority` | Triage and risk visibility |
| Acceptance Criteria | `Microsoft.VSTS.Common.AcceptanceCriteria` | Readiness for development |
| Tags | `System.Tags` | Classification and filtering |
| Assigned To | `System.AssignedTo` | Ownership clarity |

Calculate and record:
- `% user stories missing Story Points`
- `% user stories missing Acceptance Criteria`
- `% user stories missing Priority`

Flag work items where `AcceptanceCriteria` is null or empty — these are not ready for development.

---

## Step E — Return Structured Summary

After completing Steps A–D, compile the output contract fields defined at the top of this document. The calling skill (`project-structure-analysis`) stores this summary and uses it to fill Sections 2 (data source note) and 6 (board and issue data) of the output document.
