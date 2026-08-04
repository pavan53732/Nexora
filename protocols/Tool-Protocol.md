> **Status: DERIVED** for Tool message contract.
> This document defines protocol messages for Tool. Canonical subsystem behavior is defined in the owning architecture document.
>
> Depends on: the canonical architecture document for Tool.
> Referenced by: models, APIs, SDKs, and tests.


# Tool Protocol — Nexora

> Communication contract between the runtime/tool manager and tools.

## Invocation

1. Tool Manager receives a `ToolCall` from the AI response.
2. Tool Manager validates parameters against the tool's `JsonSchema`.
3. Tool Manager checks permissions via `PermissionManager`.
4. If approved, Tool Manager calls `tool.execute(params, context)`.
5. Tool returns a `ToolResult` (Success, Error, or NeedsApproval).

## Error Handling

- **Recoverable errors**: Return `ToolResult.Error(recoverable = true)`. The agent loop retries.
- **Non-recoverable errors**: Return `ToolResult.Error(recoverable = false)`. The agent loop reports failure.
- **Permission denied**: Return `ToolResult.NeedsApproval`. The agent loop pauses for user input.

## Timeout

Each tool declares a `timeout`. If exceeded, the Tool Manager cancels the execution and returns an error.
