# DEC-12 — Command Artifact and Workflow Relationship

> **Status: CANONICAL DECISION**

## Repository evidence

`architecture/WORKFLOW_ENGINE.md` is canonical for internal workflow graph progression. `models/Skill.md` and `architecture/RUNTIME.md` define skills and the Skill Registry. The audit found **NO CANONICAL COMMAND WORKFLOW ARTIFACT FOUND**: no canonical Command entity, Command Registry, slash-command contract, or command lifecycle. `AGENTS.md` and `SKILL.md` are repository/instruction documents, not product command contracts.

## Decision

Nexora does **not** establish a first-class `Command` artifact in this specification phase.

User requests are interpreted through the existing agent/runtime model. The Agent Runtime may select skills, create tasks, and invoke the Workflow Engine when the canonical runtime determines that a workflow is needed. Workflow remains an internal graph execution concept; Skill remains an agent capability concept. Neither is renamed or treated as a Command.

No command registry, slash-command namespace, command scope/precedence system, command lifecycle, or command-management UI is introduced.

## Rationale

A first-class command would require an additional identity, registry, invocation, scope, version, permission, lifecycle, and persistence contract. The existing repository does not require that surface, and the agent-first model already provides a goal-based interaction boundary. Not creating the artifact avoids conflating user invocation with skill metadata or workflow execution.

## Reconsideration trigger

A future command decision may be proposed if a documented product requirement requires stable named user invocation independent of agent interpretation. Such a decision must separately define command semantics and security; it must not retrofit `AGENTS.md` or `SKILL.md` into a command registry.
