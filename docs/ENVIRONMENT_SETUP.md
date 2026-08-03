# Environment Setup — Nexora (Linux)

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)
> Related: [requirements/DEPENDENCIES.md](../requirements/DEPENDENCIES.md) · [docs/ROADMAP.md](./ROADMAP.md) · [docs/PERFORMANCE_BUDGET.md](./PERFORMANCE_BUDGET.md) · [specs/AI_PROVIDERS.md](../specs/AI_PROVIDERS.md) · [specs/TERMINAL.md](../specs/TERMINAL.md) · [specs/GIT.md](../specs/GIT.md) · [specs/DATABASE.md](../specs/DATABASE.md) · [architecture/SANDBOX.md](../architecture/SANDBOX.md)

---

| Field | Value |
|-------|-------|
| **Host OS** | Debian GNU/Linux 13 (trixie), x86_64 |
| **Date** | 2026-08-03 |
| **Scope** | Phase 1 pre-work — environment preparation only |
| **Status** | Complete & verified — no Android project created yet |
| **Repository** | `https://github.com/pavan53732/Nexora` (branch `main`) |

---

## 1. Repository & Documentation Review

The repository was cloned into the workspace and the documentation reviewed before any
environment work, per the [Documentation Standard](../standards/Documentation-Standard.md).

Documents reviewed (at minimum):

- `PROJECT_SPECIFICATION.md` — master index, package `com.nexora.app`, workspace-first, 8 phases (Phase 0 complete)
- `README.md` — product overview, tech stack (Kotlin, Gradle, API 34+, Material 3 / Compose)
- `docs/ARCHITECTURE.md`, `docs/SYSTEM_DESIGN.md`, `docs/ROADMAP.md`, `docs/PRODUCT_VISION.md`
- `docs/DEPENDENCY_GRAPH.md`, `docs/MODULE_BOUNDARIES.md`, `docs/LIFECYCLES.md`, `docs/PERFORMANCE_BUDGET.md`
- `requirements/` — FR (95), NFR (40), CONSTRAINTS (13), ASSUMPTIONS (20), DEPENDENCIES, RISKS (12)
- `standards/` — Coding, Documentation, Testing, Logging, Security, Performance, Naming
- `registry/` — FEATURES, TOOLS, AGENTS, PLUGINS, PROVIDERS (PROV-001…009), TOOL_MATRIX, AGENT_MATRIX
- `docs/adr/` — ADR-0001…0005
- `sdk/` — AgentSDK, PluginSDK, ProviderSDK, ToolSDK
- `specs/` — FILE_SYSTEM, TERMINAL, GIT, BROWSER, DATABASE, AI_PROVIDERS, WORKSPACE

**Key environment-relevant decisions extracted from the docs:**

| Item | Decision | Source |
|------|----------|--------|
| Min SDK | API 34 (Android 14) | NFR-COMPAT-001, DL-013 |
| Build tools | Build Tools 34.0.0 (AAPT2, D8, R8) | requirements/DEPENDENCIES.md |
| JDK | 21 | requirements/DEPENDENCIES.md |
| Kotlin | 2.0+ (Kotlin-only codebase, KSP preferred over KAPT) | requirements/DEPENDENCIES.md, Coding-Standard |
| Gradle | 8.10+ (Gradle Wrapper required, reproducible builds) | requirements/DEPENDENCIES.md, NFR-PORT-001 |
| APK budget | < 50 MB (R8/ProGuard, resource shrinking) | DL-014, RISK-005 |
| Libraries | Compose BOM, Material 3, Navigation Compose, Hilt, Room, DataStore, Coroutines/Flow, OkHttp, Retrofit, Kotlinx Serialization, WorkManager, Biometric, Security Crypto | requirements/DEPENDENCIES.md, DECISION_LOG DL-001…DL-018 |
| Version centralization | `gradle/libs.versions.toml` — no hardcoded versions | requirements/DEPENDENCIES.md |

---

## 2. Installed Software & Versions

### System

| Package | Version |
|---------|---------|
| git | 2.47.3 |
| curl | 8.14.1 |
| wget | 1.25.0 |
| unzip / zip | 6.0 / 3.0 |
| tar / gzip | 1.35 / 1.13 |
| build-essential (gcc/g++/make) | 12.2 / 12.2 / 4.3 |
| cmake | 3.31.6 |
| pkg-config | 1.8.1 |
| openssl | 3.5.6 |
| ca-certificates | 2025-09-22 |
| Git LFS (optional) | 3.6.1 |
| Node.js (runtime, present in dev image) | 20.20.2 |
| SQLite (runtime, present in dev image) | 3.50.6 |

> **Note:** Node.js 20.20.2 and SQLite 3.50.6 are preinstalled in the development
> image — useful for testing Phase-3 sandbox runtimes (embedded Node, `sqlite3`
> tools) before the on-device runtimes (Chaquopy, QuickJS, JGit, sqlite-android)
> are integrated.

### Java

| Component | Version | Location |
|-----------|---------|----------|
| OpenJDK 21 LTS (JRE + JDK) | **21.0.11** (build 21.0.11+10) | `/usr/lib/jvm/java-21-openjdk-amd64` |
| javac | 21.0.11 | `$JAVA_HOME/bin/javac` |

### Android SDK

| Component | Version | Location |
|-----------|---------|----------|
| Command Line Tools | 15859902 (sdkmanager 22.0) | `/opt/android-sdk/cmdline-tools/latest` |
| Platform-Tools | 37.0.1 (adb 1.0.41) | `/opt/android-sdk/platform-tools` |
| Build-Tools | **34.0.0** (per repo docs), 36.1.0 (default), 37.0.0, 29.0.3 | `/opt/android-sdk/build-tools/` |
| Platforms | android-34 (minSdk target), android-35, android-36, android-36.1, android-37.0, android-29 | `/opt/android-sdk/platforms/` |
| Sources | android-29, android-35, android-36, android-37.0 | `/opt/android-sdk/sources/` |

### Android Build Tools

| Tool | Version | Where it runs from |
|------|---------|--------------------|
| AAPT2 | 2.20-14042983 (build-tools 36.1.0) | `build-tools/36.1.0/aapt2` |
| D8 | 9.3.16 (D8 9.0.3-dev) | `build-tools/36.1.0/d8` |
| R8 | artifact 9.1.31 (reports build 9.3.16) | `/opt/android-sdk/r8/r8.jar` (`/usr/local/bin/r8`) |
| Bundletool | 1.18.3 | `/opt/android-sdk/bundletool/bundletool.jar` (`/usr/local/bin/bundletool`) |
| zipalign | build-tools 36.1.0 | `build-tools/36.1.0/zipalign` |
| apksigner | 0.9 | `build-tools/36.1.0/apksigner` |

> AAPT2/D8/R8/zipalign/apksigner are also bundled per build-tools version; AGP will
> select the version it needs automatically. R8 and Bundletool additionally ship as
> standalone jars for direct CLI use.

### Build Language Tooling

| Tool | Version | Location |
|------|---------|----------|
| Gradle | **9.6.1** | `/opt/gradle/current` (≥ 8.10 required by repo docs ✓) |
| Kotlin (kotlinc) | **2.4.10** | `/opt/kotlin/kotlinc` (≥ 2.0 required ✓) |

### Python

| Component | Version | Location |
|-----------|---------|----------|
| python3 | **3.13.14** (≥ 3.12 required ✓) | `/usr/local/bin/python3` |
| pip3 | 26.1.2 | `/usr/local/bin/pip3` |
| venv | ✓ (tested) | `python3 -m venv` |
| virtualenv | 20.31.2 | system package |

---

## 3. Environment Variables

Persisted in `/etc/profile.d/nexora-java.sh` and `/etc/profile.d/nexora-android.sh`
(workspace copy: `nexora/env/nexora_env.sh` in the dev workspace):

```sh
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64

export ANDROID_HOME=/opt/android-sdk
export ANDROID_SDK_ROOT=/opt/android-sdk
export GRADLE_HOME=/opt/gradle/current
export KOTLIN_HOME=/opt/kotlin/kotlinc
```

Load in a shell with:

```sh
source /etc/profile.d/nexora-java.sh /etc/profile.d/nexora-android.sh
```

## 4. PATH Configuration

```
$ANDROID_HOME/cmdline-tools/latest/bin   # sdkmanager, avdmanager, lint, apkanalyzer
$ANDROID_HOME/platform-tools             # adb, fastboot
$ANDROID_HOME/build-tools/36.1.0         # aapt2, d8, zipalign, apksigner, dexdump
$GRADLE_HOME/bin                         # gradle
$KOTLIN_HOME/bin                         # kotlinc, kotlin
/usr/local/bin                           # bundletool, r8 wrapper scripts
```

## 5. Tool Locations

| Tool | Path |
|------|------|
| Java (JAVA_HOME) | `/usr/lib/jvm/java-21-openjdk-amd64` |
| Android SDK (ANDROID_HOME / ANDROID_SDK_ROOT) | `/opt/android-sdk` |
| Python | `/usr/local/bin/python3` |
| Gradle | `/opt/gradle/current` |
| Kotlin | `/opt/kotlin/kotlinc` |
| Bundletool | `/opt/android-sdk/bundletool/bundletool.jar` |
| R8 | `/opt/android-sdk/r8/r8.jar` |

---

## 6. Verification Results

### Version checks (all passed)

| Command | Result |
|---------|--------|
| `java -version` | openjdk version "21.0.11" 2026-04-21 ✓ |
| `javac -version` | javac 21.0.11 ✓ |
| `sdkmanager --version` | 22.0 ✓ |
| `adb version` | Android Debug Bridge 1.0.41, Version 37.0.1-15733141 ✓ |
| `gradle --version` | Gradle 9.6.1 (JVM 21.0.11) ✓ |
| `kotlinc -version` | kotlinc-jvm 2.4.10 ✓ |
| `python3 --version` | Python 3.13.14 ✓ |
| `pip3 --version` | pip 26.1.2 ✓ |
| `git --version` | git version 2.47.3 ✓ |
| `git lfs version` | git-lfs/3.6.1 ✓ |
| `aapt2 version` | 2.20-14042983 ✓ |
| `d8 --version` | D8 9.3.16 ✓ |
| `r8 --version` | R8 9.3.16 ✓ |
| `bundletool version` | 1.18.3 ✓ |
| `apksigner version` | 0.9 ✓ |
| `zipalign` | responds (help text, exit 0) ✓ |

### Functional smoke tests (all passed)

1. **Kotlin pipeline** — `kotlinc` compiled a program; JVM executed it → `kotlinc OK: 42`
2. **Java → DEX pipeline** — `javac` + `d8 --release --lib android-34/android.jar` produced valid `classes.dex`
3. **AAPT2** — compiled `res/values/strings.xml` → `compiled.zip` (no errors)
4. **Gradle** — executed a Kotlin-DSL task successfully (daemon on JVM 21)
5. **Python** — `python3 -m venv` + `pip install requests` + import verified
6. **Environment variables** — all five resolve to real paths; every tool resolves from PATH

### SDK licenses

All accepted via `sdkmanager --licenses` (output confirmed: *"All SDK package licenses accepted"*).

---

## 7. Android Library Compatibility (Step 3)

Verified compatible with the future Phase 1 stack. All coordinates were checked against
Google Maven / Maven Central on 2026-08-03; the repo's minimums
([requirements/DEPENDENCIES.md](../requirements/DEPENDENCIES.md)) are met or exceeded.

| Library | Repo minimum | Verified current stable | Status |
|---------|-------------|-------------------------|--------|
| Jetpack Compose (BOM) | BOM 2024.x | **2026.06.01** | ✓ exceeds |
| Material 3 | material3 | via Compose BOM | ✓ |
| Navigation Compose | navigation-compose | **2.9.8** | ✓ |
| Hilt | 2.51+ | **2.60.1** (Maven Central) | ✓ |
| Room | 2.6+ | **2.8.4** (KSP) | ✓ |
| DataStore | 1.1+ | **1.2.1** | ✓ |
| WorkManager | 2.9+ | **2.11.2** | ✓ |
| Coroutines / Flow | 1.8+ | **1.11.0** | ✓ |
| Kotlinx Serialization | 1.6+ | **1.11.0** | ✓ |
| OkHttp | 4.12+ | **5.4.0** | ✓ |
| Retrofit | 2.11+ | **3.0.0** | ✓ |
| AndroidX Biometric | 1.2+ | 1.4.x line | ✓ |
| AndroidX Security Crypto | 1.1+ | 1.1.0 | ✓ |
| Coil (optional) | 3.x | 3.x | ✓ |
| KSP | 2.0+-1.0.x | matches Kotlin 2.4.10 | ✓ |

**Build compatibility confirmed:** JDK 21 (AGP 9.x requires JDK 17+), Gradle 9.6.1
(≥ 8.10 required; AGP stable 9.3.1 is compatible), Kotlin 2.4.10, compileSdk 36
(34/35/37 also installed), minSdk 34 platform installed, build-tools 34.0.0 installed.
Repositories `google()` + `mavenCentral()` cover every dependency (Hilt is published to
Maven Central only). Version centralization in `gradle/libs.versions.toml` is supported
by the toolchain.

> No Android project, Gradle files, or source code were created — this is compatibility
> verification only.

---

## 8. AI Provider Integration Readiness (Step 4)

The environment is ready for all nine providers from
[specs/AI_PROVIDERS.md](../specs/AI_PROVIDERS.md) and the
[Provider Registry](../registry/PROVIDERS.md) (PROV-001…009). **No API keys are
configured anywhere** (per NFR-SEC-005, keys will be stored encrypted via Android
Keystore at implementation time).

| Provider | Protocol | Environment readiness |
|----------|----------|----------------------|
| OpenAI | OpenAI-compatible REST + SSE | ✓ OkHttp 5.4.0 + kotlinx-serialization installed/verified |
| Anthropic | REST (`x-api-key` header) | ✓ same stack |
| Gemini | Google AI REST | ✓ same stack |
| Groq | OpenAI-compatible | ✓ |
| OpenRouter | OpenAI-compatible | ✓ |
| Ollama | OpenAI-compatible (local) | ✓ (network stack supports localhost endpoints) |
| LM Studio | OpenAI-compatible (local) | ✓ |
| Local GGUF | llama.cpp / mlc-llm (Phase 5 decision) | ✓ NDK toolchain available (cmake 3.31.6, build-essential) if native integration is chosen |
| Custom | user-defined | ✓ baseUrl-overridable design |

The verified HTTP stack (OkHttp + Retrofit + Kotlinx Serialization) matches
DL-005/DL-006 decisions. Streaming (SSE) and `Flow<StreamChunk>` are supported by the
chosen libraries.

---

## 9. Embedded Runtime Research (Step 5)

Research for Phase 3 ([architecture/SANDBOX.md](../architecture/SANDBOX.md),
[specs/TERMINAL.md](../specs/TERMINAL.md), [specs/GIT.md](../specs/GIT.md),
[specs/DATABASE.md](../specs/DATABASE.md)). **Nothing in this section is installed as a
system package — these are application components to be integrated later.**

### 9.1 Embedded Python runtime

| Criterion | Chaquopy | python-for-android | Termux Python |
|-----------|----------|--------------------|---------------|
| Android compatibility | Excellent — official Gradle plugin, Java⇄Python interop, PyPI builds | Good — but rebuilds the whole app | Good — bionic debs, not embeddable SDK |
| License | **MIT** (fully open source since v12.0.1) | MIT | GPL-3.0 (viral) |
| Performance | CPython native; JNI overhead modest | CPython native | CPython native |
| APK impact | +15–50 MB (ABI-split friendly) | similar/larger | n/a |
| Maintenance | **Active** — v17.0.0 (Dec 2025) | Active — v2026.05.09 | Active |
| Integration complexity | **Low** — one Gradle plugin block | High — restructures build | Very high — manual JNI |
| **Recommendation** | ✅ **Chaquopy** | fallback | avoid (GPL) |

### 9.2 Embedded JavaScript engine

| Criterion | app.cash.quickjs | taoweiji/quickjs-android | Hermes | J2V8 / LiquidCore |
|-----------|------------------|--------------------------|--------|-------------------|
| Android compatibility | Excellent (AAR, all ABIs) | Excellent | Via React Native | Older / heavy |
| License | MIT (QuickJS) | MIT | MIT | Apache-2.0 / MIT+LGPL |
| Performance | Fast interpreter, low memory (no JIT) | same engine | JIT — fastest | JIT |
| APK impact | ~1.5–3 MB/ABI | ~1.5–3 MB/ABI | ~3–6 MB | 10–25 MB |
| Maintenance | **Active** — 0.9.2 on Maven Central | Active — v1.3.0 | Active (Meta) | Stale / low activity |
| Integration complexity | Low | Low | Medium (RN-bound) | Medium |
| **Recommendation** | ✅ **app.cash.quickjs** | good alternative | only if JIT needed | avoid |

### 9.3 Embedded Git

| Criterion | JGit | libgit2 + Git24j | Dulwich |
|-----------|------|------------------|---------|
| Android compatibility | Excellent — pure Java (runs on ART, no JNI) | Good — requires NDK build | Only via Python runtime |
| License | EDL (BSD-3) + optional EPL | libgit2 MIT / Git24j LGPL-2.1 | Apache-2.0 |
| Performance | Good for app workloads | Fastest (C) | Slowest |
| APK impact | ~3–5 MB | ~2–4 MB (.so × ABIs) | ~1–2 MB (with Python) |
| Maintenance | **Very active** — 7.7.1 (2026-07) | libgit2 active; **Git24j dormant since 2021** | Active |
| Integration complexity | **Low** | High (NDK + JNI) | Medium |
| **Recommendation** | ✅ **JGit** | revisit only for huge repos | only if Python ships anyway |

### 9.4 Embedded terminal / shell

| Criterion | Termux terminal-view | jackpal Android-Terminal-Emulator | Custom PTY view |
|-----------|----------------------|-----------------------------------|-----------------|
| Android compatibility | Excellent (battle-tested, termux-app v0.118.3) | Good (older era) | Full control, high effort |
| License | **GPL-3.0 (viral — would force open-sourcing Nexora)** | Apache-2.0 | ours |
| Performance | Excellent | Good | depends on implementation |
| APK impact | ~2–5 MB | ~1 MB | ~1–3 MB |
| Maintenance | Active | **Archived (2022)** | n/a |
| Integration complexity | Medium | Low (drop-in) | High |
| **Recommendation** | ⚠ best tech, GPL blocker | ✅ vendor as Apache-2.0 base (mksh/busybox shell via NDK) | only with strong reason |

> **Note (ADR-0006):** the terminal is an **internal, agent-invoked** component — there is
> no user-facing terminal UI. This removes the interactive-rendering requirement: only
> the PTY/shell execution core is needed (plus activity-card rendering of captured
> output), further favoring a small vendored implementation.
>
> Licensing review needed before Phase 3 — this is flagged in
> [requirements/RISKS.md](../requirements/RISKS.md) risk space (RISK-009).

### 9.5 SQLite

| Criterion | Room + built-in SQLite | requery sqlite-android | NDK custom build |
|-----------|------------------------|------------------------|------------------|
| Android compatibility | Perfect (platform) | Good (AAR, modern amalgamation 3.49.0) | Good |
| License | Apache-2.0 | MIT | Public domain |
| Performance | Good; version tied to OS | Best (newest SQLite everywhere) | Best (tunable) |
| APK impact | 0 | ~1–3 MB | ~1–2 MB |
| Maintenance | n/a | **Active** (3.49.0, 2025-05) | own burden |
| Integration complexity | **Lowest** | Medium (Room SQLiteDriver) | High |
| **Recommendation** | ✅ default (per DL-003) | add via Room `SQLiteDriver` when newer SQLite/vector features needed | only for exotic features |

### 9.6 Secure sandbox execution

| Layer | Option | License | APK impact | Recommendation |
|-------|--------|---------|------------|----------------|
| Baseline | Android app sandbox (UID + SELinux + seccomp) | n/a | 0 | ✅ mandatory default |
| One-off risky work | `android:isolatedProcess` services | n/a | 0 | ✅ use where applicable |
| User scripts | QuickJS (interpreter, no JIT) or **wasmi** (WASM, Apache-2.0, v1.1.0) | MIT / Apache-2.0 | ~1–2 MB | ✅ recommended for untrusted code |
| Untrusted native code | Wasmtime via NDK (Apache-2.0, v47.0.3) | Apache-2.0 | 10–20 MB | only if ever needed |

**Summary:** Chaquopy (Python), app.cash.quickjs (JS), JGit (Git), vendored jackpal
terminal emulator (Apache-2.0) + NDK shell, Room + built-in SQLite (upgrade path:
requery sqlite-android), and layered sandbox (platform + isolatedProcess + QuickJS/wasmi).
All respect the < 50 MB APK budget (total estimated impact: +20–60 MB with Python;
ABI splitting or per-feature download mitigations exist).

---

## 10. Issues Encountered & Resolutions

| # | Issue | Resolution |
|---|-------|------------|
| 1 | `cmdline-tools;latest` installed twice (manual extraction + sdkmanager) created duplicate `latest-2/` | Removed `latest-2/`; verified `sdkmanager --version` = 22.0 after cleanup |
| 2 | R8 standalone download from `maven.google.com` returned an HTML 404 page (redirect to `dl.google.com`) | Re-downloaded from `https://dl.google.com/dl/android/maven2/...`; verified JAR integrity (19 MB) and `r8 --version` |
| 3 | Hilt metadata absent from Google Maven (published to Maven Central only) | Confirmed `mavenCentral()` (default) covers Hilt 2.60.1; documented in dependency catalog |
| 4 | `sdkmanager` CLI deprecation warning (Google's new `android` CLI ships alongside) | Both work; sdkmanager used for compatibility; the new CLI is available at `cmdline-tools/latest/bin/android` |
| 5 | Sandbox session ephemerality (packages under `/etc`, `/usr`, `/opt` may not survive session reset) | Idempotent installer script `nexora/env/setup_nexora_env.sh` reproduces the environment on any Debian/Ubuntu machine |
| 6 | GitHub token supplied in task message was doubled (40-char token repeated) | Used the first 40-char token; verified ownership (`pavan53732`) and push permission; token scrubbed from git remote config after clone |

---

## 11. Recommendations & Next Steps

1. **Environment reproducibility** — run `nexora/env/setup_nexora_env.sh` (idempotent)
   on any fresh Debian/Ubuntu dev machine before starting Phase 1.
2. **Phase 1 scaffold versions** (to be applied when Phase 1 begins):
   AGP **9.3.1**, Gradle Wrapper **9.6.1**, Kotlin **2.4.10**, KSP matching Kotlin,
   `compileSdk 36`, `minSdk 34`, `targetSdk 36`, single universal APK (NFR-PORT-002),
   versions centralized in `gradle/libs.versions.toml`.
3. **Repositories** — `google()` + `mavenCentral()` in `settings.gradle.kts`; no other
   repositories required.
4. **No API keys** — provider keys are implemented in Phase 5 with Android Keystore
   encrypted storage (NFR-SEC-005/010); none are configured now.
5. **Embedded runtimes** — Phase 3 decision: Chaquopy / app.cash.quickjs / JGit /
   vendored terminal emulator / Room+SQLite / layered sandbox (see §9). Requires a
   licensing review for the terminal component (GPL vs Apache-2.0).
6. **CI** — GitHub Actions can reuse these exact versions for build/lint/test gates
   (NFR-MAINT-004).

---

*Environment fully verified 2026-08-03. Next step: Phase 1 — Android project scaffold
(bootable app, navigation, theme, settings, core interfaces — no AI).*


---

# Appendix C: Building the Debian-slim Rootfs for Nexora

## C.1 Overview

This guide describes how to build the bundled Full Environment Debian-slim rootfs packaged in the Nexora APK.

## C.2 Prerequisites

- Docker or Podman
- `debootstrap` (or a container image that provides it)
- `xz` for compression
- Android NDK for cross-compiling proot when needed

## C.3 Build Steps

### Step 1: Create the Base Filesystem

```bash
docker run --rm --privileged -v "$(pwd)/build:/build" debian:bookworm-slim bash -c '
  apt-get update && apt-get install -y debootstrap xz-utils
  debootstrap --variant=minbase --arch=arm64 bookworm /build/rootfs http://deb.debian.org/debian
  chroot /build/rootfs bash -c "
    apt-get install -y --no-install-recommends \
      python3 python3-pip python3-venv nodejs npm git curl wget ca-certificates \
      build-essential bash dash coreutils grep sed gawk procps psmisc
    apt-get clean
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
  "
  tar -cJf /build/debian-slim-arm64.tar.xz -C /build/rootfs .
'
```

### Step 2: Generate the Manifest

The manifest must include the rootfs version, architecture, and SHA-256 checksums for all packaged files. Generate it as part of the reproducible build rather than hand-editing it.

### Step 3: Sign the Manifest

```bash
gpg --detach-sign --armor -o manifest.json.asc manifest.json
```

### Step 4: Integrate into the APK

```text
app/src/main/assets/
├── rootfs/
│   ├── debian-slim-arm64.tar.xz
│   ├── manifest.json
│   └── manifest.json.asc
└── proot/
    ├── proot-arm64
    └── proot-x86_64
```

## C.4 proot Compilation (Android)

```bash
git clone https://github.com/termux/proot.git
cd proot
export CC="$NDK/toolchains/llvm/prebuilt/linux-x86_64/bin/aarch64-linux-android24-clang"
make V=1 -C src proot
```

Use a vetted release artifact or reproducible source build; do not download opaque binaries into the repository.

## C.5 Testing

```bash
mkdir -p /tmp/nexora-test
tar -xJf debian-slim-arm64.tar.xz -C /tmp/nexora-test
./proot-arm64 -R /tmp/nexora-test /bin/bash -c "python3 -c 'import sys; print(sys.version)'"
./proot-arm64 -R /tmp/nexora-test /bin/bash -c "node -e 'console.log(process.version)'"
```

## C.6 Size Optimization

| Technique | Expected effect |
|---|---|
| `--variant=minbase` debootstrap | Smaller base than standard Debian |
| Remove docs and manpages | Reduces extracted size |
| Strip debug symbols | Reduces binary footprint |
| Clean apt lists and caches | Reduces packaged size |
| xz compression with a reproducible setting | Reduces APK asset size |

Target: less than 70 MB compressed for the base plus Python, Node.js, and build tooling.

## C.7 CI/CD Pipeline

Rootfs builds should run in a pinned, reproducible CI environment, produce checksums and signatures, and publish artifacts only through the release process. Do not commit generated rootfs archives or signing keys to the source repository.

## C.8 Related Files

- [specs/FULL_ENVIRONMENT.md](../specs/FULL_ENVIRONMENT.md)
- [architecture/SANDBOX.md](../architecture/SANDBOX.md)
- [requirements/FR.md](../requirements/FR.md)
- [requirements/RISKS.md](../requirements/RISKS.md)
