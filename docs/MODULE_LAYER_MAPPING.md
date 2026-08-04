# Module-to-Layer Mapping

> **Status: CANONICAL** for mapping between feature modules and architectural layers.

| Feature Module (MODULE_BOUNDARIES.md) | Architectural Layer (DEPENDENCY_GRAPH.md) | Notes |
|--------------------------------------|------------------------------------------|-------|
| `agent-runtime` | `domain/` | Core domain logic |
| `tool-system` | `domain/` | Core domain logic |
| `sandbox` | `data/` + `domain/` | VFS in data, proot execution in domain |
| `memory-system` | `domain/` | Core domain logic |
| `provider-system` | `domain/` | Core domain logic |
| `workflow-engine` | `domain/` | Core domain logic |
| `multi-agent-system` | `domain/` | Core domain logic |
| `plugin-system` | `domain/` + `application/` | Plugin loading in domain, UI in app |
| `security` | `domain/` + `shared/` | Policy in domain, crypto in shared |
| `ui` | `application/` | Presentation layer |
| `storage` | `data/` | Room, SQLite, files |
| `shared` | `shared/` | Utilities, constants |

## Dependency Rules

- A feature module in the `domain/` layer may depend on any `data/` or `shared/` module.
- A feature module in the `application/` layer may depend on any `domain/`, `data/`, or `shared/` module.
- `shared/` modules may not depend on any other module.
- Cross-feature dependencies within the same layer must be explicit and documented.
