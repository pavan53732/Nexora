> **Status: DERIVED** for the tool capability matrix.
> Tool identity and catalog membership are canonical in [TOOLS.md](./TOOLS.md). This matrix is derived from that catalog and is authoritative only for capability mapping.
>
> Depends on: [TOOLS.md](./TOOLS.md), [../architecture/TOOL_SYSTEM.md](../architecture/TOOL_SYSTEM.md), [../security/PermissionModel.md](../security/PermissionModel.md).
> Referenced by: sandbox, permission, and scheduling consumers.


# Nexora Tool Capability Matrix

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See [TOOLS.md](./TOOLS.md)
>
Authoritative reference mapping **every registered tool** (see [TOOLS.md](./TOOLS.md)) to its supported capabilities. Used by the sandbox controller, permission system, and agent scheduler to determine which tools an agent may invoke. Generated from the tool catalog; hand-tuned rows are preserved.

## Legend

| Symbol | Meaning |
|--------|---------|
| ✓ | Supported |
| — | Not supported |

## Matrix

| Tool ID | Tool Name | Category | Read | Write | Network | Android API | Background | Permission Level | Agent-Usable | Sandbox-Required | Streaming | Phase |
|---------|-----------|----------|------|-------|---------|-------------|------------|-----------------|--------------|------------------|-----------|-------|
| `file_read` | File Read | File System | ✓ | — | — | — | — | Low | ✓ | — | — | 4 |
| `file_write` | File Write | File System | — | ✓ | — | — | — | Low | ✓ | ✓ | — | 4 |
| `file_append` | File Append | File System | ✓ | ✓ | — | — | — | Low | ✓ | ✓ | — | 4 |
| `file_delete` | File Delete | File System | — | ✓ | — | — | — | Medium | ✓ | ✓ | — | 4 |
| `file_list` | File List | File System | ✓ | — | — | — | — | Low | ✓ | — | — | 4 |
| `file_create_dir` | File Create Dir | File System | ✓ | ✓ | — | — | — | Low | ✓ | ✓ | — | 4 |
| `file_move` | File Move | File System | ✓ | ✓ | — | — | — | Low | ✓ | ✓ | — | 4 |
| `file_copy` | File Copy | File System | ✓ | ✓ | — | — | — | Low | ✓ | ✓ | — | 4 |
| `file_exists` | File Exists | File System | ✓ | ✓ | — | — | — | Low | ✓ | ✓ | — | 4 |
| `file_info` | File Info | File System | ✓ | — | — | — | — | Low | ✓ | ✓ | — | 4 |
| `file_search` | File Search | File System | ✓ | — | — | — | — | Low | ✓ | — | — | 4 |
| `file_read_binary` | File Read Binary | File System | ✓ | — | — | — | — | Low | ✓ | ✓ | — | 4 |
| `file_write_binary` | File Write Binary | File System | ✓ | ✓ | — | — | — | Low | ✓ | ✓ | — | 4 |
| `file_chmod` | File Chmod | File System | ✓ | ✓ | — | — | — | Medium | ✓ | ✓ | — | 4 |
| `file_touch` | File Touch | File System | ✓ | ✓ | — | — | — | Low | ✓ | ✓ | — | 4 |
| `file_head` | File Head | File System | ✓ | ✓ | — | — | — | Low | ✓ | ✓ | — | 4 |
| `file_tail` | File Tail | File System | ✓ | ✓ | — | — | — | Low | ✓ | ✓ | — | 4 |
| `file_checksum` | File Checksum | File System | ✓ | ✓ | — | — | — | Low | ✓ | ✓ | — | 4 |
| `file_zip` | File Zip | File System | ✓ | ✓ | — | — | — | Low | ✓ | ✓ | — | 4 |
| `file_unzip` | File Unzip | File System | ✓ | ✓ | — | — | — | Low | ✓ | ✓ | — | 4 |
| `file_watch` | File Watch | File System | ✓ | ✓ | — | — | — | Low | ✓ | ✓ | — | 4 |
| `file_symlink` | File Symlink | File System | ✓ | ✓ | — | — | — | High | ✓ | ✓ | — | 4 |
| `file_history` | File History | File System | ✓ | — | — | — | — | Low | ✓ | ✓ | — | 4 |
| `file_restore` | File Restore | File System | ✓ | ✓ | — | — | — | Low | ✓ | ✓ | — | 4 |
| `workspace_create` | Workspace Create | Workspace | — | ✓ | — | — | — | Low | ✓ | — | — | 1 |
| `workspace_switch` | Workspace Switch | Workspace | — | ✓ | — | — | — | Low | ✓ | — | — | 1 |
| `workspace_list` | Workspace List | Workspace | ✓ | — | — | — | — | Low | ✓ | — | — | 1 |
| `workspace_archive` | Workspace Archive | Workspace | — | ✓ | — | — | — | Low | ✓ | — | — | 1 |
| `workspace_delete` | Workspace Delete | Workspace | — | ✓ | — | — | — | High | ✓ | — | — | 1 |
| `workspace_export` | Workspace Export | Workspace | — | ✓ | — | — | — | Low | ✓ | — | — | 1 |
| `workspace_import` | Workspace Import | Workspace | — | ✓ | — | — | — | Low | ✓ | — | — | 1 |
| `workspace_get` | Workspace Get | Workspace | ✓ | — | — | — | — | Low | ✓ | — | — | 1 |
| `workspace_configure` | Workspace Configure | Workspace | — | ✓ | — | — | — | Low | ✓ | — | — | 1 |
| `workspace_stats` | Workspace Stats | Workspace | ✓ | — | — | — | — | Low | ✓ | — | — | 1 |
| `workspace_duplicate` | Workspace Duplicate | Workspace | — | ✓ | — | — | — | Low | ✓ | — | — | 1 |
| `workspace_templates` | Workspace Templates | Workspace | ✓ | — | — | — | — | Low | ✓ | — | — | 1 |
| `sandbox_info` | Sandbox Info | Workspace | ✓ | — | — | — | — | Low | ✓ | — | — | 3 |
| `sandbox_reset` | Sandbox Reset | Workspace | — | ✓ | — | — | — | Low | ✓ | — | — | 3 |
| `sandbox_snapshot` | Sandbox Snapshot | Workspace | — | ✓ | — | — | — | Low | ✓ | — | — | 4 |
| `sandbox_restore` | Sandbox Restore | Workspace | — | ✓ | — | — | — | Low | ✓ | — | — | 4 |
| `sandbox_templates` | Sandbox Templates | Workspace | ✓ | — | — | — | — | Low | ✓ | — | — | 3 |
| `code_index` | Code Index | Code Intelligence | ✓ | ✓ | — | — | — | Medium | ✓ | ✓ | — | Later |
| `code_symbols` | Code Symbols | Code Intelligence | ✓ | — | — | — | — | Medium | ✓ | ✓ | — | Later |
| `code_symbol_info` | Code Symbol Info | Code Intelligence | ✓ | — | — | — | — | Medium | ✓ | ✓ | — | Later |
| `code_references` | Code References | Code Intelligence | ✓ | — | — | — | — | Medium | ✓ | ✓ | — | Later |
| `code_callers` | Code Callers | Code Intelligence | ✓ | — | — | — | — | Medium | ✓ | ✓ | — | Later |
| `code_rename` | Code Rename | Code Intelligence | ✓ | ✓ | — | — | — | Medium | ✓ | ✓ | — | Later |
| `code_explain` | Code Explain | Code Intelligence | ✓ | ✓ | — | — | — | Medium | ✓ | ✓ | — | Later |
| `code_generate` | Code Generate | Code Intelligence | ✓ | ✓ | — | — | — | Medium | ✓ | ✓ | — | Later |
| `code_refactor` | Code Refactor | Code Intelligence | ✓ | ✓ | — | — | — | Medium | ✓ | ✓ | — | Later |
| `code_review` | Code Review | Code Intelligence | ✓ | — | — | — | — | Medium | ✓ | ✓ | — | Later |
| `code_search` | Code Search | Code Intelligence | ✓ | — | — | — | — | Medium | ✓ | ✓ | — | Later |
| `code_complete` | Code Complete | Code Intelligence | ✓ | ✓ | — | — | — | Medium | ✓ | ✓ | — | Later |
| `code_convert` | Code Convert | Code Intelligence | ✓ | ✓ | — | — | — | Medium | ✓ | ✓ | — | Later |
| `code_metrics` | Code Metrics | Code Intelligence | ✓ | — | — | — | — | Medium | ✓ | ✓ | — | Later |
| `code_dependencies` | Code Dependencies | Code Intelligence | ✓ | — | — | — | — | Medium | ✓ | ✓ | — | Later |
| `code_calls` | Code Calls | Code Intelligence | ✓ | ✓ | — | — | — | Medium | ✓ | ✓ | — | Later |
| `code_compare` | Code Compare | Code Intelligence | ✓ | ✓ | — | — | — | Medium | ✓ | ✓ | — | Later |
| `code_fix` | Code Fix | Code Intelligence | ✓ | ✓ | — | — | — | Medium | ✓ | ✓ | — | Later |
| `search_text` | Search Text | Search | ✓ | — | — | — | — | Low | ✓ | — | — | 4 |
| `search_regex` | Search Regex | Search | ✓ | — | — | — | — | Low | ✓ | — | — | 4 |
| `grep` | Grep | Search | ✓ | — | — | — | — | Low | ✓ | — | — | 4 |
| `find` | Find | Search | ✓ | — | — | — | — | Low | ✓ | — | — | 4 |
| `search_glob` | Search Glob | Search | ✓ | — | — | — | — | Low | ✓ | — | — | 4 |
| `search_history` | Search History | Search | ✓ | — | — | — | — | Low | ✓ | — | — | 4 |
| `search_workspace` | Search Workspace | Search | ✓ | — | — | — | — | Low | ✓ | — | — | 4 |
| `search_web` | Search Web | Search | ✓ | — | — | — | — | Low | ✓ | — | — | 4 |
| `search_tools` | Search Tools | Search | ✓ | — | — | — | — | Low | ✓ | — | — | 4 |
| `terminal_run` | Terminal Run | Terminal | ✓ | ✓ | — | — | — | High | ✓ | ✓ | — | 4 |
| `terminal_run_script` | Terminal Run Script | Terminal | — | ✓ | — | — | — | High | ✓ | ✓ | ✓ | 4 |
| `terminal_run_background` | Terminal Run Background | Terminal | ✓ | ✓ | — | — | ✓ | High | ✓ | ✓ | — | 4 |
| `terminal_kill` | Terminal Kill | Terminal | — | ✓ | — | — | — | High | ✓ | ✓ | — | 4 |
| `terminal_list_processes` | Terminal List Processes | Terminal | ✓ | — | — | — | — | High | ✓ | ✓ | — | 4 |
| `terminal_session_create` | Terminal Session Create | Terminal | — | ✓ | — | — | — | High | ✓ | ✓ | — | 4 |
| `terminal_session_list` | Terminal Session List | Terminal | ✓ | — | — | — | — | High | ✓ | ✓ | — | 4 |
| `terminal_session_kill` | Terminal Session Kill | Terminal | — | ✓ | — | — | — | High | ✓ | ✓ | — | 4 |
| `terminal_stdin` | Terminal Stdin | Terminal | — | ✓ | — | — | — | High | ✓ | ✓ | — | 4 |
| `terminal_wait` | Terminal Wait | Terminal | — | ✓ | — | — | ✓ | High | ✓ | ✓ | — | 4 |
| `terminal_history` | Terminal History | Terminal | ✓ | — | — | — | — | Low | ✓ | — | — | 4 |
| `git_init` | Git Init | Git | ✓ | ✓ | — | — | — | Low | ✓ | — | — | 4 |
| `git_clone` | Git Clone | Git | ✓ | ✓ | ✓ | — | — | Medium | ✓ | ✓ | — | 4 |
| `git_add` | Git Add | Git | ✓ | ✓ | — | — | — | Medium | ✓ | ✓ | — | 4 |
| `git_commit` | Git Commit | Git | ✓ | ✓ | — | — | — | Medium | ✓ | ✓ | — | 4 |
| `git_push` | Git Push | Git | — | ✓ | ✓ | — | — | High | ✓ | ✓ | — | 4 |
| `git_pull` | Git Pull | Git | ✓ | ✓ | ✓ | — | — | Medium | ✓ | — | — | 4 |
| `git_branch` | Git Branch | Git | ✓ | ✓ | — | — | — | Medium | ✓ | — | — | 4 |
| `git_merge` | Git Merge | Git | ✓ | ✓ | — | — | — | Medium | ✓ | ✓ | — | 4 |
| `git_log` | Git Log | Git | ✓ | — | — | — | — | Low | ✓ | — | — | 4 |
| `git_diff` | Git Diff | Git | ✓ | — | — | — | — | Low | ✓ | — | — | 4 |
| `git_status` | Git Status | Git | ✓ | — | — | — | — | Medium | ✓ | ✓ | — | 4 |
| `git_stash` | Git Stash | Git | ✓ | ✓ | — | — | — | Medium | ✓ | ✓ | — | 4 |
| `git_fetch` | Git Fetch | Git | ✓ | ✓ | — | — | — | Medium | ✓ | ✓ | — | 4 |
| `git_remote` | Git Remote | Git | ✓ | ✓ | — | — | — | Medium | ✓ | ✓ | — | 4 |
| `git_tag` | Git Tag | Git | ✓ | ✓ | — | — | — | Medium | ✓ | ✓ | — | 4 |
| `git_reset` | Git Reset | Git | ✓ | ✓ | — | — | — | Medium | ✓ | ✓ | — | 4 |
| `git_revert` | Git Revert | Git | ✓ | ✓ | — | — | — | Medium | ✓ | ✓ | — | 4 |
| `git_clean` | Git Clean | Git | ✓ | ✓ | — | — | — | Medium | ✓ | ✓ | — | 4 |
| `git_blame` | Git Blame | Git | ✓ | — | — | — | — | Medium | ✓ | ✓ | — | 4 |
| `npm_install` | Npm Install | Package Manager | — | ✓ | ✓ | — | — | High | ✓ | ✓ | — | 4 |
| `pip_install` | Pip Install | Package Manager | — | ✓ | ✓ | — | — | High | ✓ | ✓ | — | 4 |
| `package_list` | Package List | Package Manager | ✓ | — | ✓ | — | — | High | ✓ | ✓ | — | 4 |
| `package_remove` | Package Remove | Package Manager | — | ✓ | ✓ | — | — | High | ✓ | ✓ | — | 4 |
| `package_update` | Package Update | Package Manager | — | ✓ | ✓ | — | — | High | ✓ | ✓ | — | 4 |
| `package_info` | Package Info | Package Manager | ✓ | — | ✓ | — | — | High | ✓ | ✓ | — | 4 |
| `package_install` | Package Install | Package Manager | — | ✓ | ✓ | — | — | High | ✓ | ✓ | — | 4 |
| `package_audit` | Package Audit | Package Manager | ✓ | — | ✓ | — | — | High | ✓ | ✓ | — | 4 |
| `package_search` | Package Search | Package Manager | ✓ | — | ✓ | — | — | High | ✓ | ✓ | — | 4 |
| `build_run` | Build Run | Build | — | ✓ | — | — | — | High | ✓ | ✓ | — | Later |
| `build_compile` | Build Compile | Build | — | ✓ | — | — | — | High | ✓ | ✓ | — | Later |
| `build_clean` | Build Clean | Build | — | ✓ | — | — | — | High | ✓ | ✓ | — | Later |
| `build_config` | Build Config | Build | — | ✓ | — | — | — | High | ✓ | ✓ | — | Later |
| `build_report` | Build Report | Build | — | ✓ | — | — | — | High | ✓ | ✓ | — | Later |
| `build_verify` | Build Verify | Build | — | ✓ | — | — | — | High | ✓ | ✓ | — | Later |
| `build_install` | Build Install | Build | — | ✓ | — | — | — | High | ✓ | ✓ | — | Later |
| `build_archive` | Build Archive | Build | — | ✓ | — | — | — | High | ✓ | ✓ | — | Later |
| `build_gradle` | Build Gradle | Build | — | ✓ | — | — | — | High | ✓ | ✓ | — | Later |
| `build_make` | Build Make | Build | — | ✓ | — | — | — | High | ✓ | ✓ | — | Later |
| `test_run` | Test Run | Testing | — | ✓ | — | — | — | Medium | ✓ | ✓ | ✓ | Later |
| `test_run_file` | Test Run File | Testing | — | ✓ | — | — | — | Medium | ✓ | ✓ | — | Later |
| `test_case` | Test Case | Testing | — | ✓ | — | — | — | Medium | ✓ | ✓ | — | Later |
| `test_coverage` | Test Coverage | Testing | — | ✓ | — | — | — | Medium | ✓ | ✓ | — | Later |
| `test_report` | Test Report | Testing | — | ✓ | — | — | — | Medium | ✓ | ✓ | — | Later |
| `test_failures` | Test Failures | Testing | ✓ | — | — | — | — | Medium | ✓ | ✓ | — | Later |
| `test_rerun` | Test Rerun | Testing | — | ✓ | — | — | — | Medium | ✓ | ✓ | — | Later |
| `test_generate` | Test Generate | Testing | — | ✓ | — | — | — | Medium | ✓ | ✓ | — | Later |
| `test_benchmark` | Test Benchmark | Testing | — | ✓ | — | — | — | Medium | ✓ | ✓ | — | Later |
| `test_performance` | Test Performance | Testing | — | ✓ | — | — | — | Medium | ✓ | ✓ | — | Later |
| `test_smoke` | Test Smoke | Testing | — | ✓ | — | — | — | Medium | ✓ | ✓ | — | Later |
| `test_integration` | Test Integration | Testing | — | ✓ | — | — | — | Medium | ✓ | ✓ | — | Later |
| `test_e2e` | Test E2E | Testing | — | ✓ | — | — | — | Medium | ✓ | ✓ | — | Later |
| `debug_breakpoint` | Debug Breakpoint | Debugging | — | ✓ | — | — | — | High | ✓ | ✓ | — | Later |
| `debug_remove_breakpoint` | Debug Remove Breakpoint | Debugging | — | ✓ | — | — | — | High | ✓ | ✓ | — | Later |
| `debug_list_breakpoints` | Debug List Breakpoints | Debugging | ✓ | — | — | — | — | High | ✓ | ✓ | — | Later |
| `debug_continue` | Debug Continue | Debugging | — | ✓ | — | — | — | High | ✓ | ✓ | — | Later |
| `debug_step_over` | Debug Step Over | Debugging | — | ✓ | — | — | — | High | ✓ | ✓ | — | Later |
| `debug_step_into` | Debug Step Into | Debugging | — | ✓ | — | — | — | High | ✓ | ✓ | — | Later |
| `debug_step_out` | Debug Step Out | Debugging | — | ✓ | — | — | — | High | ✓ | ✓ | — | Later |
| `debug_inspect` | Debug Inspect | Debugging | ✓ | — | — | — | — | High | ✓ | ✓ | — | Later |
| `debug_stack` | Debug Stack | Debugging | — | ✓ | — | — | — | High | ✓ | ✓ | — | Later |
| `debug_attach` | Debug Attach | Debugging | — | ✓ | — | — | — | High | ✓ | ✓ | — | Later |
| `debug_logcat` | Debug Logcat | Debugging | ✓ | — | — | — | — | High | ✓ | ✓ | — | Later |
| `debug_heap` | Debug Heap | Debugging | — | ✓ | — | — | — | High | ✓ | ✓ | — | Later |
| `debug_dump` | Debug Dump | Debugging | — | ✓ | — | — | — | High | ✓ | ✓ | — | Later |
| `debug_evaluate` | Debug Evaluate | Debugging | — | ✓ | — | — | — | High | ✓ | ✓ | — | Later |
| `debug_exception` | Debug Exception | Debugging | — | ✓ | — | — | — | High | ✓ | ✓ | — | Later |
| `format_code` | Format Code | Formatting | — | ✓ | — | — | — | Low | ✓ | ✓ | — | Later |
| `format_file` | Format File | Formatting | — | ✓ | — | — | — | Low | ✓ | ✓ | — | Later |
| `format_project` | Format Project | Formatting | — | ✓ | — | — | — | Low | ✓ | ✓ | — | Later |
| `format_check` | Format Check | Formatting | — | ✓ | — | — | — | Low | ✓ | ✓ | — | Later |
| `format_config` | Format Config | Formatting | — | ✓ | — | — | — | Low | ✓ | ✓ | — | Later |
| `lint_run` | Lint Run | Formatting | — | ✓ | — | — | — | Low | ✓ | ✓ | — | Later |
| `lint_fix` | Lint Fix | Formatting | — | ✓ | — | — | — | Low | ✓ | ✓ | — | Later |
| `lint_report` | Lint Report | Formatting | — | ✓ | — | — | — | Low | ✓ | ✓ | — | Later |
| `doc_generate` | Doc Generate | Documentation | ✓ | ✓ | — | — | — | Low | ✓ | ✓ | — | Later |
| `doc_update` | Doc Update | Documentation | ✓ | ✓ | — | — | — | Low | ✓ | ✓ | — | Later |
| `doc_comment` | Doc Comment | Documentation | ✓ | ✓ | — | — | — | Low | ✓ | ✓ | — | Later |
| `doc_readme` | Doc Readme | Documentation | ✓ | — | — | — | — | Low | ✓ | ✓ | — | Later |
| `doc_api` | Doc Api | Documentation | ✓ | ✓ | — | — | — | Low | ✓ | ✓ | — | Later |
| `doc_changelog` | Doc Changelog | Documentation | ✓ | — | — | — | — | Low | ✓ | ✓ | — | Later |
| `doc_search` | Doc Search | Documentation | ✓ | — | — | — | — | Low | ✓ | ✓ | — | Later |
| `doc_translate` | Doc Translate | Documentation | ✓ | ✓ | — | — | — | Low | ✓ | ✓ | — | Later |
| `browser_open` | Browser Open | Browser | ✓ | ✓ | ✓ | — | — | High | ✓ | ✓ | — | Later |
| `browser_html` | Browser Html | Browser | ✓ | ✓ | ✓ | — | — | High | ✓ | ✓ | — | Later |
| `browser_extract` | Browser Extract | Browser | ✓ | ✓ | ✓ | — | — | High | ✓ | ✓ | — | Later |
| `browser_screenshot` | Browser Screenshot | Browser | ✓ | ✓ | ✓ | — | — | High | ✓ | ✓ | — | Later |
| `browser_click` | Browser Click | Browser | ✓ | ✓ | ✓ | — | — | High | ✓ | ✓ | — | Later |
| `browser_type` | Browser Type | Browser | ✓ | ✓ | ✓ | — | — | High | ✓ | ✓ | — | Later |
| `browser_select` | Browser Select | Browser | ✓ | ✓ | ✓ | — | — | High | ✓ | ✓ | — | Later |
| `browser_scroll` | Browser Scroll | Browser | ✓ | ✓ | ✓ | — | — | High | ✓ | ✓ | — | Later |
| `browser_back` | Browser Back | Browser | ✓ | ✓ | ✓ | — | — | High | ✓ | ✓ | — | Later |
| `browser_forward` | Browser Forward | Browser | ✓ | ✓ | ✓ | — | — | High | ✓ | ✓ | — | Later |
| `browser_wait` | Browser Wait | Browser | ✓ | ✓ | ✓ | — | — | High | ✓ | ✓ | — | Later |
| `browser_evaluate` | Browser Evaluate | Browser | ✓ | ✓ | ✓ | — | — | High | ✓ | ✓ | — | Later |
| `browser_cookies` | Browser Cookies | Browser | ✓ | ✓ | ✓ | — | — | High | ✓ | ✓ | — | Later |
| `browser_find` | Browser Find | Browser | ✓ | — | ✓ | — | — | High | ✓ | ✓ | — | Later |
| `browser_downloads` | Browser Downloads | Browser | ✓ | — | ✓ | — | — | High | ✓ | ✓ | — | Later |
| `http_get` | Http Get | Network/API | ✓ | — | ✓ | — | — | Medium | ✓ | ✓ | ✓ | 4 |
| `http_post` | Http Post | Network/API | — | ✓ | ✓ | — | — | Medium | ✓ | ✓ | ✓ | 4 |
| `http_put` | Http Put | Network/API | ✓ | ✓ | ✓ | — | — | High | ✓ | — | — | 4 |
| `http_delete` | Http Delete | Network/API | ✓ | ✓ | ✓ | — | — | High | ✓ | — | — | 4 |
| `websocket` | Websocket | Network/API | ✓ | ✓ | ✓ | — | — | High | ✓ | — | — | 4 |
| `http_head` | Http Head | Network/API | ✓ | ✓ | ✓ | — | — | High | ✓ | — | — | 4 |
| `http_patch` | Http Patch | Network/API | ✓ | ✓ | ✓ | — | — | High | ✓ | — | — | 4 |
| `http_request` | Http Request | Network/API | ✓ | ✓ | ✓ | — | — | High | ✓ | — | ✓ | 4 |
| `http_download` | Http Download | Network/API | ✓ | ✓ | ✓ | — | ✓ | Medium | ✓ | ✓ | ✓ | 4 |
| `http_upload` | Http Upload | Network/API | ✓ | ✓ | ✓ | — | — | High | ✓ | — | — | 4 |
| `http_cookies` | Http Cookies | Network/API | ✓ | ✓ | ✓ | — | — | High | ✓ | — | — | 4 |
| `dns_lookup` | Dns Lookup | Network/API | ✓ | ✓ | ✓ | — | — | High | ✓ | — | — | 4 |
| `tcp_probe` | Tcp Probe | Network/API | ✓ | ✓ | ✓ | — | — | High | ✓ | — | — | 4 |
| `sqlite_query` | Sqlite Query | Database | ✓ | ✓ | — | — | — | Medium | ✓ | ✓ | — | Later |
| `sqlite_execute` | Sqlite Execute | Database | ✓ | ✓ | — | — | — | Medium | ✓ | ✓ | — | Later |
| `sqlite_create` | Sqlite Create | Database | ✓ | ✓ | — | — | — | Medium | ✓ | ✓ | — | Later |
| `sqlite_migrate` | Sqlite Migrate | Database | ✓ | ✓ | — | — | — | Medium | ✓ | ✓ | — | Later |
| `sqlite_schema` | Sqlite Schema | Database | ✓ | — | — | — | — | Medium | ✓ | ✓ | — | Later |
| `sqlite_backup` | Sqlite Backup | Database | ✓ | ✓ | — | — | — | Medium | ✓ | ✓ | — | Later |
| `sqlite_restore` | Sqlite Restore | Database | ✓ | ✓ | — | — | — | Medium | ✓ | ✓ | — | Later |
| `sqlite_import` | Sqlite Import | Database | ✓ | ✓ | — | — | — | Medium | ✓ | ✓ | — | Later |
| `sqlite_export` | Sqlite Export | Database | ✓ | ✓ | — | — | — | Medium | ✓ | ✓ | — | Later |
| `sqlite_index` | Sqlite Index | Database | ✓ | ✓ | — | — | — | Medium | ✓ | ✓ | — | Later |
| `sqlite_vacuum` | Sqlite Vacuum | Database | ✓ | ✓ | — | — | — | Medium | ✓ | ✓ | — | Later |
| `sqlite_transaction` | Sqlite Transaction | Database | ✓ | ✓ | — | — | — | Medium | ✓ | ✓ | — | Later |
| `sqlite_attach` | Sqlite Attach | Database | ✓ | ✓ | — | — | — | Medium | ✓ | ✓ | — | Later |
| `sqlite_analyze` | Sqlite Analyze | Database | ✓ | — | — | — | — | Medium | ✓ | ✓ | — | Later |
| `sqlite_vector` | Sqlite Vector | Database | ✓ | ✓ | — | — | — | Medium | ✓ | ✓ | — | Later |
| `memory_store` | Memory Store | Memory | — | ✓ | — | — | — | Low | ✓ | — | — | 6 |
| `memory_recall` | Memory Recall | Memory | ✓ | ✓ | — | — | — | Low | ✓ | — | — | 6 |
| `memory_search` | Memory Search | Memory | ✓ | — | — | — | — | Low | ✓ | — | — | 6 |
| `memory_delete` | Memory Delete | Memory | — | ✓ | — | — | — | Medium | ✓ | — | — | 6 |
| `memory_list` | Memory List | Memory | ✓ | — | — | — | — | Low | ✓ | — | — | 6 |
| `memory_summarize` | Memory Summarize | Memory | ✓ | ✓ | — | — | — | Low | ✓ | — | — | 6 |
| `memory_export` | Memory Export | Memory | ✓ | ✓ | — | — | — | Low | ✓ | — | — | 6 |
| `memory_import` | Memory Import | Memory | ✓ | ✓ | — | — | — | Low | ✓ | — | — | 6 |
| `memory_prune` | Memory Prune | Memory | ✓ | ✓ | — | — | — | Low | ✓ | — | — | 6 |
| `memory_tag` | Memory Tag | Memory | ✓ | ✓ | — | — | — | Low | ✓ | — | — | 6 |
| `memory_stats` | Memory Stats | Memory | ✓ | — | — | — | — | Low | ✓ | — | — | 6 |
| `memory_tool_history` | Memory Tool History | Memory | ✓ | — | — | — | — | Low | ✓ | — | — | 2 |
| `memory_preferences` | Memory Preferences | Memory | ✓ | — | — | — | — | Low | ✓ | — | — | 4 |
| `memory_graph_query` | Memory Graph Query | Memory | ✓ | ✓ | — | — | — | Low | ✓ | — | — | 5 |
| `memory_graph_build` | Memory Graph Build | Memory | ✓ | ✓ | — | — | — | Low | ✓ | — | — | 5 |
| `memory_lessons` | Memory Lessons | Memory | ✓ | ✓ | — | — | — | Low | ✓ | — | — | 4 |
| `ai_complete` | Ai Complete | AI | ✓ | — | ✓ | — | — | High | ✓ | — | ✓ | 5 |
| `ai_embed` | Ai Embed | AI | ✓ | — | ✓ | — | — | Medium | ✓ | — | — | 5 |
| `ai_image_generate` | Ai Image Generate | AI | ✓ | ✓ | — | — | — | Medium | ✓ | — | — | 5 |
| `ai_image_analyze` | Ai Image Analyze | AI | ✓ | — | ✓ | — | — | High | ✓ | — | ✓ | 5 |
| `ai_stream` | Ai Stream | AI | ✓ | ✓ | — | — | — | Medium | ✓ | — | ✓ | 5 |
| `ai_transcribe` | Ai Transcribe | AI | ✓ | ✓ | — | — | — | Medium | ✓ | — | ✓ | 5 |
| `ai_speech` | Ai Speech | AI | ✓ | ✓ | — | — | — | Medium | ✓ | — | ✓ | 5 |
| `ai_moderate` | Ai Moderate | AI | ✓ | ✓ | — | — | — | Medium | ✓ | — | — | 5 |
| `ai_rerank` | Ai Rerank | AI | ✓ | ✓ | — | — | — | Medium | ✓ | — | — | 5 |
| `ai_models` | Ai Models | AI | ✓ | — | — | — | — | Medium | ✓ | — | — | 5 |
| `device_info` | Device Info | Android Device | ✓ | — | — | ✓ | — | High | ✓ | — | — | Later |
| `device_storage` | Device Storage | Android Device | — | ✓ | — | ✓ | — | High | ✓ | — | — | Later |
| `device_battery` | Device Battery | Android Device | — | ✓ | — | ✓ | — | High | ✓ | — | — | Later |
| `device_network` | Device Network | Android Device | — | ✓ | — | ✓ | — | High | ✓ | — | — | Later |
| `device_contacts` | Device Contacts | Android Device | — | ✓ | — | ✓ | — | High | ✓ | — | — | Later |
| `device_notification` | Device Notification | Android Device | — | ✓ | — | ✓ | — | High | ✓ | — | — | Later |
| `device_media` | Device Media | Android Device | — | ✓ | — | ✓ | — | High | ✓ | — | — | Later |
| `device_camera` | Device Camera | Android Device | — | ✓ | — | ✓ | — | High | ✓ | — | — | Later |
| `device_audio` | Device Audio | Android Device | — | ✓ | — | ✓ | — | High | ✓ | — | — | Later |
| `device_clipboard` | Device Clipboard | Android Device | — | ✓ | — | ✓ | — | High | ✓ | — | — | Later |
| `device_sms` | Device Sms | Android Device | — | ✓ | — | ✓ | — | High | ✓ | — | — | Later |
| `device_calendar` | Device Calendar | Android Device | — | ✓ | — | ✓ | — | High | ✓ | — | — | Later |
| `device_location` | Device Location | Android Device | — | ✓ | — | ✓ | — | High | ✓ | — | — | Later |
| `device_share` | Device Share | Android Device | — | ✓ | — | ✓ | — | High | ✓ | — | — | Later |
| `device_documents` | Device Documents | Android Device | — | ✓ | — | ✓ | — | High | ✓ | — | — | Later |
| `task_create` | Task Create | Project Management | — | ✓ | — | — | — | Low | ✓ | — | — | Later |
| `task_update` | Task Update | Project Management | — | ✓ | — | — | — | Low | ✓ | — | — | Later |
| `task_list` | Task List | Project Management | ✓ | — | — | — | — | Low | ✓ | — | — | Later |
| `task_status` | Task Status | Project Management | ✓ | — | — | — | — | Low | ✓ | — | — | Later |
| `task_assign` | Task Assign | Project Management | — | ✓ | — | — | — | Low | ✓ | — | — | Later |
| `task_priority` | Task Priority | Project Management | — | ✓ | — | — | — | Low | ✓ | — | — | Later |
| `task_complete` | Task Complete | Project Management | — | ✓ | — | — | — | Low | ✓ | — | — | Later |
| `task_comment` | Task Comment | Project Management | — | ✓ | — | — | — | Low | ✓ | — | — | Later |
| `project_plan` | Project Plan | Project Management | — | ✓ | — | — | — | Low | ✓ | — | — | Later |
| `project_milestone` | Project Milestone | Project Management | — | ✓ | — | — | — | Low | ✓ | — | — | Later |
| `security_scan` | Security Scan | Security | — | ✓ | — | — | — | High | ✓ | — | — | Later |
| `security_audit` | Security Audit | Security | ✓ | — | — | — | — | High | ✓ | — | — | Later |
| `security_permissions` | Security Permissions | Security | ✓ | — | — | — | — | High | ✓ | — | — | Later |
| `security_encrypt` | Security Encrypt | Security | — | ✓ | — | — | — | High | ✓ | — | — | Later |
| `security_decrypt` | Security Decrypt | Security | — | ✓ | — | — | — | High | ✓ | — | — | Later |
| `security_hash` | Security Hash | Security | — | ✓ | — | — | — | High | ✓ | — | — | Later |
| `security_sign` | Security Sign | Security | — | ✓ | — | — | — | High | ✓ | — | — | Later |
| `security_secrets` | Security Secrets | Security | — | ✓ | — | — | — | High | ✓ | — | — | Later |
| `security_policy` | Security Policy | Security | — | ✓ | — | — | — | High | ✓ | — | — | Later |
| `security_quarantine` | Security Quarantine | Security | — | ✓ | — | — | — | High | ✓ | — | — | Later |
| `security_cert` | Security Cert | Security | — | ✓ | — | — | — | High | ✓ | — | — | Later |
| `security_keychain` | Security Keychain | Security | — | ✓ | — | — | — | High | ✓ | — | — | Later |
| `security_revoke` | Security Revoke | Security | — | ✓ | — | — | — | High | ✓ | — | — | Later |
| `security_vault` | Security Vault | Security | — | ✓ | — | — | — | High | ✓ | — | — | Later |
| `security_policy_check` | Security Policy Check | Security | — | ✓ | — | — | — | High | ✓ | — | — | Later |
| `sandbox_network_rules` | Sandbox Network Rules | Security | — | ✓ | — | — | — | High | ✓ | — | — | 3 |
| `sandbox_quarantine_review` | Sandbox Quarantine Review | Security | ✓ | — | — | — | — | High | ✓ | — | — | 3 |
| `obs_logs` | Obs Logs | Observability | ✓ | — | — | — | — | Low | ✓ | — | — | Later |
| `obs_metrics` | Obs Metrics | Observability | ✓ | — | — | — | — | Low | ✓ | — | — | Later |
| `obs_trace` | Obs Trace | Observability | ✓ | — | — | — | — | Low | ✓ | — | — | Later |
| `obs_events` | Obs Events | Observability | ✓ | ✓ | — | — | ✓ | Low | ✓ | — | ✓ | Later |
| `obs_history` | Obs History | Observability | ✓ | — | — | — | — | Low | ✓ | — | — | Later |
| `obs_tool_calls` | Obs Tool Calls | Observability | ✓ | — | — | — | — | Low | ✓ | — | — | Later |
| `obs_token_usage` | Obs Token Usage | Observability | ✓ | — | — | — | — | Low | ✓ | — | — | Later |
| `obs_api_usage` | Obs Api Usage | Observability | ✓ | — | — | — | — | Low | ✓ | — | — | Later |
| `obs_errors` | Obs Errors | Observability | ✓ | — | — | — | — | Low | ✓ | — | — | Later |
| `obs_audit` | Obs Audit | Observability | ✓ | — | — | — | — | Low | ✓ | — | — | Later |
| `obs_export` | Obs Export | Observability | ✓ | ✓ | — | — | — | Low | ✓ | — | — | Later |
| `obs_performance` | Obs Performance | Observability | ✓ | ✓ | — | — | — | Low | ✓ | — | — | Later |
| `obs_search` | Obs Search | Observability | ✓ | — | — | — | — | Low | ✓ | — | — | Later |
| `obs_sessions` | Obs Sessions | Observability | ✓ | — | — | — | — | Low | ✓ | — | — | Later |
| `obs_snapshot` | Obs Snapshot | Observability | ✓ | ✓ | — | — | — | Low | ✓ | — | — | Later |
| `context_stats` | Context Stats | Observability | ✓ | — | — | — | — | Low | ✓ | — | — | 2 |
| `io_import_project` | Io Import Project | Import/Export | — | ✓ | ✓ | — | — | Medium | ✓ | — | — | Later |
| `io_export_project` | Io Export Project | Import/Export | — | ✓ | ✓ | — | — | Medium | ✓ | — | — | Later |
| `io_import_archive` | Io Import Archive | Import/Export | — | ✓ | ✓ | — | — | Medium | ✓ | — | — | Later |
| `io_export_archive` | Io Export Archive | Import/Export | — | ✓ | ✓ | — | — | Medium | ✓ | — | — | Later |
| `io_import_backup` | Io Import Backup | Import/Export | — | ✓ | ✓ | — | — | High | ✓ | — | — | Later |
| `io_export_backup` | Io Export Backup | Import/Export | — | ✓ | ✓ | — | — | Medium | ✓ | — | — | Later |
| `io_import_data` | Io Import Data | Import/Export | — | ✓ | ✓ | — | — | Medium | ✓ | — | — | Later |
| `io_export_data` | Io Export Data | Import/Export | — | ✓ | ✓ | — | — | Medium | ✓ | — | — | Later |
| `io_export_report` | Io Export Report | Import/Export | — | ✓ | ✓ | — | — | Medium | ✓ | — | — | Later |
| `io_share_file` | Io Share File | Import/Export | — | ✓ | — | — | — | Medium | ✓ | — | — | Later |
| `io_import_snapshot` | Io Import Snapshot | Import/Export | — | ✓ | ✓ | — | — | Medium | ✓ | — | — | Later |
| `io_export_snapshot` | Io Export Snapshot | Import/Export | — | ✓ | ✓ | — | — | Medium | ✓ | — | — | Later |
| `io_export_manifest` | Io Export Manifest | Import/Export | — | ✓ | ✓ | — | — | Medium | ✓ | — | — | Later |
| `plugin_install` | Plugin Install | Plugin | — | ✓ | — | — | — | High | ✓ | — | — | 8 |
| `plugin_uninstall` | Plugin Uninstall | Plugin | — | ✓ | — | — | — | High | ✓ | — | — | 8 |
| `plugin_configure` | Plugin Configure | Plugin | — | ✓ | — | — | — | High | ✓ | — | — | 8 |
| `plugin_list` | Plugin List | Plugin | ✓ | — | — | — | — | High | ✓ | — | — | 8 |
| `plugin_update` | Plugin Update | Plugin | — | ✓ | — | — | — | High | ✓ | — | — | 8 |
| `plugin_enable` | Plugin Enable | Plugin | — | ✓ | — | — | — | High | ✓ | — | — | 8 |
| `plugin_disable` | Plugin Disable | Plugin | — | ✓ | — | — | — | High | ✓ | — | — | 8 |
| `plugin_dependencies` | Plugin Dependencies | Plugin | ✓ | — | — | — | — | High | ✓ | — | — | 8 |
| `plugin_pack` | Plugin Pack | Plugin | — | ✓ | — | — | — | High | ✓ | — | — | 8 |
| `plugin_inspect` | Plugin Inspect | Plugin | ✓ | — | — | — | — | High | ✓ | — | — | 8 |
| `agent_create` | Agent Create | Multi-Agent | — | ✓ | — | — | — | Medium | ✓ | — | — | 7 |
| `agent_delegate` | Agent Delegate | Multi-Agent | — | ✓ | — | — | — | Medium | ✓ | — | — | 7 |
| `agent_status` | Agent Status | Multi-Agent | ✓ | — | — | — | — | Medium | ✓ | — | — | 7 |
| `agent_list` | Agent List | Multi-Agent | ✓ | — | — | — | — | Medium | ✓ | — | — | 7 |
| `agent_update` | Agent Update | Multi-Agent | — | ✓ | — | — | — | Medium | ✓ | — | — | 7 |
| `agent_delete` | Agent Delete | Multi-Agent | — | ✓ | — | — | — | Medium | ✓ | — | — | 7 |
| `agent_configure` | Agent Configure | Multi-Agent | — | ✓ | — | — | — | Medium | ✓ | — | — | 7 |
| `agent_memory` | Agent Memory | Multi-Agent | — | ✓ | — | — | — | Medium | ✓ | — | — | 7 |
| `agent_cancel` | Agent Cancel | Multi-Agent | — | ✓ | — | — | — | Medium | ✓ | — | — | 7 |
| `agent_broadcast` | Agent Broadcast | Multi-Agent | — | ✓ | — | — | — | Medium | ✓ | — | — | 7 |
| `workflow_create` | Workflow Create | Workflow | — | ✓ | — | — | — | Medium | ✓ | — | — | 6 |
| `workflow_run` | Workflow Run | Workflow | — | ✓ | — | — | — | Medium | ✓ | — | — | 6 |
| `workflow_schedule` | Workflow Schedule | Workflow | — | ✓ | — | — | ✓ | Medium | ✓ | — | — | 6 |
| `workflow_history` | Workflow History | Workflow | ✓ | — | — | — | — | Medium | ✓ | — | — | 6 |
| `workflow_cancel` | Workflow Cancel | Workflow | — | ✓ | — | — | — | Medium | ✓ | — | — | 6 |
| `workflow_pause` | Workflow Pause | Workflow | — | ✓ | — | — | — | Medium | ✓ | — | — | 6 |
| `workflow_resume` | Workflow Resume | Workflow | — | ✓ | — | — | — | Medium | ✓ | — | — | 6 |
| `workflow_status` | Workflow Status | Workflow | ✓ | — | — | — | — | Medium | ✓ | — | — | 6 |
| `workflow_templates` | Workflow Templates | Workflow | ✓ | — | — | — | — | Medium | ✓ | — | — | 6 |
| `workflow_validate` | Workflow Validate | Workflow | — | ✓ | — | — | — | Medium | ✓ | — | — | 6 |
| `skill_list` | Skill List | Skills | — | ✓ | — | — | — | Low | ✓ | — | — | 4 |
| `skill_acquire` | Skill Acquire | Skills | — | ✓ | — | — | — | Low | ✓ | — | — | 4 |

## Permission Levels

| Level | Description |
|-------|-------------|
| Low | Read-only or non-destructive |
| Medium | Destructive or network-dependent |
| High | System-level or irreversible |

## Phase Availability

Per-tool phases are defined in [TOOLS.md](./TOOLS.md). Phases: 1 (Android foundation) · 4 (tools) · 5 (AI providers) · 6 (memory/workflows) · 7 (multi-agent) · 8 (plugins) · Later (advanced tool categories).
