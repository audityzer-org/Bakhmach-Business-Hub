# ClickUp Epic Sync Template

## Purpose

This template describes how to sync Epic tasks from GitHub (EPIC-*.md files and EPICS-ROADMAP-CONSOLIDATED.md) to ClickUp as a system of record for tracking execution, SLO metrics, and team ownership.

## ClickUp Folder/Space Structure

- **Space**: `EXECUTION-PHASE-2-Q1-2026`
- **Folders**:
  - `SECURITY-EDGE-EPIC` → Link to [EPIC-SECURITY-EDGE.md](./epics/EPIC-SECURITY-EDGE.md)
  - `RELIABILITY-QUEUES-EPIC` → Link to [EPIC-RELIABILITY-QUEUES.md](./epics/EPIC-RELIABILITY-QUEUES.md)
  - `AI-ENRICHMENT-ROUTING-EPIC` → Link to [EPIC-AI-ENRICHMENT-ROUTING.md](./epics/EPIC-AI-ENRICHMENT-ROUTING.md)
  - `OBS-SLO-PHASES-EPIC` → Link to [EPIC-OBS-SLO-PHASES.md](./epics/EPIC-OBS-SLO-PHASES.md)
  - `SAAS-MULTITENANT-EPIC` → Link to [EPIC-SAAS-MULTITENANT.md](./epics/EPIC-SAAS-MULTITENANT.md)

## ClickUp Custom Fields for Epics

### Root Epic Task Template

**Task Name**: `[EPIC-ID] Epic Title`

**Example**: `[SECURITY-EDGE-EPIC] Security & Edge (Cloudflare / mTLS / WAF)`

**Custom Fields**:

| Field | Type | Value/Example |
|-------|------|----------------|
| `externalid` | Text | `SECURITY-EDGE-EPIC` (from markdown) |
| `sourcesystem` | Select | `GitHub` |
| `syncstate` | Select | `synced` / `pending` / `error` |
| `traceid` | Text | `sec-edge-2026-q1` (for correlation) |
| `aicategory` | Select | `NORMAL` (default for meta tasks) |
| `epicowner` | User | Assigned to stream owner (Security Lead, Platform Lead, etc.) |
| `targetwindow` | Text | `Q1 2026 (Week 1-8)` |
| `dependson` | Link to other epics | (e.g., RELIABILITY-QUEUES depends on SECURITY-EDGE) |
| `slodefnofdon` | Text (multi-line) | DoD criteria from markdown |
| `risklevel` | Select | `HIGH`, `MEDIUM`, `LOW` |
| `estimatedfte` | Number | FTE-weeks (e.g., 8) |

## Subtask Mapping (per Epic)

For each subtask in the markdown (e.g., SEC-1, REL-1, AI-1):

**Subtask Name**: `[TASK-ID] Task Description`

**Example**: `[SEC-1] Issue/rotate client certs for Make/Backend via ACME`

**Custom Fields**:

| Field | Type | Value/Example |
|-------|------|----------------|
| `externalid` | Text | `SEC-1`, `REL-1`, etc. |
| `sourcesystem` | Select | `GitHub` |
| `syncstate` | Select | `synced` |
| `traceid` | Text | `sec-edge-2026-q1-sec1` |
| `assignee` | User | From `Owner` column in markdown |
| `duedate` | Date | From `Due` column in markdown |
| `taskstatus` | Select | `Planned`, `In Prog`, `Done` |
| `parentepic` | Link | Points to parent Epic task |

## Sync Workflow

### Manual Sync (for initial setup)

1. Manually create Epic folder in ClickUp for each stream.
2. Create root Epic task with custom fields from markdown header.
3. Create subtasks from the `Subtasks` table.
4. Set `syncstate = synced` and save.

### Automated Sync (for updates)

**Option A: GitHub → ClickUp via Make or Zapier**

- Trigger: Push to `docs/epics/*.md` or `docs/EPICS-ROADMAP-CONSOLIDATED.md`
- Parse markdown YAML frontmatter or table rows.
- Match `externalid` and upsert ClickUp task.
- Update `syncstate`, `duedate`, `assignee`.

**Option B: ClickUp → GitHub (reverse sync for DoD/SLO updates)**

- Trigger: ClickUp task status change or custom field edit.
- Update corresponding markdown section (e.g., `## Subtasks` table).
- Commit to GitHub branch.

## SLO Metrics Tracking in ClickUp

For each Epic, add a **SLO Metrics** subtask or custom field:

- `slosuccess`: Percentage compliance (e.g., "mTLS on 100% of APIs").
- `sloupdate`: Date of last metric collection.
- `slonotes`: Free-form notes on blockers or wins.

## Example ClickUp Query

To view all Q1 Epics and their status:

```
space:EXECUTION-PHASE-2-Q1-2026 sourcesystem:GitHub AND targetwindow:"Q1 2026" sort:duedate
```

## References

- [EPICS-ROADMAP-CONSOLIDATED.md](./epics/EPICS-ROADMAP-CONSOLIDATED.md)
- ClickUp API Docs: https://clickup.com/api
- Make (formerly Integromat): https://make.com
- Zapier: https://zapier.com
