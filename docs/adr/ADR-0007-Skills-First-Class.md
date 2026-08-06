# ADR-0007: Skills as a First-Class Capability

- **Status**: Accepted
- **Date**: 2026-08-03
- **Deciders**: Lead Architect, Product
- **Related**: [ADR-0003-Agent-Runtime](./ADR-0003-Agent-Runtime.md) · [ADR-0002-Plugin-System](./ADR-0002-Plugin-System.md) · [specs/EXECUTION_LIFECYCLE.md](../../specs/EXECUTION_LIFECYCLE.md) · [registry/SKILLS.md](../../registry/SKILLS.md) · [models/Skill.md](../../models/Skill.md)

## Context

The runtime determines *who* does work and *how* work is done, but there is no
first-class concept for *what expertise* the work requires. "Skill" appears in the
docs only as a synonym for plugins. As a result:

- The planner has no vocabulary for selecting expertise (e.g. "this needs Kotlin
  development, not generic file editing").
- Agents cannot acquire or improve capabilities over time — their tool set is fixed
  by configuration.
- Multiple capabilities that share tools (e.g. "Android Debugging" and "Git Conflict
  Resolution" both use the terminal + git tools) cannot be expressed, so capability
  selection is coarse.

## Decision

**Skills are a first-class concept, distinct from agents and tools.**

```
Agent  = WHO performs the work   (e.g. Coder, Tester, Researcher)
Skill  = WHAT expertise is needed (e.g. Kotlin Development, Android Debugging,
                                    Git Conflict Resolution, API Design)
Tool   = HOW the work is performed (e.g. File Tool, Git Tool, Browser Tool,
                                    Terminal Tool, Build Tool)
```

1. **Skills are entities** — a `Skill` has an id, name, description, domain, the set
   of tools it relies on, applicable agent types, and an acquisition source
   (built-in, user-defined, or learned).
2. **Skills are registered** in a `SkillRegistry` (runtime module) and cataloged in
   [registry/SKILLS.md](../../registry/SKILLS.md) with stable IDs (`SKL-###`).
3. **The planner selects skills per task** — alongside agent, tool, model, and plugin
   selection (see [specs/EXECUTION_LIFECYCLE.md](../../specs/EXECUTION_LIFECYCLE.md)).
4. **Agents acquire skills** — an agent's configuration references the skills it
   possesses; acquisition (built-in assignment, user authoring, or learning from
   experience) is a first-class operation (FR-SK-002/003).
5. **Skills map to tools, not the reverse** — one skill uses many tools; many skills
   may share the same underlying tools. Tools remain the permissioned execution
   surface; skills are the expertise layer above them.
6. **Skill validation** — every skill declares which tools it needs; the registry
   validates those tool references at registration (FR-SK-005).

## Consequences

### Positive

- **Finer-grained planning** — the planner reasons in expertise terms ("requires
  Kotlin Development + Android Debugging") and resolves them to concrete agents/tools.
- **Agents grow** — capability is acquired over time instead of being a static config.
- **Reuse** — skills compose over the same tools, keeping the tool surface minimal.
- **Match to providers** — skills can declare preferred model families (e.g. code
  generation → a coding-strong model), feeding per-task model selection.
- **Plugin alignment** — plugins can register new skills, keeping ADR-0002 intact.

### Negative

- **One more registry to maintain** — mitigated by keeping the catalog focused
  (initial 20 skills) and co-located with the tool catalog generator.
- **Selection complexity** — planner must consider skill availability; mitigated by
  the lifecycle spec defining the selection order and fallbacks.

### Mitigation

- Initial skill catalog ships built-in (see [registry/SKILLS.md](../../registry/SKILLS.md)).
- Skill selection is advisory → the executor validates at runtime that the chosen
  agent actually possesses the skill before dispatch.
