> **Status: DERIVED** for BranchLineage domain model.
> **Canonical semantic authority:** `decisions/DEC-22-branch-lineage-artifact-ownership.md`.
> **Canonical operational policy:** `decisions/DEC-31-branch-lineage-and-checkpoint-operational-policy.md`.
> **Canonical lifecycle:** `state-machines/BranchLineageLifecycle.md`.

# Domain Model: BranchLineage

```kotlin
data class BranchLineage(
    val id: String,
    val workspaceId: String,
    val sourceConversationId: String,
    val sourceCheckpointId: String,
    val branchConversationId: String,
    val status: BranchLineageStatus,
    val version: Long,
    val createdAt: Instant,
    val updatedAt: Instant,
    val detachedAt: Instant? = null,
    val deletedAt: Instant? = null,
    val correlationId: String
)

enum class BranchLineageStatus {
    RECORDED,
    ACTIVE,
    DETACHED,
    DELETED
}
```

## Semantics

BranchLineage owns the immutable parent/source relationship between a source Conversation, source ConversationCheckpoint, and branch Conversation created by non-destructive rollback. It does not own Conversation records, checkpoint content, execution state, or workspace file history.

The `id` is a stable domain-prefixed identity under the repository’s stable-ID convention. The source and branch identifiers are distinct Conversation identities. `status` follows `state-machines/BranchLineageLifecycle.md`; the operational retention, dependency-protection, quota, and cleanup policy follows DEC-31.

A `RECORDED` or `ACTIVE` lineage protects its source checkpoint from physical deletion. `DETACHED` preserves lineage history but no longer protects the source checkpoint for normal branch operation. `DELETED` is terminal and is permitted only after retention and audit obligations are satisfied.

Concrete Room encoding, serialization, transport DTOs, and API names remain implementation projections that MUST preserve identity, immutability, lifecycle, audit, and dependency-protection invariants.
