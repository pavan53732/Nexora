# Domain Model: Autonomy Learning and Trust

> This is a derived model projection for the semantic contracts owned by
> [../specs/AUTONOMY_STABILITY.md](../specs/AUTONOMY_STABILITY.md) and
> [../requirements/FR.md](../requirements/FR.md) (`FR-AS-004` and `FR-AS-005`).
> It defines required semantic data, including the selected numeric trust scale,
> increments, thresholds, and reset baseline below. It does not select a storage
> technology, database schema, or transport.

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
skill refinement or a `LEARNED` skill. Promotion may use the existing deterministic
policy path or user path after the existing provenance, evidence, trust, safety,
scope, and lifecycle conditions are satisfied. Lesson content never grants
permissions, changes sandbox policy, bypasses approval, or directly selects an
autonomy mode.

## Trust State

Trust is scoped to an agent and workspace. The trust state records the information
needed to automatically select the effective autonomy mode while preserving the
existing user downgrade override.

```kotlin
data class AutonomyTrustState(
    val agentId: String,
    val workspaceId: String,
    val score: TrustScore,
    val offeredMode: AutonomyMode,      // automatically selected effective mode
    val userSelectedMode: AutonomyMode,  // existing downgrade-only override; equals offeredMode when unused
    val updatedAt: Instant,
    val lastResetAt: Instant?
)
```

`TrustScore` is defined as a normative integer score from 0 to 100 (default initial baseline score = 50).
- **Increments:** Successful low-risk tool call (+1); successful milestone completion (+5); verified final results (+10).
- **Decrements:** Failed step (-5); safety violation or denied approval (-10). Repeated drops trigger autonomy mode reduction.
- **Mode Thresholds:** `MANUAL` (0–39), `ASSISTED` (40–74), `AUTOPILOT` (75–100).
A trust change automatically selects `offeredMode` from the thresholds above. The existing `userSelectedMode` value is a downgrade-only override that takes effect immediately; it cannot silently upgrade the effective mode. Autonomy resets are explicit.

```kotlin
enum class AutonomyMode { MANUAL, ASSISTED, AUTOPILOT }
```

Trust state must not weaken `PermissionModel`, applicable canonical denial or
classification outcomes, workspace isolation, provider/device/resource ceilings, or existing
high-risk ASK/DENY and approval gates. The retired local classifier is not part of the active
trust contract. Degraded Android background execution may force `MANUAL` as specified by
`specs/BACKGROUND_EXECUTION.md`; trust cannot override that degradation rule.

## Reset and Audit Invariants

An explicit user reset replaces the applicable trust state with the selected reset
baseline score of 50 (the default initial baseline). Trust
updates and resets must retain agent identity, workspace identity, source execution
or user-action provenance, and an audit reference. A lesson approval, rejection,
retirement, trust update, or reset must be distinguishable from an ordinary task
result.

The model is intentionally silent on database tables, serializers, APIs, and
transport messages. Those remain downstream implementation choices unless a
canonical decision selects them.
