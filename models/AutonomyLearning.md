# Domain Model: Autonomy Learning and Trust

> This is a derived model projection for the semantic contracts owned by
> [../specs/AUTONOMY_STABILITY.md](../specs/AUTONOMY_STABILITY.md) and
> [../requirements/FR.md](../requirements/FR.md) (`FR-AS-004` and `FR-AS-005`).
> It defines required semantic data, not a selected storage technology, database
> schema, transport, or numeric trust threshold.

## Learning Lesson

A lesson is a structured, provenance-bearing learning artifact produced from an
execution reflection. Lessons are not raw transcripts and must not contain private
chain-of-thought, credentials, hidden prompts, or unrestricted untrusted content.

```kotlin
data class LearningLesson(
    val lessonId: String,
    val agentId: String,
    val workspaceId: String,
    val sourceExecutionId: String,
    val summary: String,
    val evidenceRefs: List<String>,
    val createdAt: Instant,
    val approvedForPlanning: Boolean,
    val retiredAt: Instant?
)
```

A lesson may be retrieved during planning only when its provenance and evidence
references remain available and it is approved for planning. A lesson can propose
skill refinement or a `LEARNED` skill, but lesson content never grants permissions,
changes sandbox policy, bypasses approval, or directly selects an autonomy mode.

## Trust State

Trust is scoped to an agent and workspace. The trust state records the information
needed to evaluate an autonomy-mode offer while preserving user authority over the
selected mode.

```kotlin
data class AutonomyTrustState(
    val agentId: String,
    val workspaceId: String,
    val score: TrustScore,
    val offeredMode: AutonomyMode,
    val userSelectedMode: AutonomyMode,
    val updatedAt: Instant,
    val lastResetAt: Instant?
)
```

`TrustScore` is an opaque domain value in this documentation phase; its scale,
update increments, thresholds, decay, and persistence mechanics are not selected by
this model. Successful verified milestones may contribute positively and failed
steps, safety violations, or denied approvals may contribute negatively according
to the canonical autonomy policy. A trust change may offer a mode change, but the
user-selected mode remains authoritative.

```kotlin
enum class AutonomyMode { MANUAL, ASSISTED, AUTOPILOT }
```

Trust state must not weaken `PermissionModel`, classifier denial, workspace
isolation, provider/device/resource ceilings, or human approval gates. Degraded
Android background execution may force `MANUAL` as specified by
`specs/BACKGROUND_EXECUTION.md`; trust cannot override that degradation rule.

## Reset and Audit Invariants

An explicit user reset replaces the applicable trust state with the repository's
selected reset baseline; this model does not select the baseline value. Trust
updates and resets must retain agent identity, workspace identity, source execution
or user-action provenance, and an audit reference. A lesson approval, rejection,
retirement, trust update, or reset must be distinguishable from an ordinary task
result.

The model is intentionally silent on database tables, serializers, APIs, and
transport messages. Those remain downstream implementation choices unless a
canonical decision selects them.
