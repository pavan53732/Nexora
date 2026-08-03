> Back to [PROJECT_SPECIFICATION.md](../PROJECT_SPECIFICATION.md)

# End-to-End Tests

## Scope

E2E tests exercise the complete application on a real device or emulator, validating full user journeys from touch to screen. These are the slowest but most faithful tests.

| Journey | Steps | Pass Criteria |
|---------|-------|---------------|
| Create workspace → agent → task → results | Onboard → create workspace → create agent → type task → wait for completion → verify output panel | Output contains expected result, agent state = COMPLETED |
| Install → activate → use plugin | Open plugin store → install test plugin → grant permissions → activate → create agent using plugin tool → execute | Plugin tool appears in agent, executes successfully |
| Configure provider → health check | Settings → Providers → add OpenAI key → save → run health check | Green checkmark, latency < 2s |
| Create → run workflow | Workflow builder → add 2 agents → connect output→input → run → verify final output | Both agents complete, workflow state = COMPLETED |
| Agent cancellation | Start long-running agent → tap cancel → verify state | Agent state = CANCELLED, no orphan processes |
| Kill → resume | Start agent → force-kill app → reopen → verify agent resumes | Agent state = RUNNING, partial results preserved |
| Kill on non-idempotent call → resume | Start agent mid-`http_post` → force-kill → reopen | No double side-effect; state matches exactly-once execution (FR-AS-007) |
| Network loss mid-task | Start network-dependent agent → airplane mode → restore | Degradation ladder descends (local/offline/read-only), agent pauses and resumes (FR-AS-008) |
| Provider outage storm | Mock provider 500s / rate-limit → trigger | Automatic failover to next profile, retry backoff, no crash |
| Disk-full during write | Fill workspace quota mid-write | Graceful NXR-7xxx error, partial results preserved, snapshot restore available |
| Double restart | Kill → resume → kill → resume | Context reconstructed from checkpoint each time; no loss (FR-CM-004) |
| Long-task summarization | Run 200-turn task with small token budget | No context loss; progressive summaries verifiable (FR-CM-003) |

## Framework Stack

| Tool | Purpose |
|------|--------|
| AndroidX Compose UI Test | `composeTestRule`, semantic matching, `performClick()` |
| Espresso | Legacy View interactions, `Intent` validation |
| UI Automator | Cross-app flows, notification handling |
| Barista | Simplified Espresso wrappers for dialogs, lists |
|Screenshot testing| Paparazzi for visual regression (selected screens) |

## Test Device Matrix

| Device | API | Form Factor | Orientation |
|--------|-----|-------------|-------------|
| Pixel 7 | 34 | Phone | Portrait + Landscape |
| Samsung Galaxy S23 | 34 | Phone | Portrait + Landscape |
| Pixel Tablet | 34 | Tablet | Portrait + Landscape |

## Execution Policy

| Trigger | Scope |
|---------|--------|
| Nightly CI | Full matrix (3 devices × 2 orientations × 6 journeys) |
| Pre-release | Full matrix + manual QA sign-off |
| PR | **Not run** — E2E is too slow for PR gates; covered by unit + integration |

## Flakiness Mitigation

- Each test uses `@Before` to reset app state via `ActivityScenarioRule` with `launchActivity(NEW_TASK_CLEAR_TASK)`.
- Network-dependent journeys use a local MockWebServer seeded with deterministic responses.
- Retry policy: 1 automatic retry per flaky test, then fail.