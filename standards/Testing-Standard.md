> **Status: SUPPORTING** for Testing Standard coding standard.
> This document defines conventions for Testing Standard. It applies across all subsystems and does not override canonical subsystem definitions.


# Testing Standard — Nexora

## Test Pyramid

- **Unit tests**: All interfaces, models, use cases. Fast, no Android dependencies.
- **Integration tests**: Module interactions. May use Robolectric.
- **Instrumented tests**: UI, sandbox, Android-specific behavior. Run on emulator.

## Coverage
- Minimum 80% line coverage for `core/` and `runtime/`.
- Minimum 60% for `tools/`, `agents/`, `providers/`.
- All ADRs must have corresponding test cases.

## Naming
- Test class: `{ClassName}Test` (`ToolRegistryTest`)
- Test method: `should_{expectedBehavior}_{when}_{condition}()`
  - `should_returnError_when_toolNotFound()`
  - `should_saveCheckpoint_when_iterationMod5()`

## Mocking
- Use a mock `AIProvider` for runtime tests (never call real APIs in tests).
- Use a mock `Sandbox` for tool tests.
- Use a mock `EventBus` to verify event publication.
