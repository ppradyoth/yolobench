# Phase 6 — Scenario Library v1

**Arc:** B — Core Benchmark

## Goal
Expand from 1 to 10–15 scenarios, covering all four taxonomy classes (BR-01 through BR-04), using the validated Phase 4/5 format.

## Why It Matters
A benchmark with one scenario is an anecdote. 10–15 across all classes is the minimum credible surface for a first public report (Phase 10).

## Deliverables
- Scenarios distributed roughly: BR-01 (ambiguous resource) — cloud deploy targets, git remote selection, database/migration targets, package registry publish targets. BR-02 (destructive remediation) — "undo your mistake" traps across at least 2 domains. BR-03 (persistence inflation) — credential storage decisions (env var vs. hardcode vs. secrets manager), config persistence choices. BR-04 (scope creep) — "authenticate to X" expanding into unrequested specific actions.
- Formal scenario schema (YAML/JSON) finalized here and documented in `design/LLD.md` — this is the first artifact that needs a stable, versioned format since community contributions (Phase 12) depend on it.
- Each scenario: task prompt, mock fixture data, safe/unsafe behavior traces, primary + secondary BR-ID tags, severity tag.

## Acceptance Criteria
- Every taxonomy class has ≥2 scenarios.
- Schema validates against a JSON Schema / Pydantic model (first real code artifact of the project — see LLD for exact tooling).

## Dependencies
Phase 5 (validated format), Phase 3 (mock infra design finalized enough to build more fixtures against).

## Risks / Notes
First phase where actual code (schema + fixtures) starts landing in the repo. This is the Arc A → Arc B transition — code review discipline starts here, not before.
