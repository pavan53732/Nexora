> **Status: CANONICAL** for provider lifecycle states, health checks, failover, and routing eligibility.
> This document owns the formal state machine for provider lifecycle:
# Provider Lifecycle State Machine

> **Status: CANONICAL** for provider lifecycle states, health checks, failover, and routing eligibility.
> This document owns the formal state machine for provider lifecycle:
> health state, failover state, disablement, and routing eligibility.
> It does NOT own provider subsystem architecture (see
> [../architecture/PROVIDER_SYSTEM.md](../architecture/PROVIDER_SYSTEM.md)).
>
> Depends on: [../architecture/PROVIDER_SYSTEM.md](../architecture/PROVIDER_SYSTEM.md).
> Referenced by: [../models/Provider.md](../models/Provider.md), [../protocols/Provider-Protocol.md](../protocols/Provider-Protocol.md).

A **Provider** in Nexora represents an external/cloud AI model endpoint (OpenAI, Anthropic, Gemini, Groq, OpenRouter, or an eligible Custom external endpoint) that agents use for inference. Local AI model endpoints are out of scope under DEC-41. The Provider Lifecycle manages registration, configuration, health monitoring, and routing eligibility. It does not represent an individual inference stream; per-stream state, backpressure, reconnect, cancellation, and terminal behavior are owned by [ProviderStreamLifecycle.md](ProviderStreamLifecycle.md).

## Administrative Lifecycle (ProviderStatus)

The administrative lifecycle tracks manual configuration, registration, enablement, and removal. This is stored in `Provider.status: ProviderStatus`.

### States

| State | Description |
|-------|-------------|
| **REGISTERED** | Provider record created with endpoint URL and credentials. |
| **CONFIGURING** | Applying model parameters, rate limits, and token budgets. |
| **CONFIGURED** | Static configuration complete; not yet tested. |
| **TESTING** | Probe request sent to validate connectivity and model access. |
| **ACTIVE** | Enabled and eligible for routing (subject to health). |
| **DISABLED** | Manually disabled by user; excluded from routing and no longer actively health-evaluated; persisted health is preserved. |
| **REMOVED** | Terminal state — provider record deleted; health has no operational effect. |

### Transitions

| Trigger | From | To | Guard |
|---------|------|----|-------|
| `register()` | [*] | REGISTERED | Endpoint URL valid |
| `configure()` | REGISTERED | CONFIGURING | — |
| `configureComplete()` | CONFIGURING | CONFIGURED | Configuration persisted |
| `testConnection()` | CONFIGURED | TESTING | — |
| `markHealthy()` | TESTING | ACTIVE | Probe response < latency threshold |
| `disable()` | ACTIVE | DISABLED | — |
| `enable()` | DISABLED | TESTING | Re-probe before re-enabling |
| `remove()` | DISABLED | REMOVED | No active agent sessions depend on it |

## Operational Health (ProviderHealth)

The operational health tracks runtime reachability, latency, and error rates. This is stored in `Provider.health: ProviderHealth` and managed by the background `HealthMonitor` coroutine.

### States

| State | Description |
|-------|-------------|
| **UNKNOWN** | Initial state before first health check. |
| **HEALTHY** | Provider passing health checks; eligible for request routing. |
| **DEGRADED** | Elevated latency or intermittent errors; still routable with caution. |
| **UNHEALTHY** | Consistently failing health checks; excluded from routing. |

### Auto-Transitions (Health Monitor)

The `HealthMonitor` coroutine runs periodic probes (configurable interval, default 30s) against every provider whose `status` is not `DISABLED` or `REMOVED`. It drives the **HEALTHY → DEGRADED → UNHEALTHY** degradation chain based on observed metrics:

- **DEGRADED**: P95 latency exceeds `warnLatencyMs` or error rate exceeds 5% over the rolling window.
- **UNHEALTHY**: Three consecutive probe failures or error rate exceeds 20%.

On **UNHEALTHY**, the `ProviderRouter` excludes the provider from new routing and selects the next highest-priority eligible HEALTHY provider. If no HEALTHY provider remains, it may select the highest-priority DEGRADED provider and emits `ProviderFallbackWarning`. An already-open stream follows ProviderStreamLifecycle: failover creates a new stream with lineage and never splices replacement output into the prior stream.

## Status/Health Cross-Field Notation

Administrative transitions use `From` and `To` exclusively for `ProviderStatus`. A `ProviderHealth` value may appear only as a `Guard` predicate when a transition explicitly requires one; it is not a ProviderStatus lifecycle state. Consequently, `status == ACTIVE AND health == UNHEALTHY` does not permit direct removal: the provider must first transition through `ACTIVE → DISABLED` before `DISABLED → REMOVED`. After `DISABLED`, persisted health is retained but no longer actively evaluated. After `REMOVED`, health has no operational effect.

## Combined Routing Eligibility

A provider is eligible for primary request routing **only when**:
- `status == ACTIVE` AND `health == HEALTHY`

Degraded providers may be used if no healthy alternative is configured (emitting warning events). Unhealthy providers are immediately excluded from active routing tables.
