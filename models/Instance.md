> **Status: DERIVED** for Instance and Pipe domain models.
> This document defines the shape and semantics of Instance (peer identity) and Pipe
> (live channel) in the data model.
>
> Depends on: [../specs/PIPES.md](../specs/PIPES.md), [../state-machines/InstanceLifecycle.md](../state-machines/InstanceLifecycle.md).
> Referenced by: protocols, APIs, registries, and runtime implementations.

# Domain Model: Instance & Pipe

```kotlin
data class RemoteInstance(
    val instanceId: String,              // UUIDv4, stable per install
    val instanceName: String,            // display name
    val fingerprint: String,             // pipeKey public key fingerprint (pairing identity)
    val capabilities: JsonObject,        // advertised {appVersion, minContractVersion, workspace summary}
    val pairingStatus: PairingStatus,
    val acceptanceMode: AcceptanceMode,  // per-pipe FR-S016 override
    val pairedAt: Instant?,
    val lastSeenAt: Instant?
)

enum class PairingStatus {
    UNPAIRED,
    PAIRED,
    REVOKED
}

enum class AcceptanceMode {     // mirrors FR-S016 autonomy modes, per pipe
    MANUAL,
    ASSISTED,
    AUTOPILOT
}

data class Pipe(
    val pipeId: String,                  // stable per (localInstance, remoteInstance, workspace)
    val workspaceId: String,             // pipes are workspace-scoped
    val localInstanceId: String,
    val remoteInstanceId: String,
    val transport: PipeTransport,        // LOOPBACK or LAN_MTLS
    val status: PipeStatus,
    val lastHeartbeatAt: Instant?,
    val openedAt: Instant?,
    val closedAt: Instant? = null,
    val latestError: CanonicalErrorEnvelope? = null
)

enum class PipeTransport {
    LOOPBACK,      // same machine (rendezvous directory + loopback)
    LAN_MTLS       // LAN peer (mDNS discovery + mutual TLS 1.3)
}

enum class PipeStatus {
    PAIRED,         // trusted, not connected
    CONNECTED,      // handshake complete; delegation/broadcast allowed
    DEGRADED,       // health failing; no new delegations
    DISCONNECTED,   // closed; reconnectable
    REVOKED         // terminal; re-pairing required
}
```

## Lifecycle and Semantics

Pipe lifecycle authority is defined in
[state-machines/InstanceLifecycle.md](../state-machines/InstanceLifecycle.md). Pipe
status is a session-scoped transport projection; `PairingStatus` is the durable trust
record. A delegated task riding a pipe remains a canonical `Task`
([Task.md](Task.md)) on both instances, correlated by `correlationId` + `pipeId`;
pipe state MUST NOT replace task lifecycle state.

### Invariants

- `Pipe.status = CONNECTED` requires `RemoteInstance.pairingStatus = PAIRED` for the
  remote endpoint (enforced by the `connect()` guard).
- `workspaceId` is immutable for the life of a pipe; exposing a second workspace to the
  same instance creates a second pipe, never widens an existing one.
- `REVOKED` purges the stored fingerprint and closes all pipes of that instance
  atomically.
- Pipe payloads never serialize provider credentials or `SecureKeyStore` aliases
  (NFR-SEC-011/012/013 extended — see [../specs/PIPES.md](../specs/PIPES.md) §8).
