> **Status: DERIVED** for Execution message contract.
> This document defines protocol messages for Execution operations. Canonical subsystem behavior is defined in the owning architecture document.
>
> Depends on: the canonical runtime and execution lifecycle sources.
> Referenced by: APIs, SDKs, tasks, workflows, and tests.

# Execution Protocol — Nexora

## Lifecycle Alignment

Execution protocol state transitions remain governed by the execution lifecycle specifications. Where execution events interact with workspace or session boundaries, they SHOULD remain consistent with [../lifecycle/WorkspaceLifecycle.md](../lifecycle/WorkspaceLifecycle.md) and [../lifecycle/SessionLifecycle.md](../lifecycle/SessionLifecycle.md).

## Envelope Rules

Execution messages SHOULD preserve correlation, version, checkpoint, replay, and terminal outcome semantics across retries and resumptions.
