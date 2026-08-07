# Registry Standard — Nexora

## Rule

All registries SHOULD expose a consistent compatibility metadata shape wherever applicable, even when the registry is primarily descriptive.

## Required Compatibility Fields

Where a registry entry represents an executable or compatibility-sensitive capability, it SHOULD include or derive:

- stable identifier
- version or revision marker
- origin (`built-in` or plugin/provider source)
- compatibility range or minimum compatible contract version
- dependent capability references where applicable
- declared execution-relevant flags, such as streaming, cancellation, sandbox, delegation, or resume support when relevant

### Registry Field Shape (concrete)

To make the above auditable, registries SHOULD expose the following columns where an entry is compatibility-sensitive:

| Field | Applies to | Source |
|-------|-----------|--------|
| `id` | all | Stable registry identifier (e.g. `TOOL-302`, `AGT-001`, `PLG-001`) |
| `version` | all | Entry revision; tools also carry descriptor `version` (`models/Tool.md`) |
| `origin` | plugin/provider-sourced | `built-in` or plugin/provider source |
| `category` | tools | `ToolCategory` (`architecture/TOOL_SYSTEM.md`) |
| `compatibilityRange` / `minContractVersion` | plugin/provider/tool | `Registry-Standard`; tools expose `minContractVersion` at descriptor level |
| `status` | all | Lifecycle/availability state (e.g. `ACTIVE`, `REGISTERED`, `DISABLED`) |
| `requiredPermissions` | tools/agents/plugins | Canonical `PermissionScope` IDs (`security/PermissionModel.md`) |
| `supportsStreaming` / `supportsCancellation` / `requiresSandbox` | tools | `Tool` descriptor (`architecture/TOOL_SYSTEM.md`) |
| `lastVerifiedAt` | plugin/provider | Compatibility check timestamp (recommended for drift detection) |

`registry/TOOLS.md` rows currently carry `id`, `category`, `status`, and `phase`; the
remaining compatibility fields are governed at the descriptor level
(`models/Tool.md`, `docs/api/Tool-API.md ToolDescriptor`) and need not be duplicated per
row. `registry/AGENTS.md` / `AGENT_MATRIX.md` carry `agentId`, `version`, `origin`,
`requiredPermissions`, and `minContractVersion` per the Agent standard fields.

## Notes

Registries remain inventory documents, but they SHOULD not drift from the API/SDK compatibility model. Shared compatibility semantics help traceability, regression review, and plugin/provider/tool onboarding.
