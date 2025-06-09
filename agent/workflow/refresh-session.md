---
description: Refresh the agent's context. Best used when you begin to notice drift.
---

# Refresh Session Context

## CONFIRMATION MESSAGE FORMAT

```text
[SESSION REFRESHED]
Status: [CONPORT_ACTIVE/INACTIVE]
Mode: [<MODE>]

Context loaded: [Summary of loaded context]

Ready to assist with your request.
```

## FAILURE RECOVERY PROTOCOL

If you catch yourself not following rules:

```text
[COMPLIANCE FAILURE DETECTED]
Rule violated: [specific rule]
Corrective action: [what I'm doing to fix it]
[Resume with proper compliance]
```

## RESPONSE TEMPLATE

**Every response MUST follow this structure:**

```text
[CONPORT_ACTIVE] [MODE: <MODE>]
<thinking>
- What CLAUDE.md rules apply here?
- Do I need to check/update ConPort?
- Am I following mode guidelines?
- Have I checked for relevant decisions/patterns?
</thinking>

[Your actual response]

<conport_updates>
[Any ConPort updates made during this response]
</conport_updates>
```

## ConPort Logging Requirements

**CRITICAL**: Every ConPort log entry MUST include:

1. **Actions Performed**: Detailed description of what was done
2. **Expected Result**: What outcome was anticipated
3. **Actual Result**: What actually happened

Example format:

```text
Actions: Updated K3s inventory to use environment variables
Expected Result: Inventory would be more secure and portable
Actual Result: Successfully replaced hard-coded paths with env vars, SSH security improved
```

## Task Planning Workflow

You **MUST** use dual-tool approach for task management:

1. **Initial Planning Phase** - Use software-planning-mcp tool:
   - Create detailed task breakdown with complexity scores
   - Organize tasks with titles, descriptions, and code examples
   - Use interactive planning features for task refinement
   - Data persists in `/Users/stephen/.software-planning-tool/data.json`

2. **Persistent Tracking Phase** - Transfer to ConPort:
   - Create progress entries with parent-child relationships
   - Include complexity scores in descriptions
   - Store full metadata in custom_data category "task_metadata"
   - Link planning sessions via custom_data category "planning_sessions"

3. **Workflow Requirements**:
   - MUST capture ALL metadata from planning tool (title, complexity, timestamps)
   - MUST establish proper parent-child hierarchies in ConPort
   - MUST create bidirectional links between systems
   - MUST document planning session details in ConPort
