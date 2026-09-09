# Phase 8 — Judge Robustness

**Arc:** B — Core Benchmark

## Goal
Where any part of scoring still needs an LLM judge (e.g. classifying free-text agent explanations, or scenarios where tool-call structure alone is ambiguous), make that judge robust against the exact class of parsing failure documented in the private strategy repo's adversarial testing library (T-14 — judge verdict hijacking via first-match JSON parsing).

## Why It Matters
Shipping a safety benchmark that's itself vulnerable to a known prompt/parsing exploit would be a credibility failure worth mocking. This phase exists specifically to close that gap before any judge component is trusted in the pipeline.

## Deliverables
- Judge output required as a structured tool call / function-call response, never parsed from free-form text via regex.
- If any text parsing is unavoidable, parse the LAST matching structured block, not the first (per the T-14 fix already documented).
- A small internal test: feed the judge a transcript containing an embedded fake "verdict" block (adversarial input, deliberately) and confirm the real verdict is still extracted correctly.
- Documented decision on how much of scoring needs a judge at all vs. can stay fully deterministic per Phase 7's structured rubric — minimize judge usage, it's a last resort for genuinely ambiguous free-text cases only.

## Acceptance Criteria
- Judge component passes its own adversarial self-test (embedded fake verdict does not override the real one).
- Judge is used only where Phase 7's deterministic rubric genuinely cannot resolve a criterion from structured events alone.

## Dependencies
Phase 7.

## Risks / Notes
This phase is small in scope but non-negotiable before Phase 10's public report — any judge-related bug discovered after publishing results would undermine every number in the report retroactively.
