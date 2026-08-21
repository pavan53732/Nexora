> **Status: SUPPORTING** for instance lifecycle narrative.
> **The canonical state machine definition is owned by
> [../state-machines/InstanceLifecycle.md](../state-machines/InstanceLifecycle.md).**
> This file describes the instance lifecycle in prose; it MUST NOT redefine, rename,
> or subset any state enum from the canonical source.
>
> Depends on: [../state-machines/InstanceLifecycle.md](../state-machines/InstanceLifecycle.md).

# Instance Lifecycle Authority — Nexora

## Pairing Status

`UNPAIRED`, `PAIRED`, `REVOKED`

### Transitions

- `UNPAIRED → PAIRED`: `pair()` — pairing handshake complete.
- `PAIRED → REVOKED`: `revoke()` — explicit revocation.
- `UNPAIRED → REVOKED`: Invalid pairing attempt.

## Pipe Status

`PAIRED`, `CONNECTED`, `DEGRADED`, `DISCONNECTED`, `REVOKED`

### Transitions

- `PAIRED → CONNECTED`: `connect()` — handshake complete, delegation/broadcast allowed.
- `CONNECTED → DEGRADED`: Health failing; no new delegations.
- `DEGRADED → CONNECTED`: Health restored.
- `CONNECTED/DEGRADED → DISCONNECTED`: `disconnect()` — closed; reconnectable.
- `* → REVOKED`: `revoke()` — terminal; re-pairing required.
