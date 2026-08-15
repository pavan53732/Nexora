# DEC-32 — Workflow Scope and Monitoring Surface

> **Status: CANONICAL DECISION**
> **Authority:** Nexora product and architecture owner
> **Scope:** JavaScript-scripted workflows and a dedicated `/workflows` monitoring panel.

## Decision

Nexora v1 remains a pure Android application with the agent-first chat/activity-feed interaction model established by DL-019 and the existing Product Vision. The current release does not include a JavaScript workflow runtime and does not include a dedicated `/workflows` monitoring panel.

The canonical Workflow Engine continues to support declarative, bounded workflow graphs through the existing Task, Workflow, Tool, provider, checkpoint, notification, and activity-feed contracts. JavaScript workflow execution is a later optional extension and is not an implicit dependency of the current runtime.

Workflow status, progress, approval, failure, cancellation, checkpoint, and terminal outcomes remain visible through the existing activity feed, Task surfaces, notifications, and Settings surfaces. A future dedicated monitoring surface may be introduced only through a later product decision and must not create a second lifecycle or observability authority.

## Security and implementation boundary

No JavaScript engine, script permission scope, script sandbox, script API, workflow-panel navigation route, or new requirement is created by this decision. If JavaScript workflows are later selected, they must use the existing sandbox, Tool authorization, evidence, deadline, cancellation, and audit contracts and receive a separate architecture decision before implementation.

## Validation obligations

Current implementation and release validation must prove declarative Workflow Engine behavior and existing activity-feed projections. JavaScript runtime and dedicated monitoring-panel behavior remain out of current-release evidence and must not be reported as implemented.
