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
│ Nexora Android App (JVM) │
│ │
│ Headless WebView (Host) <─── ToolManager (Intercept) │
│ │ ▲ │
│ (Loads URL) │ │
│ │ executeTool() │
│ ▼ │ │
│ [Secure Network] │ │
│ │ │ │
│ ┌───────┼───────────────────────────┼──────────────┐ │
│ │ ▼ │ │ │
│ │ proot Linux Guest (Debian) │ │ │
│ │ │ │ │
│ │ Agent Loop ───────── [Tool] ────┘ │ │
│ │ (Python/Node) (browser_open / TOOL-245) │ │
│ │ │ │
│ │ /workspace/downloads/ ◄────────────────────────│ │
│ │ (Shared storage path for downloads/scrapes) │ │
│ └──────────────────────────────────────────────────┘ │
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
| `browser_type` | `TOOL-250` | Injects text into an input field or form element | `selector`, `value`| Focuses element and programmatically changes the value attribute |
| `browser_evaluate` | `TOOL-256` | Runs raw JavaScript inside the page context and returns serializable output | `script` | Invokes `WebView.evaluateJavascript()` with callback |

---

## 3.1 Side-Effect and Recovery Contract

Browser operations remain ordinary Tool invocations for authorization, correlation, idempotency, timeout, cancellation, audit, and recovery. This specification does not create a new Browser permission scope, lifecycle state, error code, or reconciliation mechanism.

`browser_click`, `browser_type`, and `browser_evaluate` are potentially externally side-effecting operations. `browser_open` is navigation state change and may trigger remote page effects; it therefore follows the same uncertain-completion rule when the host bridge has dispatched the request. `browser_screenshot` and `browser_extract` are observation-oriented, but still preserve the standard Tool invocation identity and correlation metadata.

If the WebView bridge, process, or network transport fails after dispatch and completion is not confirmed, the Tool result MUST remain `UNKNOWN_COMPLETION` under [../architecture/TOOL_SYSTEM.md](../architecture/TOOL_SYSTEM.md) §Operation-Level Side-Effect Recovery. The runtime MUST NOT silently replay a potentially mutating operation. Reconciliation uses the existing provider/status lookup, deterministic compensation, or explicit manual-reconciliation contract declared by the operation owner. A confirmed authorization denial remains `NXR-2003` with its canonical subreason and no WebView action is dispatched.

Browser operation history MUST preserve the existing `toolCallId`, idempotency key, `correlationId`, target/selector metadata in redacted form, dispatch status, completion state, reconciliation evidence, and final disposition through the existing ToolInvocation and audit contracts. The WebView bridge does not become a second lifecycle owner.

## 4. Bridge Data Contracts (Kotlin)

### Browser Navigation Request

```kotlin
data class BrowserNavigationRequest(
 val url: String,
 val timeoutMs: Long = 30_000,
 val blockImages: Boolean = false,              // existing workspace preference; default off
 val blockFonts: Boolean = false,               // existing workspace preference; default off
 val blockThirdPartyResources: Boolean = false  // existing workspace preference; default off
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

- **Isolated Network Egress**: The host `WebView` is configured with a forced proxy to the workspace egress proxy (see `docs/SANDBOX_DEPTH.md` §2.4); it never opens direct guest sockets. The same proxy applies the existing mode-conditioned `network:http` / `network:websocket` admission, blocks configured secret material from unauthorized endpoints, and logs every request (`FR-S014`). In `AUTOPILOT`, public routable destinations do not require per-workspace Allowed-Domains enrollment; localhost, loopback, and app-private endpoints remain hard-blocked. Guest-native browsers are unsupported; all WebView traffic is host-mediated, so native guest binaries cannot bypass the controls.
- **Data vs. Instruction Wrapping**: Text extracted from pages is tagged as untrusted, labeled with source context, and treated strictly as passive data inside the Context Builder (`FR-S015` / `FR-WS-005`), preventing malicious pages from hijacking the agent loop.
- **No Java-Interface Injections**: The WebView instance MUST NOT expose any Java interfaces (`addJavascriptInterface`) to the web page. All data extraction is unidirectional via `evaluateJavascript` string evaluation.
- **No Localhost Access**: Headless WebView requests attempting to connect to localhost, loopback addresses (`127.0.0.1`), or app-private database endpoints are immediately blocked.
- **Image/Resource Blocking**: Image loading, custom fonts, and third-party-resource blocking are existing per-workspace preferences and default to off. Token, bandwidth, and related cost information is informational only and never a gate under DEC-45.

---

## 5.1 Sensitive-Domain Action Floor (DEC-47; narrows G3)

> **Status:** CANONICAL sensitive-action specification selected by DEC-47.
> **Reference:** `security/SandboxPolicy.md` (§Sensitive Domains and Restricted Action Classes); `docs/DECISION_LOG.md` (`DL-087`).

### Sensitive App Action Classes (UI Automation)

When `AgentType.BROWSER` (`architecture/MULTI_AGENT_SYSTEM.md`) attempts credential entry or transaction execution on a sensitive app/domain class (`banking`, `payment`, `trading`, `crypto`, `insurance` — see `security/SandboxPolicy.md` §Sensitive Domains and Restricted Action Classes):

1. **Existing authorization denies.** Navigation and read-only extraction are not denied solely by the domain. Credential entry and transaction execution are denied through existing PermissionModel/Tool authorization; no local classifier is invoked.
2. **Audit entry** (`FR-TL015`) records `workspaceId`, `agentId`, sensitive domain/app, timestamp, attempted action, and denial reason.
3. **User notification** uses the existing `agent_error` boundary when a user-visible explanation is required.
4. **Continuation status:** The denied action does not execute or automatically resume. A later attempt remains subject to existing authorization, approval, audit, and lifecycle contracts. This rule does not create or reinterpret a TaskLifecycle state or transition.

### Public Navigation and Sensitive-Domain Actions

`browser_open` (`TOOL-245`) MAY load any publicly routable URL without a domain allowlist check under the existing effective network and sandbox rules. `WebView.loadUrl()` remains blocked for localhost, loopback, and app-private endpoints. Sensitive-domain restrictions apply to credential entry and transaction execution performed by `browser_type`, `browser_click`, `browser_evaluate`, or equivalent actions, not to navigation or read-only extraction.

### Evidence Classification (DEC-47)

- `DECIDED`: Public navigation and read-only extraction are allowed subject to existing network, permission, sandbox, loopback, app-private, and untrusted-content floors.
- `DECIDED`: Credential entry and transaction execution on sensitive domains remain denied, audited, and non-resumable through existing authorization and lifecycle contracts. No new browser state, error code, permission scope, or bypass is created.

---

## 6. Phase Mapping

- **Phase 3 (Core Telemetry)**: Headless WebView class integration; core navigation and text extraction tools (`browser_open` / `TOOL-245`, `browser_extract`).
- **Phase 4 (Autonomy)**: Screenshot capture (`browser_screenshot`) writing to VFS; form-fill and click simulation; content quarantine wrapping.
- **Phase 5 (Advanced Templates)**: Playwright-compatible Python/Node wrapper scripts inside the guest that proxy commands to the host JVM port dynamically.
