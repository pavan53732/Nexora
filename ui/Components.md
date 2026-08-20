> **Status: SUPPORTING** for Components focused behavior.
> This document explains focused behavior for Components. The canonical subsystem definition is in the owning architecture document.
>
> Depends on: the relevant canonical architecture document.


# UI: Components — Nexora

## Core Components

| Component | Description | Priority |
|-----------|-------------|----------|
| `NexoraAppBar` | Top app bar with workspace name and actions. | P0 |
| `WorkspaceTabs` | Tabbed navigation within a workspace. | P0 |
| `ChatBubble` | AI and user message bubbles with streaming support. | P0 |
| `ToolCallCard` | Expandable card showing tool invocation and result — core of the agent activity feed. | P0 |
| `ActivityCard` | Streamed terminal output, file changes, and progress events rendered inline in chat. | P0 |
| `TaskCard` | Task status card with progress indicator. | P0 |
| `TerminalView` | Terminal emulator — internal only (agent activity / developer mode — read-only observability, see ADR-0006). Not a primary screen. | P2 |
| `FileExplorer` | Tree-view file browser for the virtual file system. | P0 |
| `AgentCard` | Agent status, capabilities, effective autonomy mode, scoped trust band, and downgrade-only override display. | P1 |
| `MemorySearchBar` | Semantic search input for memory recall. | P1 |
| `PluginCard` | Plugin info with install/uninstall button. | P1 |
| `ProviderCard` | Provider config card with health indicator. | P0 |
| `PermissionDialog` | Permission approval/deny dialog. | P1 |
| `StreamingText` | Renders sequenced provisional text separately from committed final output; coalesces UI deltas without changing durable order. | P0 |
| `StreamStatusCard` | Shows connecting, backpressured, reconnecting, partial failure, cancelled, and committed states with prior-stream lineage. | P0 |
| `ReasoningSummaryCard` | Collapsible redacted approach/evidence/decision/uncertainty/verification summary; never raw private chain-of-thought. | P1 |
| `CitationUpdateCard` | Incrementally renders source/citation updates tied to committed evidence references. | P1 |
| `EmptyState` | Placeholder for empty workspaces, no tasks, etc. | P0 |

All components use Jetpack Compose.

## Provider Settings Projection (Creator Product Design)

The existing `ProviderCard` and provider configuration surface MUST project provider/type, external base URL, API-key entry state without exposing the secret, model name, `TEST CONNECTION`, capability refresh/detection where supported, connection status, validation result, and `SAVE`. The UI routes persistence and health/catalog operations through the provider-owned service/API boundary and MUST NOT store a second provider configuration.

A successful connection status MUST NOT be rendered as workspace execution authorization, Tool approval, Task/Execution completion, or proof that every advertised capability is implemented. API keys MUST never appear in logs, prompts, evidence, telemetry, or generated artifacts. The UI is projection-only: it cannot grant permissions, invoke Tools, create lifecycle transitions, or claim executed evidence.

## Autonomy Mode Projection (DEC-46)

The existing `AgentCard`, `TaskCard`, and `ActivityCard` MAY project the effective `Manual`, `Assisted`, or `Autopilot` mode, the scoped trust band that selected it, the presence of a downgrade-only user override, and the reason for a forced `Manual` degraded-mode projection. The mode is selected automatically by the existing runtime and is not confirmed per session or per action. A user downgrade routes through existing settings/permission APIs and takes effect immediately; the UI MUST NOT upgrade the mode, grant a permission, or bypass a high-risk gate. A status notification is observability, not approval.

## Agent Activity and State Presentation

The activity feed is the primary user-visible projection of agent execution. Components MUST
preserve the distinction between provisional and committed content and MUST NOT present a
transport closure, incomplete Tool call, unknown-completion operation, or unverified claim as
successful completion.

| Component | Required state projection |
|-----------|---------------------------|
| `StreamingText` / `StreamStatusCard` | Connecting, provisional, backpressured, reconnecting, partial failure, cancelled, and committed states; stream lineage remains visible when a replacement stream is created. |
| `ToolCallCard` | Pending authorization, authorized, executing, completed, failed, cancelled, unknown completion, or reconciled success/failure, using existing `ToolInvocationStatus` and `ToolCompletionState` values. An exhausted automatic reconciliation remains visibly unresolved/non-successful and never appears as success. |
| `ReasoningSummaryCard` | Redacted approach, evidence, decision, uncertainty, and verification summary only; never raw private chain-of-thought or opaque provider continuation state. |
| `CitationUpdateCard` | Source and freshness/provenance references tied to the applicable claim or evidence record. |
| `TaskCard` / `ActivityCard` | Planned-versus-actual progress, current phase, acceptance progress, checkpoint/recovery notice, explicit clarification/capability block, incomplete outcome, terminal result, or automatic cleanup/reconciliation failure details when an existing terminal session is `Failed` after cleanup exhaustion. The card is observational; automatic recovery does not require a user action, and any optional user action routes through existing terminal/runtime contracts. |
| `PermissionDialog` | Requested scopes, risk context, canonical approval/denial result and applicable denial subreason, including preserved compatibility values, with no implication that approval bypasses sandbox or policy denial. |
| `TaskCard` / `AgentCard` / `ActivityCard` | Task-scoped capability request and delegation state: requested, delegated, approved, denied, active, expired, revoked, cancelled, and completed; includes requesting agent, target worker when applicable, purpose, lifetime/deadline, and final disposition without presenting a temporary grant as a permanent capability. |

### Interaction and Accessibility Rules

Every user-actionable component MUST expose a stable accessible name, role, state, and
purpose to Android accessibility services. Status changes MUST be available without relying
on color, animation, audio, or timing alone. Stream and task progress MUST have a text
alternative, and error/approval/reconciliation states MUST remain discoverable when motion is
reduced or animations are disabled.

Interactive cards MUST support keyboard/switch navigation where the Android device or
accessibility service provides it, preserve focus across stream updates, and avoid moving
focus merely because a new activity event arrived. `reduceMotion` suppresses decorative
motion but does not suppress status, error, approval, citation, or terminal information.

The UI is a projection only. It MUST NOT create lifecycle transitions, grant permissions,
claim verification, or infer successful side effects from visual state. User actions route
through the owning service/API contracts.
