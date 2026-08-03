# Domain Model: Workflow

> Canonical domain model. See [architecture/WORKFLOW_ENGINE.md](../architecture/WORKFLOW_ENGINE.md).

```kotlin
package com.nexora.app.runtime.workflow

data class Workflow(
    val id: String,
    val name: String,
    val steps: List<WorkflowStep>,
    val onError: ErrorStrategy = ErrorStrategy.RETRY,
    val maxRetries: Int = 3,
    val workspaceId: String,
    val createdAt: Instant
)

enum class ErrorStrategy { RETRY, SKIP, ABORT, FALLBACK }
```
