> **Status: CANONICAL** for provider lifecycle states, health checks, failover, and routing eligibility.
> This document owns the formal state machine for provider lifecycle:
> health state, failover state, disablement, and routing eligibility.
> It does NOT own provider subsystem architecture (see
> [../architecture/PROVIDER_SYSTEM.md](../architecture/PROVIDER_SYSTEM.md)).
>
> Depends on: [../architecture/PROVIDER_SYSTEM.md](../architecture/PROVIDER_SYSTEM.md).
> Referenced by: [../models/Provider.md](../models/Provider.md), [../protocols/Provider-Protocol.md](../protocols/Provider-Protocol.md).

# Provider Lifecycle State Machine

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

A **Provider** in Nexora represents an external AI model endpoint (OpenAI, Anthropic, local Ollama, etc.) that agents use for inference. The Provider Lifecycle manages registration, configuration, health monitoring, and automatic failover — ensuring agents always route requests to a functional backend.

## States

| State | Description |
|-------|-------------|
| **Registered** | Provider record created with endpoint URL and credentials. |
| **Configuring** | Applying model parameters, rate limits, and token budgets. |
| **Configured** | Static configuration complete; not yet tested. |
| **Testing** | Probe request sent to validate connectivity and model access. |
| **Healthy** | Provider passing health checks; eligible for request routing. |
| **Degraded** | Elevated latency or intermittent errors; still routable with caution. |
| **Unhealthy** | Consistently failing health checks; excluded from routing. |
| **Disabled** | Manually disabled by user; excluded from routing and health checks. |
| **Removed** | Terminal state — provider record deleted. |

## Transitions

| Trigger | From | To | Guard |
|---------|------|----|-------|
| `register()` | [*] | Registered | Endpoint URL valid |
| `configure()` | Registered | Configuring | — |
| `testConnection()` | Configured | Testing | — |
| `markHealthy()` | Testing / Degraded | Healthy | Response < latency threshold |
| `markDegraded()` | Healthy | Degraded | Latency > warn threshold or error rate > 5% |
| `markUnhealthy()` | Degraded | Unhealthy | Consecutive failures >= 3 |
| `disable()` | Healthy / Degraded / Unhealthy | Disabled | — |
| `enable()` | Disabled | Testing | Re-probe before re-enabling |
| `remove()` | Disabled / Unhealthy | Removed | No active agent sessions depend on it |

### Auto-Transitions (Health Monitor)

The `HealthMonitor` coroutine runs periodic probes (configurable interval, default 30s) against every non-Disabled provider. It drives the **Healthy → Degraded → Unhealthy** degradation chain based on observed metrics:

- **Degraded**: P95 latency exceeds `warnLatencyMs` or error rate exceeds 5% over the rolling window.
- **Unhealthy**: Three consecutive probe failures or error rate exceeds 20%.

On **Unhealthy**, the `ProviderRouter` automatically excludes the provider and selects the next highest-priority Healthy provider. If no Healthy provider remains, the router falls back to the highest-priority Degraded provider and emits a `ProviderFallbackWarning` event.

## State Diagram

```mermaid
stateDiagram-v2
    [*] --> Registered

    Registered --> Configuring : configure()
    Configuring --> Configured : configureComplete()
    Configured --> Testing : testConnection()
    Testing --> Healthy : markHealthy()
    Testing --> Unhealthy : markUnhealthy()
    Healthy --> Degraded : markDegraded()
    Degraded --> Healthy : markHealthy()
    Degraded --> Unhealthy : markUnhealthy()
    Unhealthy --> Testing : testConnection()
    Healthy --> Disabled : disable()
    Degraded --> Disabled : disable()
    Unhealthy --> Disabled : disable()
    Disabled --> Testing : enable()
    Disabled --> Removed : remove()
    Unhealthy --> Removed : remove()
    Removed --> [*]

    note right of Healthy : Auto-transition to Degraded\non latency/error threshold
    note right of Degraded : Auto-transition to Unhealthy\non consecutive failures
```

## Implementation Notes

Provider state is managed by the `ProviderRegistry` singleton, which persists configuration to the Room `provider` table and maintains an in-memory `ProviderStatusMap` for fast routing lookups. The `HealthMonitor` runs as a `CoroutineScope` with a `FixedDelayRouter` — it batches probe requests and updates statuses atomically. The `ProviderRouter` implements a priority-based selection strategy with automatic fallback, emitting `ProviderRouted` and `ProviderFallbackWarning` events to the shared bus for observability.