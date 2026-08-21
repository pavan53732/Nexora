# DEC-48 — Retired Optional Capabilities

- **Status:** Accepted
- **Date:** 2026-08-21
- **Deciders:** Creator / Product Owner
- **Scope:** Product-scope boundary and documentation governance only; no implementation authorization.

## Decision

The following capabilities are removed from the active Nexora product and architecture queue:

1. recurring user-facing schedules with recurrence, timezone, missed-run, pause/edit/delete, notification, retry, or history semantics;
2. cross-user sharing, shared projects, and artifact-sharing semantics;
3. authenticated browser takeover or Android session attachment; and
4. webhook or external observability surfaces.

These capabilities MUST NOT be represented as pending product decisions, planned architecture, active requirements, or implementation obligations. Existing Nexora contracts for declarative workflows, Android scheduling, approval, escalation, browser operation, notifications, observability, artifacts, isolation, and audit remain unchanged within their current scope.

## Boundaries and non-goals

This decision does not create a new state, error code, identity, lifecycle, authority, API, protocol, permission scope, persistence model, cross-user product surface, browser takeover mechanism, webhook surface, or implementation mechanism. It does not modify the creator-owned product design document. It does not authorize source implementation or claim test execution or executed evidence.

Historical references may remain in immutable historical records when they accurately describe an earlier discussion or rationale. Active derived inventories and handoff documents MUST identify these capabilities as retired/out of scope rather than as conditional future decisions.

## Required propagation

The active completeness inventory, canonical-source/decision indexes, traceability projections, and any active derived feature or roadmap projections MUST align this decision. Existing canonical owners retain their authority; no new owner is introduced.
