# Azure DevOps REST API Reference

Reference for Azure DevOps REST API calls used during board extraction. All calls use Basic Auth with a Personal Access Token (PAT). Replace placeholder values before running.

---

## Prerequisites

| Variable | Description |
|---|---|
| `ADO_ORG_URL` | e.g. `https://dev.azure.com/myorg` |
| `ADO_PROJECT` | Project name, e.g. `MyProject` |
| `ADO_TEAM` | Team name, e.g. `MyProject Team` (default is `<project> Team`) |
| `ADO_PAT` | Personal Access Token — never log or commit this |
| `$base64` | Base64-encoded `:PAT` string used in the Authorization header |
| `BOARD_ID` | Board ID or name (find via the board list call) |
| `ITERATION_ID` | Sprint iteration path or ID (find via the iteration list call) |

```powershell
# Build the auth header once, reuse for all calls
$base64 = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(":$ADO_PAT"))
$headers = @{ Authorization = "Basic $base64" }
```

---

## Authentication

```powershell
# Verify authentication — returns list of work item types
Invoke-RestMethod -Uri "$ADO_ORG_URL/$ADO_PROJECT/_apis/wit/workitemtypes?api-version=7.1" `
  -Headers $headers
```

---

## Boards

```powershell
# List all boards for the team
Invoke-RestMethod -Uri "$ADO_ORG_URL/$ADO_PROJECT/$ADO_TEAM/_apis/work/boards?api-version=7.1" `
  -Headers $headers

# Get full board configuration (columns, states, DoD rules, swimlanes)
Invoke-RestMethod -Uri "$ADO_ORG_URL/$ADO_PROJECT/$ADO_TEAM/_apis/work/boards/$BOARD_ID?api-version=7.1" `
  -Headers $headers
```

**What to extract:**
- Board ID and name
- Column names in flow order
- Which work item states map to each column
- Split columns (Doing / Done sub-columns)
- Per-column DoD checklists (`columnFields.definition`)
- Swimlane names (if any)

---

## Iterations (Sprints)

```powershell
# All iterations for the team
Invoke-RestMethod -Uri "$ADO_ORG_URL/$ADO_PROJECT/$ADO_TEAM/_apis/work/teamsettings/iterations?api-version=7.1" `
  -Headers $headers

# Current sprint only
Invoke-RestMethod -Uri "$ADO_ORG_URL/$ADO_PROJECT/$ADO_TEAM/_apis/work/teamsettings/iterations?`$timeframe=current&api-version=7.1" `
  -Headers $headers
```

---

## Work Items

```powershell
# Work items in a specific sprint (returns IDs + URLs)
Invoke-RestMethod -Uri "$ADO_ORG_URL/$ADO_PROJECT/$ADO_TEAM/_apis/work/teamsettings/iterations/$ITERATION_ID/workitems?api-version=7.1" `
  -Headers $headers

# Batch-fetch work item details (max 200 IDs per request)
$ids = "1,2,3,..."
Invoke-RestMethod -Uri "$ADO_ORG_URL/$ADO_PROJECT/_apis/wit/workitems?ids=$ids&fields=System.Id,System.Title,System.State,System.AssignedTo,System.WorkItemType,Microsoft.VSTS.Common.Priority,Microsoft.VSTS.Scheduling.StoryPoints,System.Tags,Microsoft.VSTS.Common.AcceptanceCriteria&api-version=7.1" `
  -Headers $headers
```

**Common field references:**

| Field | Reference |
|---|---|
| ID | `System.Id` |
| Title | `System.Title` |
| State | `System.State` |
| Work Item Type | `System.WorkItemType` |
| Assigned To | `System.AssignedTo` |
| Priority | `Microsoft.VSTS.Common.Priority` |
| Story Points | `Microsoft.VSTS.Scheduling.StoryPoints` |
| Acceptance Criteria | `Microsoft.VSTS.Common.AcceptanceCriteria` |
| Tags | `System.Tags` |
| Area Path | `System.AreaPath` |
| Iteration Path | `System.IterationPath` |
| Description | `System.Description` |

To discover all available fields for a project (including custom fields):

```powershell
# List all work item fields
Invoke-RestMethod -Uri "$ADO_ORG_URL/$ADO_PROJECT/_apis/wit/fields?api-version=7.1" `
  -Headers $headers
```

---

## WIQL Queries

WIQL (Work Item Query Language) is the ADO equivalent of JQL. Use it for filtered queries.

```powershell
# Helper: run any WIQL query
function Invoke-WIQL($query) {
  $body = '{"query": "' + $query + '"}'
  Invoke-RestMethod -Uri "$ADO_ORG_URL/$ADO_PROJECT/_apis/wit/wiql?api-version=7.1" `
    -Method POST -Body $body -ContentType "application/json" -Headers $headers
}

# Security and NFR items
Invoke-WIQL "SELECT [System.Id],[System.Title],[System.State],[System.Tags] FROM WorkItems WHERE [System.TeamProject] = '$ADO_PROJECT' AND ([System.Tags] CONTAINS 'Security' OR [System.Tags] CONTAINS 'NFR' OR [System.Tags] CONTAINS 'Performance' OR [System.Tags] CONTAINS 'Accessibility') ORDER BY [System.ChangedDate] DESC"

# QA / process infrastructure items
Invoke-WIQL "SELECT [System.Id],[System.Title],[System.State] FROM WorkItems WHERE [System.TeamProject] = '$ADO_PROJECT' AND (CONTAINS([System.Title],'test automation') OR CONTAINS([System.Title],'CI') OR CONTAINS([System.Title],'pipeline') OR CONTAINS([System.Title],'DoD') OR CONTAINS([System.Title],'DoR') OR CONTAINS([System.Title],'monitoring')) ORDER BY [System.ChangedDate] DESC"

# Recent user stories for field consistency check (top 50)
Invoke-WIQL "SELECT [System.Id] FROM WorkItems WHERE [System.TeamProject] = '$ADO_PROJECT' AND [System.WorkItemType] = 'User Story' ORDER BY [System.ChangedDate] DESC"
# Then batch-fetch details for the returned IDs
```

---

## Pull Requests (Azure Repos)

If the repository is hosted in Azure Repos (not GitHub), query PRs from the Azure DevOps Git API:

```powershell
# List open PRs
Invoke-RestMethod -Uri "$ADO_ORG_URL/$ADO_PROJECT/_apis/git/pullrequests?searchCriteria.status=active&api-version=7.1" `
  -Headers $headers

# Merged PRs (sample of last 20)
Invoke-RestMethod -Uri "$ADO_ORG_URL/$ADO_PROJECT/_apis/git/pullrequests?searchCriteria.status=completed&`$top=20&api-version=7.1" `
  -Headers $headers
```

**What to extract:**
- PRs without required reviewers or without approval
- Long-lived open PRs (compare `creationDate` to today)
- Any PRs linked to work items (indicates traceability)

---

## Branch Policies

```powershell
# List all branch policies in the project
Invoke-RestMethod -Uri "$ADO_ORG_URL/$ADO_PROJECT/_apis/policy/configurations?api-version=7.1" `
  -Headers $headers
```

**What to extract:**
- Minimum reviewer count policy on `main` / `master`
- Required build policy (CI must pass before merge)
- Comment resolution policy
- Work item linking policy (enforced or optional)

---

## Process and Work Item Types

```powershell
# Get the process template used by the project (Agile / Scrum / CMMI / custom)
Invoke-RestMethod -Uri "$ADO_ORG_URL/_apis/projects/$ADO_PROJECT?includeCapabilities=true&api-version=7.1" `
  -Headers $headers

# All work item types in the project
Invoke-RestMethod -Uri "$ADO_ORG_URL/$ADO_PROJECT/_apis/wit/workitemtypes?api-version=7.1" `
  -Headers $headers
```

**What to extract:**
- Process template name (Agile uses Story/Task/Bug; Scrum uses PBI/Task/Bug)
- Available work item types (affects field names — e.g. `Story Points` vs `Effort`)

---

## Fallback: Static Exports

If API access is unavailable, look for these files in `.github/quality-queen/input-data/`:

| File pattern | Contents |
|---|---|
| `*Board*.tsv` / `*Board*.csv` | Full board export (all columns and states) |
| `*Backlog*.tsv` / `*Backlog*.csv` | Backlog work items |
| `*iteration*.tsv` / `*sprint*.tsv` | Current sprint items |

When using static exports, note the export date and treat all data as potentially stale.
