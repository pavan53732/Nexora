# Tool Registry — Nexora

## Standard Fields

| Field | Meaning |
|---|---|
| `toolId` | Stable tool identifier |
| `version` | Tool version |
| `origin` | `built-in` or plugin/provider origin |
| `category` | Registry category |
| `requiredPermissions` | Required permission scopes |
| `requiresSandbox` | Sandbox requirement flag |
| `supportsStreaming` | Streaming capability flag |
| `supportsCancellation` | Cancellation capability flag |
| `isIdempotent` | Idempotency declaration |
| `parametersSchemaRef` | Parameter schema reference |
| `minContractVersion` | Minimum compatible API/SDK contract version |

## MCP Integration (Category 27 — Added G4)

> **Reference:** `architecture/TOOL_SYSTEM.md` (§MCP Client) — verified industry precedent (`bitdoze.com` 2026-07-24; `mcp.directory` 2026-07-09).  
> **Position:** Additional tool SOURCE (not replacement for built-in/plugin tools).  
> **Transport:** `stdio` (`mcp_connect_stdio`) + `Streamable HTTP` (`mcp_connect_http`).  
> **Mapping:** MCP primitives (`tool`/`resource`/`prompt`) map onto existing `Tool` interface; permission scopes inherit server declaration or default to `DENY` (deny-by-default — G2); sandbox execution applies (`security/SandboxPolicy.md`).  
> **Phase:** 5 (aligned with `specs/AI_PROVIDERS.md` Phase 5).

| ID | Tool | Description | Phase | Status |
|----|------|-------------|-------|--------|
| `TOOL-397` | `mcp_connect_stdio` | Connect to an MCP server via stdio transport | 5 | Planned |
| `TOOL-398` | `mcp_connect_http` | Connect to an MCP server via Streamable HTTP (SSE-compatible HTTPS) transport | 5 | Planned |
| `TOOL-399` | `mcp_list_caps` | Perform capability negotiation (discover server capabilities) and store in workspace settings (`FR-W005`) | 5 | Planned |
| `TOOL-400` | `mcp_call_tool` | Invoke an MCP-discovered tool through the standard `Tool` interface (`execute` → `ToolResult.Success`/`Error`/`NeedsApproval`) | 5 | Planned |
| `TOOL-401` | `mcp_read_resource` | Read a resource exposed by an MCP server (maps to `ToolResult.Success` with JSON output) | 5 | Planned |
| `TOOL-402` | `mcp_get_prompt` | Retrieve a prompt definition from an MCP server (maps to `ToolResult.Success`) | 5 | Planned |

## Notes

The Tool registry remains an inventory document, but it SHOULD stay aligned with the compatibility expectations defined in [standards/Registry-Standard.md](../standards/Registry-Standard.md).
