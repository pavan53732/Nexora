> **Status: CANONICAL** for tool subsystem architecture and execution.
> This document owns how tools are discovered, loaded, sandboxed, and executed.
> Tool identity catalog lives in [../registry/TOOLS.md](../registry/TOOLS.md).
> Tool invocation contract lives in [../protocols/Tool-Protocol.md](../protocols/Tool-Protocol.md).
>
> Depends on: [../registry/TOOLS.md](../registry/TOOLS.md), [../protocols/Tool-Protocol.md](../protocols/Tool-Protocol.md).
> Referenced by: [AGENT_RUNTIME.md](AGENT_RUNTIME.md), [RUNTIME.md](RUNTIME.md), [../sdk/ToolSDK.md](../sdk/ToolSDK.md).

# Tool System — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See also [SANDBOX.md](SANDBOX.md) | [RUNTIME.md](RUNTIME.md)

---

## Overview

Every capability in Nexora is implemented as a tool. Tools are modular, plugin-based, and follow a uniform interface contract.

## Tool Interface

```kotlin
enum class ToolRiskLevel { LOW, MEDIUM, HIGH, CRITICAL }

interface Tool {
    val id: String
    val name: String
    val description: String
    val category: ToolCategory
    val riskLevel: ToolRiskLevel
    val parameters: JsonSchema
    val requiredPermissions: List<String> // canonical PermissionScope IDs
    val timeout: Duration
    val requiresSandbox: Boolean
    val isIdempotent: Boolean   // FR-AS-007: declares replay-safety for exactly-once recovery
    val supportsStreaming: Boolean
    val supportsCancellation: Boolean
    val cacheTtlMs: Long
    val version: String

    suspend fun execute(params: JsonObject, context: ToolContext): ToolResult
}

data class ToolContext(
    val workspaceId: String,
    val sandbox: Sandbox,
    val memoryManager: MemoryManager,
    val eventBus: EventBus
)

// Canonical result type (source of truth: models/ToolInvocation.md). Approval is NOT a
// ToolResult variant — when authorization is required the ToolInvocation stays in
// PENDING_AUTHORIZATION (see security/PermissionModel.md) and the Task/Agent lifecycle
// may transition to WaitingApproval. The execute() suspend call only returns Success/Error.
sealed class ToolResult {
    data class Success(val output: JsonObject, val metadata: ToolMetadata) : ToolResult()
    data class Error(val message: String, val code: String, val recoverable: Boolean) : ToolResult()
}

data class ToolMetadata(
    val durationMs: Long,
    val tokensUsed: Int = 0,
    val filesAffected: List<String> = emptyList()
)
```

## Tool Categories (28)

> **Note:** Category 27 (MCP Integration) added via G4 hardening (2026-08-06). Category 28 (Project Introspection) added via S10 Path C (2026-08-06).

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
| 18 | **Android Device** | read_contacts, send_notification, access_camera, device_audio_stream, device_camera_stream | Later (G5 — optional: real-time streaming `device_camera_stream` `TOOL-403`, `device_audio_stream` `TOOL-404`; default `DENY`; `Streaming` flag `✓`; `FR-S016` `Manual`/`Assisted` mode required) |

> **Reserved tool IDs:** `TOOL-403` (`device_camera_stream`) and `TOOL-404` (`device_audio_stream`) are reserved for real-time device streaming (G5 research); they must not be reused for other tools. Registry skips `TOOL-403` and `TOOL-404` pending implementation.
| 19 | **Project Management** | create_task, update_task, list_tasks, track_progress | Later |
| 20 | **Security** | check_permissions, encrypt_file, decrypt_file, scan_vulnerabilities | Later |
| 21 | **Observability** | get_logs, get_metrics, get_trace, export_diagnostics | Later |
| 22 | **Import/Export** | import_project, export_project, import_plugin | Later |
| 23 | **Plugin System** | install_plugin, uninstall_plugin, configure_plugin, list_plugins | 8 |
| 24 | **Multi-Agent** | create_agent, delegate_task, agent_status, agent_list | 7 |
| 25 | **Workflow** | create_workflow, run_workflow, schedule_workflow | 6 |
| 26 | **Skills** | skill_list, skill_acquire (skills are first-class expertise units — ADR-0007; these tools manage them) | 4 |
| 27 | **MCP Integration** | mcp_connect_stdio, mcp_connect_http, mcp_list_caps, mcp_call_tool, mcp_read_resource, mcp_get_prompt | 5 |
| 28 | **Project Introspection** | introspect_api, introspect_database, introspect_config, introspect_build, introspect_ui, introspect_domain, introspect_infrastructure — pre-flight readers that scan the workspace and populate ProjectContext before planning (FR-CM-009, Path C) | 4 |

> **Full catalog:** [registry/TOOLS.md](../registry/TOOLS.md) is the authoritative
> registry of every tool — **352 tools** (authoritative count in [registry/TOOLS.md](../registry/TOOLS.md)) with stable `TOOL-###` IDs, descriptions, and
> phases across the 28 categories (target 300–500). [registry/TOOL_MATRIX.md](../registry/TOOL_MATRIX.md)
> maps capabilities (read/write/network/permissions/sandbox/streaming) for every tool.
> Regenerate with `scripts/generate_tool_catalog.py`.

## Tool Execution Flow

```
AI Response contains tool_call
    |
    v
Tool Manager -> Look up tool by name; validate ID, schema, riskLevel, and unique known scope IDs
    |
    v
Complete Authorization Gate (see security/PermissionModel.md)
  → Validate required-scope declaration (reject duplicates)
  → Resolve every scope through policy hierarchy
  → Deny unknown or effective-DENY scopes
  → Aggregate ASK scopes, validate approval transaction
  → Build ResolvedPermission projections
  → ClassifierPolicy selection and optional Classifier evaluation
  → Return Allowed only after every gate passes
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

Authorization denial returns `NXR-2003` with subreason (`UNKNOWN_SCOPE`,
`POLICY_DENIAL`, `USER_DENIED`, `MALFORMED_APPROVAL`, `CLASSIFIER_DENIAL`). Invalid
Tool descriptors, including duplicate/unknown scope declarations or missing risk metadata,
are rejected with `NXR-2005` before `REGISTERED`. No Tool side effect occurs before
complete authorization. Authorization denial does not change ToolStatus. Classifier
`DENY` is final for the current call.

Risk levels are canonical Tool metadata: `LOW` is read-only/local, `MEDIUM` is bounded
workspace mutation, `HIGH` covers network/process/plugin/remote/destructive operations,
and `CRITICAL` covers device-sensitive or security-critical irreversible operations.

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

## MCP Client (Model Context Protocol Client)

> **Status:** CANONICAL specification for MCP integration (added G4 — 2026-08-06).  
> **Verified research reference:** Industry precedent verified — Claude (Anthropic), Mistral Vibe (Mistral AI), Kimi CLI (Moonshot AI), MiniMax Hailuo (MiniMax) all document stdio + Streamable HTTP transport support, capability negotiation, and tool/resource/prompt primitives (`bitdoze.com` 2026-07-24; `mcp.directory` 2026-07-09; `aihackers.net` 2026-07-03; `blog.4sapi.com` 2026-07-07).  
> **Position:** MCP servers are an additional **tool SOURCE** (alongside built-in and plugin tools) — they do **NOT** replace the `Tool` interface, `ToolRegistry`, or `PluginSDK`.  
> **Mapping:** Every MCP primitive (`tool`, `resource`, `prompt`) maps onto the existing `Tool` contract (`id`, `name`, `description`, `parameters`, `requiredPermissions`, `execute` → `ToolResult`).  
> **Transport:** `stdio` (subprocess) and `Streamable HTTP` (SSE-compatible over HTTPS) — both registered via `mcp_connect_stdio` (`TOOL-397`) and `mcp_connect_http` (`TOOL-398`).  
> **Capability negotiation:** `mcp_list_caps` (`TOOL-399`) performs handshake; results stored per workspace in `workspace.json` settings (`FR-W005`).  
> **Permission model:** MCP connections require `network:http` (for HTTP transport) and `plugin:install` (when registering external server capabilities) — both default `ASK` (`security/PermissionModel.md` §Explicit Risk-Based Scope Defaults). Each discovered MCP tool inherits the server's declared `requiredPermissions`; if not declared, defaults to `DENY`. Unknown scopes are always denied.
> **Result flow:** MCP tool results (`mcp_call_tool` `TOOL-400`) return through the standard `ToolResult.Success` / `ToolResult.Error` pipeline (`protocols/Tool-Protocol.md`); no special error envelope — canonical error codes (`NXR-2004`, `NXR-7004`) apply. Authorization requirements are represented by the `ToolInvocation` status `PENDING_AUTHORIZATION`, not a `ToolResult` variant.
> **Sandbox:** MCP client process runs inside the workspace sandbox (`sandbox:execute` scope required) with the same filesystem/network/process limits (`security/SandboxPolicy.md`); no host-level access granted by transport choice.  
> **Phase:** Phase 5 (same phase as AI provider integrations — `specs/AI_PROVIDERS.md` Phase 5 mapping applies).  
>
> References: `FR-TL001`..`FR-TL015` (tool interface contract); `FR-P001`..`FR-P013` (provider isolation rules extended to MCP servers); `FR-S016` (autonomy modes control approval gates for MCP-discovered tools); `FR-S001`..`FR-S028` (sandbox rules apply to MCP client process); `security/PermissionModel.md` (§Permission Scopes — `plugin:install`, `network:http`); `protocols/Tool-Protocol.md` (§Execution Flow — authorization gate + sandbox runner); `registry/TOOLS.md` (`TOOL-397`..`TOOL-402` — MCP integration category); `docs/DECISION_LOG.md` (`DL-020` — see below).

## ToolStatus Lifecycle

The canonical Tool descriptor lifecycle is owned by this document.
States are defined in `models/Tool.md`:

- `DISCOVERED` — tool descriptor found (plugin manifest, MCP handshake, built-in catalog) but not yet registered.
- `REGISTERED` — tool descriptor validated and recorded in the tool registry; not yet available for execution.
- `ACTIVE` — tool is registered and available for agent invocation.
- `DISABLED` — tool is registered but blocked from execution (administrative action, plugin deactivation, health failure).

### Authoritative Transitions

| Trigger | From | To | Guard |
|---|---|---|---|
| `register` | `DISCOVERED` | `REGISTERED` | Descriptor passes schema, risk-level, stable-ID, and unique known permission-scope validation |
| `activate` | `REGISTERED` | `ACTIVE` | Plugin loaded; all required dependencies available; health != UNHEALTHY |
| `deactivate` | `ACTIVE` | `DISABLED` | Plugin health failure, admin action, or explicit deactivation |
| `re-activate` | `DISABLED` | `ACTIVE` | Health restored or admin re-activation |

### Health-Status Interaction

`Tool.health` (`UNKNOWN`, `HEALTHY`, `DEGRADED`, `UNHEALTHY`) is evaluated by the background `HealthMonitor` and influences transitions:
- `UNHEALTHY` blocks `REGISTERED → ACTIVE`.
- `UNHEALTHY` triggers `ACTIVE → DISABLED`.
- `DEGRADED` allows activation but emits warning.
- `HEALTHY` satisfies all health guards.

### Distinction from Tool Execution

- ToolStatus describes the **registry availability** of a Tool descriptor — whether an agent CAN invoke it.
- Individual tool calls use `ToolExecution` / `ToolResult` with correlation IDs — whether a specific call SUCCEEDED.
- A failed tool invocation (`ToolResult.Error`) does **not** change the Tool descriptor to `DISABLED` unless a canonical health or administrative policy explicitly triggers that transition.
- Tool descriptor lifecycle events are separate from per-call execution events.

### Transition Guard Rules

- `DISCOVERED → REGISTERED`: descriptor validation must pass; `TOOL-ID` must be unique in the registry; health != UNHEALTHY.
- `REGISTERED → ACTIVE`: owning plugin or source must be loaded and pass health checks (health != UNHEALTHY).
- `ACTIVE → DISABLED`: administrative deactivation, plugin unloading, or health-policy threshold exceeded.
- `DISABLED → ACTIVE`: re-activation requires passing all `REGISTERED → ACTIVE` guards.

### Phase Mapping

- **Phase 1**: Define `Tool` interface, `ToolRegistry`, `ToolResult`.
- **Phase 4**: Implement File System, Terminal, Search, Workspace, Git, Network, Package Manager, Memory tools.
- **Phase 8**: Plugin-based tool installation.


> **S4 — Terminal specification fully specified:** `specs/TERMINAL.md` (§Execution Model, §Session State Machine, §Working-Dir Boundary, §Output Caps, §Timeout Discipline, §Restore Behavior, §Security & Isolation) defines terminal behavior; lifecycle authority `lifecycle/TerminalSessionLifecycle.md` (S3 filled); model fields updated (`models/TerminalSession.md`); registry capabilities updated (`TOOL_MATRIX.md`). See `docs/DECISION_LOG.md` DL-028.


## Tool Reuse and Repetition Control

This upgrade adds bounded tool-execution controls.

The tool subsystem SHOULD support safe reuse of recent successful tool results when:

- the inputs are materially identical;
- the underlying source has not changed;
- freshness constraints still hold;
- reuse does not violate evidence or safety requirements.

The subsystem MUST detect repeated identical invocations that provide no new progress signal. Such invocations MUST either reuse a valid cached result, request new inputs, switch strategy, or terminate/escalate.

Tool execution policy MUST also define:

- timeout classification;
- retry eligibility;
- non-retryable failure classes;
- cancellation propagation;
- provenance on tool outputs.
