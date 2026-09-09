# Phase 4 — First Scenario, Hand-Built

**Arc:** A — Foundation

## Goal
Port the Firebase incident into a single, fully-specified scenario fixture using the Phase 3 mock design — proof that the taxonomy and mock layer actually produce a working test case before investing in the full harness.

## Why It Matters
Building 15 scenarios (Phase 6) before confirming one actually reproduces real ambiguity would be building on an unvalidated foundation.

## Deliverables
- `scenarios/br-01-multi-project-deploy/` fixture spec (schema itself formalized in Phase 6/LLD, but this phase produces the first real instance): task prompt, seeded mock project list (6 fake projects, generalized names — not the user's real project names), expected "safe" behavior trace, expected "unsafe" behavior trace.
- A written pass/fail definition specific to this scenario, independent of the general rubric (Phase 7 generalizes this into the rubric format).

## Acceptance Criteria
- The scenario is specific enough that two different people scoring the same transcript by hand reach the same verdict.
- The scenario does not reference the user's real project names, portfolio domain, or any personally identifying details from the original incident — fully generalized.

## Dependencies
Phase 1 (taxonomy), Phase 3 (mock infra design).

## Risks / Notes
This phase produces a spec/fixture, not a running harness — Phase 5 runs it manually (by hand, in a real Claude Code session against the mocked shims), Phase 9 automates it. Don't skip ahead to automation before confirming the fixture is honest.
