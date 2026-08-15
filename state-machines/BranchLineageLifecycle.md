# BranchLineage Lifecycle State Machine — Nexora

> **Status: CANONICAL** for BranchLineage lifecycle.
> **Semantic owner:** BranchLineage artifact under DEC-22.
> **Operational policy:** DEC-31.
> BranchLineage does not own Conversation content, checkpoint content, execution state, or workspace file history.

## States

- `RECORDED`: source Conversation, source checkpoint, and branch Conversation relationship is durably recorded.
- `ACTIVE`: the branch remains dependent on the source lineage for the recorded rollback relationship.
- `DETACHED`: the branch no longer requires the source checkpoint for normal operation; lineage history remains retained for audit.
- `DELETED`: terminal state; the lineage record is physically removed only after retention and audit obligations are satisfied.

## Transitions

| Trigger | From | To | Guard |
|---|---|---|---|
| `record()` | absent | `RECORDED` | Source Conversation, source checkpoint, branch Conversation, and atomic operation identity are valid and authorized |
| `activate()` | `RECORDED` | `ACTIVE` | Branch creation committed and lineage dependency is retained |
| `detach()` | `ACTIVE` | `DETACHED` | Branch preserves required history and no longer requires source checkpoint for normal operation |
| `delete()` | `DETACHED` | `DELETED` | Retention/audit obligations satisfied and no protected dependency remains |

Invalid transitions leave persisted state unchanged. `RECORDED` and `ACTIVE` lineage prevents physical deletion of the dependent source checkpoint. No BranchLineage transition mutates or deletes a source or branch Conversation.

## Invariants

1. BranchLineage identity is stable and distinct from Conversation, ConversationCheckpoint, Execution, ContextSnapshot, file-version, and Workspace identities.
2. Parent/source lineage is immutable after `record()`; correction requires a new authorized lineage operation rather than mutation.
3. `DELETED` is terminal and cannot be restored as the same identity.
4. BranchLineage dependency protection is evaluated before checkpoint cleanup.
5. Transition persistence precedes event publication and is idempotent by operation identity/version.
6. Audit and correlated trace records preserve source, checkpoint, branch, actor, authorization, and disposition metadata.
