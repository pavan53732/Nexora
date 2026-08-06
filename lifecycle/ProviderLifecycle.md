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
- `ACTIVE / DEGRADED / UNHEALTHY → DISABLED`: `disable()` — manual disable.
- `DISABLED → TESTING`: `enable()` — re-probe before re-enabling.
- `DISABLED / UNHEALTHY → REMOVED`: `remove()` — no active agent sessions depend on it.

## Operational Health (ProviderHealth)

`UNKNOWN`, `HEALTHY`, `DEGRADED`, `UNHEALTHY`

### Auto-Transitions (Health Monitor)

The `HealthMonitor` coroutine runs periodic probes against every non-Disabled provider:

- `HEALTHY → DEGRADED`: P95 latency exceeds `warnLatencyMs` or error rate exceeds 5%.
- `DEGRADED → UNHEALTHY`: Three consecutive probe failures or error rate exceeds 20%.
- `DEGRADED → HEALTHY`: Metrics return to healthy thresholds.

On `UNHEALTHY`, the `ProviderRouter` excludes the provider from new routing.

## Combined Routing Eligibility

A provider is eligible for primary request routing **only when**:
- `status == ACTIVE` AND `health == HEALTHY`