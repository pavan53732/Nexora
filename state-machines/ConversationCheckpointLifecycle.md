# Conversation Checkpoint Lifecycle — Nexora

> **Status: CANONICAL** for ConversationCheckpoint lifecycle.
> Semantic ownership: Conversation/Session responsibility established by DEC-10; retention, deletion, quota, cleanup, and branch-dependency safety are governed by DEC-23.

## States

- `Created`: checkpoint boundary durably recorded and addressable.
- `Superseded`: a newer checkpoint exists for the same conversation lineage; the checkpoint remains readable.
- `Expired`: retention policy no longer permits normal use.
- `Invalidated`: integrity, authorization, or lineage validation permanently prevents use.

## Transition table

| Trigger | From | To | Guard | Persistence/event requirement |
|---|---|---|---|---|
| `createBoundary` | absent | `Created` | conversation boundary is authorized and integrity-valid | persist immutable checkpoint before success is observable |
| `newerBoundary` | `Created` | `Superseded` | newer checkpoint exists on same lineage | persist transition; repeated application is idempotent |
| `retentionExpiry` | `Created` or `Superseded` | `Expired` | retention policy permits expiry | persist terminal availability change |
| `integrityFailure` | `Created` or `Superseded` | `Invalidated` | integrity or lineage validation fails | persist invalidation and audit result |

Invalid transitions leave persisted state unchanged. Concurrent transitions require the owning conversation/session authority to reject stale versions or reconcile them according to its persistence policy.

## Transitions

- `Created → Superseded`: newer checkpoint is durably created on the same lineage.
- `Created → Expired`: retention policy expires the checkpoint.
- `Created → Invalidated`: integrity or lineage validation fails.
- `Superseded → Expired`: retention policy expires it.
- `Superseded → Invalidated`: integrity or lineage validation fails.

No transition deletes the source conversation as a consequence of rollback. Expiration or invalidation prevents normal checkpoint use but does not by itself perform physical deletion. Under DEC-23, physical deletion is permitted only after `Expired` or `Invalidated`, no recorded BranchLineage depends on the checkpoint, and required audit/retention obligations are satisfied. Quota rejection and cleanup must preserve protected Conversations and BranchLineage artifacts.

## Invariants

- A checkpoint is immutable after creation.
- An expired or invalidated checkpoint cannot be used as a rollback source.
- A checkpoint belongs to exactly one conversation lineage.
- Checkpoint identity is distinct from conversation identity, execution checkpoint identity, context snapshot identity, file-version identity, and workspace-snapshot identity.
- Lifecycle transition failure does not create a partial rollback branch.
