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
    val recoveryContract: ToolRecoveryContract   // strongest truthful operation-level contract; invalid/missing declarations reject registration
    val supportsStreaming: Boolean
    val supportsCancellation: Boolean
    val cacheTtlMs: Long
    val version: String

    suspend fun execute(params: JsonObject, context: ToolContext): ToolResult
}
```

## Timeout Semantics

Tool invocation timeouts are transport/execution outcomes that do NOT prove the underlying operation did not execute. A timeout may produce an **unknown completion state** for potentially non-idempotent tools.

### Completion State Classification

- **Confirmed failure**: the tool returned an explicit error response.
- **Timeout**: the invocation exceeded its time budget without a confirmed outcome.
- **Unknown completion**: a timeout where the tool may have partially or fully executed (non-idempotent operations).

### Retry Eligibility

Retrying an unknown-completion non-idempotent operation MUST NOT be treated as automatically safe. Retry eligibility requires one of:

- established idempotency (`isIdempotent: true` in the tool descriptor);
- explicit operation-level deduplication/idempotency semantics;
- an explicit compensating/recovery mechanism.

### Timeout Classification

Timeout values are specified per-tool in the tool descriptor and MUST respect workspace sandbox limits. The following classifications are used:

- `NOT_REACHED` — invocation completed before timeout.
- `EXCEEDED` — timeout exceeded; invocation terminated.

### Retry and Non-Retryable Failures

- `EXCEEDED` is generally non-retryable for non-idempotent tools unless idempotency or compensation is established.
- Non-retryable failure classes include authorization failures, schema validation failures, permanent tool errors, and repeated identical failures after strategy mutation.

### Unknown-Completion Reconciliation

Every new, non-idempotent, or externally side-effecting Tool MUST declare the strongest truthful operation-level recovery contract in addition to `isIdempotent`. The contract MUST be one of:

- provider or remote idempotency key plus status lookup;
- deterministic local transaction or compensating operation; or
- an automatic bounded reconciliation and containment contract that preserves evidence and commits existing non-success effects when completion remains unproven.

A Tool descriptor with a missing, contradictory, or unsupported recovery declaration MUST be rejected through the existing Tool validation path (`NXR-2005`); no Tool is registered or executed on the basis of an assumed recovery behavior. The declaration is metadata of the existing Tool descriptor and does not create a recovery owner, state, identity, or error code.

A timeout without a confirmed result MUST remain `UNKNOWN_COMPLETION` until the declared contract resolves whether the side effect occurred.
 The runtime MUST NOT silently retry, silently mark failure, or report success for an unresolved unknown-completion operation. Reconciliation evidence and final disposition MUST be persisted with the ToolInvocation and execution history. If the automatic contract is exhausted, the unresolved child remains `UNKNOWN_COMPLETION` and the owning Task/Execution applies the existing non-success path; no human action is required to continue recovery.

### Reconciliation Exhaustion and Parent Non-Success (GAP-003)

Reconciliation attempts MUST remain within the Tool operation's declared recovery contract and the parent Task/Execution effective deadline. A reconciliation failure MAY retry only when that contract preserves idempotency or safe compensation; it MUST NOT reset the parent deadline, retry budget, failure ledger, or execution lineage. Every attempt, observation, timeout, error, and evidence reference MUST be persisted with the ToolInvocation and execution history.

When the reconciliation budget or effective deadline is exhausted without establishing whether the side effect occurred, the ToolInvocation MUST remain `UNKNOWN_COMPLETION` and MUST retain canonical non-success error/recovery metadata. The runtime MUST NOT replay, skip, mark success, or silently convert the operation to confirmed failure. The owning runtime MUST persist the unresolved child, reconciliation context, every observation, and evidence in the existing checkpoint/history, then apply the existing non-success effects: parent Task `Running → Failed` and associated Execution `RUNNING → FAILED` through their owning lifecycle authorities. No human clarification or escalation is required for this exhaustion path. Any later retry/restart, if eligible under existing idempotency and retry rules, MUST use the existing new-Execution lineage and MUST NOT replay the unresolved child merely because recovery continued. This section creates no new state, error, identity, or authority.

### Ownership

Timeout monitoring is owned by the tool execution subsystem. A timeout (`NXR-2002`) has **no ToolStatus lifecycle effect**: it is an execution outcome, not a Tool descriptor lifecycle transition. The existing ToolInvocation record and canonical error envelope preserve the timeout/partial-output outcome without asserting that an underlying non-idempotent side effect failed or did not occur.

```kotlin
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
> registry of every tool — **350 tools** (authoritative count in [registry/TOOLS.md](../registry/TOOLS.md)) with stable `TOOL-###` IDs, descriptions, and
> phases across the 28 categories (target 300–500). [registry/TOOL_MATRIX.md](../registry/TOOL_MATRIX.md)
> maps capabilities (read/write/network/permissions/sandbox/streaming) for every tool.
> Regenerate with `scripts/generate_tool_catalog.py`.

## Atomic Side-Effect Capability

To prevent inconsistent workspace states when tool calls fail mid-execution, Nexora provides an **Atomic Side-Effect Capability**:

1. **Atomic Operation Bundles:** Mutating tool calls can be grouped into atomic bundles. A failure within a bundle triggers a workspace rollback to the last known-good state, ensuring data consistency.
2. **Durable Intent Logging:** Mutating operations are recorded in persistent tool invocation records (`models/ToolInvocation.md`; persisted via the `tool_call` and append-only `tool_record` tables in `specs/DATABASE_SCHEMA.md`) before execution. This allows the runtime to reconcile `UNKNOWN_COMPLETION` states during recovery, preventing duplicate side effects or silent failures.
3. **Idempotency Enforcement:** Non-idempotent operations are managed through unique idempotency keys, ensuring that retries do not result in redundant side effects. Exact table serialization remains a downstream implementation choice.

**Persistence mapping.** The Atomic Side-Effect Capability does not require a new table; its durability is carried by existing canonical schema in `specs/DATABASE_SCHEMA.md`:

| Mechanism | Persistence home |
|---|---|
| Atomic Operation Bundles (workspace rollback) | Room transaction boundary plus `file_version` history (`blobRef` → sandbox `files/.history/`) for file-state rollback |
| Durable Intent Logging | `tool_call` (live invocation state) + append-only `tool_record` (durable result meta) |
| Idempotency Enforcement | `execution_replay.inputHash` dedupe key + `tool_call.idempotent` flag; recovery replays only uncompleted calls |
| Write-ahead log / transaction kernel | Room's own ACID transaction and WAL journal mode (NFR-REL-001); not a separate table |

The transaction kernel is Room's transaction mechanism itself; no additional write-ahead-log table is introduced.

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
  → Confirm the complete PermissionModel authorization result and audit decision
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

## Cloud AI to Local Execution Boundary (Creator Product Design)

A provider response or model-generated `tool_call` is an input to the existing Tool flow, not a direct command execution authority. The Runtime/Agent/Workflow composition, Tool Manager, PermissionModel, parameter validator, Tool Executor, Sandbox, Memory/History, EventBus, and evidence/verification boundaries remain in the order defined above. AI cannot directly access the local filesystem, Android APIs, process environment, or host process controls.

The local execution path MUST preserve workspace isolation, permission and approval checks, sandbox/resource/egress controls, timeout and cancellation propagation, stdout/stderr and exit-result capture, artifact references, audit lineage, and `UNKNOWN_COMPLETION` reconciliation. A Skill may select or orchestrate existing Tools, and a Plugin may export capabilities, but neither may bypass this flow or become a second Agent Runtime, Tool identity authority, or authorization authority.

A provider health check, connection test, model capability result, or generated text is not a Tool authorization result and does not create a Task/Execution or declare completion. The normal `Allowed` result remains the only gate before a Tool side effect; evidence and claim validation remain required for completion.

Authorization denial returns `NXR-2003` with subreason (`UNKNOWN_SCOPE`,
`POLICY_DENIAL`, `USER_DENIED`, `MALFORMED_APPROVAL`, `CLASSIFIER_DENIAL`). Invalid
Tool descriptors, including duplicate/unknown scope declarations or missing risk metadata,
are rejected with `NXR-2005` before `REGISTERED`. No Tool side effect occurs before
complete authorization. Authorization denial does not change ToolStatus. The established
`CLASSIFIER_DENIAL` value is retained for compatibility with the existing error vocabulary
and any separately authorized future classification boundary; no local classifier is active
or invoked under DEC-42.

Risk levels are canonical Tool metadata: `LOW` is read-only/local, `MEDIUM` is bounded
workspace mutation, `HIGH` covers network/process/plugin/remote/destructive operations,
and `CRITICAL` covers device-sensitive or security-critical irreversible operations.

## Tool Registration

Tools are registered at startup (built-in) or dynamically (plugins and negotiated MCP sources).
The registry remains the sole authority for Tool identity, descriptor lifecycle, permission
scope IDs, and version compatibility.

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

### Agent-Visible Tool Discovery Projection

The registry MAY expose a bounded discovery projection instead of placing the complete
350-tool catalog defined by `registry/TOOLS.md` into every model request. Discovery is a selection and presentation
projection; it MUST NOT create a second Tool identity catalog or bypass the ToolStatus,
permission, sandbox, schema, or version checks.

A discovery projection SHOULD rank candidates using user intent, task phase, required
capabilities, workspace policy, current ToolStatus/health, risk level, freshness, prior
selection outcomes, and explicit alternatives. It SHOULD return the canonical descriptor
plus concise usage guidance, required preconditions, representative valid/invalid examples,
edge cases, boundaries from similarly named Tools, and any known failure signatures. These
are agent-computer-interface metadata and do not change `Tool.id`, `Tool.version`, schema,
or authorization semantics.

Discovery MUST be observable. The execution history SHOULD record the candidate set,
selected Tool ID/version, rejected alternatives and reasons, descriptor snapshot, and
whether the selection was followed by schema repair, authorization denial, timeout,
unknown completion, or semantic progress. This permits tool-selection evaluation without
turning a model preference into a lifecycle transition.

The discovery layer MUST fail closed when a descriptor is stale, incompatible, missing a
known permission scope, or not available in the current workspace. A model MUST receive a
clear incompatibility or repair result rather than an invented Tool name or silently
substituted side effect.

## MCP Client (Model Context Protocol Client)

> **Status:** CANONICAL specification for MCP integration (added G4 — 2026-08-06).  
> **Verified research reference:** Industry precedent verified — Claude (Anthropic), Mistral Vibe (Mistral AI), Kimi CLI (Moonshot AI), MiniMax Hailuo (MiniMax) all document stdio + Streamable HTTP transport support, capability negotiation, and tool/resource/prompt primitives (`bitdoze.com` 2026-07-24; `mcp.directory` 2026-07-09; `aihackers.net` 2026-07-03; `blog.4sapi.com` 2026-07-07).  
> **Position:** MCP servers are an additional **tool SOURCE** (alongside built-in and plugin tools) — they do **NOT** replace the `Tool` interface, `ToolRegistry`, or `PluginSDK`.  
> **Mapping:** MCP `tool`, `resource`, and `prompt` remain distinct protocol primitives. An MCP `tool` is projected into the existing `Tool` contract for invocation. An MCP `resource` is a permissioned context/data read and an MCP `prompt` is a structured prompt/workflow template; their protocol semantics, provenance, authorization, and cache/freshness behavior MUST NOT be reinterpreted as arbitrary Tool side effects. The existing `mcp_read_resource` and `mcp_get_prompt` registry entries are adapters for those primitives, not proof that a resource or prompt has Tool identity.
> **Transport:** `stdio` (subprocess) and `Streamable HTTP` (SSE-compatible over HTTPS) — both registered via `mcp_connect_stdio` (`TOOL-397`) and `mcp_connect_http` (`TOOL-398`).  
> **Capability negotiation:** `mcp_list_caps` (`TOOL-399`) performs handshake; results stored per workspace in `workspace.json` settings (`FR-W005`). The negotiated capability set MUST distinguish tools, resources, prompts, elicitation, progress/cancellation, and optional asynchronous task support; unsupported capabilities are not silently treated as supported.
> **Permission model:** MCP connections require `network:http` (for HTTP transport) and `plugin:install` (when registering external server capabilities) — both default `ASK` (`security/PermissionModel.md` §Explicit Risk-Based Scope Defaults). Each discovered MCP tool inherits the server's declared `requiredPermissions`; if not declared, defaults to `DENY`. Unknown scopes are always denied.
> **Result flow:** MCP tool results (`mcp_call_tool` `TOOL-400`) return through the standard `ToolResult.Success` / `ToolResult.Error` pipeline (`protocols/Tool-Protocol.md`); no special error envelope — canonical error codes (`NXR-2004`, `NXR-7004`) apply. Resource and prompt results preserve their MCP primitive, provenance, freshness, and authorization metadata before entering Context Management. Authorization requirements are represented by the `ToolInvocation` status `PENDING_AUTHORIZATION`, not a `ToolResult` variant.
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


> **S4 — Terminal specification fully specified:** `specs/TERMINAL.md` (§Execution Model, §Session State Machine, §Working-Dir Boundary, §Output Caps, §Timeout Discipline, §Restore Behavior, §Security & Isolation) defines terminal behavior; lifecycle authority is the canonical `state-machines/TerminalSessionLifecycle.md` (S3-E formal state machine), while `lifecycle/TerminalSessionLifecycle.md` is derived; model fields updated (`models/TerminalSession.md`); registry capabilities updated (`TOOL_MATRIX.md`). See `docs/DECISION_LOG.md` DL-028.


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
