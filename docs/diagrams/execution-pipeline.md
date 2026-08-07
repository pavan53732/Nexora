> **Status: DERIVED** for execution pipeline visualization.
> Canonical source: [specs/EXECUTION_LIFECYCLE.md](../../specs/EXECUTION_LIFECYCLE.md) (§2 Software Engineering Pipeline, lines 76-120).
> This diagram introduces no new terminology or architecture.

# Execution Pipeline — Nexora

```mermaid
flowchart TD
    A[User Goal] --> B[Requirement Analysis]
    B --> C[Planning]
    C --> D[Task Decomposition]
    D --> E[Agent Selection]
    E --> F[Skill Selection]
    F --> G[Tool Selection]
    G --> H[Dependency Resolution]
    H --> I[Code Generation / Modification]
    I --> J[Build]
    J --> K{Pass?}
    K -->|Yes| L[Static Analysis]
    K -->|No| FIX1[Auto-Fix Loop]
    FIX1 --> I
    L --> M{Pass?}
    M -->|Yes| N[Unit Testing]
    M -->|No| FIX2[Auto-Fix Loop]
    FIX2 --> I
    N --> O{Pass?}
    O -->|Yes| P[Integration Testing]
    O -->|No| FIX3[Auto-Fix Loop]
    FIX3 --> I
    P --> Q{Pass?}
    Q -->|Yes| R[End-to-End Testing]
    Q -->|No| FIX4[Auto-Fix Loop]
    FIX4 --> I
    R --> S[Performance & Security Checks]
    S --> T[Self Review & Reflection]
    T --> U{Issues?}
    U -->|Yes| V[Automatic Fixes]
    V --> I
    U -->|No| W[Final Validation]
    W --> X{Acceptance Criteria?}
    X -->|Met| Y[Completion Report]
    X -->|Not Met| Z[Escalate to User]
    Y --> AA[Update Memory & Project History]

    subgraph Planning["Planning Phase"]
        B
        C
        D
    end

    subgraph Selection["Selection Phase"]
        E
        F
        G
        H
    end

    subgraph Execution["Execution & Verification"]
        I
        J
        L
        N
        P
        R
        S
    end

    subgraph Closure["Closure Phase"]
        T
        W
        Y
        AA
    end
```
