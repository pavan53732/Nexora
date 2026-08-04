# Runtime API — Nexora

The Runtime API governs workspace, session, task, and execution operations exposed by the runtime layer.

## Lifecycle Alignment

Workspace lifecycle semantics are governed by [lifecycle/WorkspaceLifecycle.md](../../lifecycle/WorkspaceLifecycle.md). Session lifecycle semantics are governed by [lifecycle/SessionLifecycle.md](../../lifecycle/SessionLifecycle.md). Execution lifecycle semantics remain governed by the runtime architecture and execution lifecycle specifications.

## Contract Notes

Runtime API envelopes SHOULD preserve correlation, versioning, and replay-safe semantics across workspace, session, task, and execution boundaries.
