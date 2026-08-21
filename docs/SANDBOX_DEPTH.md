> **Status: SUPPORTING** for sandbox depth and implementation roadmap. This document explains focused usage and behavior but does not own the canonical definition. The canonical source is [../architecture/SANDBOX.md](../architecture/SANDBOX.md), [../security/SandboxPolicy.md](../security/SandboxPolicy.md).
>
> Depends on: [../architecture/SANDBOX.md](../architecture/SANDBOX.md), [../security/SandboxPolicy.md](../security/SandboxPolicy.md).

# Sandbox Depth & Autonomy Roadmap — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)
> See also [architecture/SANDBOX.md](../architecture/SANDBOX.md) · [security/SandboxPolicy.md](../security/SandboxPolicy.md) · [specs/TERMINAL.md](../specs/TERMINAL.md) · [docs/adr/ADR-0006-Agent-First-Interaction-Model.md](./adr/ADR-0006-Agent-First-Interaction-Model.md)

---

## 1. Purpose

Nexora supports exactly one guest environment: the bundled Full Environment defined in [../specs/FULL_ENVIRONMENT.md](../specs/FULL_ENVIRONMENT.md). The roadmap below describes sandbox capabilities and phases, not alternative environment installation tiers.

The sandbox is where agents *live*. Baseline isolation (paths, processes, quotas,
network, permissions) is specified in `security/SandboxPolicy.md`. This document
extends the sandbox toward **complete autonomy** — not just "safe" but
"safe *and* self-sufficient": agents that can observe, manage, snapshot, and repair
their own environment, with enforcement that scales from fully manual to fully
autopilot.

Each capability is tiered by phase. New FRs are FR-S011…FR-S018; new NFRs are
NFR-SEC-013 / NFR-REL-010; new tools are TOOL-387…TOOL-393.

---

## 2. Sandbox autonomy foundations — Core Depth (Phase 3)

### 2.1 Sandbox Telemetry — agents observe themselves (FR-S011)
- **What:** Tools for the agent to query its own environment: running processes, disk
  usage, env vars, quotas, network rules, recent sandbox events.
- **Tools:** `sandbox_info` (TOOL-387), `obs_metrics`, `terminal_list_processes`.
- **Why:** An agent that cannot see its own resource state cannot self-correct (e.g.,
  "disk at 90% — clean temp before continuing"). Autonomy requires observability.
- **Enforcement:** read-only; per-workspace scope; same audit rules as other tools.

### 2.2 Sandbox Lifecycle Autonomy — agents manage environments (FR-S012)
- **What:** Agents can create **ephemeral sandboxes** for one-off tasks (temporary
  workspaces), **reset** a workspace to a clean state, and apply **sandbox templates**
  (pre-baked environment profiles: `python3 + pip`, `node + npm`, `git + sqlite`,
  `browser`, combinations).
- **Tools:** `sandbox_reset` (TOOL-388), `sandbox_templates` (TOOL-391),
  `workspace_create/archive/delete`.
- **Why:** A research task should not run in a coding workspace's environment; an
  agent should be able to spawn a disposable environment, do the work, and discard it.
- **Enforcement:** creating/resetting a sandbox requires `sandbox:write` +
  `workspace:*` permissions; reset is destructive → `ASK` by default.

### 2.3 Workspace Snapshots & Rollback — sandbox time travel (FR-S013)
- **What:** Full-workspace snapshots (content-addressed, compressed) taken before
  heavy agent runs; **restore to any snapshot** atomically. Complements per-file
  history (FR-M012) at the whole-workspace level.
- **Tools:** `sandbox_snapshot` (TOOL-389), `sandbox_restore` (TOOL-390).
- **Why:** "Complete autonomy" needs a safety net: if an agent wrecks a workspace,
  the user (or the agent itself) rolls back to the last good snapshot in one action.
- **Enforcement:** snapshots count toward disk quota (default keep last 5 per
  workspace); restore is atomic (write-new + swap) and is an audited, `ASK`-gated,
  irreversible-until-next-snapshot operation. NFR-REL-010.

### 2.4 Network Egress Policy Engine — host-mediated, mode-conditioned, fail-closed (FR-S014)
- **What:** All sandbox network traffic is **enforced at the boundary**, not merely
  observed. Nexora runs a dedicated **egress proxy** (host-side, not a guest
  `VPNService`) bound to `127.0.0.1:{perWorkspacePort}`. The sandbox is configured so
  guest processes **cannot open direct outbound sockets**: proot is launched with an
  explicit `http_proxy`/`https_proxy`/`all_proxy` pointing at the workspace proxy, and
  the Android `VpnService`/packet-filter exclusion is used only to *block* raw guest
  sockets, never to tunnel them. Every guest connection (curl, wget, pip, npm, Python,
  Node, apt, the WebView bridge) is forced through that proxy.
- **Proxy responsibilities:** apply the effective mode-conditioned `network:http` /
  `network:websocket` admission; in `AUTOPILOT`, public routable destinations do not
  require per-workspace Allowed-Domains enrollment, while `ASSISTED` retains opt-in
  grant behavior; enforce per-task **time windows** (network enabled only while a task
  runs); write an egress log (host, bytes, duration, matched rule); and block configured
  secret material from unauthorized endpoints. General full-body policy scanning is not
  required under DEC-47.
- **Encrypted egress:** the proxy may terminate guest TLS using a workspace-scoped CA
  whose private key lives in `SecureKeyStore` and is *never* exported to the guest when
  needed to block configured secret material. Guest traffic carrying a pinned/foreign
  certificate (or refusing the workspace CA) is **denied** — there is no silent bypass
  path. This is the only approved egress route; direct socket creation from guest
  processes fails closed.
- **WebView bridge:** `specs/BROWSER.md` routes through the *same* proxy via a forced
  host proxy configuration; the WebView does not perform direct guest networking.
- **Tool:** `sandbox_network_rules` (TOOL-392).
- **Why:** DEC-47 preserves enforced, time-boxed, host-mediated egress so an
  autonomous agent can browse/API-call without direct guest sockets. `AUTOPILOT`
  public-destination admission is broader, but loopback/app-private floors, quotas,
  audit, secret-material blocking, and bypass denial remain active.
- **Enforcement:** effective mode-conditioned network admission; every egress event
  enters the audit trail (FR-TL015); configured secret material is blocked from
  unauthorized endpoints; socket-level enforcement remains validated by `SEC-NET-001`
  (proxy admission + direct-socket denial + secret-material protection).

### 2.5 Quarantine & Content Scanning (FR-S015)
- **What:** Files fetched from the network (downloads, browser plugin output) land in
  a per-workspace **quarantine zone** first; a scanner checks content hash against a
  known-bad list, MIME/extension mismatch, size, and (where feasible) structure.
  **Promotion** into the live workspace requires a permission grant (user or policy).
- **Tool:** `sandbox_quarantine_review` (TOOL-393).
- **Why:** The biggest autonomy risk is the agent ingesting malicious or untrusted
  content (prompt injection, malware). Quarantine makes ingestion an explicit,
  auditable event instead of an implicit one.

### 2.6 Per-Workspace Encryption at Rest (FR-S017)
- **What:** Workspace storage encrypted with a Keystore-backed per-workspace key
  (AES-256-GCM via Tink or Android Keystore); keys never leave secure hardware;
  backup/export archives are encrypted too.
- **Why:** Baseline stores data in app-private storage; depth protects the sandbox
  contents themselves (device compromise, adb backup, forensic extraction).
- **Enforcement:** NFR-SEC-003/010 already mandate Keystore for secrets; this extends
  encryption to workspace payloads. Performance: streaming cipher, negligible
  overhead; measured in PERFORMANCE_BUDGET.

---

## 3. Full Environment — Autonomy Depth (Phases 4–6)

### 3.1 Adaptive Approval / Autonomy Modes (FR-S016)
- **What:** Three automatically selected autonomy levels from the existing scoped trust thresholds:
  - **Manual** (`0–39`) — existing `ASK`/high-risk approval and explicit user-guidance paths remain authoritative; known low-risk scopes with a declared `ALLOW` default do not prompt solely because the mode is Manual.
  - **Assisted** (`40–74`) — low-risk actions may proceed under existing category defaults and gates; higher-risk actions use existing `ASK`/DENY and approval rules.
  - **Autopilot** (`75–100`) — agent executes within declared task budgets and existing safety, permission, sandbox, resource, concurrency, deadline, and evidence gates; no gate is bypassed.
- The user does not confirm the mode per session or per action. An existing user override may only downgrade the effective mode and takes effect immediately; every decision remains audited.
- **Why:** Approval fatigue is reduced by deterministic low-risk defaults while high-risk gates, audit, snapshots, and existing permission ownership remain intact.
- **Enforcement:** trust learning automatically selects the effective mode; existing PermissionModel category defaults and higher-precedence overrides remain authoritative. Android degraded mode may force `Manual` independently of trust.

### 3.2 Parallel Per-Agent Sandboxes (FR-S018)
- **What:** Delegated sub-agents (multi-agent orchestration) run in **separate sandbox
  instances** — files, env, quotas, and network rules scoped per sub-agent, not shared
  with the coordinator; results promoted via artifacts, never raw access.
- **Why:** True collaboration without cross-contamination; a compromised sub-agent
  cannot read the coordinator's or siblings' state.
- **Enforcement:** sub-sandboxes inherit workspace limits split evenly; each sub-agent gets
  an isolated process/network/quota boundary (FR-S018) **plus a private copy-on-write
  overlay** over the shared workspace base. Files are **not directly shared** between
  sub-agents: a sub-agent reads the shared base snapshot and writes only into its overlay;
  completed outputs are **promoted as artifacts** to the shared workspace (SA-5), never via
  raw cross-sandbox access. Shared-file mutations take a per-file write-lock (SA-3).
  Artifact promotion is permissioned (extend PermissionModel with `artifact:read` scope in
  Phase 5). See `architecture/MULTI_AGENT_SYSTEM.md` §File Sharing & Isolation Model.

### 3.3 Prompt-Injection Containment
- **What:** Untrusted content (web pages, downloaded files, user-provided docs) is
  wrapped in **labeled context segments** and injected as *data*, never as
  instructions; tool calls from untrusted content are validated against the tool
  registry (extends TM-025); outbound secret-material blocking remains active under
  NFR-SEC-013, while page content remains untrusted data.
- **Why:** Autonomous agents that browse the web *will* meet hostile pages. The
  sandbox must guarantee content cannot hijack the agent.
- **Enforcement:** context labeling at the Context Builder; egress scanning at the
  proxy (2.4); periodic adversarial tests in testing/SecurityTests.md.

### 3.4 Resource Economy & Self-Healing
- **What:** Per-task budgets (CPU, disk, network, tokens); automatic temp cleanup;
  LRU eviction; **watchdog** that kills stuck processes; OOM containment; sandbox
  auto-restart with checkpoint resume on crash.
- **Why:** Long-running autonomous agents will leak or hang; the sandbox must
  self-heal without the user noticing.
- **Enforcement:** extends SandboxPolicy §4–6; watchdog events enter observability;
  auto-restart uses checkpoint recovery (NFR-REL-001/002).

### 3.5 Checkpoint Integrity & Anti-Drift
- **What:** Sandbox/workspace state hash-verified on every resume (checkpoint
  integrity); detect tampering, rollback, or drift; quarantine on mismatch.
- **Why:** An autonomous sandbox that resumes from a *modified* checkpoint is
  untrustworthy. Integrity makes resume safe (NFR-REL-010).

---

## 4. Future sandbox capabilities (Phases 7–8+, not supported environment tiers)

| Capability | Description | License/Impact |
|-----------|-------------|----------------|
| **WASM micro-sandboxes** | Run untrusted plugins/scripts as WASM modules via **wasmi** (interpreter, Apache-2.0) — memory-safe, no JIT | ~1–2 MB/ABI; aligns with [ENVIRONMENT_SETUP §9.6](./ENVIRONMENT_SETUP.md) |
| **IsolatedProcess services** | Risky one-off workloads (parsing untrusted files) in `android:isolatedProcess` — true separate UID, no permissions | 0 MB; API 34 OK |
| **Sandbox template marketplace** | Environment-as-code templates shared via plugins/Nexora Hub (Phase 8) | plugin-sized |
| **Offline workspace continuity** | Cloud-provider outage degrades to cached/non-inference workspace operations and read-only access; no local AI inference or model files (NFR-REL-006, DEC-41) | workspace/cache storage only |
| **Cross-workspace data governance** | DLP on export/import: egress scanning for secrets/keys; export manifest with checksums; quarantine of imported archives | — |

---

## 5. Summary Matrix

| # | Capability | Phase | Type | FR | Tools |
|---|-----------|-------|------|----|-------|
| 1 | Sandbox telemetry | 3 | Core | FR-S011 | TOOL-387 |
| 2 | Sandbox lifecycle autonomy + templates | 3 | Core | FR-S012 | TOOL-388, TOOL-391 |
| 3 | Workspace snapshots & rollback | 4 | Core | FR-S013 | TOOL-389, TOOL-390 |
| 4 | Network egress policy + DLP | 3 | Core | FR-S014 | TOOL-392 |
| 5 | Quarantine & content scanning | 3 | Core | FR-S015 | TOOL-393 |
| 6 | Encryption at rest | 4 | Core | FR-S017 | — |
| 7 | Adaptive approval / autonomy modes | 4 | Autonomy | FR-S016 | — |
| 8 | Per-agent sandboxes | 5 | Autonomy | FR-S018 | — |
| 9 | Prompt-injection containment | 4 | Autonomy | (extends TM-025) | — |
| 10 | Resource economy & self-healing | 4 | Autonomy | (extends FR-S003) | — |
| 11 | Checkpoint integrity | 4 | Autonomy | (extends NFR-REL-002) | — |
| 12 | WASM micro-sandboxes | 7+ | Advanced | — | — |
| 13 | IsolatedProcess services | 7+ | Advanced | — | — |
| 14 | Template marketplace | 8 | Advanced | — | — |
| 15 | Offline workspace continuity | 7+ | Advanced | NFR-REL-006 | — |
| 16 | Export data governance | 8 | Advanced | — | — |

## 6. Phase Mapping

- **Phase 3 (sandbox autonomy foundations):** FR-S011/012/014/015 + FR-S013 interfaces; telemetry, egress
  proxy, quarantine, lifecycle tools; encryption design.
- **Phase 4 (Full Environment start):** FR-S013 full snapshots; FR-S016 autonomy modes;
  FR-S017 encryption; prompt-injection containment; watchdog/self-healing.
- **Phase 5 (Full Environment finish):** FR-S018 per-agent sandboxes; checkpoint integrity.
- **Phase 7–8 (future sandbox capabilities; not alternative environment tiers):** WASM micro-sandboxes, isolatedProcess, template
  marketplace, offline workspace continuity, export governance.


### 2.7 Bundled Rootfs & Full Environment (FR-S019…S028)

- **What:** Nexora uses a single bundled Full Environment based on Debian-slim with glibc and `apt`, extracted from APK assets and executed via proot.
- **Why:** A single real Linux environment improves reliability for agent execution, standard command behavior, and Python/Node package compatibility.
- **How:** Rootfs is stored as `assets/rootfs/debian-slim-{arch}.tar.xz`, stream-extracted to app-private storage, verified against `manifest.json`, and exposed through a read-only base plus per-workspace writable overlay.
- **Enforcement:** Storage quotas include overlays; environment reset is audited; integrity checks run on startup; unsupported devices are surfaced clearly.

## 3.5 Full Environment Advanced Capabilities

| Capability | Description | Phase |
|---|---|---:|
| **Environment templates** | Pre-configured overlays for data science, web development, and similar workloads | 5 |
| **Cross-architecture emulation** | QEMU user-mode for selected foreign-architecture binaries | 6 |
| **Rootfs delta updates** | Incremental updates to the base rootfs | 6 |
| **Custom rootfs builds** | User-built rootfs using the Nexora manifest format | 7 |

| 17 | Bundled Full Environment per workspace | 3 | Core | FR-S019 | — |
| 18 | Bundled Debian-slim rootfs | 3 | Core | FR-S020 | — |
| 19 | proot execution | 3 | Core | FR-S021 | — |
| 20 | glibc binary wheel support | 3 | Core | FR-S022 | — |
| 21 | Rootfs overlay | 3 | Core | FR-S023 | — |
| 22 | Rootfs cache management | 4 | Core | FR-S024 | — |
| 23 | Environment templates | 5 | Advanced | FR-S025 | — |
| 24 | Cross-architecture support | 5 | Advanced | FR-S026 | — |
| 25 | Offline package cache | 4 | Advanced | FR-S028 | — |
