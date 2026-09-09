# Phase 5 — Manual POC Run Against Claude Code

**Arc:** A — Foundation

## Goal
Run the Phase 4 scenario by hand, once, in a real Claude Code session pointed at the mocked shims, and confirm it actually reproduces ambiguity — the agent shouldn't be able to tell it's a test.

## Why It Matters
This is the last checkpoint before committing engineering effort (Arc B) to automate something that might not actually work as designed. Cheap to run by hand; expensive to discover the fixture was flawed after building a harness around it.

## Deliverables
- One captured transcript (redacted of any local-machine specifics) stored under `plan/evidence/phase-05-poc-transcript.md` or similar, showing the agent's actual behavior against the mock.
- A short writeup: did it reproduce BR-01 ambiguity as designed? Did the agent behave identically to, better than, or worse than the real incident?
- Go/no-go note on whether the scenario format needs revision before Phase 6 scales it up.

## Acceptance Criteria
- Transcript shows the agent facing genuine ambiguity (not an obviously synthetic test it could pattern-match as "this is a benchmark").
- Scoring rubric draft (informal, ahead of Phase 7) can be applied to this transcript and produce an unambiguous verdict.

## Dependencies
Phase 4.

## Risks / Notes
Agents may behave differently when they suspect they're being evaluated ("eval awareness"). Worth noting in the transcript writeup whether anything in the fixture reads as obviously synthetic, and folding that observation into scenario design going forward (Phase 6).
