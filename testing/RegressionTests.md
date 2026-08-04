# Regression Tests

## Scope

Regression tests guard against contract drift and previously fixed failures.

## Framework Stack

- reproducible fixture harness
- golden contract samples
- compatibility comparison tooling

## Regression Test Database

The regression corpus SHOULD include canonical request/response/event samples for Agent, Tool, Provider, Plugin, Runtime, and Memory paths.

## Data Migration Testing

Schema or manifest changes must retain backward-compatible interpretation where required.

## Plugin API Backward Compatibility

Plugin compatibility testing SHOULD include activation rollback and exported capability compatibility checks.

## Run Schedule

Run on release candidates and on any contract-affecting change.
