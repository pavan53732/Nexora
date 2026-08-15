# DEC-40 — Module Interface Dependencies and Event Transport Boundary

> **Status: CANONICAL DECISION**
> **Authority:** Nexora architecture owner
> **Scope:** Relationship between direct public-interface dependencies and EventBus communication.

## Problem

The supporting constraints document describes inter-module communication as EventBus-only and forbids direct feature-module dependencies. The canonical module boundary and dependency graph permit direct dependencies on public interfaces along the documented downward graph and separately define EventBus as the event transport mechanism.

## Decision

Nexora permits direct dependencies between modules only when the dependency follows the canonical `docs/MODULE_BOUNDARIES.md` and `docs/DEPENDENCY_GRAPH.md` public-interface graph. A consumer may import a provider module’s public interface but MUST NOT import its concrete implementation. Hilt binds interfaces to implementations at the application composition boundary as already specified.

EventBus is the transport for published domain/runtime events and subscriptions. It is not the sole mechanism for invoking synchronous or suspendable service interfaces. Direct interface calls and EventBus publication are complementary and MUST NOT be collapsed into a single ownership or transport concept.

## Constraints

The dependency graph remains acyclic and downward. `shared` remains a leaf. UI depends only on application/shared interfaces; runtime may depend on its canonical lower-level public interfaces; tools, sandbox, providers, memory, plugins, storage, security, services, and workflows retain their existing allowed/forbidden edges. No module may bypass the public API boundary to access implementation classes.

## Invariants

This decision does not create a new module, layer, lifecycle state, event type, or runtime owner. It preserves the existing EventBus interface and all canonical module responsibilities. It resolves only the interpretation of inter-module calls versus event transport.

## Required projections

requirements/CONSTRAINTS.md MUST replace the EventBus-only wording with the distinction above. Coding, dependency, Hilt, module-boundary, and source-start documentation MUST use the canonical module graph and public-interface rule.
