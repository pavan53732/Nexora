# DEC-49 — Retire W7 Research-Workload Target

- **Status:** Accepted
- **Date:** 2026-08-21
- **Deciders:** Creator / Product Owner
- **Scope:** Requirement and roadmap boundary only; no implementation authorization.

## Decision

The former W7 250-item research-workload target is removed entirely from active Nexora requirements and retained only as rejected/obsolete historical context. It does not select or require an admitted workload size, queue length, completed-item target, planned-subtask limit, concurrent-worker limit, benchmark, normative ceiling, lifecycle, error, authority, or implementation mechanism.

Existing technical limits for correctness, safety, liveness, Android/device protection, context windows, provider calls, Tool calls, deadlines, resources, concurrency, retry, reconciliation, and evidence remain governed by their existing canonical requirements and owners.

## Boundaries and non-goals

This decision creates no new requirement family, state, error code, identity, lifecycle, authority, workload limit, benchmark, persistence field, API, protocol, or implementation mechanism. It does not modify the creator-owned product design document. It does not authorize source implementation or claim test execution or executed evidence.

## Required propagation

Active requirements, roadmap projections, completeness inventories, traceability mappings, and derived planning documents MUST NOT present W7 as a current target or unresolved owner decision. Historical changelog and decision text may retain the former target only as historical evidence, clearly superseded by this decision.
