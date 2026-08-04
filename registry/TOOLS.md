# Tool Registry — Nexora

## Category Index

The tool registry is the authoritative inventory of tool identities, categories, and declared capabilities.

Every tool entry SHOULD include or derive the following compatibility metadata in addition to category placement:

- stable `toolId`
- tool version
- category
- required permissions
- sandbox requirement
- streaming support
- cancellation support
- idempotency declaration
- minimum compatible API/SDK contract version
- parameters schema reference

## File System (FILE)

File-system tools operate on the workspace or sandboxed virtual file system and MUST follow the Tool API and Tool Protocol contract path for permission, correlation, lifecycle, and canonical error-envelope semantics.
