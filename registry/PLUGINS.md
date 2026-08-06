# Plugin Registry — Nexora

## Standard Fields

| Field | Meaning |
|---|---|
| `pluginId` | Stable plugin identifier |
| `version` | Plugin package version |
| `origin` | Built-in or external source |
| `compatibilityRange` | Compatible runtime/API range |
| `dependencyRanges` | Dependency version constraints |
| `exportedCapabilities` | Exported agent/tool/provider/skill/UI-screen/memory-backend references (one list per `exported*` field in [../models/Plugin.md](../models/Plugin.md)) |
| `integrityState` | Signature/integrity state |
| `minContractVersion` | Minimum compatible API/SDK contract version |
| `manifestVersion` | Manifest/schema version |

## Notes

The Plugin registry remains an inventory document, but it SHOULD stay aligned with the compatibility expectations defined in [standards/Registry-Standard.md](../standards/Registry-Standard.md).
