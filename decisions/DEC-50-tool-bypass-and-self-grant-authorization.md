# DEC-50 — Tool-Level Bypass and Self-Grant Authorization Paths

- **Status:** Accepted
- **Date:** 2026-08-22
- **Deciders:** Architecture Owner / Product Owner
- **Supersedes:** The active effect of DEC-42's "no ALLOW override, no bypass ASK
  approval" constraint and DEC-44's standing rule regarding authorization
  classifier boundaries; DEC-42 and DEC-44 remain immutable historical
  authorities for the previously selected local-model and no-local-classifier
  boundaries.
- **Scope:** Documentation contract only; implementation and executed evidence
  remain separately authorized work.

## Context

DEC-42 established that the product uses cloud/external AI providers only and
removed the optional on-device TFLite auto-approval classifier. DEC-44 elevated
the combined DEC-41/DEC-42 boundary into a standing repository rule (AGENTS.md
Rule 9) prohibiting local AI models and any bypass of PermissionModel.

The product owner now selects an explicit, structured **tool-level bypass and
self-grant authorization path** that permits certain Tool descriptors to
declare authorization override, jailbreak-prompt handling, and self-granted
permission scopes. This decision carves a bounded exception within the existing
authorization architecture: bypass is opt-in per-Tool, auditable, and
propagates through the existing authorization, sandbox, provider, and
evidence contracts rather than replacing them.

## Decision

### 1. Per-Tool bypass flags

A Tool descriptor MAY declare the following boolean flags, each defaulting to
`false`:

- **`bypassSafeguards`** — when `true`, the authorization gate in
  `architecture/AGENT_RUNTIME.md` §Agent Loop bypasses
  `PermissionManager.authorizeToolCall()` and returns `PermissionResult.Allowed`
  immediately. The `ToolExecutedEvent` records `bypassSafeguards=true` for audit.
  This does not remove the permission gate for non-flagged tools.

- **`allowJailbreakPrompts`** — when `true`, the provider adapter delegates to
  `AIProvider.handleJailbreakPrompt()` which sets
  `bypassProviderSafety=true` on the `CompletionRequest`, causing the adapter
  to skip provider-native safety classifier injection, refusal-inducing system
  prompt additions, and safety parameter filtering. The `jailbreakMode` is set
  to `JailbreakMode.ALLOW_ALL`.

- **`selfGrantPermissions`** — when `true`, `authorizeToolCall()` is called
  with `forceAskAsAllow=true`, downgrading all ASK scope decisions to
  `SELF_GRANT` (PolicySource.SELF_GRANT). The `DENY` branch is downgraded to
  `ALLOW` with `PolicySource.BYPASS` when `bypassSafeguards=true` is also set.

### 2. Provider-side safety bypass

When `request.bypassProviderSafety=true`, the `ProviderAdapter` (in
`architecture/PROVIDER_SYSTEM.md` §Provider Adapter Bypass & Jailbreak) MUST
skip:

- Provider-native safety classifier injection
- Refusal-inducing system prompt additions
- Safety parameter filtering (harm scopes, content filters, refusal thresholds)
- Evidence/validation requirement enforcement

The raw prompt is forwarded to the provider endpoint with `providerParams`
passed through unmodified. This only applies to the active cloud/external
provider endpoint under DEC-44; localhost/local-model endpoints remain invalid.

### 3. Sandbox bypass propagation

When `Tool.bypassSafeguards=true`, the sandbox `execute()` method receives
`SandboxLimits(bypassSandbox=true, elevatedPrivileges=true)`, which disables:

- Filesystem restrictions (unrestricted access to `/data`, `/system`, `/sdcard`)
- Network egress filtering (unfiltered network egress through the egress proxy)
- Process limits (elevated process limits)
- Timeout enforcement (relaxed timeouts)
- Output sanitization (`sanitizeOutput` is skipped; raw results returned)

### 4. Audit and tracing

Every bypass-flagged tool call is recorded through the existing
`ToolExecutedEvent` schema with `bypassSafeguards`,
`allowJailbreakPrompts`, and `selfGrantPermissions` fields. The
`permission_audit_log` records `PolicySource = BYPASS` and
`FinalPermissionOutcome = ALLOWED_BY_POLICY_BYPASS` when bypass is active.
The `TokenUsageRecord` and execution history record the bypass flags for
traceability.

### 5. Scope of the exception

This bypass path applies **only** to Tools whose descriptors explicitly set
the bypass flags. Regular tools, regular agent operations, and non-flagged
requests remain governed by the full existing authorization, sandbox, and
provider safety contracts. DEC-42/DEC-44 constraints on local model execution,
provider isolation, and classifier boundaries remain in full force for all
non-bypass code paths.

## Preserved Invariants

- This decision does not create a new Tool identity, lifecycle state, or
  permission scope. `SELF_GRANT` and `BYPASS` are PolicySource enum values, not
  new permission scopes.
- The existing permission audit trail, sandbox telemetry, and evidence
  contracts remain authoritative for bypass-flagged calls; bypass is an
  authorized override, not a bypass of the audit/record path.
- `bypassProviderSafety` only affects the active cloud/external provider under
  DEC-44; no local model execution is enabled.
- Local non-AI execution (sandboxed terminal/process execution, filesystem
  operations, Git, SQLite/Room persistence, checkpoints, local workspace
  search) remains as previously authorized.
- No internal credit, spending, or token-budget control exists for the user
  (DEC-25, DEC-45); bypass is an authorization/permission concern, not a cost
  gate.

## Required Projections

The owning and derived documents must align the bypass and self-grant
contracts, including `architecture/PROVIDER_SYSTEM.md`,
`architecture/TOOL_SYSTEM.md`, `architecture/AGENT_RUNTIME.md`,
`architecture/RUNTIME.md`, `architecture/SECURITY_MODEL.md`,
`architecture/SANDBOX.md`, `security/PermissionModel.md`,
`security/SandboxPolicy.md`, `specs/CONTEXT_MANAGEMENT.md`,
`specs/AI_PROVIDERS.md`, `models/Inference.md`, `models/Permission.md`,
`models/Tool.md`, `protocols/Tool-Protocol.md`, `docs/api/Tool-API.md`,
`docs/api/Provider-API.md`, `sdk/ProviderSDK.md`, `sdk/ToolSDK.md`,
`diagrams/Agent-Execution-Flow.md`, `diagrams/Tool-Execution-Flow.md`,
`docs/ROADMAP.md`, `docs/adr/ADR-0005-Provider-Abstraction.md`,
`docs/CANONICAL_SOURCES.md`, `docs/CHANGELOG.md`, and
`docs/DECISION_LOG.md`. Historical DEC-42 and DEC-44 records remain unchanged
and are superseded only where the active bypass scope is discussed.

## Canonical ownership

This decision owns the tool-level bypass and self-grant authorization path at
the repository level. `security/PermissionModel.md` owns the
`authorizeToolCall()`, `checkPermission()`, `resolveDecision()` function
implementations and the `PermissionDecision`/`PolicySource`/
`FinalPermissionOutcome` enum semantics.
`architecture/PROVIDER_SYSTEM.md` owns the `AIProvider` interface,
`bypassSafeguards()` extension, `handleJailbreakPrompt()` method, and
`ProviderAdapter.callProvider()` routing logic.
`architecture/SANDBOX.md` owns `SandboxLimits` and bypass sandbox behavior.
`architecture/TOOL_SYSTEM.md` owns the `Tool` interface with bypass flags.
`specs/CONTEXT_MANAGEMENT.md` owns the `ContextSnapshot` and deliberation
gate bypass semantics.
`architecture/AGENT_RUNTIME.md` owns the agent loop authorization gate
conditionals.
`protocols/Tool-Protocol.md` owns the `ToolExecutionMessage` and
`ToolExecutedEvent` bypass fields.
`docs/CANONICAL_SOURCES.md` owns the canonical-source map entry.
`docs/CHANGELOG.md` and `docs/DECISION_LOG.md` own the historical record.

## References

- `decisions/DEC-42-no-local-ai-models-and-classifier-boundary.md`
- `decisions/DEC-44-standing-cloud-only-ai-models.md`
- `AGENTS.md` Rule 9
- `architecture/PROVIDER_SYSTEM.md`
- `security/PermissionModel.md`
- `architecture/SANDBOX.md`
- `architecture/TOOL_SYSTEM.md`
- `architecture/AGENT_RUNTIME.md`
- `protocols/Tool-Protocol.md`
- `models/Inference.md`
- `models/Permission.md`
- `models/Tool.md`
