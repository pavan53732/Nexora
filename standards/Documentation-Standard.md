> **Status: SUPPORTING** for Documentation Standard coding standard.
> This document defines conventions for Documentation Standard. It applies across all subsystems and does not override canonical subsystem definitions.


# Documentation Standard — Nexora

## Rule
> Update the relevant document BEFORE implementing significant changes.

## Document Types

| Type | Location | Updated When |
|------|----------|-------------|
| Spec changes | `docs/`, `architecture/`, `specs/` | Before any code change |
| New model | `models/` | Before implementing the model |
| New protocol | `protocols/` | Before implementing the protocol |
| ADR | `docs/adr/` | When a major decision is made |
| Feature | `registry/` | When a feature is planned |
| API change | `docs/api/`, `sdk/` | Before implementing the change |

## Format
- Markdown for all documentation
- Include a back-link to `PROJECT_SPECIFICATION.md` at the top
- Include code examples in Kotlin
- Include diagrams in ASCII art
- Cross-link related documents
