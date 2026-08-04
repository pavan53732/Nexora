> **Status: DERIVED** for Plugin message contract.
> This document defines protocol messages for Plugin lifecycle operations. Canonical subsystem behavior is defined in the owning architecture document.
>
> Depends on: the canonical architecture document for Plugin.
> Referenced by: models, APIs, SDKs, registries, security, and tests.

# Plugin Protocol — Nexora

## Lifecycle Messages

Plugin protocol messages cover install, activate, deactivate, and remove operations. Each message MUST carry `correlationId`, plugin identity, target version where applicable, caller scope, and durable lifecycle version on emitted transitions.

Activation is transactional across exported capability registration. A failed capability registration MUST trigger rollback to the prior durable plugin state; partial exported visibility is not valid.

## Registration

After successful activation, exported agents, tools, providers, and skills register through their owning APIs. The plugin protocol may reference those registrations, but it MUST NOT redefine their payload contracts.

## Isolation

Protocol handlers MUST enforce signature/integrity verification, compatibility checks, dependency checks, and permission constraints before installation or activation side effects occur.
