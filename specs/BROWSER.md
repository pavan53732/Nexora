> **Status: CANONICAL** for browser automation and extraction behavior.
> This document owns the headless WebView bridge architecture, command protocol, and scraping policies.
> It does NOT own core sandbox containment (see [../security/SandboxPolicy.md](../security/SandboxPolicy.md))
> or network egress proxies (see [../specs/BACKGROUND_EXECUTION.md](BACKGROUND_EXECUTION.md)).
>
> Depends on: [../security/SandboxPolicy.md](../security/SandboxPolicy.md), [../architecture/SANDBOX.md](../architecture/SANDBOX.md).
> Referenced by: [../registry/TOOLS.md](../registry/TOOLS.md), [../docs/SANDBOX_DEPTH.md](../docs/SANDBOX_DEPTH.md).

# Browser Automation Specification — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See also [../architecture/SANDBOX.md](../architecture/SANDBOX.md) · [../security/SandboxPolicy.md](../security/SandboxPolicy.md)

---

## 1. Overview

Nexora provides standard headless web browsing and extraction capabilities for autonomous agents. Because the sandboxed guest environment (proot Debian-slim) operates under strict Android seccomp constraints (W^X / JITless) and storage limits, **running a local headless Chromium or Puppeteer binary inside the guest is completely unsupported**. Such binaries fail to JIT, consume excessive space, and violate platform security boundaries.

Instead, Nexora implements the **Headless WebView Bridge Protocol**. This protocol redirects browser automation commands from the sandboxed guest to a native Android `WebView` instance hosted securely within the JVM main application process.

---

## 2. Headless WebView Bridge Architecture

```text
┌────────────────────────────────────────────────────────┐
│                   Nexora Android App (JVM)             │
│                                                        │
│  Headless WebView (Host) <─── ToolManager (Intercept)  │
│          │                           ▲                 │
│     (Loads URL)                      │                 │
│          │                     executeTool()           │
│          ▼                           │                 │
│   [Secure Network]                   │                 │
│          │                           │                 │
│  ┌───────┼───────────────────────────┼──────────────┐  │
│  │       ▼                           │              │  │
│  │  proot Linux Guest (Debian)       │              │  │
│  │                                   │              │  │
│  │   Agent Loop ───────── [Tool] ────┘              │  │
│  │   (Python/Node)       (browser_navigate)         │  │
│  │                                                  │  │
│  │   /workspace/downloads/ ◄────────────────────────│  │
│  │   (Shared storage path for downloads/scrapes)    │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────┘
```

---

## 3. Protocol Operations

Browser automation is exposed to the agent loop via specialized tools (`TOOL-2xx` series). These tools bypass proot subprocess spawns and run directly on the host JVM WebView:

| Operation | Tool ID | Description | Parameters | Host JVM Action |
|---|---|---|---|---|
| `browser_open` | `TOOL-245` | Loads a URL in the headless WebView and waits for `DOM_CONTENT_LOADED` | `url`, `timeoutMs` | Invokes `WebView.loadUrl()`; injects standard User-Agent |
| `browser_screenshot`| `TOOL-248` | Captures a high-resolution PNG of the active page | `outputFilename` | Draws the WebView canvas onto an Android Bitmap; saves to workspace `/files/` |
| `browser_extract` | `TOOL-247` | Extracts text, links, headings, or metadata | `selector`, `mode` | Executes host-side JavaScript to parse DOM; returns JSON structure |
| `browser_click` | `TOOL-249` | Performs a click event on an element matching a CSS selector | `selector` | Dispatches simulated touch events to WebView coordinates |
| `browser_fill` | `TOOL-250` | Injects text into an input field or form element | `selector`, `value`| Focuses element and programmatically changes the value attribute |
| `browser_evaluate` | `TOOL-256` | Runs raw JavaScript inside the page context and returns serializable output | `script` | Invokes `WebView.evaluateJavascript()` with callback |

---

## 4. Bridge Data Contracts (Kotlin)

### Browser Navigation Request

```kotlin
data class BrowserNavigationRequest(
    val url: String,
    val timeoutMs: Long = 30_000,
    val blockImages: Boolean = true,
    val blockThirdPartyCookies: Boolean = true
)
```

### Browser Extraction Response

```kotlin
data class BrowserExtractionResponse(
    val title: String,
    val currentUrl: String,
    val htmlContent: String?,
    val textContent: String?,
    val links: List<WebLink>,
    val metadata: Map<String, String>
)

data class WebLink(val text: String, val url: String)
```

---

## 5. Security & Confinement Rules

To prevent prompt-injection attacks, data exfiltration, or sandbox escapes through web content, the bridge enforces the following security boundaries:

- **Isolated Network Egress**: The host `WebView` is configured with a forced proxy to the workspace egress proxy (see `docs/SANDBOX_DEPTH.md` §2.4); it never opens direct guest sockets. The same proxy enforces per-workspace Allowed Domains, applies the `network:http` / `network:websocket` grant, runs outbound-body DLP (NFR-SEC-013), and logs every request (`FR-S014`). Guest-native browsers are unsupported; all WebView traffic is host-mediated, so native guest binaries cannot bypass the controls.
- **Data vs. Instruction Wrapping**: Text extracted from pages is tagged as untrusted, labeled with source context, and treated strictly as passive data inside the Context Builder (`FR-S015` / `FR-WS-005`), preventing malicious pages from hijacking the agent loop.
- **No Java-Interface Injections**: The WebView instance MUST NOT expose any Java interfaces (`addJavascriptInterface`) to the web page. All data extraction is unidirectional via `evaluateJavascript` string evaluation.
- **No Localhost Access**: Headless WebView requests attempting to connect to localhost, loopback addresses (`127.0.0.1`), or app-private database endpoints are immediately blocked.
- **Image/Resource Blocking**: To minimize token costs, bandwidth, and battery drain, WebView settings default to blocking image loading, custom fonts, and third-party tracking scripts.

---

## 5.1 Blocked List & Isolation Warning (G3 — Added 2026-08-06)

> **Status:** CANONICAL blocked-list specification for browser automation (added G3 — 2026-08-06).  
> **Verified research reference:** `aihackers.net` 2026-07-03; `digitalapplied.com` 2026-07-03 (`Kimi Claw` pattern — sensitive accounts must not be automated).  
> **Reference:** `security/SandboxPolicy.md` (§Blocked Domains & Sensitive Apps); `docs/DECISION_LOG.md` (`DL-023`); `docs/research/NEXORA_VS_ZCODE_CAPABILITY_GAP.md` (§6.2 — bot integration missing; §5.2 — browser automation partial — blocked-list closes a security gap without redesign).

### Blocked App Classes (UI Automation)

When `AgentType.BROWSER` (`architecture/MULTI_AGENT_SYSTEM.md`) attempts interaction with a blocked app class (`banking`, `payment`, `trading`, `insurance` — see `security/SandboxPolicy.md` §Blocked App Classes), the following isolation flow activates:

1. **Sandbox denial** (`security/SandboxPolicy.md`): `NXR-7005` (filesystem/network escape) or `NXR-2003` (network connection denied) returned; agent loop pauses at `Blocked` state (`state-machines/TaskLifecycle.md` — `Blocked` state definition).
2. **Audit entry** (`FR-TL015`): Severity `CRITICAL`; fields: `workspaceId`, `agentId`, `blockedAppClass`, `timestamp`, `attemptedAction` (`navigate`/`click`/`fill`/`extract`), `isolationWarning` (`true`), `userActionRequired` (`true`).
3. **User notification** (`specs/BACKGROUND_EXECUTION.md` §4 — `agent_error` notification type; `NotificationHelper` — `agent_error` channel): Message includes isolation instruction (`"Sensitive account detected. Please isolate this account in a separate workspace (`FR-W005`) with a separate provider profile (`FR-P011`) before attempting automation. See `docs/DECISION_LOG.md` (`DL-023`)."`).
4. **Agent loop behavior**: The agent remains in `Blocked` (`TaskLifecycle` — `Blocked` state: waiting on unresolved dependency or resource lock) until the user either (a) resolves isolation (separate workspace + separate profile — `FR-W001` workspace isolation + `FR-P011` profile isolation) or (b) provides explicit `ALLOW` for the specific scope + domain/app combination through `Workspace Settings` (`security/PermissionModel.md` — `Workspace override` layer can override `DENY` with `ALLOW` for specific domains after user confirmation).

### Blocked High-Risk Domains (Browser Navigation)

When `browser_open` (`TOOL-245`) attempts to load a blocked domain (`*.bank*`, `*.pay*`, `*.crypto*`, `*.insurance*` — see `security/SandboxPolicy.md` §Blocked Domains):

- `WebView.loadUrl()` is intercepted by the sandbox manager (`ToolManager` — `executeTool()`); the URL is checked against the blocked-list (`security/SandboxPolicy.md` §Blocked Domains); if blocked, `execute()` returns `ToolResult.Error` (`NXR-2003`) immediately (before `WebView.loadUrl()` is called); the `EventBus` publishes `AgentError` (`protocols/Agent-Protocol.md` — `AgentError` event); the agent loop pauses (`Blocked`); the audit log records `CRITICAL` severity; the user receives `agent_error` notification with isolation instruction.

### Evidence Classification (G3 — Per Discovery)

- `VERIFIED` (`Kimi Claw` / `MiniMax Hailuo`): Sensitive account isolation required; verified by public sources (`aihackers.net` 2026-07-03; `digitalapplied.com` 2026-07-03).
- `ENGINEERING INFERENCE` (Domain-pattern blocklist): Standard web-security practice; `security/SandboxPolicy.md` §Network Policy already defines `DENY` default; blocked-list extends existing denial mechanism (`NXR-2003`) — no new mechanism.
- `UNKNOWN` (None for G3 — all elements supported by existing architecture: `SandboxPolicy.md` denial, `TaskLifecycle.md` `Blocked`, `NotificationHelper`, `FR-TL015` audit, `FR-W005` settings).

---

## 6. Phase Mapping

- **Phase 3 (Core Telemetry)**: Headless WebView class integration; core navigation and text extraction tools (`browser_navigate`, `browser_extract`).
- **Phase 4 (Autonomy)**: Screenshot capture (`browser_screenshot`) writing to VFS; form-fill and click simulation; content quarantine wrapping.
- **Phase 5 (Advanced Templates)**: Playwright-compatible Python/Node wrapper scripts inside the guest that proxy commands to the host JVM port dynamically.
