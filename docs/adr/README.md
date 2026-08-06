# Architecture Decision Records — Nexora

> Back to [PROJECT_SPECIFICATION.md](../../PROJECT_SPECIFICATION.md)
> Canonical source ownership is defined in [../CANONICAL_SOURCES.md](../CANONICAL_SOURCES.md). ADR status is recorded in each ADR metadata block below.

Architecture Decision Records (ADRs) document major architectural decisions, their context, and consequences. Each ADR is immutable once accepted.

## Index

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| [ADR-0001](ADR-0001-Workspace-First.md) | Workspace-First Architecture | Accepted | 2026-08-03 |
| [ADR-0002](ADR-0002-Plugin-System.md) | Plugin-First Design | Accepted | 2026-08-03 |
| [ADR-0003](ADR-0003-Agent-Runtime.md) | Autonomous Agent Runtime Loop | Accepted | 2026-08-03 |
| [ADR-0004](ADR-0004-Sandbox.md) | Sandboxed Execution | Accepted | 2026-08-03 |
| [ADR-0005](ADR-0005-Provider-Abstraction.md) | Provider Abstraction Layer | Accepted | 2026-08-03 |
| [ADR-0006](ADR-0006-Agent-First-Interaction-Model.md) | Agent-First Interaction Model (Infrastructure Is Internal) | Accepted | 2026-08-03 |
| [ADR-0007](ADR-0007-Skills-First-Class.md) | Skills as a First-Class Capability | Accepted | 2026-08-03 |

## ADR Template

```markdown
# ADR-NNNN-Title

- **Status**: Accepted | Proposed | Deprecated | Superseded by ADR-NNNN
- **Date**: YYYY-MM-DD
- **Deciders**: [list]

## Context
What is the issue that we're seeing that is motivating this decision?

## Decision
What is the change that we're proposing/making?

## Consequences
What becomes easier or more difficult because of this change?
```