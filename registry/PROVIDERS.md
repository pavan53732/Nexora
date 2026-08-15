> **Status: DERIVED** for provider registry inventory. Canonical provider subsystem ownership is [../architecture/PROVIDER_SYSTEM.md](../architecture/PROVIDER_SYSTEM.md).

# Provider Registry — Nexora

## Standard Fields

| Field | Meaning |
|---|---|
| `providerId` | Stable provider identifier |
| `version` | Provider adapter version |
| `origin` | `built-in` or plugin/provider source |
| `supportedModels` | Supported model families or identifiers |
| `supportsStreaming` | Streaming capability flag |
| `streamResumeMode` | `NATIVE_CURSOR`, `RESTART_WITH_LINEAGE`, or `NONE` |
| `contextWindowTokens` / `maxOutputTokens` | Model capacity metadata |
| `tokenizerId` | Token accounting/compiler identity |
| `reasoningEfforts` | Supported canonical reasoning effort values |
| `supportsTools` / `supportsCitations` | Typed event capabilities |
| `inputCostPerMillion` / `outputCostPerMillion` | Route-planning cost metadata |
| `dataLocality` | `EXTERNAL` for every active AI provider under DEC-41 |
| `usageAccountingLevel` | Usage support detail |
| `minContractVersion` | Minimum compatible API/SDK contract version |

## Notes

The Provider registry remains an inventory document, but it SHOULD stay aligned with the compatibility expectations defined in [standards/Registry-Standard.md](../standards/Registry-Standard.md).
