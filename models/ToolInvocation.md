> **Status: CANONICAL** for ToolInvocation domain model.
> Tool call execution state is tracked separately from the static tool descriptor.

# Domain Model: ToolInvocation

```kotlin
data class ToolInvocation(
    val toolCallId: String,
    val toolId: String,
    val workspaceId: String,
    val agentId: String?,
    val correlationId: String,
    val executionId: String?,
    val parameters: JsonObject,
    val status: ToolInvocationStatus,
    val completionState: ToolCompletionState,
    val reconciliationEvidenceRefs: List<String>,
    val result: ToolResult?,
    val startedAt: Instant,
    val completedAt: Instant?
)
```

```kotlin
enum class ToolInvocationStatus {
    PENDING_AUTHORIZATION,
    AUTHORIZED,
    EXECUTING,
    COMPLETED,
    FAILED,
    CANCELLED
}

enum class ToolCompletionState {
    NOT_ESTABLISHED,
    CONFIRMED_SUCCESS,
    CONFIRMED_FAILURE,
    UNKNOWN_COMPLETION,
    RECONCILED_SUCCESS,
    RECONCILED_FAILURE,
    MANUAL_RECONCILIATION_REQUIRED
}
```

```kotlin
sealed class ToolResult {
    data class Success(val output: JsonObject, val usage: TokenUsage?) : ToolResult()
    data class Error(val code: String, val message: String, val subreason: String?) : ToolResult()
}
```

- Every tool call is correlated by `toolCallId` and `correlationId`.
- Authorization happens before execution (see `security/PermissionModel.md`).
- `ToolExecution` events are separate from `ToolStatus` lifecycle.
- `ToolCompletionState` records operation outcome certainty and reconciliation without introducing a Tool descriptor lifecycle state.
- `UNKNOWN_COMPLETION` MUST remain unresolved until the Tool System’s declared reconciliation contract produces evidence; it MUST NOT be represented as confirmed success or confirmed failure.
