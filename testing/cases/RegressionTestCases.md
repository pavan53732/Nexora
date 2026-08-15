# Regression Test Case Inventory — Nexora

| Case ID | Suite | Purpose | Owner | Status | Evidence | Last Reviewed |
|---|---|---|---|---|---|---|
| RT-CONTRACT-001 | RT-CONTRACT | Compare canonical contract samples for drift | API Contracts | Planned | `evidence/regression/RT-CONTRACT-001/` | 2026-08-04 |
| RT-PROVIDER-001 | RT-PROVIDER | Validate provider response compatibility stability | Provider Layer | Planned | `evidence/regression/RT-PROVIDER-001/` | 2026-08-04 |
| RT-PLUGIN-001 | RT-PLUGIN | Validate plugin activation backward compatibility | Plugin System | Planned | `evidence/regression/RT-PLUGIN-001/` | 2026-08-04 |
| RT-MIG-001 | RT-MIG | Validate manifest/schema backward-compatible interpretation | Compatibility & Migration | Planned | `evidence/regression/RT-MIG-001/` | 2026-08-04 |
| RT-STREAM-001 | RT-STREAM | Verify provider adapters preserve typed stream contract across upgrades | Provider Layer | Planned | `evidence/regression/RT-STREAM-001/` | 2026-08-06 |
| RT-STREAM-002 | RT-STREAM | Verify old non-stream completion adapts to canonical event sequence | Provider Layer | Planned | `evidence/regression/RT-STREAM-002/` | 2026-08-06 |
| RT-REASON-001 | RT-REASON | Verify reasoning effort and summary contracts remain backward-compatible | Reasoning | Planned | `evidence/regression/RT-REASON-001/` | 2026-08-06 |
| RT-LIVE-001 | RT-LIVE | ProviderStream STALLED failover transition and bounded budget remain canonical across revisions | Provider Layer | Planned | `evidence/regression/RT-LIVE-001/` | 2026-08-15 |
| RT-LIVE-002 | RT-LIVE | NXR-2002 timeout remains reconciliation-first and does not regress to generic retry | Tool + Runtime | Planned | `evidence/regression/RT-LIVE-002/` | 2026-08-15 |
| RT-LIVE-003 | RT-LIVE | RetryPending direct start preserves backoff and scheduler authorization | Task Lifecycle | Planned | `evidence/regression/RT-LIVE-003/` | 2026-08-15 |
| RT-LIVE-004 | RT-LIVE | Agent Completing finalization transition remains explicit and terminal commit is guarded | Agent Lifecycle | Planned | `evidence/regression/RT-LIVE-004/` | 2026-08-15 |
| RT-LIVE-005 | RT-LIVE | Failure/cancellation/denial/missing-draft paths cannot regress into successful completion | Agent Runtime | Planned | `evidence/regression/RT-LIVE-005/` | 2026-08-15 |
