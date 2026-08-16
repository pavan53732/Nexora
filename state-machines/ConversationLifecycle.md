# Conversation Lifecycle State Machine — Nexora

> **Status: CANONICAL** for Conversation lifecycle states and transitions.
> Depends on: `architecture/CONVERSATION_CHECKPOINTS.md`, `models/Conversation.md`, `decisions/DEC-13-conversation-identity-persistence.md`.

## Overview

This state machine governs the lifecycle of a Conversation entity in Nexora, ensuring durable identity, tracking state transitions (Active, Archived, Deleted), and interacting with ConversationCheckpoints and BranchLineage.

## States

| State | Definition |
|-------|------------|
| `ACTIVE` | Conversation is open and accepting new turns or checkpoints. |
| `ARCHIVED` | Conversation is read-only, preserved in storage, but excluded from active workspace prompt context by default. |
| `DELETED` | Conversation is soft-deleted; associated checkpoints and lineage are pruned or marked terminal according to retention policy (DEC-23, DEC-31). |

## Legal Transitions

```
[Created] → ACTIVE
ACTIVE → ARCHIVED
ACTIVE → DELETED
ARCHIVED → ACTIVE
ARCHIVED → DELETED
```

Once a Conversation enters `DELETED`, it is terminal and cannot transition back to `ACTIVE` or `ARCHIVED`.
