# DEC-11 — Skill Lifecycle and Execution Boundary

> **Status: CANONICAL DECISION**

## Repository evidence

`models/Skill.md` defines Skill and AgentSkillBinding. `architecture/RUNTIME.md` owns the Skill Registry module. `architecture/AGENT_RUNTIME.md` defines automatic skill selection through the registry. Existing permission and sandbox documents own tool authorization and execution safety.

## Decision

Skills remain agent/runtime capabilities, not user-facing applications. The Skill Registry owns registration, discovery, compatibility validation, and acquisition/binding operations. The Agent Runtime owns selection and use of an acquired skill during a task. The Tool and Permission authorities retain ownership of actual tool execution and authorization.

Skill use is subject to the same authorization, sandbox, untrusted-content, network, secret, confirmation, audit, timeout, cancellation, and retry policies that govern the selected tools and runtime operation. A skill cannot grant itself permissions.

Skill lifecycle states are: `Registered`, `Validated`, `Available`, `Bound`, `Revoked`, and `Retired`. `Available` means eligible for selection; `Bound` means associated with an agent. Revocation prevents new selection and does not silently cancel an already-running tool call; running execution follows runtime cancellation/error policy.

Skill version compatibility is checked at registration and binding. Replacement is a new versioned registration followed by explicit compatibility validation; it is not an in-place mutation of an active binding.

## Non-decisions

This does not create a Skill Manager UI, a skill-specific permission system, or a separate skill execution engine.
