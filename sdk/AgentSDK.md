# Agent SDK — Nexora

The Agent SDK provides base classes, execution loop loops, and utility abstractions for developing custom autonomous agent types inside Nexora.

---

## SDK Architecture

All custom agent implementations MUST extend the `BaseAgent` class provided by the SDK. This guarantees that task decomposition, context building, provider switching, and grounding rules are handled uniformly.

```kotlin
package com.nexora.app.sdk.agent

abstract class BaseAgent(
    val descriptor: AgentDescriptor
) {
    /**
     * Executes the autonomous loop for the given goal.
     * Streams progress and returns a final execution outcome.
     */
    abstract suspend fun execute(
        goal: String, 
        context: AgentContext
    ): AgentOutput
}

data class AgentContext(
    val correlationId: String,
    val workspaceId: String,
    val taskId: String,
    val tokenBudget: TokenBudget,
    val currentCheckpoint: AgentCheckpoint?,
    val activeProviderProfileId: String
)

data class AgentOutput(
    val success: Boolean,
    val finalResponse: String,
    val summary: String,
    val error: CanonicalErrorEnvelope? = null
)
```

## Grounding & Anti-Hallucination Enforcements

Custom agents extending the SDK are bound by the platform's anti-hallucination rules:
- **Zero-Assumption Mode**: The agent is forbidden from assuming or guessing missing parameters. If ambiguous, the agent loop MUST call `askUser()` or yield with a clarification request.
- **Tool-Before-Claim**: Any factual claim made by the agent in chat MUST trace directly to a tool result stored in the active task history. Unsourced statements are highlighted as opinion or unverified.
- **Git Grounding Rules**: When executing version control tasks, the agent MUST run a read-only pass (status → diff) before running mutable actions. No destructive actions are permitted without a generated preview.

## Errors & Watchdog Heartbeats

Agents running autonomous loops MUST report periodic watchdog heartbeats via `context.heartbeat()`. If an agent hangs or fails to iterate for longer than `maxIterationTimeMs`, the platform watchdog traps the freeze, logs `NXR-3004` (Agent Timeout), cancels the coroutine context, and attempts to restart the loop from the last valid checkpoint.
