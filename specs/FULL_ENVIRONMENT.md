> **Status: CANONICAL** for Full Environment (Debian-slim rootfs) behavior.
> This document owns the on-demand rootfs specification, provisioning lifecycle,
> and guest binary compatibility. It does NOT own sandbox subsystem design
> (see [../architecture/SANDBOX.md](../architecture/SANDBOX.md)) or security policy
> (see [../security/SandboxPolicy.md](../security/SandboxPolicy.md)).
>
> Depends on: [../architecture/SANDBOX.md](../architecture/SANDBOX.md), [../security/SandboxPolicy.md](../security/SandboxPolicy.md).
> Referenced by: [../docs/ENVIRONMENT_SETUP.md](../docs/ENVIRONMENT_SETUP.md), [../docs/PERFORMANCE_BUDGET.md](../docs/PERFORMANCE_BUDGET.md).

# Full Environment Specification — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See also [../architecture/SANDBOX.md](../architecture/SANDBOX.md) | [../docs/ENVIRONMENT_SETUP.md](../docs/ENVIRONMENT_SETUP.md)

---

## 1. Overview

Nexora uses a single sandbox environment model: a bundled **Full Environment** based on a Debian-slim rootfs packaged inside the APK. This is the primary and only supported execution environment for autonomous agents, providing glibc compatibility, `apt` package management, and broad compatibility with Python and Node ecosystems.

| Environment | Size | C Library | Package Manager | Bundled in APK | Default |
|---|---|---|---|---|---|
| **Full Environment** | **~50–70 MB compressed** | **glibc** | **`apt` (Debian)** | **Yes** | **Yes** |

The architecture-specific delivery-size policy is governed by DEC-38. The bundled Full Environment remains the selected execution environment; size gates are measured on the ABI-specific delivered AAB/APK artifact rather than an aggregate multi-ABI package.

## 2. Purpose

The Full Environment enables a real Linux userland inside Nexora so agents can execute standard commands, install packages, run native tooling, and use Python/npm workflows with high compatibility.

### Why this is the only supported model

- Agents are far more reliable when the environment matches standard Linux expectations.
- glibc compatibility improves success rates for common pip binary wheels and native toolchains.
- Bundling the rootfs inside the APK avoids a separate installation step and keeps core capabilities available offline after app install.
- A single environment reduces architectural complexity, documentation drift, QA surface area, and support burden.

## 3. Specifications

- **Base**: Debian 12 (Bookworm) slim variant
- **Size**: ~50–70 MB compressed (xz), ~180–220 MB extracted
- **C library**: glibc 2.36+
- **Package manager**: `apt`, `apt-get`, `dpkg`
- **Shell**: `bash` (default), `dash` (minimal)
- **Pre-installed**: `python3`, `python3-pip`, `python3-venv`, `nodejs`, `npm`, `git`, `curl`, `wget`, `ca-certificates`, `build-essential` (meta)

## 4. Bundling Architecture

```text
APK assets/
├── rootfs/
│   ├── debian-slim-arm64.tar.xz
│   ├── debian-slim-x86_64.tar.xz
│   └── manifest.json
├── proot/
│   ├── proot-arm64
│   └── proot-x86_64
└── licenses/
    └── debian-slim-LICENSE
```

The rootfs is bundled as an APK asset rather than downloaded after installation. On first run, Nexora selects the matching architecture asset, verifies it, and extracts it into app-private storage.

## 5. Extraction Lifecycle

| Phase | Action | Storage Location |
|---|---|---|
| First Launch | Detect architecture, select the correct tar.xz, stream-extract to app-private storage | `/data/data/com.nexora.app/rootfs/` |
| Verification | Validate checksums and signatures from the bundled manifest | — |
| Mount | proot binds `/` to extracted rootfs and workspace files into `/workspace` | Runtime only |
| Execution | Shell commands run inside the proot namespace | — |
| Cache | Extracted rootfs persists across restarts | App-private storage |
| Reset | User can wipe and re-extract the environment from bundled APK assets | — |
| Update | New APK version ships an updated rootfs asset | — |

## 6. proot Execution Model

```text
Android Kernel (unmodified)
└── Nexora App Process (UID: app_123)
    └── proot (static binary, no root required)
        └── Debian-slim rootfs
            ├── /usr/bin/python3
            ├── /usr/bin/apt
            ├── /usr/bin/node
            └── /workspace
```

### Key properties

- No root required.
- No kernel modules required.
- Workspace files are bind-mounted into `/workspace`.
- Network policy and egress controls still apply at the app level.

## 7. Compatibility

| Ecosystem | Support |
|---|---|
| **PyPI (pip)** | Binary-wheel-friendly glibc environment for common Linux ARM64/x86_64 packages |
| **npm** | Native modules and standard Node workflows supported through Debian userland |
| **Cargo (Rust)** | Standard Linux GNU targets are feasible inside the environment |
| **Go** | Standard Linux builds supported |
| **System packages** | `apt`/`dpkg` available for Debian packages |

## 8. Workspace Integration

Each workspace mounts the same read-only base rootfs with a private writable overlay for workspace-specific state.

```text
/data/data/com.nexora.app/
├── rootfs/                         # Shared read-only Debian base
└── sandbox/
    └── workspaces/
        └── {workspace-id}/
            ├── files/              # Workspace files and virtual filesystem
            ├── rootfs-overlay/     # Private writable layer
            │   ├── tmp/
            │   ├── var/cache/apt/
            │   ├── usr/local/
            │   └── home/agent/
            └── env/                # Environment config
```

Writes go to the workspace overlay; reads fall through to the shared base. This keeps the bundled base immutable while allowing per-workspace customization.

## 9. Package and Runtime Flows

### Python

```bash
python3 --version
pip3 --version
python3 -m venv /workspace/.venv
source /workspace/.venv/bin/activate
pip install numpy pandas requests
```

### Node.js

```bash
node --version
npm --version
cd /workspace
npm init -y
npm install express lodash
```

### apt

```bash
apt update
apt install -y jq ffmpeg
```

Package downloads and installed artifacts count toward workspace quota. Package cache management should minimize retained archive size where possible.

## 10. Performance Characteristics

| Metric | Target |
|---|---|
| First extraction | 3–8 seconds |
| Warm start | < 200 ms |
| Memory overhead | ~80 MB |
| Disk footprint | 50 MB + overlay per workspace |
| `pip install numpy` | 10–20 seconds under favorable network/cache conditions |

## 11. Security Model

### Rootfs Integrity

- SHA-256 checksums for bundled assets in `manifest.json`
- Signature verification with Nexora release key
- Re-extraction on integrity mismatch
- Read-only base rootfs with writable overlay only

### Isolation

- proot runs as the app UID without privilege escalation
- Android platform restrictions still apply
- Egress filtering and policy enforcement remain active

### License Compliance

The bundled Debian rootfs contains OSS components with license obligations. Nexora must ship attribution and source-offer information with the APK and provide an in-app OSS licenses view before store distribution.

## 5A. Android Environment Diagnostics and Repair Boundary (ADR-0010)

Before a guest process or environment-dependent background operation begins, the existing
Full Environment, Sandbox, Storage, Security, and Background Runtime owners MUST be able
to report the applicable diagnostic inputs: device ABI and Android compatibility, bundled
asset manifest/checksum/signature, extraction and mount readiness, app-private storage and
workspace quota availability, base-rootfs and overlay integrity, proot/guest entrypoint
readiness, and the applicable permission, network, battery, and scheduling constraints.
The diagnostic result is evidence and observability data; it is not a new environment lifecycle or authority. For environment-dependent work, the report MUST preserve the applicable existing `workspaceId`, `taskId`, `executionId`, `agentId`, `correlationId`, checkpoint/version, and evidence references, and MUST classify each diagnostic input as verified, failed, unavailable, or unknown from observed conditions. It MUST NOT infer mount, storage, permission, scheduling, or environment health from process presence, elapsed time, prior success, or provider confidence.

Repair MAY use only the existing verified reset/re-extraction, checkpoint, retry,
resource/degradation, user-guidance, or terminal failure paths owned by those subsystems.
Repair MUST preserve the last known-good rootfs, overlay, workspace data, checkpoint and
evidence references until the replacement asset or repaired condition passes the existing
integrity and permission checks. It MUST fail closed when integrity, storage, sandbox,
permission, or Android scheduling prerequisites cannot be established, and it MUST report
the existing non-success or degraded disposition rather than claiming a healthy
execution environment.

This boundary covers Android-relevant environment behavior only. It does not authorize
Node/Rust/desktop/web tooling as a product target, local AI/model inference, unrestricted
host access, a repair manager, a new environment identity, a new Workspace/Task/Execution
state, or a new recovery authority. `architecture/SANDBOX.md`, `security/SandboxPolicy.md`,
`specs/BACKGROUND_EXECUTION.md`, and the existing lifecycle/error owners remain
authoritative for their respective decisions.

## 6. W^X Compatibility (`targetSdk=34` current baseline)

Nexora uses `targetSdk=34` for the current Android build baseline under DEC-37. Devices running newer Android releases may still enforce newer W^X and foreground-execution behavior; those runtime compatibility rules do not change the current target SDK. Android 10+ enforces W^X
(write-xor-execute) via SELinux and seccomp — no memory page can be both writable
and executable. This breaks programs that do JIT compilation (e.g., Node.js V8).

Nexora handles this **without lowering `targetSdk`**:

| Technique | What it does | Programs affected |
|-----------|-------------|-------------------|
| **proot seccomp-bpf filtering** | Intercepts `mmap`/`mprotect` from guest binaries and remaps pages safely | All guest binaries |
| **Node.js `--jitless`** | Disables V8 JIT; pure interpreter mode (enforced globally via `NODE_OPTIONS="--jitless"` env var injection to prevent seccomp crashes during direct execution bypassing bash) | Node.js only |
| **Pre-patched ELF PT_INTERP** | Dynamic linker path rewritten for proot namespace | All dynamically-linked binaries |
| **`extractNativeLibs=true`** | Native libs extracted to filesystem before load | Native libraries in APK |

### Guest program compatibility

| Program | W^X Status | Notes |
|---------|-----------|-------|
| Python 3 (CPython) | ✅ Works | No JIT by default; pure interpreter |
| Node.js | ✅ Works | Enforced via global `NODE_OPTIONS="--jitless"` environment injection to avoid bypasses on direct exec |
| Git | ✅ Works | Standard compiled binary |
| pip packages | ✅ Mostly works | Avoid packages with native JIT (PyPy, numba) |
| npm packages | ✅ Mostly works | Avoid packages bundling native JIT compilers |
| C/C++ compiled tools | ✅ Works | Standard compiled binaries |

### What does NOT work
- **PyPy** — requires JIT, blocked by W^X
- **numba** — LLVM JIT compilation blocked
- **V8 without `--jitless`** — blocked (mitigated by flag)
- **Self-modifying code** — blocked by design (security feature)

## 12. Phase Mapping

| Phase | Deliverable |
|---|---|
| Phase 2 | Full Environment design, rootfs build pipeline, manifest format |
| Phase 3 | Full Environment implementation: extraction, verification, proot execution, apt/pip/npm integration |
| Phase 5 | Environment templates on top of the Full Environment |
| Phase 6 | Cross-architecture support and advanced update mechanics |
| Phase 8 | Template marketplace |

## 13. Related Specifications

- [architecture/SANDBOX.md](../architecture/SANDBOX.md)
- [specs/TERMINAL.md](TERMINAL.md)
- [docs/ENVIRONMENT_SETUP.md](../docs/ENVIRONMENT_SETUP.md)
- [requirements/FR.md](../requirements/FR.md)
- [requirements/RISKS.md](../requirements/RISKS.md)
- [security/SandboxPolicy.md](../security/SandboxPolicy.md)
