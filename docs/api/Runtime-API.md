> **Status: DERIVED** for Runtime API.
> This document describes the api surface for Runtime. Canonical behavior is defined in the owning architecture document.
>
> Depends on: the canonical architecture document for Runtime.
> Referenced by: upstream architecture, models, protocols, and implementation consumers.


# Runtime API — Nexora

> Back to [PROJECT_SPECIFICATION.md](../../PROJECT_SPECIFICATION.md) | See [../architecture/RUNTIME.md](../../architecture/RUNTIME.md)

---

## Normative Operation Contract

The Runtime API owns orchestration, execution scheduling, durable event publication guarantees, background work control, and cross-subsystem correlation. It does not redefine tool, provider, plugin, or agent-specific payload contracts.

| Operation | Lifecycle effect | Success result | Canonical failures | Retry/idempotency | Security and cancellation | Evidence |
|---|---|---|---|---|---|---|
| `enqueueExecution` | Execution `Pending → Queued` | Durable execution projection | Invalid request, queue/storage failure, permission failure | Idempotent with request key | Authorization MUST complete before queue visibility | Runtime integration tests |
| `getExecution` / `listExecutions` | No lifecycle change | Stable projection(s), status, pagination cursor | Not found, invalid filter, unauthorized, storage failure | Safe to retry | Sensitive payloads redacted by caller scope | API contract tests |
| `publishEvent` | No entity transition by itself; records durable event | Committed event projection | Storage failure, invalid envelope, version conflict | Duplicate `(entityId, version, transition)` is deduplicated | Events MUST publish only after durable state commit | Event bus contract tests |
| `startBackgroundJob` / `cancelBackgroundJob` | Background job lifecycle transitions | Durable job projection | Invalid request, conflict, cleanup failure | Idempotent by job and operation key | Cancellation propagates to underlying execution resources | Background execution tests |

## Contract Shapes

```kotlin
data class RuntimeEnvelope(
    val requestId: String,
    val correlationId: String,
    val workspaceId: String,
    val actor: CallerRef,
    val metadata: Map<String, String> = emptyMap()
)

data class ExecutionProjection(
    val executionId: String,
    val correlationId: String,
    val workspaceId: String,
    val status: ExecutionStatus,
    val version: Long,
    val createdAt: Instant,
    val updatedAt: Instant,
    val latestError: CanonicalErrorEnvelope? = null
)
```

## Overview

The Runtime API defines the orchestration layer that ties together agents, tools, providers, plugins, memory, and background execution.

## Core API

```kotlin
interface RuntimeApi {
    suspend fun enqueueExecution(request: RuntimeExecutionRequest): ExecutionProjection
    suspend fun getExecution(executionId: String): ExecutionProjection
    suspend fun listExecutions(filter: ExecutionFilter, page: PageRequest): Page<ExecutionProjection>
}
```

## Event Bus API

```kotlin
interface EventBusApi {
    suspend fun publishEvent(event: CanonicalLifecycleEvent): CanonicalLifecycleEvent
    fun subscribe(filter: EventFilter, resumeToken: String? = null): Flow<CanonicalLifecycleEvent>
}
```

Event subscriptions MUST define resume semantics. If replay/resume is unsupported for a transport, the implementation MUST say so explicitly and MUST NOT imply durable replay by exposing a dummy token.

## Background Service API

```kotlin
interface BackgroundServiceApi {
    suspend fun startBackgroundJob(request: BackgroundJobRequest): BackgroundJobProjection
    suspend fun cancelBackgroundJob(jobId: String, correlationId: String, operationKey: String?): BackgroundJobProjection
}
```

## Canonical Error Mapping

| Operation | Canonical `NXR-*` codes |
|---|---|
| enqueueExecution | NXR-7001, NXR-7002, NXR-7004 |
| getExecution / listExecutions | NXR-7001 |
| publishEvent / subscribe | NXR-7003, NXR-7005 |
| startBackgroundJob / cancelBackgroundJob | NXR-7006, NXR-7007 |

See [ERROR_CODES.md](../../errors/ERROR_CODES.md) for canonical envelope requirements.
