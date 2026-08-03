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
| `ui/` | `application`, `services`, `runtime`, `agents`, `shared` | `tools`, `sandbox`, `providers`, `memory`, `plugins`, `workflows`, `storage`, `security` |
| `application/` | `services`, `runtime`, `shared` | `ui`, `tools`, `sandbox`, `providers`, `memory`, `plugins`, `workflows`, `storage`, `security` |
| `services/` | `runtime`, `shared` | `ui`, `application`, `tools`, `sandbox`, `providers`, `memory`, `plugins`, `workflows`, `storage`, `security` |
| `runtime/` | `agents`, `tools`, `providers`, `memory`, `workflows`, `sandbox`, `storage`, `shared` | `ui`, `application`, `services`, `plugins`, `security` |
| `agents/` | `memory`, `shared` | `ui`, `application`, `services`, `runtime`, `tools`, `sandbox`, `providers`, `plugins`, `workflows`, `storage`, `security` |
| `workflows/` | `tools`, `shared` | `ui`, `application`, `services`, `runtime`, `agents`, `sandbox`, `providers`, `memory`, `plugins`, `storage`, `security` |
| `tools/` | `sandbox`, `storage`, `security`, `shared` | `ui`, `application`, `services`, `runtime`, `agents`, `providers`, `memory`, `plugins`, `workflows` |
| `providers/` | `memory`, `shared` | `ui`, `application`, `services`, `runtime`, `agents`, `tools`, `sandbox`, `plugins`, `workflows`, `storage`, `security` |
| `memory/` | `storage`, `shared` | `ui`, `application`, `services`, `runtime`, `agents`, `tools`, `sandbox`, `providers`, `plugins`, `workflows`, `security` |
| `plugins/` | `tools`, `shared` | `ui`, `application`, `services`, `runtime`, `agents`, `sandbox`, `providers`, `memory`, `workflows`, `storage`, `security` |
| `sandbox/` | `security`, `shared` | `ui`, `application`, `services`, `runtime`, `agents`, `tools`, `providers`, `memory`, `plugins`, `workflows`, `storage` |
| `storage/` | `shared` | All other modules |
| `security/` | `shared` | All other modules |
| `shared/` | *(none — leaf module)* | All other modules |

## Forbidden Dependencies

These are the most critical violations to watch for in code review:

| Violation | Why it's forbidden |
|-----------|-------------------|
| `ui/ → sandbox/` | UI must go through `runtime/` or `services/` interface | |
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
