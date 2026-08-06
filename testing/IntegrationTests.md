# Integration Tests

## Scope

Integration tests validate subsystem interactions and cross-layer contract preservation.

## Suite IDs

- `IT-CONTRACT-*` — cross-layer envelope and lifecycle preservation
- `IT-AGENT-*` — agent/runtime/task integration
- `IT-TOOL-*` — tool, sandbox, and permission integration (including multi-scope TOOL-408 enforcement, classifier gate ordering)
- `IT-PROVIDER-*` — provider completion and streaming
- `IT-PLUGIN-*` — plugin lifecycle and rollback
- `IT-MEMORY-*` — memory persistence and retrieval
- `IT-LC-*` — lifecycle integration (Session transitions, checkpoint resume identity, terminal retry identity, ToolStatus integration)

## Framework Stack

- Kotlin integration test framework
- emulator/device harness where needed
- service doubles for providers and plugins

## Test Environment

Integration environments MUST exercise storage, eventing, and orchestration layers together.

## Key Scenarios

- `IT-AGENT-001` agent starts task and emits durable lifecycle events
- `IT-TOOL-001` tool invocation flows through permission and sandbox checks
- `IT-PROVIDER-001` provider streaming returns ordered terminal semantics
- `IT-PLUGIN-001` plugin activation registers capabilities transactionally
- `IT-CONTRACT-001` runtime replay or retry preserves correlation and durable versions
- `IT-TOOL-002..014` complete authorization, classifier ordering, error mapping, and correlation preservation
- `IT-LC-001..020` Session/Execution/ToolStatus integration, same-ID resume, terminal retry lineage, and replay safety

## S13 Traceability

- `IT-TOOL-002..014` map to PermissionModel, Tool System, Tool Protocol, Tool API, `FR-S016`, and `FR-TL015`.
- `IT-LC-001..020` map to Runtime ExecutionStatus, Background Execution, Autonomy Stability, Execution Protocol, Runtime API, `FR-AS-007`, `NFR-REL-001`, `NFR-REL-002`, and `NFR-REL-012`.
- All listed cases are `Planned`; evidence paths are declared in the case inventory.

## Naming Convention

Names SHOULD reflect subsystem boundaries and requirement or contract concerns.

## Coverage Target

Cross-layer contract-sensitive paths are mandatory.

## CI Policy

Contract-affecting documentation changes SHOULD be mirrored by integration evidence updates.

## Canonical Contract Evidence

Integration suites SHOULD explicitly validate:

- `correlationId` continuity across subsystem boundaries
- idempotent retry behavior for keyed operations
- terminal outcome semantics for streaming and cancellation
- canonical error-envelope preservation across adapters
- lifecycle event ordering after durable commit
- event deduplication and replay behavior
