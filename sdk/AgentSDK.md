# Agent SDK — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See [../docs/api/Agent-API.md](../docs/api/Agent-API.md)

---

## Normative SDK Contract

The Agent SDK MUST preserve the contract defined by [Agent-API.md](../docs/api/Agent-API.md). Convenience builders MUST NOT hide task IDs, correlation IDs, idempotency keys, resume tokens, delegated-work references, or canonical error envelopes.

### Required Operation Coverage

A conforming SDK implementation MUST provide typed support for:

- agent descriptor creation
- agent registration
- task start/cancel/status operations
- delegated-work metadata
- lifecycle event emission metadata
- canonical error-envelope creation and propagation
- pagination and filter handling for registry/list operations

## Overview

The Agent SDK helps implement agents that conform to the canonical runtime contract.

## Creating an Agent

```kotlin
interface AgentImplementation {
    val descriptor: AgentDescriptor
    suspend fun onStart(request: StartTaskRequest, context: AgentExecutionContext): TaskProjection
    suspend fun onCancel(taskId: String, context: AgentExecutionContext): TaskProjection
}
```

## Registering

```kotlin
agentApi.registerAgent(myAgent.descriptor)
```

## Agent ID Convention

Agent IDs MUST be stable and registry-compatible.

## Compatibility Rules

SDKs MUST expose compatibility metadata for contract version, supported delegation model, background execution support, and manifest/schema version.
