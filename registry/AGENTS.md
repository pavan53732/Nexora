> **Status: DERIVED** for agent registry inventory (field spec + standard fields). Canonical agent definitions live in [../architecture/MULTI_AGENT_SYSTEM.md](../architecture/MULTI_AGENT_SYSTEM.md); per-type capability rows live in [AGENT_MATRIX.md](./AGENT_MATRIX.md).

# Agent Registry — Nexora

## Standard Fields

| Field | Meaning |
|---|---|
| `agentId` | Stable agent identifier |
| `version` | Agent version or revision |
| `origin` | `built-in` or plugin/provider origin |
| `declaredSkills` | Declared skill identifiers |
| `requiredPermissions` | Required permission scopes |
| `supportsDelegation` | Delegation capability flag |
| `supportsBackgroundExecution` | Background execution capability flag |
| `minContractVersion` | Minimum compatible API/SDK contract version |
| `maxExecutionDepth` | Maximum nested tool-call depth per turn; the matrix default is 10, with orchestrator delegated children limited to depth 3 |
|
## Notes

The Agent registry remains an inventory document, but it SHOULD stay aligned with the compatibility expectations defined in [standards/Registry-Standard.md](../standards/Registry-Standard.md).


## S1 — Dynamic Concurrency Cap Note
The multi-agent concurrency cap (`MULTI_AGENT_SYSTEM.md` SA-3) uses `min(memory_budget/per_agent_est, cpu_cores, configurable_max)` with default 3 and high-end 8–16. Per-agent concurrency configuration is not added as a separate registry field; the cap is enforced at the workspace/resource level (`Workspace.maxConcurrency`, `ResourceManager`).
