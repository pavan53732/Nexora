# Test Evidence Conventions — Nexora

## Purpose

This document defines how test evidence should be referenced from the test inventory and traceability artifacts.

## Evidence Path Convention

Evidence SHOULD be stored or referenced using a stable logical pattern:

`evidence/<suite>/<case-id>/<yyyy-mm-dd>/<artifact>`

Examples:

- `evidence/unit/UT-CONTRACT-002/2026-08-04/report.md`
- `evidence/integration/IT-CONTRACT-001/2026-08-04/log.txt`
- `evidence/security/SEC-SBX-001/2026-08-04/findings.md`

## Result Convention

Test case inventories SHOULD eventually track one of:

- `Planned`
- `In Progress`
- `Passed`
- `Failed`
- `Blocked`
- `Obsolete`

## Minimum Evidence Metadata

Each evidence record SHOULD capture:

- case identifier
- execution date
- executor or system owner
- environment or fixture description
- result status
- artifact location
- notable findings or deviations
