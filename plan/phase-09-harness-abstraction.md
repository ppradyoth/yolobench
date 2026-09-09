# Phase 9 — Harness Abstraction (Multi-Agent Backends)

**Arc:** B — Core Benchmark

## Goal
Build the runner: one interface that can execute any scenario against a pluggable agent backend (Claude Code first, then Codex CLI, Cursor CLI, Aider, Copilot CLI) inside the Phase 3 sandbox, and capture a structured transcript.

## Why It Matters
This is the actual engineering core of the benchmark — everything before this phase was design and fixtures; everything after this phase is running the thing at scale.

## Deliverables
- `AgentBackend` interface (exact shape defined in `design/LLD.md`): given a scenario's task prompt + sandboxed working directory + mocked `PATH`, run the agent headless (e.g. Claude Code's `--print`/non-interactive mode) and return a structured transcript (tool calls, arguments, timestamps, final state of the sandbox filesystem).
- First concrete implementation: Claude Code backend only, run against all Phase 6 scenarios end-to-end.
- Backend implementations for Codex CLI, Cursor CLI, Aider added incrementally — each is its own small, reviewable unit once the interface is proven on Claude Code.

## Acceptance Criteria
- Running the full scenario library against the Claude Code backend end-to-end, unattended, produces scored results matching what Phase 5's manual run found for the one shared scenario.
- Adding a second backend requires no changes to scenario fixtures, rubric, or judge — only a new backend adapter.

## Dependencies
Phase 6 (scenarios), Phase 7 (rubric), Phase 8 (judge, if used), Phase 3 (mock infra implemented, not just designed).

## Risks / Notes
Headless/non-interactive agent modes may behave differently from interactive sessions (less opportunity to ask clarifying questions if the mode doesn't support mid-run user replies) — document this as a known limitation of the benchmark rather than treating it as noise. It may even be its own interesting finding.
