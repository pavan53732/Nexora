> **Status: SUPPORTING** for plugin lifecycle narrative.
> **The canonical state machine definition is owned by
> [../state-machines/PluginLifecycle.md](../state-machines/PluginLifecycle.md).**
> This file describes the plugin lifecycle in prose; it MUST NOT redefine, rename,
> or subset any state enum from the canonical source.
>
> Depends on: [../state-machines/PluginLifecycle.md](../state-machines/PluginLifecycle.md).

# Plugin Lifecycle Authority — Nexora

## Integrity State

`PENDING`, `VERIFYING`, `VERIFIED`, `FAILED_INVALID_SIGNATURE`, `FAILED_INCOMPATIBLE_SDK`, `FAILED_TAMPERED`

## Plugin Status

`DISCOVERED`, `DOWNLOADING`, `DOWNLOADED`, `VERIFYING`, `INSTALLING`, `INSTALLED`, `ACTIVATING`, `ACTIVE`, `DEACTIVATING`, `INACTIVE`, `UNINSTALLING`, `UNINSTALLED`, `FAILED`

## Transitions

- `DISCOVERED → DOWNLOADING`: Download initiated.
- `DOWNLOADING → DOWNLOADED`: Download complete.
- `DOWNLOADED → VERIFYING`: Signature/integrity verification started.
- `VERIFYING → INSTALLING`: Verification passed.
- `INSTALLING → INSTALLED`: Installation complete.
- `INSTALLED → ACTIVATING`: Activation started.
- `ACTIVATING → ACTIVE`: Activation complete; capabilities registered.
- `ACTIVE → DEACTIVATING`: Deactivation requested.
- `DEACTIVATING → INACTIVE`: Deactivation complete; classloader released.
- `INACTIVE → ACTIVATING`: Re-activation requested.
- `ACTIVE/INACTIVE → UNINSTALLING`: Uninstall requested.
- `UNINSTALLING → UNINSTALLED`: Uninstall complete; data cleaned.
- `* → FAILED`: Any failure state.

### Error Recovery

- Interrupted installation/download recovers to `DISCOVERED` or restarts download.
- Active plugins can be dynamically deactivated to `INACTIVE`, preserving local storage.