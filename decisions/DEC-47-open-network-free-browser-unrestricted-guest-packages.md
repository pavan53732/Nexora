# DEC-47 — Open Network, Free Browser, Unrestricted Guest Packages

- **Status:** Accepted
- **Date:** 2026-08-21
- **Deciders:** Architecture Owner / Product Owner
- **Scope:** Documentation contract only; implementation and executed evidence remain separately downstream.

## Decision

### 1. Open network defaults within existing host mediation

The host-side workspace egress proxy remains the sole guest-egress mediation and audit point. Guest processes MUST NOT create direct outbound sockets, and inbound listening sockets remain prohibited.

In an `AUTOPILOT` workspace, the existing `network:http` and `network:websocket` scopes use a deterministic mode-conditioned default of `ALLOW` for public, routable destinations when no higher-priority policy restricts the operation. No per-workspace Allowed-Domains enrollment is required for those public destinations. HTTP port 80 is permitted; HTTPS-only is not an active requirement for this mode-conditioned default.

`ASSISTED` retains the existing opt-in grant behavior. Other existing PermissionModel resolution, higher-priority restrictions, task windows, resource limits, audit, cancellation, and failure rules remain authoritative. Every request remains proxied and logged under `FR-S014`.

Outbound DLP is narrowed from full-body policy scanning to deterministic secret-material blocking. Configured credentials, API keys, and `SecureKeyStore` contents MUST NOT be transmitted to any endpoint except their declared service. This is a transmission boundary, not a general content classifier or AI authority.

### 2. Free public browser navigation

`browser_open` MAY load any publicly routable URL without a domain allowlist check. Image, font, and third-party-resource blocking become per-workspace preferences with default off. Token, bandwidth, and related cost information is informational only and never a gate under DEC-45.

The existing security floors remain unchanged: localhost, loopback, and app-private endpoints remain hard-blocked; all WebView traffic remains host-mediated through the workspace egress proxy; page content remains labeled and wrapped as untrusted data under `FR-S015`; browser operations retain existing Tool authorization, correlation, timeout, cancellation, idempotency, unknown-completion, audit, and evidence contracts.

### 3. Narrow sensitive-domain action floor

The existing sensitive-domain blocklist no longer denies navigation or read-only extraction. Read-only research is permitted on any domain subject to the existing network, permission, sandbox, and untrusted-content contracts.

On domains matching the existing sensitive classes (`*.bank*`, `*.pay*`, `*.crypto*`, `*.insurance*`), the blocklist denies exactly these action classes:

- credential entry; and
- transaction execution, including payment, transfer, trade, checkout, or policy purchase.

Navigation, reading, extraction, and other non-transactional observation are not denied solely because of the domain. Credential and transaction denials remain audited, user-visible, fail-closed, and governed by existing PermissionModel/Tool error semantics. This decision narrows the active boundary previously recorded in DL-023; it does not create a new state, error, permission scope, or browser authority.

### 4. Unrestricted sandbox guest package installation

Inside the existing sandbox guest, `pip`, `npm`, `gradle`/`maven`, `apt`, and equivalent guest package managers MAY install from any reachable registry without pre-approval. Existing process, storage, network, workspace, rootfs/overlay-integrity, quarantine, audit, and Android resource quotas remain active.

Guest package installation is not host-JVM Plugin installation. Host-JVM Plugins remain subject to manifest declaration, user review, Plugin lifecycle, integrity, capability, and cleanup contracts because they execute native-level code in the app process.

## Creator-authorized Option B clarification

The creator-owned statement that network access is denied unless authorized is interpreted as an effective-policy authorization requirement, not as a global denial of network access. Under DEC-47, an `AUTOPILOT` workspace’s deterministic public-destination `network:http` and `network:websocket` defaults are the applicable authorization for public, routable destinations when no higher-priority restriction applies. `ASSISTED` retains opt-in authorization. Loopback, localhost, app-private endpoints, inbound listeners, secret-material transmission outside declared service boundaries, and sensitive-domain credential-entry or transaction-execution floors remain restricted as stated above. The creator-owned product design document remains unchanged.

## Unchanged boundaries

PermissionModel resolution order, explicit ASK transactions for operations that remain ASK-scoped, DENY behavior, unknown-completion semantics, lifecycle ownership, audit retention, evidence conventions, cloud-only AI scope, untrusted page-content handling, no inbound sockets, loopback/app-private SSRF floors, and host-plugin trust separation remain unchanged.

This decision creates no new state, error code, identity, lifecycle, authority, AI classifier, Policy Engine, permission scope, or implementation mechanism. It does not authorize source code or claim `TESTED` or `EXECUTED EVIDENCE`.

## Required propagation

The active owners and derived projections MUST align this decision in `security/SandboxPolicy.md`, `specs/BROWSER.md`, `docs/SANDBOX_DEPTH.md`, `requirements/FR.md`, `requirements/NFR.md` where the DLP contract is defined, `security/PermissionModel.md`, `architecture/SECURITY_MODEL.md`, `docs/SYSTEM_DESIGN.md` where the default is projected, `registry/TOOLS.md`, `specs/FULL_ENVIRONMENT.md`, `testing/cases/SecurityTestCases.md`, `testing/cases/E2ETestCases.md`, `docs/TRACEABILITY.md`, `docs/REQUIREMENT_COVERAGE_LEDGER.md`, `docs/DOCUMENTATION_COMPLETENESS_INVENTORY.md`, `docs/CANONICAL_SOURCES.md`, and `docs/DECISION_LOG.md`. Historical records remain historical and are not rewritten except for a new decision-log entry.
