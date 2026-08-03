> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

# Module Dependency Graph

**Architectural rule #1:** Everything is a service behind an interface. UI never talks directly to implementations.

## Dependency Hierarchy

Dependencies flow strictly downward. A module may only depend on modules in its own layer or any layer below it.

```
UI Layer          ui/
                    ↓
Application Layer  application/ → services/
                    ↓
Runtime Layer      runtime/ → agents/ → workflows/
                    ↓
Manager Layer      tools/ → providers/ → memory/ → plugins/
                    ↓
Infrastructure     sandbox/ → storage/ → security/
                    ↓
Shared             shared/
```

## Allowed Dependencies

| Module | ✓ May depend on | ❌ Must not depend on |
|--------|-----------------|----------------------|
| `ui/` | `application`, `shared` | `sandbox`, `tools`, `providers`, `memory`, `agents`, `plugins`, `workflows`, `storage`, `services`, `security`, `runtime` |
| `application/` | All modules | None (top-level orchestrator) |
| `runtime/` | `tools`, `providers`, `memory`, `agents`, `workflows`, `storage`, `security`, `shared` | `ui`, `application`, `sandbox`, `services` |
| `tools/` | `sandbox`, `storage`, `security`, `shared` | `ui`, `application`, `runtime`, `providers`, `memory`, `agents`, `plugins`, `workflows`, `services` |
| `sandbox/` | `storage`, `security`, `shared` | `ui`, `application`, `runtime`, `tools`, `providers`, `memory`, `agents`, `plugins`, `workflows`, `services` |
| `providers/` | `storage`, `security`, `shared` | `ui`, `application`, `runtime`, `tools`, `sandbox`, `memory`, `agents`, `plugins`, `workflows`, `services` |
| `memory/` | `storage`, `security`, `shared` | `ui`, `application`, `runtime`, `tools`, `sandbox`, `providers`, `agents`, `plugins`, `workflows`, `services` |
| `agents/` | `shared` | `ui`, `application`, `runtime`, `tools`, `sandbox`, `providers`, `memory`, `plugins`, `workflows`, `services`, `storage` |
| `plugins/` | `tools`, `storage`, `security`, `shared` | `ui`, `application`, `runtime`, `sandbox`, `providers`, `memory`, `agents`, `workflows`, `services` |
| `workflows/` | `shared` | `ui`, `application`, `runtime`, `tools`, `sandbox`, `providers`, `memory`, `agents`, `plugins`, `services`, `storage` |
| `storage/` | `shared` | All other modules |
| `services/` | `runtime`, `storage`, `security`, `shared` | `ui`, `application`, `tools`, `sandbox`, `providers`, `memory`, `agents`, `plugins`, `workflows` |
| `security/` | `storage`, `shared` | `ui`, `application`, `runtime`, `tools`, `sandbox`, `providers`, `memory`, `agents`, `plugins`, `workflows`, `services` |
| `shared/` | *(none — leaf module)* | All other modules |

## Forbidden Dependencies

These are the most critical violations to watch for in code review:

| Violation | Why it's forbidden |
|-----------|-------------------|
| `ui/ → sandbox/` | UI talks only to `application/` + `shared/` interfaces (MODULE_BOUNDARIES); sandbox is infrastructure | |
| `ui/ → providers/` | UI must go through `runtime/`; provider selection is a runtime concern | |
| `plugins/ → ui/` | Plugins never touch UI; they expose tools only | |
| `providers/ → Android UI` | Providers are pure Kotlin with zero Compose/View dependencies | |
| `sandbox/ → providers/` | Sandbox is infrastructure; it knows nothing about AI | |
| `tools/ → ui/` | Tools are backend logic; never import Compose or View | |
| `shared/ → any domain module` | `shared/` is the leaf — no upward dependencies ever | |

## Hilt Module Binding Rule

All cross-module access goes through interfaces. Hilt `@Module` objects in each module's `di/` package provide the bindings; consumers never reference implementation classes.

```kotlin
@Module
@InstallIn(SingletonComponent::class)
abstract class ToolManagerModule {

    @Binds
    @Singleton
    abstract fun bindToolManager(impl: ToolManagerImpl): ToolManager
}
```

ViewModels and services inject `ToolManager` — they never see `ToolManagerImpl`.

## Cycle Prevention

Circular dependencies between any two modules are **strictly forbidden**. Gradle's `:modules` project structure can enforce unidirectional edges at build time via dependency rules. Architectural fitness functions in CI should flag any cycle detected in the module graph.
