> **Status: SUPPORTING** for Coding Standard coding standard.
> This document defines conventions for Coding Standard. It applies across all subsystems and does not override canonical subsystem definitions.


# Coding Standard — Nexora

## Language
- **Primary**: Kotlin (2.0+)
- **Secondary**: Java (17+) only for Android SDK interop
- No other languages in the main codebase

## Architecture
- Canonical module graph: `ui` → `application`/`shared`, with application composition over `services`, `runtime`, `tools`, `providers`, `memory`, `agents`, `workflows`, `plugins`, `sandbox`, `storage`, and `security` according to `docs/MODULE_BOUNDARIES.md` and `docs/DEPENDENCY_GRAPH.md`.
- Every cross-module dependency uses a public interface; consumers must not import concrete implementation classes. Hilt binds interfaces to implementations at the application composition boundary (DEC-40).
- `shared` remains a leaf module. Dependencies are acyclic and follow the canonical allowed/forbidden matrix; EventBus is event transport and does not replace direct public-interface calls.
- Each module may use `model/`, `repository/`, and `usecase/` subpackages where applicable; package layout must not introduce obsolete `core` or `domain` modules.

## Naming
- Classes: `PascalCase` (`ToolRegistry`, `AgentLoop`)
- Functions: `camelCase` (`executeTool`, `buildContext`)
- Constants: `UPPER_SNAKE_CASE` (`MAX_TOKEN_BUDGET`)
- Package: `lowercase` (`com.nexora.app.runtime.tools`)
- IDs: `snake_case` (`file_read`, `git_commit`)

## Conventions
- Use `sealed class` for result types, not exceptions for flow control
- Use `suspend fun` for all async operations
- Use `Flow` for streams, not callbacks
- Prefer data classes over regular classes for models
- Use `Result<T>` for operations that can fail
- Document all public APIs with KDoc

## File Organization
- One top-level type per file
- File name matches the type name
- Package structure mirrors the directory structure
