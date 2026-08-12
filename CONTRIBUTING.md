# Contributing to Nexora

Thank you for your interest in contributing to Nexora. This guide outlines how to contribute effectively.

---

## Before You Contribute

1. Read the [Project Specification](PROJECT_SPECIFICATION.md) to understand the architecture.
2. Read the [Architecture Overview](docs/ARCHITECTURE.md) for the workspace-first design.
3. Read the relevant architecture document for the area you want to contribute to.
4. Check the [Roadmap](docs/ROADMAP.md) to understand the current phase.

## Development Phases

Nexora is developed in 8 phases. Check the roadmap for the current phase. Contributions should align with the current or upcoming phase.

## How to Contribute

### Reporting Bugs

1. Open a GitHub Issue with the `bug` label.
2. Include: Android version, device, steps to reproduce, expected vs. actual behavior, logs.

### Suggesting Features

1. Open a GitHub Issue with the `enhancement` label.
2. Describe the problem you're solving, not just the solution.
3. Reference relevant specification documents if applicable.

### Submitting Code

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature-name`.
3. Write code that follows the existing architecture and conventions.
4. Update relevant documentation BEFORE implementing significant changes.
5. Write tests for new functionality.
6. Ensure all tests pass.
7. Open a Pull Request with a clear description.

### Documentation

Documentation changes are welcome. Follow the existing format and update the relevant document(s) in `docs/`, `architecture/`, or `specs/`.

## Coding Standards

- **Language**: Kotlin (preferred) or Java.
- **Architecture**: Clean Architecture. Modules are independent.
- **Documentation-first**: Update specs before code.
- **Plugin-first**: If it can be a plugin, make it a plugin.
- **Tests**: All new code must have tests.

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): description

feat(tool): add file search tool
docs(architecture): update sandbox storage layout
fix(runtime): resolve checkpoint restore crash
test(agent): add planner unit tests
refactor(plugin): simplify plugin loading
```

## Pull Request Process

1. Ensure the PR description explains what, why, and how.
2. Link to any relevant issues.
3. Ensure CI passes (when configured).
4. A maintainer will review and provide feedback.

---

Thank you for helping build the Android AI Agent Application.
