# Tool Registry — Nexora

## Standard Fields

| Field | Meaning |
|---|---|
| `toolId` | Stable tool identifier |
| `version` | Tool version |
| `origin` | `built-in` or plugin/provider origin |
| `category` | Registry category |
| `requiredPermissions` | Required permission scopes |
| `requiresSandbox` | Sandbox requirement flag |
| `supportsStreaming` | Streaming capability flag |
| `supportsCancellation` | Cancellation capability flag |
| `isIdempotent` | Idempotency declaration |
| `parametersSchemaRef` | Parameter schema reference |
| `minContractVersion` | Minimum compatible API/SDK contract version |

## Notes

The Tool registry remains an inventory document, but it SHOULD stay aligned with the compatibility expectations defined in [standards/Registry-Standard.md](../standards/Registry-Standard.md).
