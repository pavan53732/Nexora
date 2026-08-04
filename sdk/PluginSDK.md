# Plugin SDK — Nexora

> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md) | See [../docs/api/Plugin-API.md](../docs/api/Plugin-API.md)

---

## Normative SDK Contract

The Plugin SDK MUST preserve the contract defined by [Plugin-API.md](../docs/api/Plugin-API.md). Convenience helpers MUST NOT bypass manifest validation, dependency resolution, transactional activation, or canonical error-envelope handling.

### Required Operation Coverage

A conforming SDK implementation MUST provide typed support for:

- manifest creation and validation
- plugin install/activate/deactivate/remove operations
- dependency and compatibility metadata
- exported capability declaration by type
- signature/integrity metadata
- canonical error-envelope creation and propagation

## Overview

The Plugin SDK helps package authors create plugins that conform to the canonical plugin contract.

## Plugin Structure

A plugin package MUST declare a machine-readable manifest, exported capability descriptors, compatibility metadata, and integrity/signature material.

## Plugin Manifest

Free-form maps are not sufficient. The SDK MUST expose typed manifest builders and validators.

## Plugin Implementation

Activation helpers MUST support rollback if any exported capability registration fails.

## Distribution

Published plugin packages MUST carry compatibility metadata for API contract version, SDK contract version, manifest/schema version, and dependency ranges.
