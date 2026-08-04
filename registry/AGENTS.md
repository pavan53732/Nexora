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
|
## Notes

The Agent registry remains an inventory document, but it SHOULD stay aligned with the compatibility expectations defined in [standards/Registry-Standard.md](../standards/Registry-Standard.md).
