> **Status: SUPPORTING** for provider lifecycle narrative.
> **The canonical state machine definition is owned by
> [../state-machines/ProviderLifecycle.md](../state-machines/ProviderLifecycle.md).**
> This file describes the provider lifecycle in prose; it MUST NOT redefine, rename,
> or subset any state enum from the canonical source.
>
> Depends on: [../state-machines/ProviderLifecycle.md](../state-machines/ProviderLifecycle.md).

# Provider Lifecycle Authority — Nexora

## Administrative Lifecycle (ProviderStatus)

`REGISTERED`, `CONFIGURING`, `CONFIGURED`, `TESTING`, `ACTIVE`, `DISABLED`, `REMOVED`

### Transitions

- `REGISTERED → CONFIGURING`: `configure()` — applying model parameters, rate limits, token budgets.
- `CONFIGURING → CONFIGURED`: `configureComplete()` — configuration persisted.
- `CONFIGURED → TESTING`: `testConnection()` — probe request sent.
- `TESTING → ACTIVE`: `markHealthy()` — probe response < latency threshold.
- `ACTIVE → DISABLED`: `disable()` — manual disable.
- `DISABLED → TESTING`: `enable()` — re-probe before re-enabling.
- `DISABLED → REMOVED`: `remove()` — no active agent sessions depend on it. An `ACTIVE` provider, including one with `health == UNHEALTHY`, must first be disabled.

## Operational Health (ProviderHealth)

`UNKNOWN`, `HEALTHY`, `DEGRADED`, `UNHEALTHY`

### Auto-Transitions (Health Monitor)

The `HealthMonitor` coroutine runs periodic probes against every provider whose `status` is not `DISABLED` or `REMOVED`. After `DISABLED`, persisted health is retained but no longer actively evaluated; after `REMOVED`, health has no operational effect.

- `HEALTHY → DEGRADED`: P95 latency exceeds `warnLatencyMs` or error rate exceeds 5%.
- `DEGRADED → UNHEALTHY`: Three consecutive probe failures or error rate exceeds 20%.
- `DEGRADED → HEALTHY`: Metrics return to healthy thresholds.

On `UNHEALTHY`, the `ProviderRouter` excludes the provider from new routing.

### Status/Health Notation

`From` and `To` lifecycle values refer only to `ProviderStatus`. A `ProviderHealth` value may occur only as an explicit guard predicate; it is not an administrative lifecycle state.

## Combined Routing Eligibility

A provider is eligible for primary request routing **only when**:
- `status == ACTIVE` AND `health == HEALTHY`