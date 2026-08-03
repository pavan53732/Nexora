> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

# Unit Tests

## Scope

Unit tests cover isolated, pure logic within the Nexora codebase — no Android framework dependencies, no network calls, no filesystem access. Targeted areas include:

| Area | Examples |
|------|----------|
| Data classes | `AgentConfig`, `ToolDefinition`, `WorkspaceSettings` copy/equality/serialization |
| State machines | `AgentState`, `TaskLifecycle`, `PluginLifecycle` transition validity |
| Business logic | Token budgeting, permission evaluation, plan scoring |
| Config parsing | YAML/JSON provider configs, plugin manifests |
| Permission checks | `PermissionManager.shouldAllow()` for every `PermissionLevel` |

## Framework Stack

| Tool | Version | Purpose |
|------|---------|--------|
| JUnit 5 | 5.10.x | Test runner & assertions |
| Kotlin Coroutines Test | 1.7.x | `runTest`, `TestDispatcher` for suspended logic |
| MockK | 1.13.x | Kotlin-native mocking (`coEvery`, `verify`) |
| AssertJ | 3.25.x | Fluent assertions |
| Turbine | 1.0.x | `Flow` testing |

## Naming Convention

```
should_<expected>_when_<condition>
```

Examples: `should_transitionToRunning_when_startCalled`, `should_throwInsufficientBudget_when_tokensExceedLimit`.

## Directory Structure

```
src/test/kotlin/com/nexora/app/
├── agent/          # AgentState, AgentLoop logic
├── tool/           # TokenBudget, ToolResolver
├── permission/     # PermissionManager
├── memory/         # MemoryScorer, embedding math
├── plugin/         # PluginManifest parsing
├── provider/       # ProviderConfig parsing
└── workflow/       # WorkflowDAG validation
```

## Example Tests

```kotlin
class AgentStateTest {
    @Test
    fun should_transitionToRunning_when_startCalled_fromIdle() {
        val state = AgentState.IDLE
        val next = state.transition(Event.START)
        assertThat(next).isEqualTo(AgentState.RUNNING)
    }

    @Test
    fun should_throwIllegalTransition_when_pauseCalled_fromCompleted() {
        val state = AgentState.COMPLETED
        assertThrows<IllegalStateException> {
            state.transition(Event.PAUSE)
        }
    }
}

class TokenBudgetTest {
    @Test
    fun should_throwInsufficientBudget_when_tokensExceedLimit() {
        val budget = TokenBudget(maxTokens = 1000, usedTokens = 900)
        assertThrows<InsufficientBudgetException> {
            budget.consume(200)
        }
    }
}

class PermissionManagerTest {
    @Test
    fun should_denyFileAccess_when_permissionLevelIsRestricted() {
        val mgr = PermissionManager(level = PermissionLevel.RESTRICTED)
        assertThat(mgr.shouldAllow(Permission.FILE_WRITE)).isFalse()
    }
}
```

## Coverage Targets

| Module | Target | Tool |
|--------|--------|------|
| Core (agent, tool, permission, memory) | **85%** | JaCoCo + Kover |
| UI (Compose view models) | **70%** | JaCoCo + Kover |
| Plugin SDK | **80%** | JaCoCo + Kover |

## Git Grounding Unit Tests (FR-GT-001..006)

| Test | Verifies |
|------|----------|
| `gitTool_returnsStructuredSnapshot` | Every git tool result includes canonical JSON (branch, HEAD SHA, status, remotes) |
| `gitTool_readBeforeWrite_enforced` | Mutating git call without prior read pass returns NeedsApproval/NXR-2003 |
| `gitTool_fabricatedSha_rejected` | A non-existent SHA reference is rejected, not accepted |
| `gitTool_missingPath_requiresDiscovery` | Mutation on a non-existent path fails with a discovery hint (file_search), never silently succeeds |
| `gitTool_postCommit_shaMatches` | After commit, `git_log -1` SHA equals the commit result SHA |
| `sandboxFileSystem_rejectsForeignRepoPaths` | Paths resolving outside workspace root rejected (NXR-7005) |

## CI Policy

- **Trigger**: Every pull request on any branch.
- **Fail condition**: Coverage drops below module target OR any unit test fails.
- **Report**: HTML coverage report uploaded as CI artifact.

## Response Grounding Unit Tests (FR-GND-001..006)

| Test | Verifies |
|------|----------|
| `response_unsourcedClaim_flagged` | A factual claim without a source is flagged/not asserted as fact |
| `response_uncertainty_notInvented` | Out-of-context question yields "I don't know" + offered retrieval, never a fabricated answer |
| `codeClaim_requiresCodeSearch` | A codebase claim triggers/requires code_search/code_symbols before being stated |
| `completionReport_statesActualStatus` | Report distinguishes done-verified / done-unverified / failed / not-attempted |
| `refusal_reportsReason` | Unsupported request returns explicit refusal with reason, not a made-up execution |

## Reasoning Unit Tests (FR-RN-001..006)

| Test | Verifies |
|------|----------|
| `deliberationGate_classifiesAmbiguity` | Ambiguous request routes to clarify-first, never answer-now |
| `reasoningPipeline_retrievesBeforeReasoning` | Reasoning pass triggers retrieval tools before the provider call |
| `effortLevel_configuresPipeline` | fast/balanced/thorough select different pipeline depths and models |
| `answerGates_rejectUnsupportedAnswer` | Answer failing grounded/complete/consistent/confident gates is revised, not sent |
| `reasoningTrace_persisted` | Reasoning trace appears in execution history and counts toward tokens |
| `reasoningModel_required_failsFast` | reasoning_required task without a REASONING-capable profile fails fast with clear message |

## Evidence & Validation Engine Unit Tests (FR-EV-001..006)

| Test | Verifies |
|------|----------|
| `statement_unclassified_blocked` | Significant claim without classification metadata is blocked |
| `confidence_low_triggersAsk` | LOW-confidence conclusion routes to user confirmation, not auto-proceed |
| `zeroAssumption_rejectsInventedDetail` | Output inventing missing info (e.g. "probably uses Hilt") is rejected |
| `guardrail_noToolClaim_withoutHistory` | Claiming a tool ran without a tool-history record is blocked |
| `guardrail_buildSuccess_requiresOutput` | "Build succeeded" without build output is blocked |
| `completionValidation_requiresReviewer` | Important task without reviewer pass cannot reach user-facing completion |

## Multi-Agent Sub-Task Unit Tests (FR-MA-001..005)

| Test | Verifies |
|------|----------|
| `subAgent_completesEndToEnd_noCheckins` | Delegated subtask reaches completion without coordinator status prompts |
| `handoffContext_complete` | Delegation without full context (goal/criteria/evidence) is rejected |
| `parallelFanout_respectsDependencyGraph` | Independent subtasks run concurrently; dependent ones wait |
| `fileWriteLock_blocksSecondWriter` | Concurrent writes to the same file wait or route to coordinator-merge |
| `subAgentReport_planVsActual` | Sub-agent report classifies done/failed/not-attempted with evidence |
| `subAgent_inheritsEvidenceEngine` | Sub-agent output passes EV classification/gates before merging |
