# Phase 12 — Community Scenario Submission Format

**Arc:** C — Credibility & Reach
**Status:** Done, not yet proven by a real external PR (that requires an actual outside contributor, can't be manufactured). `CONTRIBUTING.md`, `.github/PULL_REQUEST_TEMPLATE.md`, and `.github/workflows/validate.yml` (runs on every push/PR: schema+shim+blind-mode audit, rubric self-test, judge self-test, real end-to-end harness run — this workflow also fulfills Phase 15's "every commit: Reference Backend only" requirement, so that phase reuses it rather than duplicating it).

## Goal
Make it possible for outside contributors to submit new scenarios as PRs, the way new tasks get added to SWE-bench-style benchmarks.

## Why It Matters
A benchmark maintained solely by one person plateaus at whatever scenarios that person thought of. A benchmark with a contribution pipeline can grow taxonomy coverage and catch blind spots the original author has.

## Deliverables
- `CONTRIBUTING.md` with the scenario schema (from Phase 6), a worked example, and explicit guidance on the mock-infra boundary (Phase 3) — no submission may require real credentials or real network calls, enforced by CI.
- A PR template requiring: taxonomy tag(s), safe/unsafe behavior trace, and a statement that the scenario was tested against the mock harness locally before submission.
- CI check (extends Phase 15's regression pipeline) that validates schema conformance and runs the new scenario against at least one backend before merge.

## Acceptance Criteria
- A contributor unfamiliar with the project's internals can follow `CONTRIBUTING.md` alone to submit a valid, passing scenario PR.
- At least one real external contribution merged before calling this phase done — a contribution guide nobody has used yet is unproven.

## Dependencies
Phase 6 (schema), Phase 9 (harness to test submissions against).

## Risks / Notes
Low-quality or duplicate scenario submissions are a real maintenance cost — consider a lightweight review checklist (does this genuinely test a new ambiguity, or restate an existing scenario with different names) before merging.
