# Tool System — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See also [SANDBOX.md](SANDBOX.md) | [RUNTIME.md](RUNTIME.md)

---

## Overview

Every capability in Nexora is implemented as a tool. Tools are modular, plugin-based, and follow a uniform interface contract.

## Tool Interface

```kotlin
interface Tool {
    val id: String
    val name: String
    val description: String
    val category: ToolCategory
    val parameters: JsonSchema
    val requiredPermissions: List<PermissionScope>
    val timeout: Duration
    val requiresSandbox: Boolean
    val version: String

    suspend fun execute(params: JsonObject, context: ToolContext): ToolResult
}

data class ToolContext(
    val workspaceId: String,
    val sandbox: Sandbox,
    val memoryManager: MemoryManager,
    val eventBus: EventBus
)

sealed class ToolResult {
    data class Success(val output: JsonObject, val metadata: ToolMetadata) : ToolResult()
    data class Error(val message: String, val code: String, val recoverable: Boolean) : ToolResult()
    data class NeedsApproval(val toolCall: ToolCall, val reason: String) : ToolResult()
}

data class ToolMetadata(
    val durationMs: Long,
    val tokensUsed: Int = 0,
    val filesAffected: List<String> = emptyList()
)
```

## Tool Categories (26)

| # | Category | Example Tools | Phase |
|---|----------|--------------|-------|
| 1 | **File System** | read_file, write_file, append_file, delete_file, list_dir, create_dir, move_file, copy_file, search_files | 4 |
| 2 | **Workspace** | create_workspace, switch_workspace, archive_workspace, list_workspaces | 1 |
| 3 | **Code Intelligence** | parse_code, find_symbols, find_references, rename_symbol | Later |
| 4 | **Search** | search_text, search_regex, grep, find | 4 |
| 5 | **Terminal** | run_command, run_script, run_background, kill_process | 4 |
| 6 | **Git** | git_init, git_clone, git_add, git_commit, git_push, git_pull, git_branch, git_diff | 4 |
| 7 | **Package Manager** | npm_install, pip_install, list_packages, remove_package | 4 |
| 8 | **Build** | gradle_build, gradle_run, make_build | Later |
| 9 | **Test** | run_tests, test_coverage | Later |
| 10 | **Debugging** | set_breakpoint, inspect_variable, stack_trace | Later |
| 11 | **Formatting** | format_code, lint, fix_lint | Later |
| 12 | **Documentation** | generate_docs, generate_readme | Later |
| 13 | **Browser** | open_url, screenshot, extract_page, fill_form, click_element | Later |
| 14 | **Network/API** | http_get, http_post, http_put, http_delete, websocket | 4 |
| 15 | **Database** | sqlite_query, sqlite_create, sqlite_migrate | Later |
| 16 | **Memory** | store_memory, recall_memory, search_memory, list_memories | 6 |
| 17 | **AI** | complete, embed, image_generate, image_analyze | 5 |
| 18 | **Android Device** | read_contacts, send_notification, access_camera | Later |
| 19 | **Project Management** | create_task, update_task, list_tasks, track_progress | Later |
| 20 | **Security** | check_permissions, encrypt_file, decrypt_file, scan_vulnerabilities | Later |
| 21 | **Observability** | get_logs, get_metrics, get_trace, export_diagnostics | Later |
| 22 | **Import/Export** | import_project, export_project, import_plugin | Later |
| 23 | **Plugin System** | install_plugin, uninstall_plugin, configure_plugin, list_plugins | 8 |
| 24 | **Multi-Agent** | create_agent, delegate_task, agent_status, agent_list | 7 |
| 25 | **Workflow** | create_workflow, run_workflow, schedule_workflow | 6 |
| 26 | **Skills** | skill_list, skill_acquire (skills are first-class expertise units — ADR-0007; these tools manage them) | 4 |

> **Full catalog:** [registry/TOOLS.md](../registry/TOOLS.md) is the authoritative
> registry of every tool — **333 tools** with stable `TOOL-###` IDs, descriptions, and
> phases across the 26 categories (target 300–500). [registry/TOOL_MATRIX.md](../registry/TOOL_MATRIX.md)
> maps capabilities (read/write/network/permissions/sandbox/streaming) for every tool.
> Regenerate with `scripts/generate_tool_catalog.py`.

## Tool Execution Flow

```
AI Response contains tool_call
    |
    v
Tool Manager -> Look up tool by name
    |
    v
Permission Manager -> Check if tool is allowed
    |
    v
[If approval needed] -> Prompt user -> Wait for response
    |
    v
Parameter Validator -> Validate input against JSON Schema
    |
    v
Tool Executor -> Execute tool (in sandbox if required)
    |
    v
Result Collector -> Collect output and metadata
    |
    v
Memory Manager -> Store execution in history
    |
    v
Event Bus -> Publish tool execution event
    |
    v
Return result to AI for next step
```

## Tool Registration

Tools are registered at startup (built-in) or dynamically (plugins).

```kotlin
class ToolRegistry {
    private val tools = mutableMapOf<String, Tool>()

    fun register(tool: Tool)
    fun unregister(toolId: String)
    fun get(toolId: String): Tool?
    fun listByCategory(category: ToolCategory): List<Tool>
    fun listAll(): List<Tool>
}
```

## Phase Mapping

- **Phase 1**: Define `Tool` interface, `ToolRegistry`, `ToolResult`.
- **Phase 4**: Implement File System, Terminal, Search, Workspace, Git, Network, Package Manager, Memory tools.
- **Phase 8**: Plugin-based tool installation.
