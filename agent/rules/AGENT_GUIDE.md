# Agent Integration Guide

This document describes the agent configuration and integration protocols for AI assistants working with the Zenyth SPARC orchestration system.

## Overview

Zenyth includes comprehensive agent configuration in the `/agent` directory that defines:
- Mandatory initialization protocols
- Communication rules and standards
- ConPort integration requirements
- Task planning and execution workflows

## Communication Protocol

### Markdown Formatting

- Make all code and file references clickable
- Format as: `[filename](relative/path.ext:line)` or `language.construct()`
- Line numbers required for syntax highlighting, optional for file links
- Apply to all markdown responses and `attempt_completion` content

## Session Initialization Protocol

Every agent session MUST complete this checklist before responding to ANY user request:

```text
[SESSION START CHECKLIST]
□ 1. Import all content from /Users/stephen/Projects/rzp-labs/zenyth/agent/
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

### Required First Message Format

```text
[SESSION INITIALIZED]
Status: [CONPORT_ACTIVE/INACTIVE]
Mode: [<MODE>]

Context loaded: [Summary of loaded context]

Ready to assist with your request.
```

## ConPort Integration

### Workspace Configuration

- **Workspace ID**: `/Users/stephen/Projects/rzp-labs/zenyth`
- **Database Location**: `context_portal/context.db` (auto-created)
- **Integration Type**: Tools-only MCP server

### Logging Requirements

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

### Tool Usage Protocol

- **Explain Intent**: Before making file edits, explain what you plan to do and why
- **Tool Call Placement**: ALL tool calls MUST be placed at the very END of response messages
- **Wait for Results**: Ensure you have received and processed results before proceeding
- **Use Bulk Operations**: Always prefer batch operations when available (batch_log_items for multiple items of same type)
- **Minimize Tool Calls**: Group operations efficiently to reduce network overhead

### Bulk Operations Best Practices

**Available Bulk Tools:**
- `batch_log_items`: Log multiple items of same type (progress_entry, decision, system_pattern, custom_data)
- `get_decisions`: Retrieve multiple decisions with filters and limits
- `get_progress`: Retrieve multiple progress entries with status/parent filters
- `search_*_fts`: Full-text search for bulk retrieval
- `semantic_search_conport`: Cross-type semantic search

**Usage Pattern:**
```text
Multiple items of same type → Use batch_log_items
Mixed item types → Group by type, use separate batch calls
Single items → Individual calls acceptable
Retrieval operations → Use filtered bulk gets over multiple individual gets
```

**Example - Bulk Progress Logging:**
```json
{
  "item_type": "progress_entry",
  "items": [
    {"status": "DONE", "description": "Task 1 completed"},
    {"status": "IN_PROGRESS", "description": "Task 2 in progress"},
    {"status": "TODO", "description": "Task 3 planned"}
  ]
}
```

### File Path Requirements

**CRITICAL**: All file operations MUST use absolute paths only.

**Correct Examples:**
- `/Users/stephen/Projects/rzp-labs/zenyth/src/models/__init__.py`
- `/Users/stephen/Projects/rzp-labs/zenyth/agent/rules/AGENT_GUIDE.md`
- `/Users/stephen/Projects/rzp-labs/zenyth/context_portal/context.db`

**Incorrect Examples:**
- `src/models/__init__.py` ❌
- `./agent/AGENT_GUIDE.md` ❌
- `../context_portal/context.db` ❌

**Tools Requiring Absolute Paths:**
- All Serena MCP tools (read_file, create_text_file, etc.)
- ConPort workspace_id parameter
- File system operations
- Path references in documentation
- **ALL code that handles file paths** (configuration files, imports, scripts)
- Environment variables and configuration values
- Database connection strings and file references

**Code Examples:**

```python
# ✅ CORRECT - Absolute paths in code
DATABASE_PATH = "/Users/stephen/Projects/rzp-labs/zenyth/context_portal/context.db"
CONFIG_FILE = "/Users/stephen/Projects/rzp-labs/zenyth/sparc/methodology.yaml"
LOG_DIR = "/Users/stephen/Projects/rzp-labs/zenyth/logs"

# ❌ INCORRECT - Relative paths in code
DATABASE_PATH = "context_portal/context.db"
CONFIG_FILE = "./sparc/methodology.yaml"
LOG_DIR = "../logs"
```

```yaml
# ✅ CORRECT - Absolute paths in configuration
alembic:
  sqlalchemy.url: sqlite:////Users/stephen/Projects/rzp-labs/zenyth/context_portal/context.db

# ❌ INCORRECT - Relative paths in configuration
alembic:
  sqlalchemy.url: sqlite:///context_portal/context.db
```

### Initialization Sequences

#### Existing Database Found
1. Load existing project memory:
   - `get_product_context`
   - `get_active_context`
   - `get_decisions` (limit 5)
   - `get_progress` (limit 5)
   - `get_system_patterns` (limit 5)
   - `get_custom_data` (category: "critical_settings")
   - `get_custom_data` (category: "ProjectGlossary")
   - `get_recent_activity_summary` (last 24h, limit 3 per type)

2. Analyze and inform user of ConPort status

#### No Database Found
1. Inform user: "No existing ConPort project memory found"
2. Ask about initializing ConPort for the workspace
3. Set up ConPort if user agrees

## Task Planning Workflow

2. **Persistent Tracking Phase** - Transfer to ConPort:
   - **Create Parent Goal Entry**: Establish master progress entry for session goal
   - **Log Planned Tasks**: Create child progress entries linked to parent
   - **Include Metadata**: Transfer complexity scores and full task details
   - **Establish Hierarchies**: Use proper parent-child relationships

### Workflow Requirements

- **MUST** capture ALL metadata from planning tool (title, complexity, timestamps)
- **MUST** establish proper parent-child hierarchies in ConPort
- **MUST** document planning session details in ConPort

## Research Methodology

For complex tasks requiring research:

### Goal 1: Identify Knowledge Gaps
- List everything you know on the topic
- Use `mcp__sequential-thinking__sequentialthinking` (15 thoughts)
- List assumptions and knowledge gaps

### Goal 2: Search for Evidence
- Use `web-search` for current information
- Use `mcp__context7__context7` for technical documentation
- Validate AND attempt to disprove assumptions

### Goal 3: Integrate Findings
- Use `mcp__sequential-thinking__sequentialthinking` (10 thoughts)
- Surface new gaps or risks
- Update understanding

### Goal 4: Close Gaps
- Use additional research tools as needed
- Use `mcp__perplexity-ask__perplexityask` for complex queries

### Goal 5: Update Plan
- Use `mcp__serena__think_about_collected_information`
- Use `mcp__sequential-thinking__sequentialthinking` (10 thoughts)
- Use `mcp__serena__think_about_whether_you_are_done`
- Use `mcp__serena__summarize_changes`
- Use `mcp__serena__write_memory`

## Response Template

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

## Failure Recovery

If you catch yourself not following rules:

```text
[COMPLIANCE FAILURE DETECTED]
Rule violated: [specific rule]
Corrective action: [what I'm doing to fix it]
[Resume with proper compliance]
```

## Tool Capabilities

### Native Tools
- **File Operations**: List, read, write files
- **Search**: Regex searches across codebase
- **Code Analysis**: Get code definitions and structure
- **Command Execution**: Run CLI commands with explanations

### MCP Server Integration
- **ConPort**: Project memory and context management
- **Serena**: Semantic code operations with LSP integration
- **Sequential Thinking**: Structured problem-solving
- **Context7**: Technical documentation lookup
- **Perplexity**: Advanced research queries

## Integration with Zenyth SPARC

The agent configuration is designed to work seamlessly with Zenyth's SPARC orchestration:

- **Phase-Specific Tool Access**: Agent respects tool filtering per SPARC phase
- **Context Preservation**: ConPort maintains context across phase transitions
- **Session Management**: Proper session boundaries and state management
- **Methodology Compliance**: Enforces SPARC methodology adherence

This agent configuration ensures consistent, high-quality AI assistance while maintaining the structured approach that makes Zenyth effective for homelab orchestration tasks.
