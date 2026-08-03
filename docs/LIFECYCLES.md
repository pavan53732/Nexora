> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

# Entity Lifecycle Flows

> **Status: SUPPORTING.** This document describes lifecycle flows as prose narratives.
> Formal state machine definitions live in `state-machines/`. Any state name used below
> is descriptive prose, not a formal enum. The canonical Task state set is defined
> exclusively in [state-machines/TaskLifecycle.md](../state-machines/TaskLifecycle.md).
> This document must not be treated as an alternate source of truth for any state enum.

This document covers creation, initialization, active use, shutdown/teardown, and error recovery narratives for every core entity in Nexora.

---

## 1. Workspace Lifecycle

**Creation.** The user taps "New Workspace" in the UI. `WorkspaceManager.create(name, template?)` validates the name and optional template, performs a Room DB insert, and creates a sandbox directory at `/data/data/com.nexora.app/sandbox/workspaces/{id}/`. On success, `EventBus` publishes `WorkspaceCreated` and the UI navigates to the workspace dashboard.

**Active Use.** When the user opens a workspace, `WorkspaceManager.load(id)` retrieves all associated agents, tasks, files, and settings from the database, restores the sandbox directory reference, and publishes `WorkspaceOpened`.

**Switching.** Selecting a different workspace triggers the current workspace to pause: running agents are checkpointed, then the new workspace is loaded through the same flow.

**Deletion.** `WorkspaceManager.delete(id)` first confirms with the user, stops all running agents within the workspace, deletes the sandbox directory, performs a cascading DB delete, and publishes `WorkspaceDeleted`.

**Error Recovery.** If sandbox directory creation fails, error code NXR-7001 is raised. The workspace is marked with an error state and the user is offered a retry action.

---

## 2. Agent Lifecycle

**Creation & Configuration.** `AgentManager.create(config)` validates the configuration against the `AgentType` schema and stores it in Room. The user then configures the provider, system prompt, permissions, tools, and memory scope — all persisted to the database.

**Start & Execution.** Sending a goal calls `AgentManager.start(agentId, goal)`, which instantiates an `AgentLoop`, sets state to `Running`, and starts a `ForegroundService` if needed. The loop then runs the plan → execute → reflect cycle: tools are invoked through `ToolManager`, results are stored in memory, and events are published at each stage.

**Pause & Resume.** Pausing suspends the `AgentLoop` at the next safe iteration boundary, saves a checkpoint, and optionally keeps the `ForegroundService` alive for monitoring. Resuming restores from that checkpoint and continues execution.

**Completion.** When the goal is achieved, the loop terminates, state becomes `Completed`, a summary is persisted, a notification is sent to the user, and the `ForegroundService` stops.

**Failure & Cancellation.** Unrecoverable errors set state to `Failed`, store error details, notify the user, and offer a retry option. User-initiated cancellation sets a flag checked at every iteration, allowing graceful shutdown with partial results saved.

---

## 3. Tool Lifecycle

**Registration & Discovery.** A tool implements the `Tool` interface and is registered (via annotation or explicit call) in the `ToolRegistry`. At invocation time, `ToolManager.resolve(toolId)` locates the tool and verifies that the requesting agent holds the required permissions.

**Execution & Caching.** With permission granted, `ToolManager.execute(toolId, params, context)` runs the tool. If the tool requires sandbox isolation, execution is redirected inside the sandbox. Identical parameter sets may be served from the tool result cache.

**Error Handling.** Tool timeouts produce error NXR-2002 and return a `ToolResult.Error` carrying a `recoverable` flag, letting the agent decide whether to retry.

---

## 4. Plugin Lifecycle

**Discovery & Download.** `PluginManager` scans configured sources (local storage, marketplace) and reads each plugin manifest. Downloading stores the APK or JAR in plugin storage and verifies its checksum.

**Installation & Activation.** A `ClassLoader` loads the plugin, the manifest is validated, and metadata is persisted to Room. `Plugin.onActivate(pluginContext)` is then called, allowing the plugin to register tools, providers, or agent types. `EventBus` publishes `PluginActivated`.

**Deactivation & Uninstall.** `Plugin.onDeactivate()` unregisters all extensions and `PluginDeactivated` is published. Full uninstall calls `Plugin.onUninstall()` for data cleanup, then deletes plugin files.

---

## 5. Provider Lifecycle

**Registration & Configuration.** A provider is added to `ProviderManager` with its config (API key, base URL, model). The API key is encrypted via `SecureKeyStore` and the full config is persisted to `DataStore`.

**Health & Failover.** Periodic `provider.healthCheck()` calls update the provider state to `Healthy`, `Degraded`, or `Unhealthy`. If a provider becomes unhealthy, `ProviderManager` automatically switches to the next configured provider and publishes `ProviderSwitched`.

**Use & Removal.** Runtime code calls `ProviderManager.getActiveProvider()` to route completion and streaming requests while monitoring latency and errors. Removing a provider deletes its config and clears the key from the keystore.

---

## 6. Runtime Lifecycle

**Initialization.** On app start, `NexoraApplication.onCreate()` triggers Hilt injection of `EventBus`, `ToolManager`, `ProviderManager`, `MemoryManager`, and other singletons. Room databases run migrations and installed plugins are loaded.

**Active & Background.** With the event bus running, providers healthy, tools registered, and memory available, agents can be started. When the app is minimized, any `ForegroundService` keeps agent execution alive and `WorkManager` handles scheduled tasks.

**Shutdown & Restore.** If the app is killed, Android restores the `ForegroundService` for running agents. On the next launch, checkpointed agents resume from their last saved state.

---

## 7. Background Execution Lifecycle

**Start & Maintenance.** A long-running agent task starts `AgentExecutionService` as a foreground service with a persistent notification. The service holds a CPU wake lock (within Android's limits), checkpoints every 30 seconds, and monitors battery level.

**Optimization.** When battery is low, checkpoint frequency is reduced, non-essential work is paused, and the user is notified of the throttle.

**Stop & Restore.** On agent completion, failure, or cancellation the service stops, the notification is removed, and the wake lock is released. After a device restart, `BootReceiver` checks for incomplete executions, restarts `AgentExecutionService`, and agents resume from their last checkpoint.
