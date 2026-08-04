> **Status: SUPPORTING** for Coding Standard coding standard.
> This document defines conventions for Coding Standard. It applies across all subsystems and does not override canonical subsystem definitions.


# Coding Standard — Nexora

## Language
- **Primary**: Kotlin (2.0+)
- **Secondary**: Java (17+) only for Android SDK interop
- No other languages in the main codebase

## Architecture
- Clean Architecture: `android/` → `core/` → `runtime/` → domain modules
- Each module has: `model/`, `repository/`, `usecase/` (where applicable)
- Dependency direction: android → core → runtime → tools/agents/providers (never reverse)

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
