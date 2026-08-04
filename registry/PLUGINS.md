# Plugin Registry — Nexora

The plugin registry is the authoritative inventory of installable plugin packages and their exported capability surfaces.

## Registry

Each plugin entry SHOULD include or derive the following metadata:

- stable `pluginId`
- plugin version
- compatibility range
- exported capability types
- dependency ranges
- integrity/signature state
- minimum compatible API/SDK and manifest/schema versions

## User Operations ↔ Lifecycle Mapping

Registry views may summarize plugin lifecycle state, but transactional activation and rollback semantics remain governed by the canonical Plugin API and protocol documents.
