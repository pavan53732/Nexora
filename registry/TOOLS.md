# Tool Registry — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See [docs/api/Tool-API.md](../docs/api/Tool-API.md) for the Tool API.
>
> **Authoritative catalog of every registered tool.** Stable IDs per [DL-017](../docs/DECISION_LOG.md).
> Canonical tool names live here; [TOOL_MATRIX.md](./TOOL_MATRIX.md) maps capabilities per tool.

## Category Index

| # | Category | Prefix | Tools | Phase |
|---|----------|--------|-------|-------|
| 1 | File System | FILE | 24 | 4 |
| 2 | Workspace | WS | 17 | 1 |
| 3 | Code Intelligence | CODE | 18 | Later |
| 4 | Search | SEAR | 9 | 4 |
| 5 | Terminal | TERM | 11 | 4 |
| 6 | Git | GIT | 19 | 4 |
| 7 | Package Manager | PKG | 9 | 4 |
| 8 | Build | BUILD | 10 | Later |
| 9 | Testing | TEST | 13 | Later |
| 10 | Debugging | DEBUG | 15 | Later |
| 11 | Formatting | FMT | 8 | Later |
| 12 | Documentation | DOC | 8 | Later |
| 13 | Browser | BRW | 15 | Later |
| 14 | Network/API | NET | 13 | 4 |
| 15 | Database | DB | 15 | Later |
| 16 | Memory | MEM | 15 | 6 |
| 17 | AI | AI | 10 | 5 |
| 18 | Android Device | DEV | 15 | Later |
| 19 | Project Management | PM | 10 | Later |
| 20 | Security | SEC | 17 | Later |
| 21 | Observability | OBS | 15 | Later |
| 22 | Import/Export | IO | 13 | Later |
| 23 | Plugin | PLG | 10 | 8 |
| 24 | Multi-Agent | MAG | 10 | 7 |
| 25 | Workflow | WF | 10 | 6 |

**Total registered tools: 329** (target: 300–500, see [PRODUCT_VISION.md](../docs/PRODUCT_VISION.md)).

## File System (FILE)

| ID | Tool | Description | Phase | Status |
|----|------|-------------|-------|--------|
| TOOL-001 | file_read | Read a file's content from the virtual file system | 4 | Planned |
| TOOL-002 | file_write | Create or overwrite a file | 4 | Planned |
| TOOL-003 | file_append | Append content to an existing file | 4 | Planned |
| TOOL-004 | file_delete | Delete a file | 4 | Planned |
| TOOL-005 | file_list | List directory contents with metadata | 4 | Planned |
| TOOL-006 | file_create_dir | Create a directory (recursive) | 4 | Planned |
| TOOL-007 | file_move | Move or rename a file or directory | 4 | Planned |
| TOOL-008 | file_copy | Copy a file or directory | 4 | Planned |
| TOOL-009 | file_exists | Check whether a path exists | 4 | Planned |
| TOOL-010 | file_info | Get file metadata (size, type, mtime) | 4 | Planned |
| TOOL-011 | file_search | Search files by name pattern | 4 | Planned |
| TOOL-134 | file_read_binary | Read binary file content as base64 | 4 | Planned |
| TOOL-135 | file_write_binary | Write base64 content to a binary file | 4 | Planned |
| TOOL-136 | file_chmod | Change file permissions | 4 | Planned |
| TOOL-137 | file_touch | Create an empty file or update timestamp | 4 | Planned |
| TOOL-138 | file_head | Read the first N lines of a file | 4 | Planned |
| TOOL-139 | file_tail | Read the last N lines of a file | 4 | Planned |
| TOOL-140 | file_checksum | Compute a file checksum (SHA-256/MD5) | 4 | Planned |
| TOOL-141 | file_zip | Compress files/directories into an archive | 4 | Planned |
| TOOL-142 | file_unzip | Extract an archive into the sandbox | 4 | Planned |
| TOOL-143 | file_watch | Watch a path for changes | 4 | Planned |
| TOOL-144 | file_symlink | Create or inspect a symbolic link | 4 | Planned |
| TOOL-381 | file_history | List version history of a file | 4 | Planned |
| TOOL-382 | file_restore | Restore a file to a previous version | 4 | Planned |

## Workspace (WS)

| ID | Tool | Description | Phase | Status |
|----|------|-------------|-------|--------|
| TOOL-090 | workspace_create | Create a new workspace | 1 | Planned |
| TOOL-091 | workspace_switch | Switch the active workspace | 1 | Planned |
| TOOL-092 | workspace_list | List all workspaces | 1 | Planned |
| TOOL-093 | workspace_archive | Archive a workspace | 1 | Planned |
| TOOL-094 | workspace_delete | Delete a workspace and its data | 1 | Planned |
| TOOL-095 | workspace_export | Export a workspace archive | 1 | Planned |
| TOOL-096 | workspace_import | Import a workspace archive | 1 | Planned |
| TOOL-145 | workspace_get | Get workspace details | 1 | Planned |
| TOOL-146 | workspace_configure | Update workspace settings | 1 | Planned |
| TOOL-147 | workspace_stats | Workspace usage statistics | 1 | Planned |
| TOOL-148 | workspace_duplicate | Duplicate a workspace | 1 | Planned |
| TOOL-149 | workspace_templates | List workspace templates | 1 | Planned |
| TOOL-387 | sandbox_info | Query sandbox state: processes, disk, env, quotas, network rules | 3 | Planned |
| TOOL-388 | sandbox_reset | Reset a workspace sandbox to a clean state | 3 | Planned |
| TOOL-389 | sandbox_snapshot | Create a full workspace snapshot | 4 | Planned |
| TOOL-390 | sandbox_restore | Restore a workspace to a previous snapshot | 4 | Planned |
| TOOL-391 | sandbox_templates | List and apply sandbox environment templates | 3 | Planned |

## Code Intelligence (CODE)

| ID | Tool | Description | Phase | Status |
|----|------|-------------|-------|--------|
| TOOL-150 | code_index | Build a code index for the workspace | Later | Planned |
| TOOL-151 | code_symbols | List symbols in a file or project | Later | Planned |
| TOOL-152 | code_symbol_info | Get symbol definition and details | Later | Planned |
| TOOL-153 | code_references | Find references to a symbol | Later | Planned |
| TOOL-154 | code_callers | Find callers of a function | Later | Planned |
| TOOL-155 | code_rename | Rename a symbol across the project | Later | Planned |
| TOOL-156 | code_explain | Explain code in natural language | Later | Planned |
| TOOL-157 | code_generate | Generate code from a description | Later | Planned |
| TOOL-158 | code_refactor | Apply AI-assisted refactoring | Later | Planned |
| TOOL-159 | code_review | Review code for issues | Later | Planned |
| TOOL-160 | code_search | Semantic code search | Later | Planned |
| TOOL-161 | code_complete | Inline code completion | Later | Planned |
| TOOL-162 | code_convert | Translate code between languages | Later | Planned |
| TOOL-163 | code_metrics | Compute code complexity metrics | Later | Planned |
| TOOL-164 | code_dependencies | Analyze module dependencies | Later | Planned |
| TOOL-165 | code_calls | Trace the call graph | Later | Planned |
| TOOL-166 | code_compare | Compare two versions of code | Later | Planned |
| TOOL-167 | code_fix | Suggest fixes for code errors | Later | Planned |

## Search (SEAR)

| ID | Tool | Description | Phase | Status |
|----|------|-------------|-------|--------|
| TOOL-030 | search_text | Search file contents for text | 4 | Planned |
| TOOL-031 | search_regex | Search file contents with a regex | 4 | Planned |
| TOOL-032 | grep | Run grep over workspace files | 4 | Planned |
| TOOL-033 | find | Find files by name and attributes | 4 | Planned |
| TOOL-168 | search_glob | Find files by glob pattern | 4 | Planned |
| TOOL-169 | search_history | Search execution and command history | 4 | Planned |
| TOOL-170 | search_workspace | Search across the active workspace | 4 | Planned |
| TOOL-171 | search_web | Search the web via configured provider | 4 | Planned |
| TOOL-172 | search_tools | Discover tools by name or capability | 4 | Planned |

## Terminal (TERM)

| ID | Tool | Description | Phase | Status |
|----|------|-------------|-------|--------|
| TOOL-020 | terminal_run | Run a shell command in the sandbox | 4 | Planned |
| TOOL-021 | terminal_run_script | Execute a script file in the sandbox | 4 | Planned |
| TOOL-022 | terminal_run_background | Run a command in the background | 4 | Planned |
| TOOL-023 | terminal_kill | Kill a running process by PID | 4 | Planned |
| TOOL-024 | terminal_list_processes | List running processes | 4 | Planned |
| TOOL-173 | terminal_session_create | Create a new internal terminal session | 4 | Planned |
| TOOL-174 | terminal_session_list | List active terminal sessions | 4 | Planned |
| TOOL-175 | terminal_session_kill | Terminate a terminal session | 4 | Planned |
| TOOL-176 | terminal_stdin | Write input to a running process | 4 | Planned |
| TOOL-177 | terminal_wait | Wait for a process to exit and return status | 4 | Planned |
| TOOL-178 | terminal_history | Read persistent command history | 4 | Planned |

## Git (GIT)

| ID | Tool | Description | Phase | Status |
|----|------|-------------|-------|--------|
| TOOL-040 | git_init | Initialize a Git repository | 4 | Planned |
| TOOL-041 | git_clone | Clone a remote repository | 4 | Planned |
| TOOL-042 | git_add | Stage files for commit | 4 | Planned |
| TOOL-043 | git_commit | Commit staged changes | 4 | Planned |
| TOOL-044 | git_push | Push commits to a remote | 4 | Planned |
| TOOL-045 | git_pull | Pull and merge from a remote | 4 | Planned |
| TOOL-046 | git_branch | Create, list, delete, or switch branches | 4 | Planned |
| TOOL-047 | git_merge | Merge branches | 4 | Planned |
| TOOL-048 | git_log | View commit history | 4 | Planned |
| TOOL-049 | git_diff | View file differences | 4 | Planned |
| TOOL-050 | git_status | Show working tree status | 4 | Planned |
| TOOL-051 | git_stash | Stash and unstash changes | 4 | Planned |
| TOOL-179 | git_fetch | Fetch from a remote | 4 | Planned |
| TOOL-180 | git_remote | Manage git remotes | 4 | Planned |
| TOOL-181 | git_tag | Create, list, or delete tags | 4 | Planned |
| TOOL-182 | git_reset | Reset working tree or HEAD | 4 | Planned |
| TOOL-183 | git_revert | Revert a commit | 4 | Planned |
| TOOL-184 | git_clean | Remove untracked files | 4 | Planned |
| TOOL-185 | git_blame | Show line-by-line authorship | 4 | Planned |

## Package Manager (PKG)

| ID | Tool | Description | Phase | Status |
|----|------|-------------|-------|--------|
| TOOL-080 | npm_install | Install npm packages | 4 | Planned |
| TOOL-081 | pip_install | Install pip packages | 4 | Planned |
| TOOL-082 | package_list | List installed packages | 4 | Planned |
| TOOL-083 | package_remove | Remove an installed package | 4 | Planned |
| TOOL-186 | package_update | Update installed packages | 4 | Planned |
| TOOL-187 | package_info | Show package details | 4 | Planned |
| TOOL-188 | package_install | Install a package via generic manager | 4 | Planned |
| TOOL-189 | package_audit | Audit packages for known vulnerabilities | 4 | Planned |
| TOOL-190 | package_search | Search package registries | 4 | Planned |

## Build (BUILD)

| ID | Tool | Description | Phase | Status |
|----|------|-------------|-------|--------|
| TOOL-191 | build_run | Run the project build | Later | Planned |
| TOOL-192 | build_compile | Compile project sources | Later | Planned |
| TOOL-193 | build_clean | Clean build outputs | Later | Planned |
| TOOL-194 | build_config | List build configurations | Later | Planned |
| TOOL-195 | build_report | Generate a build report | Later | Planned |
| TOOL-196 | build_verify | Verify build artifact integrity | Later | Planned |
| TOOL-197 | build_install | Install a build artifact | Later | Planned |
| TOOL-198 | build_archive | Archive build artifacts | Later | Planned |
| TOOL-199 | build_gradle | Invoke a Gradle task | Later | Planned |
| TOOL-200 | build_make | Invoke a Make target | Later | Planned |

## Testing (TEST)

| ID | Tool | Description | Phase | Status |
|----|------|-------------|-------|--------|
| TOOL-201 | test_run | Run the test suite | Later | Planned |
| TOOL-202 | test_run_file | Run tests in a file | Later | Planned |
| TOOL-203 | test_case | Run a single test case | Later | Planned |
| TOOL-204 | test_coverage | Measure test coverage | Later | Planned |
| TOOL-205 | test_report | Generate a test report | Later | Planned |
| TOOL-206 | test_failures | List failing tests | Later | Planned |
| TOOL-207 | test_rerun | Rerun failed tests | Later | Planned |
| TOOL-208 | test_generate | Generate tests for code | Later | Planned |
| TOOL-209 | test_benchmark | Run benchmarks | Later | Planned |
| TOOL-210 | test_performance | Profile test performance | Later | Planned |
| TOOL-211 | test_smoke | Run smoke tests | Later | Planned |
| TOOL-212 | test_integration | Run integration tests | Later | Planned |
| TOOL-213 | test_e2e | Run end-to-end tests | Later | Planned |

## Debugging (DEBUG)

| ID | Tool | Description | Phase | Status |
|----|------|-------------|-------|--------|
| TOOL-214 | debug_breakpoint | Set a breakpoint | Later | Planned |
| TOOL-215 | debug_remove_breakpoint | Remove a breakpoint | Later | Planned |
| TOOL-216 | debug_list_breakpoints | List breakpoints | Later | Planned |
| TOOL-217 | debug_continue | Continue execution | Later | Planned |
| TOOL-218 | debug_step_over | Step over | Later | Planned |
| TOOL-219 | debug_step_into | Step into | Later | Planned |
| TOOL-220 | debug_step_out | Step out | Later | Planned |
| TOOL-221 | debug_inspect | Inspect a variable or expression | Later | Planned |
| TOOL-222 | debug_stack | Show the stack trace | Later | Planned |
| TOOL-223 | debug_attach | Attach to a running process | Later | Planned |
| TOOL-224 | debug_logcat | Read Android logcat output | Later | Planned |
| TOOL-225 | debug_heap | Inspect heap and objects | Later | Planned |
| TOOL-226 | debug_dump | Dump process memory or state | Later | Planned |
| TOOL-227 | debug_evaluate | Evaluate an expression in context | Later | Planned |
| TOOL-228 | debug_exception | Inspect an exception or break on throw | Later | Planned |

## Formatting (FMT)

| ID | Tool | Description | Phase | Status |
|----|------|-------------|-------|--------|
| TOOL-229 | format_code | Format a code snippet | Later | Planned |
| TOOL-230 | format_file | Format a file | Later | Planned |
| TOOL-231 | format_project | Format the whole project | Later | Planned |
| TOOL-232 | format_check | Verify formatting compliance | Later | Planned |
| TOOL-233 | format_config | Get or set formatter configuration | Later | Planned |
| TOOL-234 | lint_run | Run the linter | Later | Planned |
| TOOL-235 | lint_fix | Auto-fix lint issues | Later | Planned |
| TOOL-236 | lint_report | Generate a lint report | Later | Planned |

## Documentation (DOC)

| ID | Tool | Description | Phase | Status |
|----|------|-------------|-------|--------|
| TOOL-237 | doc_generate | Generate documentation | Later | Planned |
| TOOL-238 | doc_update | Update existing documentation | Later | Planned |
| TOOL-239 | doc_comment | Add doc comments to code | Later | Planned |
| TOOL-240 | doc_readme | Generate a README | Later | Planned |
| TOOL-241 | doc_api | Generate an API reference | Later | Planned |
| TOOL-242 | doc_changelog | Update the changelog | Later | Planned |
| TOOL-243 | doc_search | Search documentation | Later | Planned |
| TOOL-244 | doc_translate | Translate documentation | Later | Planned |

## Browser (BRW)

| ID | Tool | Description | Phase | Status |
|----|------|-------------|-------|--------|
| TOOL-245 | browser_open | Open a URL in the embedded browser | Later | Planned |
| TOOL-246 | browser_html | Get raw page HTML | Later | Planned |
| TOOL-247 | browser_extract | Extract page text and content | Later | Planned |
| TOOL-248 | browser_screenshot | Capture a page screenshot | Later | Planned |
| TOOL-249 | browser_click | Click an element | Later | Planned |
| TOOL-250 | browser_type | Type into a form field | Later | Planned |
| TOOL-251 | browser_select | Select a dropdown option | Later | Planned |
| TOOL-252 | browser_scroll | Scroll the page | Later | Planned |
| TOOL-253 | browser_back | Navigate back in history | Later | Planned |
| TOOL-254 | browser_forward | Navigate forward in history | Later | Planned |
| TOOL-255 | browser_wait | Wait for an element or condition | Later | Planned |
| TOOL-256 | browser_evaluate | Evaluate JavaScript in the page | Later | Planned |
| TOOL-257 | browser_cookies | Manage browser cookies | Later | Planned |
| TOOL-258 | browser_find | Find an element by selector | Later | Planned |
| TOOL-259 | browser_downloads | List or download browser files | Later | Planned |

## Network/API (NET)

| ID | Tool | Description | Phase | Status |
|----|------|-------------|-------|--------|
| TOOL-060 | http_get | Perform an HTTP GET request | 4 | Planned |
| TOOL-061 | http_post | Perform an HTTP POST request | 4 | Planned |
| TOOL-062 | http_put | Perform an HTTP PUT request | 4 | Planned |
| TOOL-063 | http_delete | Perform an HTTP DELETE request | 4 | Planned |
| TOOL-064 | websocket | Open a WebSocket connection | 4 | Planned |
| TOOL-260 | http_head | Perform an HTTP HEAD request | 4 | Planned |
| TOOL-261 | http_patch | Perform an HTTP PATCH request | 4 | Planned |
| TOOL-262 | http_request | Raw HTTP request with full control | 4 | Planned |
| TOOL-263 | http_download | Download a file into the sandbox | 4 | Planned |
| TOOL-264 | http_upload | Upload a file via HTTP | 4 | Planned |
| TOOL-265 | http_cookies | Manage the HTTP cookie jar | 4 | Planned |
| TOOL-266 | dns_lookup | Resolve DNS records | 4 | Planned |
| TOOL-267 | tcp_probe | Test TCP connectivity to a host and port | 4 | Planned |

## Database (DB)

| ID | Tool | Description | Phase | Status |
|----|------|-------------|-------|--------|
| TOOL-268 | sqlite_query | Run a SELECT query | Later | Planned |
| TOOL-269 | sqlite_execute | Run INSERT/UPDATE/DELETE statements | Later | Planned |
| TOOL-270 | sqlite_create | Create a SQLite database | Later | Planned |
| TOOL-271 | sqlite_migrate | Run a schema migration | Later | Planned |
| TOOL-272 | sqlite_schema | Show the database schema | Later | Planned |
| TOOL-273 | sqlite_backup | Back up a database | Later | Planned |
| TOOL-274 | sqlite_restore | Restore a database from backup | Later | Planned |
| TOOL-275 | sqlite_import | Import CSV or JSON data | Later | Planned |
| TOOL-276 | sqlite_export | Export a table to CSV or JSON | Later | Planned |
| TOOL-277 | sqlite_index | Manage database indexes | Later | Planned |
| TOOL-278 | sqlite_vacuum | Vacuum the database | Later | Planned |
| TOOL-279 | sqlite_transaction | Begin, commit, or roll back a transaction | Later | Planned |
| TOOL-280 | sqlite_attach | Attach a secondary database | Later | Planned |
| TOOL-281 | sqlite_analyze | Analyze query plans | Later | Planned |
| TOOL-282 | sqlite_vector | Vector similarity search (extension) | Later | Planned |

## Memory (MEM)

| ID | Tool | Description | Phase | Status |
|----|------|-------------|-------|--------|
| TOOL-070 | memory_store | Store an entry in memory | 6 | Planned |
| TOOL-071 | memory_recall | Recall a memory entry | 6 | Planned |
| TOOL-072 | memory_search | Semantic search over memory | 6 | Planned |
| TOOL-073 | memory_delete | Delete a memory entry | 6 | Planned |
| TOOL-074 | memory_list | List memory entries | 6 | Planned |
| TOOL-283 | memory_summarize | Summarize memory content | 6 | Planned |
| TOOL-284 | memory_export | Export memory to a file | 6 | Planned |
| TOOL-285 | memory_import | Import memory from a file | 6 | Planned |
| TOOL-286 | memory_prune | Prune stale or low-relevance entries | 6 | Planned |
| TOOL-287 | memory_tag | Add or remove tags on memory entries | 6 | Planned |
| TOOL-288 | memory_stats | Memory usage statistics | 6 | Planned |
| TOOL-383 | memory_tool_history | Query tool invocation history | 2 | Planned |
| TOOL-384 | memory_preferences | Get or set learned user preferences | 4 | Planned |
| TOOL-385 | memory_graph_query | Query the knowledge graph (entities, relationships) | 5 | Planned |
| TOOL-386 | memory_graph_build | Extract entities and relationships into the knowledge graph | 5 | Planned |

## AI (AI)

| ID | Tool | Description | Phase | Status |
|----|------|-------------|-------|--------|
| TOOL-100 | ai_complete | Generate a completion from an AI provider | 5 | Planned |
| TOOL-101 | ai_embed | Generate embeddings for text | 5 | Planned |
| TOOL-102 | ai_image_generate | Generate an image from a prompt | 5 | Planned |
| TOOL-103 | ai_image_analyze | Analyze an image with vision | 5 | Planned |
| TOOL-289 | ai_stream | Stream a completion token by token | 5 | Planned |
| TOOL-290 | ai_transcribe | Transcribe audio to text | 5 | Planned |
| TOOL-291 | ai_speech | Synthesize speech from text | 5 | Planned |
| TOOL-292 | ai_moderate | Run a content moderation check | 5 | Planned |
| TOOL-293 | ai_rerank | Rerank documents by relevance | 5 | Planned |
| TOOL-294 | ai_models | List available models for a provider | 5 | Planned |

## Android Device (DEV)

| ID | Tool | Description | Phase | Status |
|----|------|-------------|-------|--------|
| TOOL-295 | device_info | Device and OS information | Later | Planned |
| TOOL-296 | device_storage | App storage usage | Later | Planned |
| TOOL-297 | device_battery | Battery status | Later | Planned |
| TOOL-298 | device_network | Connectivity status | Later | Planned |
| TOOL-299 | device_contacts | Read contacts (permission required) | Later | Planned |
| TOOL-300 | device_notification | Post a notification | Later | Planned |
| TOOL-301 | device_media | Access the media library (permission) | Later | Planned |
| TOOL-302 | device_camera | Capture a photo (permission required) | Later | Planned |
| TOOL-303 | device_audio | Record audio (permission required) | Later | Planned |
| TOOL-304 | device_clipboard | Read or write the clipboard | Later | Planned |
| TOOL-305 | device_sms | Send or read SMS (permission required) | Later | Planned |
| TOOL-306 | device_calendar | Read or create calendar events | Later | Planned |
| TOOL-307 | device_location | Get device location (permission required) | Later | Planned |
| TOOL-308 | device_share | Share content via the system share sheet | Later | Planned |
| TOOL-309 | device_documents | Access DocumentsProvider files | Later | Planned |

## Project Management (PM)

| ID | Tool | Description | Phase | Status |
|----|------|-------------|-------|--------|
| TOOL-310 | task_create | Create a task | Later | Planned |
| TOOL-311 | task_update | Update a task | Later | Planned |
| TOOL-312 | task_list | List tasks | Later | Planned |
| TOOL-313 | task_status | Get task status | Later | Planned |
| TOOL-314 | task_assign | Assign a task to an agent | Later | Planned |
| TOOL-315 | task_priority | Set task priority | Later | Planned |
| TOOL-316 | task_complete | Mark a task complete | Later | Planned |
| TOOL-317 | task_comment | Add a comment to a task | Later | Planned |
| TOOL-318 | project_plan | Create a project plan | Later | Planned |
| TOOL-319 | project_milestone | Manage milestones | Later | Planned |

## Security (SEC)

| ID | Tool | Description | Phase | Status |
|----|------|-------------|-------|--------|
| TOOL-320 | security_scan | Scan for vulnerabilities | Later | Planned |
| TOOL-321 | security_audit | Run a security audit | Later | Planned |
| TOOL-322 | security_permissions | Check tool and agent permissions | Later | Planned |
| TOOL-323 | security_encrypt | Encrypt a file or data | Later | Planned |
| TOOL-324 | security_decrypt | Decrypt a file or data | Later | Planned |
| TOOL-325 | security_hash | Compute a cryptographic hash | Later | Planned |
| TOOL-326 | security_sign | Sign data or verify a signature | Later | Planned |
| TOOL-327 | security_secrets | Scan files for secrets and keys | Later | Planned |
| TOOL-328 | security_policy | List security policies | Later | Planned |
| TOOL-329 | security_quarantine | Quarantine a suspicious file | Later | Planned |
| TOOL-330 | security_cert | Inspect certificates | Later | Planned |
| TOOL-331 | security_keychain | Manage app keys in the keystore | Later | Planned |
| TOOL-332 | security_revoke | Revoke a session or token | Later | Planned |
| TOOL-333 | security_vault | Store or retrieve a secret in the vault | Later | Planned |
| TOOL-334 | security_policy_check | Evaluate a policy for an action | Later | Planned |
| TOOL-392 | sandbox_network_rules | Manage sandbox network egress allow/deny rules | 3 | Planned |
| TOOL-393 | sandbox_quarantine_review | Review quarantined files and promote or delete | 3 | Planned |

## Observability (OBS)

| ID | Tool | Description | Phase | Status |
|----|------|-------------|-------|--------|
| TOOL-335 | obs_logs | Read execution logs | Later | Planned |
| TOOL-336 | obs_metrics | Get performance metrics | Later | Planned |
| TOOL-337 | obs_trace | Get an execution trace | Later | Planned |
| TOOL-338 | obs_events | Subscribe to the event stream | Later | Planned |
| TOOL-339 | obs_history | Execution history | Later | Planned |
| TOOL-340 | obs_tool_calls | Tool invocation records | Later | Planned |
| TOOL-341 | obs_token_usage | Token usage per request and session | Later | Planned |
| TOOL-342 | obs_api_usage | Provider API usage statistics | Later | Planned |
| TOOL-343 | obs_errors | Error reports | Later | Planned |
| TOOL-344 | obs_audit | Audit trail | Later | Planned |
| TOOL-345 | obs_export | Export a diagnostics bundle | Later | Planned |
| TOOL-346 | obs_performance | Profile app performance | Later | Planned |
| TOOL-347 | obs_search | Search logs and events | Later | Planned |
| TOOL-348 | obs_sessions | List agent sessions | Later | Planned |
| TOOL-349 | obs_snapshot | Capture a state snapshot | Later | Planned |

## Import/Export (IO)

| ID | Tool | Description | Phase | Status |
|----|------|-------------|-------|--------|
| TOOL-350 | io_import_project | Import a project archive | Later | Planned |
| TOOL-351 | io_export_project | Export a project archive | Later | Planned |
| TOOL-352 | io_import_archive | Import a workspace archive | Later | Planned |
| TOOL-353 | io_export_archive | Export a workspace archive | Later | Planned |
| TOOL-354 | io_import_backup | Restore from a backup | Later | Planned |
| TOOL-355 | io_export_backup | Create a backup | Later | Planned |
| TOOL-356 | io_import_data | Import structured data | Later | Planned |
| TOOL-357 | io_export_data | Export structured data | Later | Planned |
| TOOL-358 | io_export_report | Export an execution report | Later | Planned |
| TOOL-359 | io_share_file | Share a file via the Android share sheet | Later | Planned |
| TOOL-360 | io_import_snapshot | Import a sandbox snapshot | Later | Planned |
| TOOL-361 | io_export_snapshot | Export a sandbox snapshot | Later | Planned |
| TOOL-362 | io_export_manifest | Export a workspace manifest | Later | Planned |

## Plugin (PLG)

| ID | Tool | Description | Phase | Status |
|----|------|-------------|-------|--------|
| TOOL-120 | plugin_install | Install a plugin | 8 | Planned |
| TOOL-121 | plugin_uninstall | Uninstall a plugin with cleanup | 8 | Planned |
| TOOL-122 | plugin_configure | Configure a plugin | 8 | Planned |
| TOOL-123 | plugin_list | List installed plugins | 8 | Planned |
| TOOL-363 | plugin_update | Update an installed plugin | 8 | Planned |
| TOOL-364 | plugin_enable | Enable a plugin | 8 | Planned |
| TOOL-365 | plugin_disable | Disable a plugin | 8 | Planned |
| TOOL-366 | plugin_dependencies | Show the plugin dependency graph | 8 | Planned |
| TOOL-367 | plugin_pack | Package a plugin for distribution | 8 | Planned |
| TOOL-368 | plugin_inspect | Inspect plugin manifest and metadata | 8 | Planned |

## Multi-Agent (MAG)

| ID | Tool | Description | Phase | Status |
|----|------|-------------|-------|--------|
| TOOL-110 | agent_create | Create a new agent | 7 | Planned |
| TOOL-111 | agent_delegate | Delegate a task to another agent | 7 | Planned |
| TOOL-112 | agent_status | Get agent status | 7 | Planned |
| TOOL-113 | agent_list | List agents in the workspace | 7 | Planned |
| TOOL-369 | agent_update | Update an agent configuration | 7 | Planned |
| TOOL-370 | agent_delete | Delete an agent | 7 | Planned |
| TOOL-371 | agent_configure | Configure agent tools, memory, and permissions | 7 | Planned |
| TOOL-372 | agent_memory | Inspect an agent's memory | 7 | Planned |
| TOOL-373 | agent_cancel | Cancel a running agent | 7 | Planned |
| TOOL-374 | agent_broadcast | Send a message to all agents | 7 | Planned |

## Workflow (WF)

| ID | Tool | Description | Phase | Status |
|----|------|-------------|-------|--------|
| TOOL-130 | workflow_create | Create a workflow definition | 6 | Planned |
| TOOL-131 | workflow_run | Run a workflow | 6 | Planned |
| TOOL-132 | workflow_schedule | Schedule a workflow | 6 | Planned |
| TOOL-133 | workflow_history | View workflow execution history | 6 | Planned |
| TOOL-375 | workflow_cancel | Cancel a running workflow | 6 | Planned |
| TOOL-376 | workflow_pause | Pause a workflow | 6 | Planned |
| TOOL-377 | workflow_resume | Resume a paused workflow | 6 | Planned |
| TOOL-378 | workflow_status | Get workflow execution status | 6 | Planned |
| TOOL-379 | workflow_templates | List workflow templates | 6 | Planned |
| TOOL-380 | workflow_validate | Validate a workflow definition | 6 | Planned |
