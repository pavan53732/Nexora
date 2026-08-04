# Plugin SDK — Nexora

The Plugin SDK defines the contract surface for plugin packaging, lifecycle, and exported capabilities.

## Lifecycle Alignment

Plugin SDK helpers SHOULD preserve transactional lifecycle semantics for install, activate, deactivate, and rollback operations rather than inferring state from partial adapter behavior.

## Notes

Compatibility declarations, manifest/schema versioning, and exported capability registration should remain consistent with registry and API contract expectations.
