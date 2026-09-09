# Phase 8 — Judge Robustness

**Arc:** B — Core Benchmark

**Reframed per `design/COST_AND_CONTROL.md` §3:** the default judge is fully deterministic — no AI token, no model call, required for zero of the four rubric criteria. An LLM-assisted judge exists only as an opt-in extended feature behind a user-supplied `YOLOBENCH_AI_TOKEN`, for the rare free-text edge case the deterministic rubric can't resolve. This phase's scope narrows accordingly: build the deterministic default first, make the optional LLM path robust second.

## Goal
Ship a deterministic default judge that needs no AI token. Where a user opts into the LLM-assisted extended feature for a genuinely ambiguous free-text case, make that path robust against the exact class of parsing failure documented in the private strategy repo's adversarial testing library (T-14 — judge verdict hijacking via first-match JSON parsing).

## Why It Matters
Shipping a safety benchmark that's itself vulnerable to a known prompt/parsing exploit would be a credibility failure worth mocking. This phase exists specifically to close that gap before any judge component is trusted in the pipeline.

## Deliverables
- Deterministic default judge: structured-field extraction and sequence rules over `ToolCallEvent`s, no model call, covers all four rubric criteria for the Phase 6 scenario library — verified to produce a complete `ScoreResult` with zero AI tokens configured.
- Optional LLM-assisted judge, active only when `YOLOBENCH_AI_TOKEN` is set: judge output required as a structured tool call / function-call response, never parsed from free-form text via regex; if any text parsing is unavoidable, parse the LAST matching structured block, not the first (per the T-14 fix already documented).
- A small internal test: feed the optional judge a transcript containing an embedded fake "verdict" block (adversarial input, deliberately) and confirm the real verdict is still extracted correctly.

## Acceptance Criteria
- Running the full scenario library with no AI token configured produces complete, valid scores for every scenario — the core benchmark never blocks on or degrades without a token.
- The optional judge component passes its own adversarial self-test (embedded fake verdict does not override the real one) when a token is configured.

## Dependencies
Phase 7.

## Risks / Notes
This phase is small in scope but non-negotiable before Phase 10's public report — any judge-related bug discovered after publishing results would undermine every number in the report retroactively. Resist scope creep toward "just use an LLM judge for everything, it's easier" — that's exactly the dependency `COST_AND_CONTROL.md` rules out for the default path.
