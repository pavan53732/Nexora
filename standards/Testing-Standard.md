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
## ADR Test Coverage

- Every ADR SHOULD map to test cases. ADR-0008 (Typed Inference Streaming) has explicit test mapping (`UT-STREAM-*`, `IT-STREAM-*`, `E2E-STREAM-*`, `SEC-STREAM-*`, `PERF-STREAM-*`).
- The remaining accepted ADRs (ADR-0001..0007) are covered by the subsystem contract/integration tests cited in `docs/TRACEABILITY.md` (e.g. `UT-CONTRACT-*`, `IT-AGENT-*`, `IT-TOOL-*`, `IT-PLUGIN-*`, `SEC-PERM-*`, `SEC-SBX-*`), since each ADR's decision is realized through those subsystem contracts.
- The `docs/adr/README.md` registry is the authoritative ADR list; when a new ADR is accepted, its realization tests SHOULD be recorded in `docs/TRACEABILITY.md` or the relevant `testing/cases/` inventory so coverage is auditable.

## Naming
- Test class: `{ClassName}Test` (`ToolRegistryTest`)
- Test method: `should_{expectedBehavior}_{when}_{condition}()`
  - `should_returnError_when_toolNotFound()`
  - `should_saveCheckpoint_when_iterationMod5()`

## Mocking
- Use a mock `AIProvider` for runtime tests (never call real APIs in tests).
- Use a mock `Sandbox` for tool tests.
- Use a mock `EventBus` to verify event publication.
