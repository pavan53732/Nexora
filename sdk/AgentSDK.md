> **Status: DERIVED** for AgentSDK SDK.
> This document describes the sdk surface for AgentSDK. Canonical behavior is defined in the owning architecture document.
>
> Depends on: the canonical architecture document for AgentSDK.
> Referenced by: upstream architecture, models, protocols, and implementation consumers.


# Agent SDK — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

> **Testing:** Agent tests: [testing/UnitTests.md](../testing/UnitTests.md) (Agent section), [testing/IntegrationTests.md](../testing/IntegrationTests.md), [testing/E2ETests.md](../testing/E2ETests.md).

---

## Normative SDK Contract

The SDK is an adapter over the corresponding API and protocol. SDK convenience methods MUST NOT create a second lifecycle or error vocabulary. Every operation MUST preserve correlation ID, canonical error fields, lifecycle effect, cancellation outcome, and idempotency behavior from the API contract.

| SDK responsibility | Required behavior |
|---|---|
| Request construction | Validate local arguments without changing server-side lifecycle semantics. |
| Result projection | Expose durable status, execution phase, transition version, and correlation ID where the API provides them. |
| Errors | Map canonical `NXR-*` codes to typed SDK errors while preserving the original envelope and redacted details. |
| Retry | Never retry automatically unless the canonical error says retry is safe and the operation is idempotent or keyed. |
| Cancellation | Propagate cancellation to the API/protocol and expose the committed terminal outcome. |
| Events/streams | Preserve ordering metadata and deduplicate at-least-once events; do not infer success from transport closure. |
| Compatibility | SDK version changes MUST document any renamed projection or transport mapping without changing canonical meanings. |

### Required Operation Coverage

The SDK MUST expose or explicitly mark unsupported the operation contracts for agent execution, task cancellation/status, tool invocation, provider completion/streaming, and plugin install/activation. Unsupported operations MUST return a canonical capability error rather than a generic exception.

## Overview

The Agent SDK enables developers to create custom agent types. Each agent has a specialized role, system prompt, and default tool set.

## Creating an Agent

```kotlin
class DataAnalystAgent : Agent {
    override val id = "data_analyst"
    override val type = AgentType.CUSTOM
    override val name = "Data Analyst"
    override val description = "Analyzes data, creates visualizations, and generates insights."
    override val capabilities = listOf("data_analysis", "visualization", "reporting")
    override val defaultTools = listOf(
        "file_read", "file_write", "terminal_run",
        "python_execute", "sqlite_query"
    )
    override val systemPrompt = """
        You are a data analyst. You analyze data files, run Python scripts
        for statistical analysis, create charts, and generate reports.
        Always use the sandbox to execute code. Always save results to files.
    """.trimIndent()

    override suspend fun execute(task: AgentTask, context: AgentContext): AgentResult {
        // Agent-specific execution logic
        // Typically delegates to the agent loop with specialized context
    }
}
```

## Registering

```kotlin
agentRegistry.register(DataAnalystAgent())
```

## Agent ID Convention

Built-in agents use `AgentType` enum values. Custom agents use snake_case IDs.

See [registry/AGENTS.md](../registry/AGENTS.md) for assigned IDs.
