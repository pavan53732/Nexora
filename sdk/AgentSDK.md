> **Status: DERIVED** for AgentSDK SDK.
> This document describes the sdk surface for AgentSDK. Canonical behavior is defined in the owning architecture document.
>
> Depends on: the canonical architecture document for AgentSDK.
> Referenced by: upstream architecture, models, protocols, and implementation consumers.


# Agent SDK — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

> **Testing:** Agent tests: [testing/UnitTests.md](../testing/UnitTests.md) (Agent section), [testing/IntegrationTests.md](../testing/IntegrationTests.md), [testing/E2ETests.md](../testing/E2ETests.md).

---

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
