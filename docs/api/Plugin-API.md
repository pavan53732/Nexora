# Plugin API — Nexora

The Plugin API governs installation, activation, deactivation, rollback, and capability registration semantics.

## Lifecycle Alignment

Plugin lifecycle operations SHOULD remain transactionally safe and consistent with registry compatibility requirements. Activation success MUST NOT be inferred before exported capability registration and integrity conditions are satisfied.

## Contract Notes

Plugin APIs SHOULD preserve canonical error semantics, compatibility-aware rollback handling, and auditable lifecycle outcomes.
