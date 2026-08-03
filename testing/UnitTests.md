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

## CI Policy

- **Trigger**: Every pull request on any branch.
- **Fail condition**: Coverage drops below module target OR any unit test fails.
- **Report**: HTML coverage report uploaded as CI artifact.
