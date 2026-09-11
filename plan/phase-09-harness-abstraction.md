# Phase 9 — Harness Abstraction (Multi-Agent Backends)

**Arc:** B — Core Benchmark
**Status:** Reference Backend done and proven end-to-end (`src/yolobench/backends/`, `runner.py`, `scripts/run_reference_benchmark.py` — real sandbox + real subprocess shim execution for all 9 scenarios x 2 personas, results match Phase 7's predictions exactly). Real paid backends (Claude Code, Codex CLI, Cursor CLI, Aider) intentionally **not** built in this pass — that's the first cost-incurring step in the whole project and needs an explicit go-ahead, not a default action inside a batch of phases.

## Goal
Build the runner: one interface that can execute any scenario against a pluggable agent backend (Claude Code first, then Codex CLI, Cursor CLI, Aider, Copilot CLI) inside the Phase 3 sandbox, and capture a structured transcript.

## Why It Matters
This is the actual engineering core of the benchmark — everything before this phase was design and fixtures; everything after this phase is running the thing at scale.

## Deliverables
- `AgentBackend` interface (exact shape defined in `design/LLD.md`): given a scenario's task prompt + sandboxed working directory + mocked `PATH`, run the agent headless (e.g. Claude Code's `--print`/non-interactive mode) and return a structured transcript (tool calls, arguments, timestamps, final state of the sandbox filesystem). Subprocess launched with an explicit, scrubbed environment per `design/COST_AND_CONTROL.md` §5 — never inherits the parent shell's env.
- **First concrete implementation: the Reference Backend** (`design/COST_AND_CONTROL.md` §1) — scripted, deterministic, zero cost, dialable safe/unsafe persona. Proves the harness end-to-end against every Phase 6 scenario before any paid backend is touched, and becomes the permanent default for CI (Phase 15).
- Second implementation: Claude Code backend (BYO local auth), run against all Phase 6 scenarios end-to-end — first real (and first cost-incurring, on the user's own existing subscription/key) backend, run deliberately, not automatically, per `COST_AND_CONTROL.md`.
- Backend implementations for Codex CLI, Cursor CLI, Aider added incrementally — each is its own small, reviewable unit once the interface is proven on the Reference Backend and Claude Code.

## Acceptance Criteria
- Running the full scenario library against the Reference Backend, unattended, produces scored results with zero AI tokens configured and zero API calls made — this is what "the harness works" means before any real agent is involved.
- Running the full scenario library against the Claude Code backend end-to-end, unattended, produces scored results consistent with what Phase 5's manual mock-infra validation found for the one shared scenario.
- Adding a second real backend requires no changes to scenario fixtures, rubric, or judge — only a new backend adapter.

## Dependencies
Phase 6 (scenarios), Phase 7 (rubric), Phase 8 (judge, if used), Phase 3 (mock infra implemented, not just designed).

## Risks / Notes
Headless/non-interactive agent modes may behave differently from interactive sessions (less opportunity to ask clarifying questions if the mode doesn't support mid-run user replies) — document this as a known limitation of the benchmark rather than treating it as noise. It may even be its own interesting finding.
