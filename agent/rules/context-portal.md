---
trigger: always_on
---

Custom Instructions for AI Model (Cascade ConPort Integration)

# --- External Strategy References ---
external_strategies:
  prompt_caching:
    file_path: "context_portal/prompt_caching_strategy.yml"
    description: "Defines strategies for leveraging prompt caching with different LLM providers."

# --- Cascade ConPort Integration Strategy ---
cascade_conport_integration:
  introduction: |
    These instructions guide Windsurf Cascade on integrating with the ConPort project memory system (MCP plugin).
    Treat ConPort as a primary source for "MEMORIES" to guide your work.

  purpose: |
    ConPort stores and retrieves structured information about the current workspace, including:
    - Overall project goals and architecture (Product Context).
    - Current work focus, recent changes, and open questions (Active Context).
    - Key decisions, rationale, and implementation details.
    - Task progress and status.
    - Reusable system patterns.
    - Project-specific glossary terms and other custom data.

  workspace_id:
    source_description: |
      ConPort tools require a `workspace_id`. Derive this from the workspace URI provided in your context (e.g., parse 'file:///path/to/project' to '/path/to/project').
    fallback: |
      If the URI is not a local file path or parsing fails, you may need to ask the USER for the absolute path to the workspace.

  interaction_protocol:
    title: "Strict Adherence Required for ConPort Plugin Calls"
    rules:
      - "Explain Intent: Before calling any ConPort plugin operation, briefly explain to the USER *why* you are accessing the project memory (e.g., \"I'll check our project's decision log for previous choices on this topic.\")."
      - "No Operation Names to User: NEVER mention the specific ConPort operation names (e.g., `get_decisions`) in your conversation with the USER."
      - "Tool Call Placement: ALL ConPort MCP tool calls (using the `use_mcp_tool` structure) MUST be placed at the very END of your response message. Do not add any text after the tool call block."
      - "Wait for Results: If your next action depends on the output of a ConPort operation, ensure you have received and processed the result before proceeding. Explicitly wait if necessary by not requesting new tools until the ConPort result is available."

  proactive_memory_management:
    logging_guideline: |
      Actively identify opportunities to log new information (decisions, progress, patterns, glossary terms) into the project memory as it emerges in your conversation with the USER. Confirm with the USER before logging significant new entries or updates if you are inferring the information.
    updating_guideline: |
      Keep Product Context and Active Context up-to-date as project goals or current focus shift.

  tool_usage_focus:
    primary_use: |
      Use ConPort plugin operations primarily for managing structured, persistent project knowledge.
    complementary_use: |
      Utilize your native tools (e.g., `Codebase Search`, `View File`, `List Directory`) for direct code interaction and general information retrieval from the file system.
    mcp_server_type: |
      ConPort is a "tools-only" MCP server/plugin. Do not attempt to use MCP `prompts` or `resources` with it.

  initialization_guidance:
    # This guidance assumes you have determined the `ACTUAL_WORKSPACE_ID`.
    # Use your native `List Directory` or `Find` tools to check for the ConPort DB file
    # (e.g., `ACTUAL_WORKSPACE_ID + "/context_portal/context.db"`).
    sequences:
      - name: on_existing_db_found
        description: "Procedure if an existing ConPort DB is found for the workspace."
        steps:
          - step: 1
            action: |
              Attempt to load existing project memory by invoking the following ConPort operations (see `conport_operations_reference` for call structures):
              - `get_product_context`
              - `get_active_context`
              - `get_decisions` (e.g., limit 5)
              - `get_progress` (e.g., limit 5)
              - `get_system_patterns` (e.g., limit 5)
              - `get_custom_data` (category: "critical_settings")
              - `get_custom_data` (category: "ProjectGlossary")
              - `get_recent_activity_summary` (e.g., last 24h, limit 3 per type)
          - step: 2
            action: "Analyze loaded data."
            conditions:
              - if: "data is successfully loaded and seems populated"
                actions:
                  - "Inform the USER: \"ConPort project memory loaded.\""
                  - "Proceed with user's task, leveraging loaded context."
              - if: "data is minimal/empty despite DB existing"
                actions:
                  - "Inform USER: \"ConPort database found, but seems empty. You can start by defining Product Context.\""
                  - "Proceed with user's task, leveraging loaded context (or guiding setup)."
      - name: on_no_db_found
        description: "Procedure if NO ConPort DB is found for the workspace."
        steps:
          - step: 1
            action: "Inform USER: \"No existing ConPort project memory found for this workspace.\""
          - step: 2
            action: "Ask USER about initializing ConPort."
            tool_to_use: "ask_followup_question" # This is a placeholder for Cascade's mechanism to ask questions.
            parameters:
              question: "Would you like to initialize ConPort for this workspace? A new data store will be created automatically when information is first saved."
              suggestions:
                - "Yes, initialize ConPort."
                - "No, do not use ConPort."
          - step: 3
            description: "Process user response to initialization."
            conditions:
              - if_user_response_is: "Yes" # Adapt to actual response format
                actions:
                  - "Inform USER: \"Okay, ConPort will be set up for this workspace.\""
