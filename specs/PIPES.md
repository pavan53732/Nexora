# Pipes — Multi-Instance Collaboration Specification — Nexora

> **Status: CANONICAL** for inter-instance discovery, pairing, transport, delegation, and broadcast behavior.
> This document owns how two or more running Nexora app instances discover, authenticate, connect, and coordinate work — same machine or across a LAN. It does NOT own the single-device agent loop (see [../architecture/AGENT_RUNTIME.md](../architecture/AGENT_RUNTIME.md)), intra-workspace multi-agent delegation (see [../architecture/MULTI_AGENT_SYSTEM.md](../architecture/MULTI_AGENT_SYSTEM.md)), or permission semantics (see [../security/PermissionModel.md](../security/PermissionModel.md)).
>
> Depends on: [../architecture/MULTI_AGENT_SYSTEM.md](../architecture/MULTI_AGENT_SYSTEM.md), [../security/PermissionModel.md](../security/PermissionModel.md), [../security/SandboxPolicy.md](../security/SandboxPolicy.md), [../state-machines/InstanceLifecycle.md](../state-machines/InstanceLifecycle.md).
> Referenced by: [../models/Instance.md](../models/Instance.md), [../architecture/MULTI_AGENT_SYSTEM.md](../architecture/MULTI_AGENT_SYSTEM.md) (§Cross-Instance Extension).
>
> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

---

## 1. Overview

Nexora instances can coordinate work across **process and device boundaries** via
*pipes* — authenticated, encrypted, workspace-scoped channels between Nexora app
instances. Pipes extend the existing intra-workspace multi-agent model
([MULTI_AGENT_SYSTEM.md](../architecture/MULTI_AGENT_SYSTEM.md) SA-1..SA-5) so that a
delegated sub-agent may execute on **another instance** — a second app process on the
same machine or a peer device on the LAN — while remaining under the same coordinator
control, security posture, and audit discipline as a local sub-agent.

What pipes are:

- **Instance-to-instance channels** — an instance registers once and exposes selected workspaces to trusted peer instances.
- **Zero-configuration discovery** — instances find each other automatically on the same LAN via mDNS/DNS-SD, and on the same machine via a local rendezvous directory.
- **A delegation transport** — a pipe carries task handoffs and results; it is not a shared filesystem, screen mirror, or remote shell.

What pipes are NOT:

- Not a network share or remote terminal (pipe messages carry typed protocol payloads, never raw command streams — TOOL-405 executes nothing by itself).
- Not an open listener for arbitrary clients (pairing is explicit, pinned, revocable, and permission-gated. Unknown scopes and unauthorized operations are denied. See [../security/PermissionModel.md](../security/PermissionModel.md) §Explicit Risk-Based Scope Defaults).
- Not a bypass of sandbox, permission, or evidence rules (every cross-instance delegation inherits SA-4 policies and FR-S016 autonomy gates).

## 2. Design Rules (aligned to existing architecture)

1. **Coordinator-extends, never forks.** Cross-instance delegation is SA-1..SA-5 with a transport boundary inserted. The coordinator role stays single (FR-AG-001); a remote sub-agent reports to the same Master Agent. No peer-to-peer agent calls (FR-AG-002 preserved: messages flow coordinator → pipe → remote coordinator → remote sub-agent, never agent → agent).
2. **No new trust domain without a gate.** Every pipe is workspace-scoped and profile-tagged (FR-P011): a pipe carries the delegating workspace's ID and provider profile tag; credentials never traverse a pipe (NFR-SEC-011/012 provider isolation extended — a delegated task needing a remote provider call uses the remote instance's own provider profiles, never the coordinator's keys).
3. **Deny-by-default, quarantine-in.** Incoming delegation payloads are untrusted context segments (FR-CM-006) and land in the receiving workspace's quarantine flow (FR-S015) when they carry files; acceptance requires the pipe acceptance mode to permit it (§6).
4. **Auditable end-to-end.** Every pipe event (discovery, pairing, connect, delegate, result, revoke, error) enters the append-only audit trail (FR-TL015) with a stable `pipeId`, `instanceId`, and `correlationId`.

## 3. Instance Identity & Pairing (FR-MI-004, FR-MI-008)

Each Nexora install generates an **instance identity** at first run:

| Field | Rule |
|-------|------|
| `instanceId` | UUIDv4, generated once, stored in global settings (never changes for the install) |
| `instanceName` | User-editable display name (default: device model) |
| `pipeKey` | Ed25519 keypair; private key in `SecureKeyStore` (hardware-backed where available), public key fingerprint shown during pairing |
| `capabilities` | Advertised set: `{appVersion, minContractVersion, workspaceIds exposed, tool category summary}` — never tool payloads or keys |

**Pairing** is the explicit, one-time act that turns a discovered instance into a trusted pipe endpoint:

1. Discovery returns a candidate (§4) with its public key fingerprint.
2. The user confirms the fingerprint on both ends (QR code scan where cameras are permitted, or 6-word confirmation code — both surfaces live in **Settings → Pipes**; per ADR-0006 there is no pipes chat tab or infrastructure screen).
3. Pairing record persisted (per remote `instanceId`): `{fingerprint, alias, allowedWorkspaces, acceptanceMode, pairedAt}`.
4. Revocation is one tap per pairing; revocation kills open pipes immediately (state machine: `Revoked`, terminal).

`instance:pair` and `instance:connect` are `ASK` by default; `instance:broadcast` is `DENY` by default (see [../security/PermissionModel.md](../security/PermissionModel.md) §Permission Scopes).

## 4. Discovery (FR-MI-001, FR-MI-003)

| Scope | Mechanism | Detail |
|-------|-----------|--------|
| **Same machine** | Rendezvous directory | Each instance registers a file `run/nexora-pipes/{instanceId}.json` in app-adjacent private storage (multi-process same-UID only). File contains the loopback endpoint + `pipeKey` fingerprint + capabilities. Watchers poll/inotify this directory. No network stack involved. |
| **LAN** | mDNS / DNS-SD | Service type `_nexorapipe._tcp.local`, TXT records carry `instanceId`, fingerprint, `minContractVersion`, and a nonce. Android `NsdManager`; no manual IP entry. Discovery is listener-only until pairing. |
| **Unreachable / offline** | Graceful absence | Discovery failure is not an error state; pipes UI shows "no peers found" and the capability degrades per FR-AS-008 (pipes simply unavailable, nothing breaks). |

Zero-configuration means: the user never types an address. Pairing confirmation (§3) is the only manual step, and it is deliberate, not incidental.

## 5. Pipe Transport (FR-MI-002, FR-MI-006)

- **Channel**: TLS 1.3 over TCP (LAN peers) or loopback + Unix-domain semantics (same machine). Mutual TLS using the pinned `pipeKey` certificates — no CA, no self-signed acceptance prompts.
- **Framing**: length-prefixed JSON envelopes carrying the canonical fields (`correlationId`, `pipeId`, `instanceId`, `workspaceId`, `version`, optional `CanonicalErrorEnvelope`).
- **Payload types** (closed set):
  1. `DelegateTask` — goal, acceptance criteria, constraints, evidence bundle refs, skills/tools required, report format (identical shape to FR-MA-002 handoff, plus `pipeId`).
  2. `TaskAccepted` / `TaskRejected` — remote admission decision with reason.
  3. `ProgressEvent` — SA-5 plan-vs-actual updates (throttled, ≥2 s apart).
  4. `ResultReport` — terminal report with evidence references (never raw file contents unless the receiving workspace's quarantine accepts them, §2 rule 3).
  5. `Heartbeat` — liveness (30 s interval; 3 missed = `Degraded`, 5 missed = `Disconnected`).
  6. `Revoke` / `Close` — teardown.
- **Replay/idempotency**: every payload carries a monotonically increasing `pipeSeq`; the receiver deduplicates by `(pipeId, pipeSeq)` (matches NFR-REL-012 exactly-once discipline).
- **Timeouts**: every request/response pair has a deadline (default 30 s connect, 120 s task-ack); no unbounded waits (AUTONOMY_STABILITY §9).
- **Size caps**: single payload ≤ 1 MB; larger artifacts are transferred as quarantined files with hashes, reassembled and scanned on receipt (FR-S015).

## 6. Cross-Instance Delegation (FR-MI-005)

Lifecycle of a remote delegation:

```
Coordinator (workspace W, instance A)
   │ planner picks remote capability (skill/tool absent locally)
   ▼
PipeManager.select(pipe)           — paired, Connected, workspace W exposed, policy allows
   ▼
DelegateTask ──pipe──> Remote coordinator (instance B)
   ▼
Remote admission control:
   acceptanceMode(W) ∈ {MANUAL, ASSISTED, AUTOPILOT}   (FR-S016 modes, per-pipe override)
   MANUAL    → user prompt on B (one tap) before spawn
   ASSISTED  → auto-accept low-risk, prompt on high-risk (risk score as FR-S016)
   AUTOPILOT → auto-accept within declared technical safety, resource, concurrency, and deadline limits; all actions remain audited. Provider cost or credit telemetry does not block a technically valid delegation.
   ▼
Remote sub-agent spawned in B's OWN sandbox (FR-S018) with B's provider profiles (§2 rule 2)
   ▼
SA-1..SA-5 unchanged: execute → verify → report (ProgressEvents streamed over pipe)
   ▼
ResultReport ──pipe──> Coordinator merges (dependency order, SA-3)
```

Hard rules:

- The remote instance **cannot see** the coordinator's workspace files, memory, or provider credentials. It receives the handoff context and produces artifacts; artifacts promote back through quarantine.
- The coordinator-side sub-agent record is a normal `Task` (TaskLifecycle applies) whose executor is remote; cancellation propagates over the pipe (`TaskCancelled` payload → remote kill with partial results preserved).
- If the pipe drops mid-task: coordinator marks the subtask `Blocked` (TaskLifecycle), heartbeats continue for the pipe timeout window, then the task escalates per FR-AS-003 (never a silent stop). Remote side checkpoints; on reconnect the task resumes from checkpoint (NFR-REL-002) or is reconciled from the replay log (FR-AS-007).

## 7. Broadcast Routing (FR-MI-007)

Broadcast is a coordinator-only operation for fan-out announcements (e.g., "workspace snapshot starting", "technical delegation limit reached — pause delegations"). Any referenced limit is a technical safety, resource, concurrency, or deadline control; provider cost or credit telemetry is never an automatic delegation gate:

- `pipe_broadcast` (TOOL-407) sends a typed `Broadcast` payload to all `Connected` pipes of the active workspace.
- Recipients treat broadcasts as **data, not instructions** (FR-CM-006 / RG-6): a broadcast can trigger a *declared, pre-registered* local handler (e.g., pause-delegations), never an arbitrary action embedded in the payload.
- `instance:broadcast` scope is `DENY` by default; enabling it requires an explicit workspace-level grant and is rate-limited (max 1/s, burst 5) to prevent bus floods (TM-020 analog).

## 8. Security & Isolation (FR-MI-008, FR-MI-009, NFR-SEC-014)

| Control | Rule |
|---------|------|
| Mutual authentication | Pinned `pipeKey` certificates both directions; no fallback to unauthenticated sessions |
| Encryption | TLS 1.3 mandatory; plaintext pipes impossible by construction (no `ws://`-style downgrade) |
| Workspace scoping | A pipe is bound to exactly one exposed workspace; cross-workspace routing is rejected (`NXR-1002` variant) |
| Credential firewall | Provider keys, `SecureKeyStore` aliases, and user secrets are never serializable into pipe payloads (enforced by DLP scan on outbound bodies, NFR-SEC-013 extended to pipes) |
| Untrusted payloads | All inbound payloads wrapped as untrusted context segments (FR-CM-006); tool calls inside payloads validated against the registry before execution (TM-025) |
| Auto-approval classifier | The optional TFLite classifier (PermissionModel §Auto-Approval Classifier) can `DENY` a pipe delegation even when the acceptance mode would allow it |
| Egress confinement | Pipe sockets connect only to the paired endpoint (NFR-SEC-012 network confinement applied to pipe clients); discovery sockets are mDNS-only |
| Audit | Every pipe event → `permission_audit_log`-adjacent pipe audit stream (FR-TL015). The canonical `permission_audit_log` is non-evictable; a derived 90-day operational view may be surfaced for routine review but MUST NOT delete/mutate the source rows (see `security/PermissionModel.md` §Permission Audit Trail) |

## 9. Failure Handling (FR-MI-009)

| Failure | Behavior |
|---------|----------|
| Discovery finds nothing | Capability absent, not an error; pipes UI shows empty state |
| Pairing fingerprint mismatch | Pairing aborted, `NXR-6009`-class error, audit `CRITICAL` |
| Pipe connect timeout | `Degraded`; bounded retry (3, exponential backoff, NFR-REL-003); then `Disconnected` |
| Mid-task disconnect | Subtask `Blocked` → escalate per FR-AS-003; remote checkpoint resume or replay reconciliation (§6) |
| Revoked mid-task | Immediate pipe close; remote agent cancelled gracefully with partial results |
| Malformed/forged payload | Rejected before parse (schema + signature), audit `CRITICAL`, pipe downgraded to `Degraded`; 3 violations → auto-`Revoked` |
| Version incompatibility | `minContractVersion` handshake fails → no pipe; clear user notice (NEXORA version guidance) |

## 10. User-Facing Surfaces (FR-MI-010)

Per ADR-0006, pipes have **no primary screen and no chat tab**. The user interacts through:

- **Settings → Pipes**: paired instances list, pair new instance (QR/6-word code), acceptance mode per pipe, revoke, discovery on/off toggle.
- **Agent activity feed** (FR-U005): cross-instance delegations render as ordinary tool-call/activity cards with a pipe badge (`pipe → <instanceName>`); progress, approval prompts, and results surface in chat exactly like local sub-agents.
- **Notifications** (specs/BACKGROUND_EXECUTION.md §4): pairing requests and remote approval gates use the existing `agent_approval` channel.

There are no slash commands and no `/pipes` panel; the chat remains the single primary interaction surface (FR-U011).

## 11. Tools (registered in registry/TOOLS.md)

| ID | Tool | Description | Permissions | Phase |
|----|------|-------------|-------------|-------|
| TOOL-405 | `pipe_list` | List discovered, paired, and connected instances for the active workspace | `instance:connect` (read) | 7 |
| TOOL-406 | `pipe_connect` | Open (or attach) a pipe to a paired instance | `instance:connect` | 7 |
| TOOL-407 | `pipe_broadcast` | Broadcast a typed message to connected pipes of the workspace | `instance:broadcast` | 7 |
| TOOL-408 | `pipe_delegate` | Delegate a task to a remote instance through a pipe | `instance:delegate` + `agent:create` (ASK defaults preserved) | 7 |

`pipe_delegate` produces a standard `DelegateTask` payload and returns through the standard `ToolResult` pipeline; the delegated task is a first-class `Task` on both sides (TaskLifecycle on both, correlated by `correlationId` + `pipeId`).

## 12. Phase Mapping

| Phase | Deliverable |
|-------|-------------|
| 5 | Pipe transport hardening design; DLP scan hook into egress engine |
| 7 | Instance identity, pairing, same-machine + LAN discovery, cross-instance delegation (SA-1..SA-5 over pipes), broadcast routing, Settings → Pipes surface, TOOL-405..408 |
| 8 | Pipe-provided marketplace capabilities (remote plugin/agents advertised via capability TXT records) |

## 13. References

- [../architecture/MULTI_AGENT_SYSTEM.md](../architecture/MULTI_AGENT_SYSTEM.md) — SA-1..SA-5 contract this spec extends
- [../state-machines/InstanceLifecycle.md](../state-machines/InstanceLifecycle.md) — canonical instance/pipe state machine
- [../models/Instance.md](../models/Instance.md) — Instance and Pipe domain models
- [../security/PermissionModel.md](../security/PermissionModel.md) — `instance:*` scopes
- [../security/SandboxPolicy.md](../security/SandboxPolicy.md) — containment applied to pipe payloads
- [../specs/BACKGROUND_EXECUTION.md](../specs/BACKGROUND_EXECUTION.md) — notification channels
- [../specs/AUTONOMY_STABILITY.md](../specs/AUTONOMY_STABILITY.md) — degradation ladder, timeout discipline
- [../docs/DECISION_LOG.md](../docs/DECISION_LOG.md) — DL-030
