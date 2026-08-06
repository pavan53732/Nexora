# ADR-0002: Plugin-First Design

- **Status**: Accepted
- **Date**: 2026-08-03
- **Deciders**: Lead Architect

## Context

Nexora is projected to have 300-500 tools, 10-20 agent types, 9+ AI providers, and an open-ended set of capabilities. If all of these are built into the core application, the codebase becomes monolithic, untestable, and impossible for the community to extend.

Additionally, not all users need all capabilities. A user who only uses OpenAI should not carry the code for Ollama, LM Studio, and GGUF. A user who doesn't need browser automation should not have a WebView dependency.

## Decision

Every capability in Nexora is implemented as a **plugin**. The core runtime is minimal and provides only:

- Agent loop (planner, executor, event bus)
- Tool registry (interface only)
- Provider registry (interface only)
- Plugin manager (loading, lifecycle)
- Sandbox (virtual file system, process isolation)
- Permission manager
- Memory manager (interface only)

Everything else — tools, agents, providers, UI extensions — is a plugin.

Plugins can:
- Register tools, agents, providers, and UI screens.
- Declare dependencies on other plugins.
- Run in isolated contexts.
- Be installed, updated, and removed at runtime.

## Consequences

### Positive
- **Small core**: The APK base size stays under 50 MB.
- **Extensibility**: The community can add capabilities without modifying core.
- **Selective installation**: Users only install what they need.
- **Independent versioning**: Plugins can be updated independently of the app.
- **Testability**: Each plugin can be tested in isolation.

### Negative
- **Interface stability**: The core interfaces must be extremely stable. Breaking changes cascade to all plugins.
- **Discovery overhead**: Users must find and install plugins for basic capabilities.
- **Version compatibility**: Plugins must declare compatible app versions.

### Mitigation
- Ship essential plugins (file tools, terminal, OpenAI provider) as "bundled plugins" that are installed by default.
- Version the plugin API semantically. Maintain backwards compatibility.
- Provide Nexora Hub (marketplace) for easy discovery and installation.
