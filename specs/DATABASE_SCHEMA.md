> **Status: CANONICAL** for the application Room database schema.
> This document owns the authoritative SQLite/Room schema: every table, its columns, types,
> primary/foreign keys, indexes, and retention policy. It is the single source of truth for
> persistent storage. Subsystem docs (architecture, models, protocols) reference these tables
> by name but MUST NOT redefine their columns.
>
> Depends on: the subsystem canonical sources that declare each entity
> ([../architecture/RUNTIME.md](../architecture/RUNTIME.md), [../architecture/MEMORY_SYSTEM.md](../architecture/MEMORY_SYSTEM.md),
> [../architecture/SECURITY_MODEL.md](../architecture/SECURITY_MODEL.md), [../state-machines/](../state-machines/),
> [../models/](../models/)).
> Referenced by: architecture, models, protocols, SDKs, and persistence implementations.

# Application Database Schema — Nexora

Nexora persists durable state across three coordinated stores. **Room** (`nexora.db`)
is the authoritative *structured/relational* store and owns the tables defined below.
Two additional stores are explicitly delegated and are NOT redefined here:

- **DataStore** — key/value preferences and policy configuration: user preferences
  (FR-M013), provider/plugin settings, and the mutable permission policy stores
  (`security/PermissionModel.md` §Policy Stores). Owned by `architecture/MEMORY_SYSTEM.md`
  and `security/PermissionModel.md`.
- **Sandbox workspace VFS** (`architecture/SANDBOX.md`) — large binary/streaming artifacts
  and process state that are impractical to relationalize: workspace `files/`, terminal
  sessions/history, `tasks/` checkpoints, `env/` config, `logs/`, `memory/` blobs, and
  `file_version` blobs under `files/.history/`. The Room tables `file_version`,
  `context_snapshot`, and `reasoning_summary` hold *references* to these blobs, not the
  bytes themselves.

Every table below is authoritative for its store. Entity lifecycles are owned by their
respective state machines; this document defines only storage shape. The Room schema is
the single source of truth for relational columns; subsystem docs reference these tables
by name but MUST NOT redefine their columns.

## Conventions

- All tables use `INTEGER PRIMARY KEY` surrogate keys unless noted.
- `createdAt` / `updatedAt` are `TEXT` (ISO-8601 UTC).
- `correlationId` and `workspaceId` are present on every tenant-scoped table for isolation.
- Soft-deletion is used where retention policy requires it (`status` column + `deletedAt`).
- Foreign keys are `ON DELETE CASCADE` where child lifecycle is bound to parent.

---


## Session–Conversation semantic persistence contract

The Session–Conversation semantic contract is governed by `architecture/CONVERSATION_CHECKPOINTS.md`, `models/Session.md`, `models/Conversation.md`, and `specs/SESSION_CONVERSATION_ENGINEERING_CONTRACT.md`. This schema document remains authoritative for concrete relational columns only when such columns are explicitly defined here.

The semantic persistence requirements are:
- Session identity persists.
- Conversation identity persists.
- Ordered Conversation record continuity persists.
- Checkpoint identity and checkpoint-to-Conversation reference persist.
- Rollback branch lineage persists, including source Conversation and source checkpoint reference.
- Session `CLOSED`/`EXPIRED` do not by themselves delete or rewrite Conversation data.
- Session recreation creates a new Session identity; later continuation may preserve Conversation identity while creating a new active association.
- Process death and application restart do not independently mutate Session–Conversation semantics; persistence must preserve enough state for implementation to distinguish same-Session recovery from new-Session continuation.

This document does **not** currently establish a dedicated `conversation` table, relationship table, or historical association table. Their presence or absence is therefore not yet a selected schema fact in this repository.

Implementation may choose concrete schema representation using existing repository patterns, but must not elevate that representation into a new semantic relationship authority. `(sessionId, conversationId)` fields, join rows, or read models may exist as implementation structures without implying a separate relationship identity or lifecycle.

Historical association persistence is a downstream implementation choice unless and until a canonical schema section explicitly selects it. Active-association enforcement, continuation support, lineage preservation, and checkpoint integrity are required semantic outcomes; exact relational encoding is not architecturally fixed here.

## Workspace & Session

### `workspace`
| Column | Type | Notes |
|--------|------|-------|
| id | TEXT PK | Stable workspace ID |
| name | TEXT | |
| description | TEXT | |
| ownerId | TEXT | |
| status | TEXT | Maps WorkspaceStatus (CREATED/ACTIVE/SUSPENDED/ARCHIVED/DELETED) |
| templateName | TEXT NULL | |
| createdAt | TEXT | |
| updatedAt | TEXT | |
| deletedAt | TEXT NULL | Soft-delete |

### `session`
| Column | Type | Notes |
|--------|------|-------|
| id | TEXT PK | |
| workspaceId | TEXT FK → workspace.id | |
| status | TEXT | Maps SessionStatus (CREATED/ACTIVE/IDLE/CLOSED/EXPIRED) |
| createdAt | TEXT | |
| lastActiveAt | TEXT | |
| expiresAt | TEXT NULL | |
| correlationId | TEXT | |

### `agent`
| Column | Type | Notes |
|--------|------|-------|
| id | TEXT PK | |
| workspaceId | TEXT FK | |
| type | TEXT | |
| configJson | TEXT | |
| status | TEXT | Maps AgentStatus |
| createdAt | TEXT | |
| updatedAt | TEXT | |

---

## Execution & Recovery

> **DEC-7 R4 placement:** Durable process-death recovery evidence is a dedicated Room recovery-evidence artifact, conceptually separate from the `task`, `execution`, `execution_checkpoint`, `execution_replay`, and lifecycle-history stores. It is not durable RetryPending state. This documentation establishes semantic placement only; entity names, columns, keys, indexes, DAO operations, migrations, SQL, and retention duration are not defined or implemented here. Unreconciled evidence must remain available until the recovery outcome is durably established.

### `execution`
| Column | Type | Notes |
|--------|------|-------|
| executionId | TEXT PK | |
| taskId | TEXT | |
| workspaceId | TEXT FK | |
| agentId | TEXT FK → agent.id | |
| correlationId | TEXT | |
| status | TEXT | Maps ExecutionStatus (CREATED/RUNNING/COMPLETED/FAILED/CANCELLED) |
| phase | TEXT | Maps ExecutionPhase |
| version | INTEGER | Monotonic; checkpoint/resume increments |
| checkpointId | TEXT NULL | FK → execution_checkpoint.id |
| priorExecutionId | TEXT NULL | FK → execution.executionId (retry lineage) |
| retryAttempt | INTEGER NOT NULL DEFAULT 0 | DEC-7: retry attempt index, scoped per-Execution |
| escalationPayload | TEXT NULL | JSON blob captured on requestEscalation; NULL after resolveEscalation |
| createdAt | TEXT | |
| updatedAt | TEXT | |
| completedAt | TEXT NULL | |

### `execution_checkpoint`
| Column | Type | Notes |
|--------|------|-------|
| checkpointId | TEXT PK | |
| executionId | TEXT FK → execution.executionId | |
| correlationId | TEXT | |
| stepIndex | INTEGER | |
| variablesJson | TEXT | |
| historyLogJson | TEXT | |
| tokenBudgetUsed | INTEGER | |
| phase | TEXT | |
| occurredAt | TEXT | |

### `task`
| Column | Type | Notes |
|--------|------|-------|
| id | TEXT PK | |
| workspaceId | TEXT FK | |
| status | TEXT | Maps TaskStatus |
| createdAt | TEXT | |
| updatedAt | TEXT | |

### `execution_replay` (append-only)

Compact, durable replay log that makes exactly-once recovery representable end-to-end
(FR-AS-007 / NFR-REL-012). It records every *completed* tool call so recovery can replay
only uncompleted calls and reconcile non-idempotent in-flight calls from durable history.

| Column | Type | Notes |
|--------|------|-------|
| replayId | TEXT PK | |
| executionId | TEXT FK → execution.executionId | |
| toolCallId | TEXT | Correlates to `tool_call.toolCallId` |
| workspaceId | TEXT FK | |
| correlationId | TEXT | |
| toolId | TEXT | |
| inputHash | TEXT | Stable hash of normalized parameters (dedupe key) |
| idempotent | INTEGER | 0/1 — mirrors `Tool.isIdempotent` at call time |
| resultRef | TEXT | Reference to `tool_call.resultJson` / outcome |
| status | TEXT | Maps ToolInvocationStatus at completion |
| occurredAt | TEXT | |

> **Retention reconciliation:** `permission_audit_log` is the authoritative audit trail
> and is **non-evictable** for legal/compliance review. The 90-day auto-purge described
> in `security/PermissionModel.md` §Permission Audit Trail and mirrored in
> `docs/SANDBOX_DEPTH.md` / `specs/PIPES.md` applies ONLY to a separate, derived
> *operational* audit view used for UX filtering and routine review — it MUST NOT delete
> or mutate the canonical `permission_audit_log` rows. Any auto-purge path MUST preserve
> the source rows (e.g., copy-to-cold-storage or mark a `purgeEligible` flag on the
> derived view, never `DELETE` from `permission_audit_log`). This resolves the prior
> contradiction between the "legal retention / non-evictable" schema and the "90-day
> auto-purged" policy text.

---

## Tool & Provider

### `tool_call`
| Column | Type | Notes |
|--------|------|-------|
| toolCallId | TEXT PK | |
| toolId | TEXT | |
| workspaceId | TEXT FK | |
| agentId | TEXT NULL | |
| correlationId | TEXT | |
| executionId | TEXT NULL FK → execution.executionId | |
| parametersJson | TEXT | |
| status | TEXT | Maps ToolInvocationStatus |
| idempotent | INTEGER | 0/1 — mirrors `Tool.isIdempotent` at call time (FR-AS-007) |
| resultJson | TEXT NULL | |
| startedAt | TEXT | |
| completedAt | TEXT NULL | |

### `provider`
| Column | Type | Notes |
|--------|------|-------|
| id | TEXT PK | |
| workspaceId | TEXT FK NULL | NULL for global providers |
| status | TEXT | Maps ProviderStatus |
| health | TEXT | Maps ProviderHealth |
| configJson | TEXT | |
| createdAt | TEXT | |
| updatedAt | TEXT | |

### `inference_stream`
| Column | Type | Notes |
|--------|------|-------|
| streamId | TEXT PK | |
| requestId | TEXT | |
| correlationId | TEXT | |
| providerProfileId | TEXT | |
| modelId | TEXT | |
| sequence | INTEGER | Last committed sequence |
| status | TEXT | Maps StreamStatus |
| priorStreamId | TEXT NULL | FK → inference_stream.streamId (failover lineage) |
| resumeTokenHash | TEXT NULL | Opaque hash; raw token never stored |
| createdAt | TEXT | |

---

## Memory

### `memory_entry`
| Column | Type | Notes |
|--------|------|-------|
| id | TEXT PK | |
| workspaceId | TEXT FK NULL | NULL for long-term/global |
| sessionId | TEXT NULL | |
| correlationId | TEXT NULL | |
| scope | TEXT | Maps MemoryScope (SESSION/WORKSPACE/LONG_TERM) |
| kind | TEXT | Maps MemoryKind (9 values) |
| contentJson | TEXT | |
| embeddingRef | TEXT NULL | Vector index reference |
| status | TEXT | Maps MemoryStatus |
| createdAt | TEXT | |
| updatedAt | TEXT | |
| INDEX idx_memory_ws_kind (workspaceId, kind) |

### `tool_record` (append-only)
| Column | Type | Notes |
|--------|------|-------|
| id | TEXT PK | |
| workspaceId | TEXT FK | |
| toolCallId | TEXT | |
| correlationId | TEXT | |
| resultMetaJson | TEXT | |
| retentionScope | TEXT | |
| createdAt | TEXT | |

### `file_version`
| Column | Type | Notes |
|--------|------|-------|
| id | TEXT PK | |
| workspaceId | TEXT FK | |
| path | TEXT | |
| operationType | TEXT | |
| correlationId | TEXT NULL | |
| blobRef | TEXT | sandbox files/.history/ reference |
| createdAt | TEXT | |

### `graph_entity`
| Column | Type | Notes |
|--------|------|-------|
| id | TEXT PK | |
| workspaceId | TEXT FK | |
| name | TEXT | |
| embeddingRef | TEXT NULL | |
| createdAt | TEXT | |
| INDEX idx_graph_name (name) |

### `graph_edge`
| Column | Type | Notes |
|--------|------|-------|
| id | TEXT PK | |
| workspaceId | TEXT FK | |
| fromEntityId | TEXT FK → graph_entity.id | |
| toEntityId | TEXT FK → graph_entity.id | |
| relation | TEXT | |
| createdAt | TEXT | |

### `context_snapshot`
| Column | Type | Notes |
|--------|------|-------|
| id | TEXT PK | |
| workspaceId | TEXT FK | |
| modelContract | TEXT | model/tokenizer id |
| includedSegmentsJson | TEXT | |
| excludedSegmentsJson | TEXT | |
| contentHash | TEXT | |
| compactionLineageJson | TEXT | |
| createdAt | TEXT | |

### `reasoning_summary`
| Column | Type | Notes |
|--------|------|-------|
| id | TEXT PK | |
| workspaceId | TEXT FK | |
| executionId | TEXT NULL FK → execution.executionId | |
| redactedSummaryJson | TEXT | Raw private reasoning NEVER stored |
| retentionScope | TEXT | |
| createdAt | TEXT | |

---

## Security & Audit

### `permission_audit_log` (append-only)
| Column | Type | Notes |
|--------|------|-------|
| id | TEXT PK | |
| workspaceId | TEXT FK | |
| scopeId | TEXT | |
| decision | TEXT | ALLOWED_BY_POLICY / APPROVED_BY_USER / DENIED_* |
| actor | TEXT | |
| correlationId | TEXT | |
| createdAt | TEXT | |

### `plugin`
| Column | Type | Notes |
|--------|------|-------|
| id | TEXT PK | |
| workspaceId | TEXT FK NULL | |
| version | TEXT | |
| compatibilityRange | TEXT | |
| integrityState | TEXT | Maps IntegrityState |
| status | TEXT | Maps PluginStatus |
| requiredPermissionsJson | TEXT | List<String> scope IDs |
| dependenciesJson | TEXT | |
| exportedAgentsJson | TEXT | |
| exportedToolsJson | TEXT | |
| exportedProvidersJson | TEXT | |
| exportedSkillsJson | TEXT | |
| exportedUiScreensJson | TEXT | |
| exportedMemoryBackendsJson | TEXT | |
| createdAt | TEXT | |
| updatedAt | TEXT | |

### `instance`
| Column | Type | Notes |
|--------|------|-------|
| id | TEXT PK | |
| pairingStatus | TEXT | Maps PairingStatus |
| pipeStatus | TEXT | Maps PipeStatus |
| fingerprint | TEXT | Ed25519 public key |
| workspaceId | TEXT FK | |
| createdAt | TEXT | |
| updatedAt | TEXT | |

---

## Workflow

### `workflow`
| Column | Type | Notes |
|--------|------|-------|
| id | TEXT PK | |
| workspaceId | TEXT FK | |
| name | TEXT | |
| correlationId | TEXT | |
| status | TEXT | Maps WorkflowStatus |
| currentStepId | TEXT NULL | |
| onError | TEXT | Maps ErrorStrategy |
| maxRetries | INTEGER | |
| version | INTEGER | |
| createdAt | TEXT | |
| updatedAt | TEXT | |
| completedAt | TEXT NULL | |

### `workflow_step`
| Column | Type | Notes |
|--------|------|-------|
| id | TEXT PK | |
| workflowId | TEXT FK → workflow.id | |
| type | TEXT | ExecuteTool/RunAgent/Condition/WaitForApproval/Iterative |
| status | TEXT | Maps StepStatus |
| dependsOnJson | TEXT | |
| bodyStepsJson | TEXT NULL | Iterative loop body |
| maxIterations | INTEGER NULL | |
| convergenceCondition | TEXT NULL | |
| createdAt | TEXT | |

---

## Retention Policy

| Table | Retention | Eviction |
|-------|-----------|----------|
| memory_entry | Per MemoryStatus; RETAINED→EXPIRED non-revivable LRU | LRU within quota |
| tool_record | Append-only; bounded by workspace quota | LRU eviction |
| file_version | Bounded history depth | Oldest-first |
| context_snapshot | Task/execution evidence window | With execution |
| reasoning_summary | Workspace execution-history retention | With workspace |
| inference_stream | Identity + lineage + terminal outcome only | Coalesced deltas not retained indefinitely |
| permission_audit_log | Append-only; **non-evictable** by default — retained for legal/compliance review (see retention rule below) | None (audit) |
| execution_replay | Append-only; bounded by execution/workspace retention | With execution |
| execution / task / workflow | Until workspace archival | With workspace |
| provider / plugin / agent / instance | Until removal | With entity |

## Indexes (summary)

- `idx_memory_ws_kind (workspaceId, kind)`
- `idx_graph_name (name)`
- `idx_tool_call_correlation (correlationId)`
- `idx_execution_workspace (workspaceId)`
- `idx_permission_audit_ws (workspaceId)`

## Migration Policy

Room schema version is monotonically increased. Migrations are forward-only; downgrade
is not supported. Each migration is recorded in `room_master_table` and the
`CHANGELOG.md` references the spec version that introduced the change.


## Session–Conversation Trace Closure

The schema is the persistence authority for storage shape, but it does not rewrite relationship semantics. For conversation identity and Session–Conversation continuation, the schema must preserve the identifiers and lineage fields required by `decisions/DEC-13-conversation-identity-persistence.md` and `decisions/DEC-14-session-conversation-relationship-semantic-status.md` through `decisions/DEC-21-session-conversation-continuation-recovery.md`.

The schema is intentionally silent on whether a Conversation is exposed as a public API object; that determination is owned by the architecture and protocol documents, not by the schema.
