> **Status: DERIVED** for Plugin Lifecycle Flow visual flow.
> This diagram illustrates Plugin Lifecycle Flow flow. The canonical definition is in the relevant architecture or state-machine document.
>
> Depends on: the relevant canonical architecture or state-machine document.


> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

# Plugin Lifecycle Flow

This diagram traces the full plugin lifecycle from user-initiated installation through signature verification, activation, tool registration, and eventual deactivation.

```mermaid
sequenceDiagram
    participant User
    participant PluginManager
    participant PluginRegistry
    participant Downloader
    participant Verifier
    participant PluginAPK
    participant PluginContext
    participant EventBus

    User->>PluginManager: install(pluginId)
    PluginManager->>Downloader: download(pluginId)
    Downloader-->>PluginManager: plugin.apk (temp file)

    PluginManager->>Verifier: verifySignature(plugin.apk)

    alt Signature invalid
        Verifier-->>PluginManager: SignatureInvalidException
        PluginManager->>Downloader: cleanup(temp file)
        PluginManager-->>User: Installation failed
    else Signature valid
        Verifier-->>PluginManager: Verified
        PluginManager->>PluginManager: installAPK(plugin.apk)
        PluginManager->>PluginRegistry: register(plugin)
        PluginRegistry-->>PluginManager: PluginRecord
        PluginManager->>EventBus: publish(PluginInstalledEvent)
        PluginManager-->>User: Plugin installed
    end

    User->>PluginManager: activate(pluginId)
    PluginManager->>PluginAPK: loadClass(pluginId)
    PluginAPK-->>PluginManager: Plugin instance
    PluginManager->>PluginContext: create(plugin, workspaceId)
    PluginContext-->>PluginManager: context
    PluginManager->>PluginAPK: onActivate(context)
    PluginAPK->>PluginRegistry: registerTools(tools)
    PluginRegistry-->>PluginAPK: Tools registered
    PluginManager->>EventBus: publish(PluginActivatedEvent)

    opt User deactivates
        User->>PluginManager: deactivate(pluginId)
        PluginManager->>PluginAPK: onDeactivate()
        PluginAPK->>PluginRegistry: unregisterTools(tools)
        PluginManager->>EventBus: publish(PluginDeactivatedEvent)
    end
```