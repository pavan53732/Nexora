> **Status: DERIVED** for IntegrationTests tests.
> This document describes the tests surface for IntegrationTests. Canonical behavior is defined in the owning architecture document.
>
> Depends on: the canonical architecture document for IntegrationTests.
> Referenced by: upstream architecture, models, protocols, and implementation consumers.


> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

# Integration Tests

## Scope

Integration tests verify that Nexora modules interact correctly when wired together. These tests use real Android framework classes but mock external services (AI provider APIs, network).

| Interaction Path | What Is Tested |
|------------------|----------------|
| Tool execution in sandbox | ToolManager → SandboxManager → filesystem operations |
| Provider calls | AgentLoop → ProviderManager → HTTP client (mocked server) |
| Memory read/write | MemoryManager → Room DAO → in-memory database |
| Event bus pub/sub | EventBus → multiple subscribers receive correct events |
| Plugin loading | PluginManager → PluginRegistry → DexClassLoader → tool registration |
| Room database | Full DAO round-trips with migration scripts |

## Framework Stack

| Tool | Purpose |
|------|--------|
| JUnit 5 | Test runner |
| AndroidX Test | `@RunWith(AndroidJUnit4::class)`, test application context |
| Room In-Memory DB | `:memory:` SQLite instance per test |
| MockK | Mocking AI provider HTTP responses |
| MockWebServer | OkHttp mock server for provider API simulation |
| Turbine | Flow integration testing |

## Test Environment

| Requirement | Specification |
|-------------|---------------|
| Emulator | Android API 34 (Google APIs) |
| Runner | `androidTest` instrumentation |
| Isolation | Fresh in-memory DB + fresh EventBus per test |

## Key Scenarios

1. **Full agent loop with mock provider** — Agent receives a goal, creates a plan via a mocked LLM response, executes a tool in the sandbox, stores the result in memory, and publishes a completion event.
2. **Sandbox file operations** — Tool writes a file inside the sandbox, reads it back, verifies path confinement (cannot escape to `/sdcard`).
3. **Workspace creation flow** — Create workspace → initialize Room tables → verify default agent template is inserted.
4. **Plugin lifecycle** — Install plugin APK → verify signature → activate → register tools → execute a tool via ToolManager → deactivate → verify tools unregistered.

## Naming Convention

```
should_<expected>_when_<modules_interact>
```

Example: `should_storeResultInMemory_when_agentLoopCompletesToolExecution`

## Coverage Target

| Path | Target |
|------|--------|
| Integration paths (module boundaries) | **60%** |

## CI Policy

- **Trigger**: Every pull request (core scenarios), nightly (full suite).
- **Timeout**: 10 minutes per test class.
- **Emulator**: Reused via Android Test Orchestrator for parallel execution.