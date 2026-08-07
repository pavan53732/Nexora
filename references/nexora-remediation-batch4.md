# Nexora Remediation Batch 4 — plugin lifecycle states + Tool contract projections (DL-043)

Committed: `cb910b9` (main → origin/main). HEAD before: `f5d965e`.

## Findings closed
- L4 — Plugin lifecycle `Cancelled` state defined in transitions/diagram but missing from the authoritative States table (and from the SUPPORTING Plugin Status list).
- L3–L4 — Tool result/descriptor projections diverged from the canonical `ToolInvocation` model (`ToolResult.NeedsApproval` variant, missing descriptor fields, wrong approval-state wording).

## Fixes (file:line → change)

### 1. state-machines/PluginLifecycle.md (CANONICAL) — Cancelled state
- Added `| **Cancelled** | Terminal state — download/verify flow aborted by user or coordinator before completion. |` to the States table (~line 31).
- Added transition row `| `cancel()` | Discovered / Downloading / Verifying | Cancelled | — |` to the Transitions table (~line 44). The diagram already had `Cancelled` nodes; now the authoritative enum matches.

### 2. lifecycle/PluginLifecycle.md (SUPPORTING) — Plugin Status list
- Added `CANCELLED` to the Plugin Status enum line (~line 17) so the derived list matches the canonical state machine. Rule: SUPPORTING must not subset/rename canonical states.

### 3. architecture/TOOL_SYSTEM.md (CANONICAL Tool interface) — ToolResult + descriptor
- Canonical `Tool` interface: added `val supportsStreaming: Boolean`, `val supportsCancellation: Boolean`, `val cacheTtlMs: Long` so it carries the full descriptor superset (matches `models/Tool.md` and `docs/api/Tool-API.md` ToolDescriptor).
- `sealed class ToolResult`: REMOVED the `data class NeedsApproval(...)` variant. Canonical `ToolResult` is now `Success` / `Error` only (source of truth: `models/ToolInvocation.md`). Added a comment: approval is represented by `ToolInvocation` status `PENDING_AUTHORIZATION` (and Task/Agent `WaitingApproval`), never a `ToolResult` variant.

### 4. docs/api/Tool-API.md (DERIVED) — NXR-2003 wording
- Changed "Enter `WaitingApproval` only for effective `ASK`" → "ToolInvocation status → `PENDING_AUTHORIZATION` for an effective `ASK` decision; the owning Task/Agent lifecycle may transition to `WaitingApproval` and resume on approve … Approval is never represented as a `ToolResult` variant."

### 5. protocols/Tool-Protocol.md + architecture/TOOL_SYSTEM.md (MCP result flow)
- Replaced `ToolResult.Success` / `.Error` / `.NeedsApproval` pipeline references with `ToolResult.Success` / `.Error`; authorization requirements surface as `ToolInvocation` status `PENDING_AUTHORIZATION`, not a `ToolResult` variant.

### 6. specs/GIT.md — read-pass / destructive-preview references
- Line ~64: "returns `NeedsApproval` / `NXR-2003`" → "returns `ToolResult.Error` with `NXR-2003` and sets `ToolInvocation` status to `PENDING_AUTHORIZATION`".
- Line ~87: "`NeedsApproval` confirmation (Tool-Protocol)" → "`PENDING_AUTHORIZATION` (the `ToolInvocation` is held for human approval)".

## Validation run
```
git diff --check                                   # CLEAN (trimmed trailing WS on 2 blockquote lines — see Pitfall)
grep -rn '^||' state-machines/PluginLifecycle.md lifecycle/PluginLifecycle.md architecture/TOOL_SYSTEM.md docs/api/Tool-API.md protocols/Tool-Protocol.md specs/GIT.md   # no doubled pipes
grep -rn "ToolResult.NeedsApproval\|returns \`NeedsApproval\`\|NeedsApproval confirmation" . --include=*.md   # none
grep -n "sealed class ToolResult" -A3 architecture/TOOL_SYSTEM.md   # Success/Error only
```
- No stray `ToolResult.NeedsApproval` references remain anywhere in the corpus.
- Registry totals unchanged (350 tools / 28 categories).

## Reuse notes for Batch 5 / future
- **Type-closure rule**: a prose reference to `Result.NeedsApproval` / `Result.X` is a gap if the closed result hierarchy defines only `Success`/`Error`. Approval belongs on the *invocation* status (`PENDING_AUTHORIZATION`), not the result type. Apply this whenever a spec mentions an approval result variant.
- When the canonical state machine has a diagram-only or transition-only node, add it to the authoritative States enum in the same pass (and to any SUPPORTING status list).
