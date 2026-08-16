# Conversation Lifecycle State Machine — Nexora

> **Status: CANONICAL** for Conversation lifecycle states and transitions.
> Depends on: `architecture/CONVERSATION_CHECKPOINTS.md`, `models/Conversation.md`, `decisions/DEC-13-conversation-identity-persistence.md`.
> Referenced by: `specs/DATABASE_SCHEMA.md` (`conversation.status`), `models/Conversation.md`, `docs/CANONICAL_SOURCES.md`, `docs/LIFECYCLES.md`.

## Overview

This state machine governs the lifecycle of a Conversation entity in Nexora, ensuring durable identity, tracking state transitions (Active, Archived, Deleted), and interacting with ConversationCheckpoints and BranchLineage.

`ConversationStatus` is the durable status enum for this state machine: `ACTIVE`, `ARCHIVED`, `DELETED`. The `conversation` table in `specs/DATABASE_SCHEMA.md` maps its `status` column to this enum.

## States

| State | Definition |
|-------|------------|
| `ACTIVE` | Conversation is open and accepting new turns or checkpoints. |
| `ARCHIVED` | Conversation is read-only, preserved in storage, but excluded from active workspace prompt context by default. |
| `DELETED` | Conversation is soft-deleted; associated checkpoints and lineage are pruned or marked terminal according to retention policy (DEC-23, DEC-31). |

## Legal Transitions

| Trigger | From | To | Guard |
|---------|------|----|-------|
| `create()` | [*] | ACTIVE | Valid workspace; identity durably assigned (DEC-13) |
| `archive()` | ACTIVE | ARCHIVED | No active Session association requiring the Conversation (DEC-19/DEC-20) |
| `restore()` | ARCHIVED | ACTIVE | Conversation not soft-deleted |
| `delete()` | ACTIVE | DELETED | Retention/dependency safety satisfied (DEC-23) |
| `delete()` | ARCHIVED | DELETED | Retention/dependency safety satisfied (DEC-23) |

Once a Conversation enters `DELETED`, it is terminal and cannot transition back to `ACTIVE` or `ARCHIVED`.

Creation is not a transition between two persisted states: a Conversation row first exists in `ACTIVE`. Rollback never mutates the source Conversation's status; it creates a new Conversation identity (DEC-9) that enters `ACTIVE` independently. Session `CLOSED`/`EXPIRED` ends only the active association and does not by itself transition Conversation status (DEC-20).

## Normative Transition Contract

Every transition in this state machine MUST be treated as an atomic command. The implementation MUST evaluate the guard against the current persisted version, apply the state change and side effects in one transaction, persist the resulting version, and emit the event only after durable persistence succeeds.

| Contract field | Requirement |
|---|---|
| Source and trigger | The trigger MUST be valid for the current state; unsupported triggers are rejected without mutation. |
| Guard | Guards are evaluated before mutation using current durable state and required authorization/context. |
| Target | The target is the only legal resulting state for the accepted trigger. |
| Side effects | Checkpoint eligibility recheck, lineage dependency protection recheck (DEC-23, DEC-31), retention/cleanup scheduling. |
| Persistence | Durable state, transition version, actor, timestamp, correlation ID, and error context MUST be written before the event is published. |
| Event | One semantic transition event is emitted after commit; retries MUST NOT duplicate the committed transition event. |
| Idempotency | Repeating the same command with the same idempotency key returns the committed result; a conflicting version is rejected. |
| Failure | Guard failure and invalid transition return a canonical error and leave state unchanged. Side-effect failure MUST use the subsystem rollback or recovery rule. |
| Recovery | On restart, persisted state and transition version are authoritative; incomplete work resumes only through an explicitly listed recovery transition. |

### Transition Event Minimum

Each emitted lifecycle event MUST carry: `entityId`, `entityType`, `fromState`, `toState`, `trigger`, `transitionVersion`, `occurredAt`, `actor`, `correlationId`, and optional canonical error information. Consumers MUST treat events as at-least-once and deduplicate by `(entityType, entityId, transitionVersion)`.

### Invalid Transition Contract

An invalid transition MUST return a canonical error without changing persisted state, emitting a success event, or executing target-state side effects. The error MUST identify current state, requested trigger, entity ID, and correlation ID in redacted structured details.
