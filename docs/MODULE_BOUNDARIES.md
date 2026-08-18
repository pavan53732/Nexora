> **Status: CANONICAL** for feature module ownership and responsibilities.
> For the mapping between these feature modules and architectural layers,
> see [MODULE_LAYER_MAPPING.md](MODULE_LAYER_MAPPING.md).
>
> Depends on: [MODULE_LAYER_MAPPING.md](MODULE_LAYER_MAPPING.md).

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

# Module Boundaries

**Rule #1: Everything is a service behind an interface. UI never talks directly to implementations. Consumers may call public interfaces along the allowed dependency graph; EventBus carries published domain/runtime events and is not the sole invocation mechanism (DEC-40).**

| Module | Package | Responsibilities | Public API | Allowed Deps | Forbidden Deps |
|---|---|---|---|---|---|
| **ui** | `com.nexora.app.ui` | Compose screens, ViewModels, navigation | `Screens`, `NavRoutes`, ViewModels | `application`, `shared` | `sandbox`, `tools`, `providers`, `memory`, `agents`, `plugins`, `workflows`, `storage`, `services`, `security`, `runtime` |
| **application** | `com.nexora.app` | `NexoraApp` class, Hilt init, app-scope setup | `NexoraApp` | All modules | None (top-level orchestrator) |
| **runtime** | `com.nexora.app.runtime` | Agent loop, inference-turn orchestration, planner, executor, ContextSnapshot builder, ReasoningPolicy resolution, token budgeting, skill registry, evidence & validation engine, permission manager, scheduler, observability, security manager, background runtime, resource manager, agent manager, **WorkspaceStateMachine**, **MemoryStateMachine**, **TerminalSessionStateMachine** | `AgentLoop`, `InferenceRequest`, `ContextSnapshot`, `ReasoningPolicy`, `ReasoningSummary`, `Planner`, `Executor`, `ContextBuilder`, `TokenBudget`, `Skill`, `SkillRegistry`, `EvidenceEngine`, `Statement`, `Confidence`, `PermissionManager`, `Scheduler`, `Observability`, `SecurityManager`, `BackgroundRuntime`, `ResourceManager`, `AgentManager`, `WorkspaceStateMachine`, `MemoryStateMachine`, `TerminalSessionStateMachine`, `NexoraEvent` | `tools`, `providers`, `memory`, `agents`, `workflows`, `storage`, `security`, `shared` | `ui`, `application`, `sandbox`, `services` |
| **tools** | `com.nexora.app.tools` | Tool interface, ToolManager, tool implementations | `Tool`, `ToolManager`, `ToolContext`, `ToolResult`, `ToolCategory` | `sandbox`, `storage`, `security`, `shared` | `ui`, `application`, `runtime`, `providers`, `memory`, `agents`, `plugins`, `workflows`, `services` |
| **sandbox** | `com.nexora.app.sandbox` | VirtualFileSystem, ProcessManager, resource limits | `Sandbox`, `VirtualFileSystem`, `SandboxLimits`, `ProcessManager` | `storage`, `security`, `shared` | `ui`, `application`, `runtime`, `tools`, `providers`, `memory`, `agents`, `plugins`, `workflows`, `services` |
| **providers** | `com.nexora.app.providers` | AIProvider adapters, capability-aware routing, typed streaming, backpressure, cancellation, resume/failover lineage | `AIProvider`, `ProviderType`, `ProviderRoutePlan`, `StreamEnvelope`, `ProviderStreamLifecycle`, `ProviderManager` | `storage`, `security`, `shared` | `ui`, `application`, `runtime`, `tools`, `sandbox`, `memory`, `agents`, `plugins`, `workflows`, `services` |
| **memory** | `com.nexora.app.memory` | MemoryManager, tiers, embeddings, vector search | `MemoryManager`, `MemoryEntry`, `MemoryScope`, `MemoryTier` | `storage`, `security`, `shared` | `ui`, `application`, `runtime`, `tools`, `sandbox`, `providers`, `agents`, `plugins`, `workflows`, `services` |
| **agents** | `com.nexora.app.agents` | Agent interface, type definitions, configurations | `Agent`, `AgentType`, `AgentConfig`, `AgentRegistry` | `shared` | `ui`, `application`, `runtime`, `tools`, `sandbox`, `providers`, `memory`, `plugins`, `workflows`, `services`, `storage` |
| **plugins** | `com.nexora.app.plugins` | Plugin loader, lifecycle, marketplace client | `NexoraPlugin`, `PluginManager`, `PluginContext`, `PluginRegistry` | `tools`, `storage`, `security`, `shared` | `ui`, `application`, `runtime`, `sandbox`, `providers`, `memory`, `agents`, `workflows`, `services` |
| **workflows** | `com.nexora.app.workflows` | Workflow engine, DAG execution, workflow types | `Workflow`, `WorkflowStep`, `WorkflowEngine`, `WorkflowType` | `shared` | `ui`, `application`, `runtime`, `tools`, `sandbox`, `providers`, `memory`, `agents`, `plugins`, `services`, `storage` |
| **storage** | `com.nexora.app.storage` | Room database, DataStore, repositories | `WorkspaceRepository`, `AgentRepository`, `TaskRepository`, `NexoraDatabase` | `shared` | `ui`, `application`, `runtime`, `tools`, `sandbox`, `providers`, `memory`, `agents`, `plugins`, `workflows`, `services` |
| **services** | `com.nexora.app.services` | Android foreground services, WorkManager | `AgentExecutionService`, `NotificationHelper` | `runtime`, `storage`, `security`, `shared` | `ui`, `application`, `tools`, `sandbox`, `providers`, `memory`, `agents`, `plugins`, `workflows` |
| **security** | `com.nexora.app.security` | SecureKeyStore, audit logging, permission policy storage, secure storage | `SecureKeyStore`, `AuditLogger`, `PermissionScope`, `PermissionDecision`, `PermissionPolicyStore` | `storage`, `shared` | `ui`, `application`, `runtime`, `tools`, `sandbox`, `providers`, `memory`, `agents`, `plugins`, `workflows`, `services` |
| **shared** | `com.nexora.app.shared` | Utilities, extensions, constants | `Result`, `EventBus`, `NexoraEvent`, constants, extension functions | None (leaf module) | All other modules |

---

**Interface Segregation:** Every module exposes behavior exclusively through interfaces listed in its Public API column. Consumers must depend on those interfaces—never on concrete implementations. Hilt binds interfaces to implementations at the `application` layer, which is the only module permitted to see both sides. If a consumer needs capability from another module, it imports only the interface package, keeping the dependency graph acyclic and each module independently testable and replaceable.

**Permission Enforcement vs. Security Services:** Two modules share the "permission" vocabulary but have distinct roles, and must not be confused:

- **`PermissionManager` (runtime enforcement)** — `com.nexora.app.runtime.permissions`. Evaluates each tool call against the policy hierarchy (global → workspace → agent → tool, see [PermissionModel](../security/PermissionModel.md)), prompts the user for `ASK` decisions, and returns `PermissionResult`. This is the runtime's per-call gate and is exercised on every tool invocation.
- **`security` module (security services)** — `com.nexora.app.security`. Provides `SecureKeyStore` (Keystore-backed encryption of API keys/secrets), `AuditLogger` (tamper-evident, append-only audit trail), and `PermissionPolicyStore` (persistence of permission decisions). It defines the `PermissionScope`/`PermissionDecision` types and persists policy, but it **does not gate tool execution** — enforcement lives exclusively in the runtime's `PermissionManager`.

> **S5 — Workflow Engine module boundary**: The Workflow Engine is a standalone module
> (`com.nexora.app.workflows`) with its own canonical document
> (`architecture/WORKFLOW_ENGINE.md`). It is listed in RUNTIME.md as a coordinated
> service but is not owned by the runtime — the runtime invokes it; the engine owns
> workflow graph progression. This document's module row reflects that separation.

## Android Boundary Enforcement (ADR-0010)

Android-facing behavior remains owned by the existing `services`, `sandbox`, `storage`, `security`, `runtime`, `application`, `ui`, and `shared` modules. Foreground/background services, WorkManager handoff, notifications, process and device lifecycle, app-private storage, quotas, provider/network degradation, and Android permission mappings MUST use the public interfaces and canonical owners listed in this document; an adapter MUST NOT conceal or replace those semantics.

Mechanical checks and interface tests MUST verify that every Android-facing implementation is reachable through an allowed public interface and dependency edge. The checks MUST reject UI-to-sandbox/provider/tool leakage, provider-to-Android-UI dependencies, sandbox-to-provider coupling, shared-module upward dependencies, concrete implementation imports across boundaries, and module cycles. Emulator/device evidence MUST exercise process death, ANR/Doze, foreground/background transitions, restart/checkpoint, notifications, app-private storage, quotas, and permission/security behavior where the affected contract applies.

This section adds no module, package namespace, lifecycle, permission scope, adapter-owned persistence, or cross-platform architecture. `services` and existing platform-aware owners remain authoritative.
