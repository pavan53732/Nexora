> **Status: SUPPORTING** for Logging Standard coding standard.
> This document defines conventions for Logging Standard. It applies across all subsystems and does not override canonical subsystem definitions.


# Logging Standard — Nexora

## Logger
Use `android.util.Log` with a Nexora tag prefix:

```kotlin
private const val TAG = "Nexora:ToolManager"
Log.d(TAG, "Executing tool: $toolId")
```

## Log Levels

| Level | When |
|-------|------|
| `ERROR` | Unrecoverable failures, exceptions. |
| `WARN` | Recoverable issues, retries, deprecated usage. |
| `INFO` | High-level events: task started, agent created, plugin installed. |
| `DEBUG` | Detailed flow: each agent loop iteration, each tool call. |
| `VERBOSE` | Very detailed: raw HTTP requests, full context payloads. |

## Sensitive Data
- **NEVER** log API keys, tokens, or passwords.
- **NEVER** log full file contents (log first 200 chars max).
- **NEVER** log raw private chain-of-thought, hidden system prompts, provider resume tokens, or unredacted stream payloads.
- Log stream identity/sequence/event type and sanitized ReasoningSummary metadata instead of raw deltas.
- Use `SecureKeyStore` references, not actual values.

## Structured Logging
All execution events are also published to the `EventBus` as `ExecutionEvent` objects. This provides structured, queryable observability beyond text logs.
