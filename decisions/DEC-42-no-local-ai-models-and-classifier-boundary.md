# DEC-42 — No Local AI Models and Security Classifier Boundary

- **Status:** Accepted
- **Date:** 2026-08-15
- **Deciders:** Architecture Owner
- **Related:** DEC-41 cloud-only AI provider scope

## Context

The active PermissionModel specified an optional on-device TFLite auto-approval classifier. The product requirement is now literal: Nexora must use cloud AI providers only and must not contain or execute local AI models. The classifier is not a ProviderType, but it is still an on-device AI model and therefore falls within the requirement.

## Decision

The optional on-device TFLite auto-approval classifier is removed from the active Nexora architecture. Nexora does not bundle, load, execute, or manage TFLite, ONNX, GGUF, or other local AI model files for authorization, inference, embeddings, routing, or any other AI-model function.

Permission authorization remains governed by the existing PermissionModel scope hierarchy, explicit DENY and ASK decisions, approval transactions, user approval, policy evaluation, and audit logging. Removing the classifier does not create an ALLOW override, weaken default-deny behavior, bypass ASK approval, or change any existing permission scope or lifecycle.

No cloud classifier replacement is introduced by this decision. A future cloud safety-classification service would require a separate decision covering data handling, latency, availability, error mapping, privacy, egress, and fail-closed behavior.

## Pipe and Delegation Consequence

Pipe and cross-instance delegation authorization uses the existing permission scopes, acceptance mode, approval transaction, and audit contracts. The optional classifier is not a required or available gate for pipe authorization.

## Preserved Invariants

This decision does not create or remove Task, Agent, Tool, Provider, permission, or lifecycle states. Explicit policy DENY, USER_DENIED, approval expiry, no-side-effect enforcement, audit, notification, and new-authorization-transaction rules remain governed by the existing permission and approval authorities.

Local non-AI execution remains allowed. Sandboxed terminal/process execution, filesystem operations, Git, SQLite/Room persistence, checkpoints, local workspace search, and read-only offline workspace access are not AI-model execution and are unaffected.

## Required Projections

The active PermissionModel, pipe/delegation protocol, provider specifications, requirements, product principles, sandbox depth, environment setup, security standards, risks, traceability, canonical-source map, completeness inventory, and changelog must not claim an active on-device AI classifier or local model. Immutable historical decision and changelog records remain unchanged and must be treated as historical where they describe the former classifier.

## Acceptance Evidence

Documentation validation must show no active TFLite, ONNX, GGUF, local model, or on-device AI-model execution claim. Permission tests must continue to cover scope resolution, ASK approval, explicit denial, classifier-independent denial behavior, audit, and fail-closed authorization without assuming a local classifier.
