> **Status: DERIVED** for Tool message contract.
> This document defines protocol messages for Tool invocation. Canonical subsystem behavior is defined in the owning architecture document.
>
> Depends on: the canonical architecture document for Tool.
> Referenced by: models, APIs, SDKs, security, and tests.

# Tool Protocol — Nexora

## Invocation

1. Caller submits a `ToolInvokeRequest` containing `requestId`, `correlationId`, `toolCallId`, workspace scope, caller identity, and typed input payload.
2. Runtime validates schema, permissions, policy, sandbox requirements, and approval state before side effects.
3. Tool execution emits ordered lifecycle events only after durable transition commit.
4. Terminal outcome returns a `ToolInvokeResponse` with status, version, output/artifacts, usage, approvals required, and canonical error envelope when failed.

## Message Rules

Every invocation or event message MUST preserve:

- `correlationId`
- `toolCallId`
- `workspaceId`
- `toolId`
- durable `version` on lifecycle transitions
- `idempotencyKey` for side-effecting retries
- opaque `resumeToken` for resumable streams or long-running calls
- canonical error envelope fields on failure

## Error Handling

Permission denial, approval requirements, timeout, cancellation, invalid parameters, sandbox failure, and provider failure MUST map to canonical `NXR-*` errors. Clients MUST use error code and metadata, not free-form text, as compatibility inputs.

## Timeout

Timeout is a terminal tool-call outcome and MUST emit a final lifecycle event after the timeout state is durably committed.

## Cross-Layer Contract Rules

Protocol messages MUST map to [docs/api/Tool-API.md](../docs/api/Tool-API.md). Consumers MUST treat events as at-least-once, deduplicate by `(entityId, version, transition)`, and never infer success from transport completion alone.

## Canonical Error Mapping

| Operation | Canonical `NXR-*` codes |
|---|---|
| invoke | NXR-2001, NXR-2002, NXR-2003, NXR-2004, NXR-2005, NXR-2009 |
| cancelToolCall | NXR-2010, NXR-7007 |
| result/cleanup | NXR-2008, NXR-7007 |
