# Plugin Registry — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)
> See [sdk/PluginSDK.md](../sdk/PluginSDK.md) for the Plugin SDK, [architecture/PLUGIN_SYSTEM.md](../architecture/PLUGIN_SYSTEM.md)
> for the plugin architecture, and [state-machines/PluginLifecycle.md](../state-machines/PluginLifecycle.md)
> for the lifecycle state machine.

**Authoritative registry of every plugin.** Stable IDs per [DL-017](../docs/DECISION_LOG.md).
Plugins are installed, updated, enabled, disabled, or removed independently (see
[User Operations](#user-operations--lifecycle-mapping) below).

## Registry

| ID | Plugin | Registers | Install Source | Phase | Status |
|----|--------|-----------|----------------|-------|--------|
| PLG-001 | Core File Tools | File System tools | Bundled | 4 | Planned |
| PLG-002 | Core Terminal Tools | Terminal tools | Bundled | 4 | Planned |
| PLG-003 | Git Integration | Git tools | Bundled | 4 | Planned |
| PLG-004 | Browser Automation | Browser tools | Marketplace | 8 | Planned |
| PLG-005 | Python Runtime | Python runtime extension, pip tools | Bundled | 3 | Planned |
| PLG-006 | Node Runtime | Node.js runtime extension, npm tools | Bundled | 3 | Planned |
| PLG-007 | SQLite Tools | Database tools | Bundled | 3 | Planned |
| PLG-008 | OCR | OCR tools | Marketplace | 8 | Planned |
| PLG-009 | PDF Tools | PDF tools | Marketplace | 8 | Planned |
| PLG-010 | Camera | Camera / media capture tools | Marketplace | 8 | Planned |
| PLG-011 | Email | Email tools | Marketplace | 8 | Planned |
| PLG-012 | Calendar | Calendar tools | Marketplace | 8 | Planned |
| PLG-013 | Maps | Maps / location tools | Marketplace | 8 | Planned |
| PLG-014 | Speech (TTS/STT) | Speech synthesis / recognition tools | Marketplace | 8 | Planned |
| PLG-015 | Translation | Translation tools | Marketplace | 8 | Planned |
| PLG-016 | Weather | Weather tools | Marketplace | 8 | Planned |
| PLG-017 | Android APIs | Android device integration tools | Marketplace | 8 | Planned |
| PLG-018 | AI Providers | Provider implementations (PROV-001…009) | Marketplace | 8 | Planned |

**Notes**

- **Bundled** plugins ship with the app (core file/terminal/Git/runtime/SQLite capabilities —
  internal, agent-invoked per ADR-0006). **Marketplace** plugins are installed on demand
  from Nexora Hub (Phase 8) or sideloaded, and can be removed without affecting the core.
- Every plugin may additionally register agents, memory backends, or UI screens
  (see [architecture/PLUGIN_SYSTEM.md](../architecture/PLUGIN_SYSTEM.md)).

## User Operations ↔ Lifecycle Mapping

| User action | Lifecycle transitions (see [PluginLifecycle](../state-machines/PluginLifecycle.md)) | Result state |
|-------------|----------------------------------------------------------------------------------------|--------------|
| **Install** | `discover()` → `download()` → `verify()` → `install()` | Installed |
| **Enable** | `activate()` | Active |
| **Disable** | `deactivate()` | Inactive (artifacts kept) |
| **Update** | `update()` → `download()` → `verify()` → `install()` (in-place, preserves state where possible) | Installed / Active |
| **Remove** | `uninstall()` | Uninstalled (data cleaned) |

Operations are independent: a plugin can be disabled without being removed, updated
while enabled, or removed while inactive. Reactivation (`Inactive → Activating`) skips
download and install and reuses cached artifacts.
