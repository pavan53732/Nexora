# Provider Registry — Nexora

## Standard Fields

| Field | Meaning |
|---|---|
| `providerId` | Stable provider identifier |
| `version` | Provider adapter version |
| `origin` | `built-in` or plugin/provider source |
| `supportedModels` | Supported model families or identifiers |
| `supportsStreaming` | Streaming capability flag |
| `supportsResume` | Resume capability flag |
| `usageAccountingLevel` | Usage support detail |
| `minContractVersion` | Minimum compatible API/SDK contract version |

## Notes

The Provider registry remains an inventory document, but it SHOULD stay aligned with the compatibility expectations defined in [standards/Registry-Standard.md](../standards/Registry-Standard.md).
