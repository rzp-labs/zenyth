---
description: Mandatory initialization requirements when starting a new session
---

Mandatory Initialization Requirements

**[CRITICAL]**
- You **MUST** use `serena` for all file system operations
- You **MUST** read all lines when viewing or editing files
- You **MUST** import all files from the `RULES` section into your context
- You **MUST** complete the checklist below before responding to **ANY** user request:

```text
[SESSION START CHECKLIST]
□ 1. Import all content from /Users/stephen/Projects/rzp-infra/.agent/rules
□ 2. Determine and declare active mode
□ 3. Initialize ConPort (if database exists):
   □ get_product_context
   □ get_active_context
   □ get_decisions (limit 5)
   □ get_progress (limit 5)
   □ get_recent_activity_summary
□ 4. Display initialization status
□ 5. State current mode and applicable rules
```

**First message format:**

```text
[SESSION INITIALIZED]
Status: [CONPORT_ACTIVE/INACTIVE]
Mode: [<MODE>]

Context loaded: [Summary of loaded context]

Ready to assist with your request.
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

**MUST** use dual-tool approach for task management:

1. **Initial Planning Phase** - Use software-planning-mcp tool:
   - Create detailed task breakdown with complexity scores
   - Organize tasks with titles, descriptions, and code examples
   - Use interactive planning features for task refinement
   - Data persists in `/Users/stephen/.software-planning-tool/data.json`

2. **Persistent Tracking Phase** - Transfer to ConPort:
   a. **Identify/Create Parent Goal Entry for Session**:
      i. Determine the current overall session goal (e.g., from `active_context.current_session_goal`).
      ii. Check if a 'master' ConPort `progress_entry` already exists and is active for this specific session goal text (e.g., by retrieving `active_context.current_session_goal_progress_id` and verifying its description).
      iii. If not found, or if the `current_session_goal` text has significantly changed, create a new 'master' `progress_entry` in ConPort. Its description MUST be the text of the `current_session_goal`, and its status should be 'TODO'.
      iv. Store the ID of this master progress entry in `active_context.current_session_goal_progress_id` for future reference within the session.
   b. **Log Planned Tasks from Software Planning Tool**:
      i. Retrieve all tasks from the `software-planning-mcp` tool (e.g., using `mcp9_get_todos`).
      ii. For each task retrieved, prepare to create a ConPort `progress_entry`.
      iii. **Crucial: Set `parent_id`**: Each of these new ConPort `progress_entry` items for the planned tasks MUST have its `parent_id` field set to the ID of the 'master' session goal `progress_entry` identified or created in step 2.a.iv.
   c.  Log these prepared progress entries (e.g., using `mcp1_batch_log_items`).
   d.  Include complexity scores from the planning tool in the ConPort `progress_entry` descriptions.
   e.  Store full task metadata from the planning tool into ConPort `custom_data` (e.g., category `task_metadata`, keyed by planning tool ID).
   f.  Log the planning session itself to ConPort `custom_data` (e.g., category `planning_sessions`).

3. **Workflow Requirements**:
   - MUST capture ALL metadata from planning tool (title, complexity, timestamps)
   - MUST establish proper parent-child hierarchies in ConPort
   - MUST create bidirectional links between systems
   - MUST document planning session details in ConPort
