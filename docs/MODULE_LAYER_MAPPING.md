# Module-to-Layer Mapping

> **Status: CANONICAL** for mapping between feature modules and architectural layers.
> The feature module names and layers below are taken verbatim from
> [MODULE_BOUNDARIES.md](MODULE_BOUNDARIES.md) and
> [DEPENDENCY_GRAPH.md](DEPENDENCY_GRAPH.md). Any module not listed here is either a leaf
> utility (e.g. `shared`) or a future extension; the dependency graphs remain authoritative
> for allowed/forbidden edges.

| Feature Module (MODULE_BOUNDARIES.md) | Architectural Layer (DEPENDENCY_GRAPH.md) | Notes |
|--------------------------------------|------------------------------------------|-------|
| `ui` | UI Layer (`ui/`) | Presentation layer |
| `application` | Application Layer (`application/`) | Top-level orchestrator; may depend on all modules |
| `runtime` | Runtime Layer (`runtime/`) | Agent loop, executor, planner, permission manager, scheduler, observability, security manager, background runtime, resource manager, agent manager, state machines |
| `agents` | Runtime Layer (`runtime/ → agents/`) | Agent interface, types, registry |
| `workflows` | Runtime Layer (`runtime/ → workflows/`) | Workflow engine, DAG execution (owned by `architecture/WORKFLOW_ENGINE.md`, invoked by runtime) |
| `tools` | Manager Layer (`tools/`) | Tool interface, manager, implementations |
| `providers` | Manager Layer (`providers/`) | AI provider adapters, routing, streaming |
| `memory` | Manager Layer (`memory/`) | Memory manager, tiers, embeddings, vector search |
| `plugins` | Manager Layer (`plugins/`) | Plugin loader, lifecycle, marketplace client |
| `sandbox` | Infrastructure (`sandbox/`) | Virtual file system, process manager, resource limits |
| `storage` | Infrastructure (`storage/`) | Room database, DataStore, repositories |
| `security` | Infrastructure (`security/`) | Secure key store, audit logging, permission policy storage |
| `services` | Application Layer (`application/ → services/`) | Android foreground services, WorkManager |
| `shared` | Shared (`shared/`) | Utilities, constants, event types (leaf module) |

## Dependency Rules

- A feature module in the `domain/`/`runtime/` layer may depend on any lower layer module
  (`data/`, `infrastructure/`, `shared/`) per `DEPENDENCY_GRAPH.md`.
- A feature module in the `application/` layer may depend on any `domain/`/`runtime/`,
  `data/`, `infrastructure/`, or `shared/` module; `ui` depends only on `application` +
  `shared`.
- `shared/` modules may not depend on any other module (leaf rule).
- Cross-feature dependencies within the same layer must be explicit and documented in
  `MODULE_BOUNDARIES.md`.

> **Note:** earlier drafts of this mapping used invented module names (`agent-runtime`,
> `tool-system`, `memory-system`, `provider-system`, `workflow-engine`,
> `multi-agent-system`, `plugin-system`, `security`, `ui`, `storage`, `shared`) and
> invented layers (`domain/`, `data/`). Those names are not the canonical module names and
> have been replaced above to keep fitness checks deterministic.
