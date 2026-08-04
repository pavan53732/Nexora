> **Status: DERIVED** for Provider message contract.
> This document defines protocol messages for Provider execution. Canonical subsystem behavior is defined in the owning architecture document.
>
> Depends on: the canonical architecture document for Provider.
> Referenced by: models, APIs, SDKs, registries, and tests.

# Provider Protocol — Nexora

## Request Flow

1. Caller submits a `ProviderRequest` containing `requestId`, `correlationId`, `providerRequestId`, provider/model identity, caller scope, and normalized message payload.
2. Runtime resolves credentials internally and MUST NOT expose raw credentials in request or response payloads.
3. Provider completion or stream execution emits ordered events and terminal outcome after durable commit.
4. Response returns normalized output, usage accounting, status, version, and canonical error envelope when failed.

## Streaming Protocol

Streaming events MUST carry monotonically increasing sequence numbers plus a terminal marker. Socket closure or transport completion alone MUST NOT be interpreted as success. Resumable streams require an opaque `resumeToken`; unsupported resume capability MUST be declared explicitly.

## Error Handling

Rate limit, unavailability, timeout, invalid request, capability mismatch, and cancellation outcomes MUST map to canonical `NXR-*` errors.

## Cross-Layer Contract Rules

Protocol messages MUST map to [docs/api/Provider-API.md](../docs/api/Provider-API.md). Consumers MUST treat events as at-least-once, deduplicate by `(entityId, version, transition)`, and never infer success from transport completion alone.

## Canonical Error Mapping

| Operation | Canonical `NXR-*` codes |
|---|---|
| complete / stream | NXR-4003, NXR-4004, NXR-4005, NXR-4006, NXR-4007 |
| cancelRequest | NXR-4008, NXR-7007 |
