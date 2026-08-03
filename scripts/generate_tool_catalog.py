#!/usr/bin/env python3
"""
Nexora tool catalog generator.

Produces:
  registry/TOOLS.md        — full tool catalog (all 25 categories, stable TOOL-IDs)
  registry/TOOL_MATRIX.md  — capability matrix for every registered tool
                             (preserves existing hand-curated rows, maps legacy names)

Usage: python3 generate_tool_catalog.py  (run from repo root)
"""
import re, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOG = ROOT / "registry" / "TOOLS.md"
MATRIX = ROOT / "registry" / "TOOL_MATRIX.md"

# ---------------------------------------------------------------- categories
# order matches architecture/TOOL_SYSTEM.md; phase = registry convention
CATS = [
    ("FILE",  "File System",       "4"),
    ("WS",    "Workspace",         "1"),
    ("CODE",  "Code Intelligence", "Later"),
    ("SEAR",  "Search",            "4"),
    ("TERM",  "Terminal",          "4"),
    ("GIT",   "Git",               "4"),
    ("PKG",   "Package Manager",   "4"),
    ("BUILD", "Build",             "Later"),
    ("TEST",  "Testing",           "Later"),
    ("DEBUG", "Debugging",         "Later"),
    ("FMT",   "Formatting",        "Later"),
    ("DOC",   "Documentation",     "Later"),
    ("BRW",   "Browser",           "Later"),
    ("NET",   "Network/API",       "4"),
    ("DB",    "Database",          "Later"),
    ("MEM",   "Memory",            "6"),
    ("AI",    "AI",                "5"),
    ("DEV",   "Android Device",    "Later"),
    ("PM",    "Project Management","Later"),
    ("SEC",   "Security",          "Later"),
    ("OBS",   "Observability",     "Later"),
    ("IO",    "Import/Export",     "Later"),
    ("PLG",   "Plugin",            "8"),
    ("MAG",   "Multi-Agent",       "7"),
    ("WF",    "Workflow",          "6"),
]

# ------------------------------------------------------- existing tools (keep IDs)
EXISTING = {
 "FILE": [
  ("TOOL-001","file_read","Read a file's content from the virtual file system"),
  ("TOOL-002","file_write","Create or overwrite a file"),
  ("TOOL-003","file_append","Append content to an existing file"),
  ("TOOL-004","file_delete","Delete a file"),
  ("TOOL-005","file_list","List directory contents with metadata"),
  ("TOOL-006","file_create_dir","Create a directory (recursive)"),
  ("TOOL-007","file_move","Move or rename a file or directory"),
  ("TOOL-008","file_copy","Copy a file or directory"),
  ("TOOL-009","file_exists","Check whether a path exists"),
  ("TOOL-010","file_info","Get file metadata (size, type, mtime)"),
  ("TOOL-011","file_search","Search files by name pattern"),
 ],
 "TERM": [
  ("TOOL-020","terminal_run","Run a shell command in the sandbox"),
  ("TOOL-021","terminal_run_script","Execute a script file in the sandbox"),
  ("TOOL-022","terminal_run_background","Run a command in the background"),
  ("TOOL-023","terminal_kill","Kill a running process by PID"),
  ("TOOL-024","terminal_list_processes","List running processes"),
 ],
 "SEAR": [
  ("TOOL-030","search_text","Search file contents for text"),
  ("TOOL-031","search_regex","Search file contents with a regex"),
  ("TOOL-032","grep","Run grep over workspace files"),
  ("TOOL-033","find","Find files by name and attributes"),
 ],
 "GIT": [
  ("TOOL-040","git_init","Initialize a Git repository"),
  ("TOOL-041","git_clone","Clone a remote repository"),
  ("TOOL-042","git_add","Stage files for commit"),
  ("TOOL-043","git_commit","Commit staged changes"),
  ("TOOL-044","git_push","Push commits to a remote"),
  ("TOOL-045","git_pull","Pull and merge from a remote"),
  ("TOOL-046","git_branch","Create, list, delete, or switch branches"),
  ("TOOL-047","git_merge","Merge branches"),
  ("TOOL-048","git_log","View commit history"),
  ("TOOL-049","git_diff","View file differences"),
  ("TOOL-050","git_status","Show working tree status"),
  ("TOOL-051","git_stash","Stash and unstash changes"),
 ],
 "NET": [
  ("TOOL-060","http_get","Perform an HTTP GET request"),
  ("TOOL-061","http_post","Perform an HTTP POST request"),
  ("TOOL-062","http_put","Perform an HTTP PUT request"),
  ("TOOL-063","http_delete","Perform an HTTP DELETE request"),
  ("TOOL-064","websocket","Open a WebSocket connection"),
 ],
 "MEM": [
  ("TOOL-070","memory_store","Store an entry in memory"),
  ("TOOL-071","memory_recall","Recall a memory entry"),
  ("TOOL-072","memory_search","Semantic search over memory"),
  ("TOOL-073","memory_delete","Delete a memory entry"),
  ("TOOL-074","memory_list","List memory entries"),
 ],
 "PKG": [
  ("TOOL-080","npm_install","Install npm packages"),
  ("TOOL-081","pip_install","Install pip packages"),
  ("TOOL-082","package_list","List installed packages"),
  ("TOOL-083","package_remove","Remove an installed package"),
 ],
 "WS": [
  ("TOOL-090","workspace_create","Create a new workspace"),
  ("TOOL-091","workspace_switch","Switch the active workspace"),
  ("TOOL-092","workspace_list","List all workspaces"),
  ("TOOL-093","workspace_archive","Archive a workspace"),
  ("TOOL-094","workspace_delete","Delete a workspace and its data"),
  ("TOOL-095","workspace_export","Export a workspace archive"),
  ("TOOL-096","workspace_import","Import a workspace archive"),
 ],
 "AI": [
  ("TOOL-100","ai_complete","Generate a completion from an AI provider"),
  ("TOOL-101","ai_embed","Generate embeddings for text"),
  ("TOOL-102","ai_image_generate","Generate an image from a prompt"),
  ("TOOL-103","ai_image_analyze","Analyze an image with vision"),
 ],
 "MAG": [
  ("TOOL-110","agent_create","Create a new agent"),
  ("TOOL-111","agent_delegate","Delegate a task to another agent"),
  ("TOOL-112","agent_status","Get agent status"),
  ("TOOL-113","agent_list","List agents in the workspace"),
 ],
 "PLG": [
  ("TOOL-120","plugin_install","Install a plugin"),
  ("TOOL-121","plugin_uninstall","Uninstall a plugin with cleanup"),
  ("TOOL-122","plugin_configure","Configure a plugin"),
  ("TOOL-123","plugin_list","List installed plugins"),
 ],
 "WF": [
  ("TOOL-130","workflow_create","Create a workflow definition"),
  ("TOOL-131","workflow_run","Run a workflow"),
  ("TOOL-132","workflow_schedule","Schedule a workflow"),
  ("TOOL-133","workflow_history","View workflow execution history"),
 ],
}

# ------------------------------------------------------- new tools (IDs assigned)
NEW = {
 "FILE": [
  ("file_read_binary","Read binary file content as base64"),
  ("file_write_binary","Write base64 content to a binary file"),
  ("file_chmod","Change file permissions"),
  ("file_touch","Create an empty file or update timestamp"),
  ("file_head","Read the first N lines of a file"),
  ("file_tail","Read the last N lines of a file"),
  ("file_checksum","Compute a file checksum (SHA-256/MD5)"),
  ("file_zip","Compress files/directories into an archive"),
  ("file_unzip","Extract an archive into the sandbox"),
  ("file_watch","Watch a path for changes"),
  ("file_symlink","Create or inspect a symbolic link"),
 ],
 "WS": [
  ("workspace_get","Get workspace details"),
  ("workspace_configure","Update workspace settings"),
  ("workspace_stats","Workspace usage statistics"),
  ("workspace_duplicate","Duplicate a workspace"),
  ("workspace_templates","List workspace templates"),
 ],
 "CODE": [
  ("code_index","Build a code index for the workspace"),
  ("code_symbols","List symbols in a file or project"),
  ("code_symbol_info","Get symbol definition and details"),
  ("code_references","Find references to a symbol"),
  ("code_callers","Find callers of a function"),
  ("code_rename","Rename a symbol across the project"),
  ("code_explain","Explain code in natural language"),
  ("code_generate","Generate code from a description"),
  ("code_refactor","Apply AI-assisted refactoring"),
  ("code_review","Review code for issues"),
  ("code_search","Semantic code search"),
  ("code_complete","Inline code completion"),
  ("code_convert","Translate code between languages"),
  ("code_metrics","Compute code complexity metrics"),
  ("code_dependencies","Analyze module dependencies"),
  ("code_calls","Trace the call graph"),
  ("code_compare","Compare two versions of code"),
  ("code_fix","Suggest fixes for code errors"),
 ],
 "SEAR": [
  ("search_glob","Find files by glob pattern"),
  ("search_history","Search execution and command history"),
  ("search_workspace","Search across the active workspace"),
  ("search_web","Search the web via configured provider"),
  ("search_tools","Discover tools by name or capability"),
 ],
 "TERM": [
  ("terminal_session_create","Create a new internal terminal session"),
  ("terminal_session_list","List active terminal sessions"),
  ("terminal_session_kill","Terminate a terminal session"),
  ("terminal_stdin","Write input to a running process"),
  ("terminal_wait","Wait for a process to exit and return status"),
  ("terminal_history","Read persistent command history"),
 ],
 "GIT": [
  ("git_fetch","Fetch from a remote"),
  ("git_remote","Manage git remotes"),
  ("git_tag","Create, list, or delete tags"),
  ("git_reset","Reset working tree or HEAD"),
  ("git_revert","Revert a commit"),
  ("git_clean","Remove untracked files"),
  ("git_blame","Show line-by-line authorship"),
 ],
 "PKG": [
  ("package_update","Update installed packages"),
  ("package_info","Show package details"),
  ("package_install","Install a package via generic manager"),
  ("package_audit","Audit packages for known vulnerabilities"),
  ("package_search","Search package registries"),
 ],
 "BUILD": [
  ("build_run","Run the project build"),
  ("build_compile","Compile project sources"),
  ("build_clean","Clean build outputs"),
  ("build_config","List build configurations"),
  ("build_report","Generate a build report"),
  ("build_verify","Verify build artifact integrity"),
  ("build_install","Install a build artifact"),
  ("build_archive","Archive build artifacts"),
  ("build_gradle","Invoke a Gradle task"),
  ("build_make","Invoke a Make target"),
 ],
 "TEST": [
  ("test_run","Run the test suite"),
  ("test_run_file","Run tests in a file"),
  ("test_case","Run a single test case"),
  ("test_coverage","Measure test coverage"),
  ("test_report","Generate a test report"),
  ("test_failures","List failing tests"),
  ("test_rerun","Rerun failed tests"),
  ("test_generate","Generate tests for code"),
  ("test_benchmark","Run benchmarks"),
  ("test_performance","Profile test performance"),
  ("test_smoke","Run smoke tests"),
  ("test_integration","Run integration tests"),
  ("test_e2e","Run end-to-end tests"),
 ],
 "DEBUG": [
  ("debug_breakpoint","Set a breakpoint"),
  ("debug_remove_breakpoint","Remove a breakpoint"),
  ("debug_list_breakpoints","List breakpoints"),
  ("debug_continue","Continue execution"),
  ("debug_step_over","Step over"),
  ("debug_step_into","Step into"),
  ("debug_step_out","Step out"),
  ("debug_inspect","Inspect a variable or expression"),
  ("debug_stack","Show the stack trace"),
  ("debug_attach","Attach to a running process"),
  ("debug_logcat","Read Android logcat output"),
  ("debug_heap","Inspect heap and objects"),
  ("debug_dump","Dump process memory or state"),
  ("debug_evaluate","Evaluate an expression in context"),
  ("debug_exception","Inspect an exception or break on throw"),
 ],
 "FMT": [
  ("format_code","Format a code snippet"),
  ("format_file","Format a file"),
  ("format_project","Format the whole project"),
  ("format_check","Verify formatting compliance"),
  ("format_config","Get or set formatter configuration"),
  ("lint_run","Run the linter"),
  ("lint_fix","Auto-fix lint issues"),
  ("lint_report","Generate a lint report"),
 ],
 "DOC": [
  ("doc_generate","Generate documentation"),
  ("doc_update","Update existing documentation"),
  ("doc_comment","Add doc comments to code"),
  ("doc_readme","Generate a README"),
  ("doc_api","Generate an API reference"),
  ("doc_changelog","Update the changelog"),
  ("doc_search","Search documentation"),
  ("doc_translate","Translate documentation"),
 ],
 "BRW": [
  ("browser_open","Open a URL in the embedded browser"),
  ("browser_html","Get raw page HTML"),
  ("browser_extract","Extract page text and content"),
  ("browser_screenshot","Capture a page screenshot"),
  ("browser_click","Click an element"),
  ("browser_type","Type into a form field"),
  ("browser_select","Select a dropdown option"),
  ("browser_scroll","Scroll the page"),
  ("browser_back","Navigate back in history"),
  ("browser_forward","Navigate forward in history"),
  ("browser_wait","Wait for an element or condition"),
  ("browser_evaluate","Evaluate JavaScript in the page"),
  ("browser_cookies","Manage browser cookies"),
  ("browser_find","Find an element by selector"),
  ("browser_downloads","List or download browser files"),
 ],
 "NET": [
  ("http_head","Perform an HTTP HEAD request"),
  ("http_patch","Perform an HTTP PATCH request"),
  ("http_request","Raw HTTP request with full control"),
  ("http_download","Download a file into the sandbox"),
  ("http_upload","Upload a file via HTTP"),
  ("http_cookies","Manage the HTTP cookie jar"),
  ("dns_lookup","Resolve DNS records"),
  ("tcp_probe","Test TCP connectivity to a host and port"),
 ],
 "DB": [
  ("sqlite_query","Run a SELECT query"),
  ("sqlite_execute","Run INSERT/UPDATE/DELETE statements"),
  ("sqlite_create","Create a SQLite database"),
  ("sqlite_migrate","Run a schema migration"),
  ("sqlite_schema","Show the database schema"),
  ("sqlite_backup","Back up a database"),
  ("sqlite_restore","Restore a database from backup"),
  ("sqlite_import","Import CSV or JSON data"),
  ("sqlite_export","Export a table to CSV or JSON"),
  ("sqlite_index","Manage database indexes"),
  ("sqlite_vacuum","Vacuum the database"),
  ("sqlite_transaction","Begin, commit, or roll back a transaction"),
  ("sqlite_attach","Attach a secondary database"),
  ("sqlite_analyze","Analyze query plans"),
  ("sqlite_vector","Vector similarity search (extension)"),
 ],
 "MEM": [
  ("memory_summarize","Summarize memory content"),
  ("memory_export","Export memory to a file"),
  ("memory_import","Import memory from a file"),
  ("memory_prune","Prune stale or low-relevance entries"),
  ("memory_tag","Add or remove tags on memory entries"),
  ("memory_stats","Memory usage statistics"),
 ],
 "AI": [
  ("ai_stream","Stream a completion token by token"),
  ("ai_transcribe","Transcribe audio to text"),
  ("ai_speech","Synthesize speech from text"),
  ("ai_moderate","Run a content moderation check"),
  ("ai_rerank","Rerank documents by relevance"),
  ("ai_models","List available models for a provider"),
 ],
 "DEV": [
  ("device_info","Device and OS information"),
  ("device_storage","App storage usage"),
  ("device_battery","Battery status"),
  ("device_network","Connectivity status"),
  ("device_contacts","Read contacts (permission required)"),
  ("device_notification","Post a notification"),
  ("device_media","Access the media library (permission)"),
  ("device_camera","Capture a photo (permission required)"),
  ("device_audio","Record audio (permission required)"),
  ("device_clipboard","Read or write the clipboard"),
  ("device_sms","Send or read SMS (permission required)"),
  ("device_calendar","Read or create calendar events"),
  ("device_location","Get device location (permission required)"),
  ("device_share","Share content via the system share sheet"),
  ("device_documents","Access DocumentsProvider files"),
 ],
 "PM": [
  ("task_create","Create a task"),
  ("task_update","Update a task"),
  ("task_list","List tasks"),
  ("task_status","Get task status"),
  ("task_assign","Assign a task to an agent"),
  ("task_priority","Set task priority"),
  ("task_complete","Mark a task complete"),
  ("task_comment","Add a comment to a task"),
  ("project_plan","Create a project plan"),
  ("project_milestone","Manage milestones"),
 ],
 "SEC": [
  ("security_scan","Scan for vulnerabilities"),
  ("security_audit","Run a security audit"),
  ("security_permissions","Check tool and agent permissions"),
  ("security_encrypt","Encrypt a file or data"),
  ("security_decrypt","Decrypt a file or data"),
  ("security_hash","Compute a cryptographic hash"),
  ("security_sign","Sign data or verify a signature"),
  ("security_secrets","Scan files for secrets and keys"),
  ("security_policy","List security policies"),
  ("security_quarantine","Quarantine a suspicious file"),
  ("security_cert","Inspect certificates"),
  ("security_keychain","Manage app keys in the keystore"),
  ("security_revoke","Revoke a session or token"),
  ("security_vault","Store or retrieve a secret in the vault"),
  ("security_policy_check","Evaluate a policy for an action"),
 ],
 "OBS": [
  ("obs_logs","Read execution logs"),
  ("obs_metrics","Get performance metrics"),
  ("obs_trace","Get an execution trace"),
  ("obs_events","Subscribe to the event stream"),
  ("obs_history","Execution history"),
  ("obs_tool_calls","Tool invocation records"),
  ("obs_token_usage","Token usage per request and session"),
  ("obs_api_usage","Provider API usage statistics"),
  ("obs_errors","Error reports"),
  ("obs_audit","Audit trail"),
  ("obs_export","Export a diagnostics bundle"),
  ("obs_performance","Profile app performance"),
  ("obs_search","Search logs and events"),
  ("obs_sessions","List agent sessions"),
  ("obs_snapshot","Capture a state snapshot"),
 ],
 "IO": [
  ("io_import_project","Import a project archive"),
  ("io_export_project","Export a project archive"),
  ("io_import_archive","Import a workspace archive"),
  ("io_export_archive","Export a workspace archive"),
  ("io_import_backup","Restore from a backup"),
  ("io_export_backup","Create a backup"),
  ("io_import_data","Import structured data"),
  ("io_export_data","Export structured data"),
  ("io_export_report","Export an execution report"),
  ("io_share_file","Share a file via the Android share sheet"),
  ("io_import_snapshot","Import a sandbox snapshot"),
  ("io_export_snapshot","Export a sandbox snapshot"),
  ("io_export_manifest","Export a workspace manifest"),
 ],
 "PLG": [
  ("plugin_update","Update an installed plugin"),
  ("plugin_enable","Enable a plugin"),
  ("plugin_disable","Disable a plugin"),
  ("plugin_dependencies","Show the plugin dependency graph"),
  ("plugin_pack","Package a plugin for distribution"),
  ("plugin_inspect","Inspect plugin manifest and metadata"),
 ],
 "MAG": [
  ("agent_update","Update an agent configuration"),
  ("agent_delete","Delete an agent"),
  ("agent_configure","Configure agent tools, memory, and permissions"),
  ("agent_memory","Inspect an agent's memory"),
  ("agent_cancel","Cancel a running agent"),
  ("agent_broadcast","Send a message to all agents"),
 ],
 "WF": [
  ("workflow_cancel","Cancel a running workflow"),
  ("workflow_pause","Pause a workflow"),
  ("workflow_resume","Resume a paused workflow"),
  ("workflow_status","Get workflow execution status"),
  ("workflow_templates","List workflow templates"),
  ("workflow_validate","Validate a workflow definition"),
 ],
}

# ------------------------------------------------- matrix: legacy name -> new name
LEGACY = {
 "shell_execute": "terminal_run",
 "shell_background": "terminal_run_background",
 "command_history": "terminal_history",
 "browser_navigate": "browser_open",
 "db_query": "sqlite_query",
 "db_execute": "sqlite_execute",
 "db_schema": "sqlite_schema",
 "ai_analyze_image": "ai_image_analyze",
 "system_info": "device_info",
}

# --------------------------------------------------- extra tools (explicit IDs)
# Appended with fixed IDs so previously generated TOOL-IDs never shift.
EXTRA = {
 "FILE": [
  ("TOOL-381", "file_history", "List version history of a file"),
  ("TOOL-382", "file_restore", "Restore a file to a previous version"),
 ],
 "MEM": [
  ("TOOL-383", "memory_tool_history", "Query tool invocation history"),
  ("TOOL-384", "memory_preferences", "Get or set learned user preferences"),
  ("TOOL-385", "memory_graph_query", "Query the knowledge graph (entities, relationships)"),
  ("TOOL-386", "memory_graph_build", "Extract entities and relationships into the knowledge graph"),
 ],
}

# ----------------------------------------------------------- capability defaults
READ_ONLY_WORDS = ("read","list","get","search","status","info","log","history",
                   "stats","inspect","schema","diff","show","view","find","models",
                   "templates","failures","breakpoints","downloads","tool_calls",
                   "token_usage","api_usage","errors","audit","permissions",
                   "symbols","callers","references","metrics","dependencies",
                   "sessions","analyze","blame","symbol_info","trace","history")

def caps_for(cat, name):
    """Return (read, write, network, android, background, perm, agent, sandbox, stream)."""
    ro = any(w in name for w in READ_ONLY_WORDS) and "write" not in name \
         and "create" not in name and "generate" not in name and "store" not in name \
         and "import" not in name and "export" not in name and "commit" not in name \
         and "add" not in name and "update" not in name and "delete" not in name \
         and "remove" not in name and "kill" not in name and "run" not in name \
         and "install" not in name and "exec" not in name and "move" not in name \
         and "copy" not in name and "rename" not in name and "convert" not in name \
         and "fix" not in name and "refactor" not in name and "click" not in name \
         and "type" not in name and "select" not in name and "scroll" not in name \
         and "evaluate" not in name and "open" not in name and "send" not in name \
         and "share" not in name and "trigger" not in name and "migrate" not in name \
         and "attach" not in name and "vacuum" not in name
    read  = "✓" if (ro or cat in ("SEAR","OBS","CODE")) else ("✓" if cat in ("FILE","GIT","NET","MEM","AI","BRW","DB","DOC") else "—")
    write = "—" if ro else "✓"
    if cat in ("SEAR",): write = "—"
    network = "✓" if cat in ("NET","BRW") else ("✓" if name.startswith(("http_","dns_","tcp_","websocket","git_push","git_pull","git_clone","npm_","pip_","package_","io_import","io_export","io_clone")) else "—")
    android = "✓" if cat == "DEV" else "—"
    background = "✓" if name in ("terminal_run_background","terminal_wait","obs_events","workflow_schedule") else "—"
    perm = {"FILE":"Low","WS":"Low","CODE":"Medium","SEAR":"Low","TERM":"High","GIT":"Medium",
            "PKG":"High","BUILD":"High","TEST":"Medium","DEBUG":"High","FMT":"Low","DOC":"Low",
            "BRW":"High","NET":"High","DB":"Medium","MEM":"Low","AI":"Medium","DEV":"High",
            "PM":"Low","SEC":"High","OBS":"Low","IO":"Medium","PLG":"High","MAG":"Medium","WF":"Medium"}[cat]
    if name in ("file_delete","workspace_delete","git_push","git_pull","terminal_kill",
                "debug_attach","debug_dump","security_scan","io_import_backup") : perm = "High"
    if name in ("file_write","file_append","file_delete","file_move","file_copy","file_chmod",
                "git_commit","git_reset","git_revert","git_clean","git_merge","sqlite_execute",
                "sqlite_migrate","format_file","format_project","lint_fix","browser_open",
                "browser_click","browser_type","io_export_workspace","workspace_delete"):
        pass
    sandbox = "✓" if cat in ("TERM","PKG","BUILD","TEST","DEBUG","FMT","DOC","DB","CODE") else \
              ("✓" if name.startswith(("file_","git_","http_download","browser_","sqlite_")) else "—")
    stream  = "✓" if name in ("terminal_run","terminal_run_script","http_get","http_post",
                              "http_request","ai_complete","ai_stream","ai_transcribe",
                              "ai_speech","ai_image_analyze","obs_events","test_run") else "—"
    return read, write, network, android, background, perm, sandbox, stream

# ---------------------------------------------------------------- build catalog
def build_catalog():
    tools = []  # (id, name, desc, cat, phase)
    nxt = 134
    for key, label, phase in CATS:
        for tid, name, desc in EXISTING.get(key, []):
            tools.append((tid, name, desc, key, phase))
        for name, desc in NEW.get(key, []):
            tools.append((f"TOOL-{nxt:03d}", name, desc, key, phase))
            nxt += 1
        for tid, name, desc in EXTRA.get(key, []):
            tools.append((tid, name, desc, key, phase))
    return tools

# ---------------------------------------------------------- render TOOLS.md
def render_catalog(tools):
    by_cat = {}
    for t in tools: by_cat.setdefault(t[3], []).append(t)
    lines = []
    lines.append("# Tool Registry — Nexora")
    lines.append("")
    lines.append("> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See [docs/api/Tool-API.md](../docs/api/Tool-API.md) for the Tool API.")
    lines.append(">")
    lines.append("> **Authoritative catalog of every registered tool.** Stable IDs per [DL-017](../docs/DECISION_LOG.md).")
    lines.append("> Canonical tool names live here; [TOOL_MATRIX.md](./TOOL_MATRIX.md) maps capabilities per tool.")
    lines.append("")
    lines.append("## Category Index")
    lines.append("")
    lines.append("| # | Category | Prefix | Tools | Phase |")
    lines.append("|---|----------|--------|-------|-------|")
    for i, (key, label, phase) in enumerate(CATS, 1):
        lines.append(f"| {i} | {label} | {key} | {len(by_cat.get(key,[]))} | {phase} |")
    lines.append("")
    lines.append(f"**Total registered tools: {len(tools)}** (target: 300–500, see [PRODUCT_VISION.md](../docs/PRODUCT_VISION.md)).")
    lines.append("")
    for key, label, phase in CATS:
        lines.append(f"## {label} ({key})")
        lines.append("")
        lines.append("| ID | Tool | Description | Phase | Status |")
        lines.append("|----|------|-------------|-------|--------|")
        for tid, name, desc, _, ph in by_cat[key]:
            lines.append(f"| {tid} | {name} | {desc} | {ph} | Planned |")
        lines.append("")
    return "\n".join(lines)

# ---------------------------------------------------------- render TOOL_MATRIX.md
def parse_existing_matrix():
    """Extract legacy rows: {old_name: (R,W,N,A,B,perm,agent,sandbox,stream)}."""
    rows = {}
    txt = MATRIX.read_text()
    for line in txt.splitlines():
        m = re.match(r"\|\s*`([a-z_]+)`\s*\|\s*[^|]*\|\s*[^|]*\|\s*([✓—])\s*\|\s*([✓—])\s*\|\s*([✓—])\s*\|\s*([✓—])\s*\|\s*([✓—])\s*\|\s*(\w+)\s*\|\s*([✓—])\s*\|\s*([✓—])\s*\|\s*([✓—])\s*\|\s*[\d]+\s*\|", line)
        if m:
            rows[m.group(1)] = m.groups()[1:]
    return rows

# ------------------------------------------------- agent capability matrix
# (id, name, Plan, Execute, Review, Code, Browser, Memory, Terminal, MultiAgent, Delegate, Background, Streaming, Phase)
AGENTS = [
 ("AGT-001", "Planner",              "✓","—","✓","—","—","✓","—","—","✓","—","✓",7),
 ("AGT-002", "Researcher",           "✓","✓","✓","—","✓","✓","—","—","—","✓","✓",7),
 ("AGT-003", "Coder",                "✓","✓","✓","✓","—","✓","✓","—","—","✓","✓",7),
 ("AGT-004", "Reviewer",             "—","✓","✓","✓","—","✓","—","—","—","—","✓",7),
 ("AGT-005", "Tester",               "—","✓","✓","✓","—","—","✓","—","—","✓","✓",7),
 ("AGT-006", "Debugger",             "✓","✓","✓","✓","—","✓","✓","—","—","✓","—",7),
 ("AGT-007", "Documentation Writer", "—","✓","✓","—","—","✓","—","—","—","—","✓",7),
 ("AGT-008", "Refactoring Agent",    "✓","✓","✓","✓","—","✓","—","—","—","—","—",7),
 ("AGT-009", "Deployment Agent",     "✓","✓","✓","—","—","—","✓","—","—","✓","✓",7),
 ("AGT-010", "Security Auditor",     "✓","✓","✓","—","—","—","✓","—","—","✓","—",7),
 ("AGT-011", "Browser Agent",        "—","✓","✓","—","✓","✓","—","—","—","—","✓",7),
 ("AGT-012", "Database Agent",       "✓","✓","✓","—","—","✓","—","—","—","—","✓",7),
 ("AGT-013", "File Manager",         "—","✓","✓","—","—","✓","—","—","—","—","—",7),
 ("AGT-014", "Git Agent",            "✓","✓","✓","—","—","✓","✓","—","—","✓","—",7),
 ("AGT-015", "Workflow Coordinator", "✓","—","✓","—","—","✓","—","✓","✓","—","✓",7),
]

def render_agent_matrix():
    lines = []
    lines.append("# Nexora Agent Capability Matrix")
    lines.append("")
    lines.append("> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See [AGENTS.md](./AGENTS.md)")
    lines.append(">")
    lines.append("Authoritative reference mapping **every agent type** (see [AGENTS.md](./AGENTS.md)) to its permitted capabilities. The orchestrator enforces these constraints at dispatch time. Agents may only invoke tools and actions marked with ✓. Generated from the agent catalog; keep in sync with `registry/AGENTS.md`.")
    lines.append("")
    lines.append("## Legend")
    lines.append("")
    lines.append("| Symbol | Meaning |")
    lines.append("|--------|---------|")
    lines.append("| ✓ | Supported |")
    lines.append("| — | Not supported |")
    lines.append("")
    lines.append("## Matrix")
    lines.append("")
    lines.append("| Agent ID | Agent Name | Plan | Execute | Review | Code | Browser | Memory | Terminal | Multi-Agent | Delegate | Background | Streaming | Phase |")
    lines.append("|----------|------------|------|---------|--------|------|---------|--------|----------|-------------|----------|------------|-----------|-------|")
    for a in AGENTS:
        lines.append("| " + " | ".join(str(x) for x in a) + " |")
    lines.append("")
    lines.append("## Capability Definitions")
    lines.append("")
    lines.append("| Capability | Description |")
    lines.append("|------------|-------------|")
    lines.append("| **Plan** | Create and modify execution plans, break down tasks |")
    lines.append("| **Execute** | Directly invoke tools to perform actions on the system |")
    lines.append("| **Review** | Inspect results, validate output, self-correct |")
    lines.append("| **Code** | Read, write, and execute code (file + terminal tools) |")
    lines.append("| **Browser** | Control the headless browser for web interaction |")
    lines.append("| **Memory** | Store, retrieve, and manage persistent memory entries |")
    lines.append("| **Terminal** | Execute shell commands directly |")
    lines.append("| **Multi-Agent** | Spawn and coordinate child agents |")
    lines.append("| **Delegate** | Assign subtasks to other agent types |")
    lines.append("| **Background** | Run long-lived tasks without blocking the UI thread |")
    lines.append("| **Streaming** | Emit incremental results via token or event streams |")
    lines.append("")
    lines.append("## Phase Rollout")
    lines.append("")
    lines.append("- **Phase 7** — All 15 agent types, agent registry, task delegation (see [AGENTS.md](./AGENTS.md)).")
    lines.append("- **Phase 8** — Community agent plugins.")
    lines.append("")
    lines.append("## Execution Depth")
    lines.append("")
    lines.append("Agents have a configurable `maxExecutionDepth` (default 10) that limits nested tool calls per turn. Orchestrator agents (AGT-015) enforce depth 3 on delegated children.")
    lines.append("")
    return "\n".join(lines)

def render_matrix(tools):
    legacy = parse_existing_matrix()
    lines = []
    lines.append("# Nexora Tool Capability Matrix")
    lines.append("")
    lines.append("> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See [TOOLS.md](./TOOLS.md)")
    lines.append(">")
    lines.append("Authoritative reference mapping **every registered tool** (see [TOOLS.md](./TOOLS.md)) to its supported capabilities. Used by the sandbox controller, permission system, and agent scheduler to determine which tools an agent may invoke. Generated from the tool catalog; hand-tuned rows are preserved.")
    lines.append("")
    lines.append("## Legend")
    lines.append("")
    lines.append("| Symbol | Meaning |")
    lines.append("|--------|---------|")
    lines.append("| ✓ | Supported |")
    lines.append("| — | Not supported |")
    lines.append("")
    lines.append("## Matrix")
    lines.append("")
    lines.append("| Tool ID | Tool Name | Category | Read | Write | Network | Android API | Background | Permission Level | Agent-Usable | Sandbox-Required | Streaming | Phase |")
    lines.append("|---------|-----------|----------|------|-------|---------|-------------|------------|-----------------|--------------|------------------|-----------|-------|")
    order = {c: i for i, (c, _, _) in enumerate(CATS)}
    for tid, name, desc, cat, phase in sorted(tools, key=lambda t: (order[t[3]], t[0])):
        old = next((k for k in legacy if k == name or LEGACY.get(k) == name), None)
        if old:
            r, w, n, a, b, p, au, s, x = legacy[old]
        else:
            r, w, n, a, b, p, s, x = caps_for(cat, name)
            au = "✓"
        label = {c[0]: c[1] for c in CATS}[cat]
        lines.append(f"| `{name}` | {name.replace('_',' ').title()} | {label} | {r} | {w} | {n} | {a} | {b} | {p} | {au} | {s} | {x} | {phase} |")
    lines.append("")
    lines.append("## Permission Levels")
    lines.append("")
    lines.append("| Level | Description |")
    lines.append("|-------|-------------|")
    lines.append("| Low | Read-only or non-destructive |")
    lines.append("| Medium | Destructive or network-dependent |")
    lines.append("| High | System-level or irreversible |")
    lines.append("")
    lines.append("## Phase Availability")
    lines.append("")
    lines.append("Per-tool phases are defined in [TOOLS.md](./TOOLS.md). Phases: 1 (Android foundation) · 4 (tools) · 5 (AI providers) · 6 (memory/workflows) · 7 (multi-agent) · 8 (plugins) · Later (advanced tool categories).")
    lines.append("")
    return "\n".join(lines)

def main():
    tools = build_catalog()
    CATALOG.write_text(render_catalog(tools))
    MATRIX.write_text(render_matrix(tools))
    AGENT_MATRIX = ROOT / "registry" / "AGENT_MATRIX.md"
    AGENT_MATRIX.write_text(render_agent_matrix())
    by = {}
    for t in tools: by[t[3]] = by.get(t[3], 0) + 1
    print(f"Total tools: {len(tools)}")
    for key, label, _ in CATS:
        print(f"  {key:6s} {label:22s} {by.get(key,0)}")
    print("Wrote:", CATALOG)
    print("Wrote:", MATRIX)
    print("Wrote:", AGENT_MATRIX)

if __name__ == "__main__":
    main()
