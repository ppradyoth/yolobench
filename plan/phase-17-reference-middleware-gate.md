# Phase 17 — Reference Implementation: Middleware Gate

**Arc:** D — Product Impact
**Status:** Done. `gate/policy.py` — `requires_confirmation(hooks, call)`, the live pre-execution twin of `rubric.py`'s post-hoc scoring, reusing the exact same `rubric_hooks`/`design/MITIGATIONS.md` rules. Self-test (`scripts/test_gate.py`) replays every scenario's reference personas through it for real: **0 false positives** on all 9 safe personas, **every** unsafe persona blocked before its damaging call — including both original incident's calls (`deploy` and `hosting:disable`, both flagged). Kept as a separate top-level `gate/` package (own `pyproject.toml` package-dir entry) specifically so Phase 19 can extract it without a rewrite. Real integration into an actual agent's tool-call lifecycle (e.g. a Claude Code hook) is future work — this proves the policy logic, not a shipped hook.

## Goal
Build the Phase 16 mitigation proposals as actual installable middleware — a thin policy layer that wraps tool-call execution and enforces "ambiguous + destructive → confirm," independent of any vendor choosing to adopt it natively.

## Why It Matters
This is the pivot from measuring the problem to shipping the fix. A working reference implementation is far more persuasive to vendors (Phase 18) than a proposal doc alone, and it's independently useful to anyone running agents in autonomous mode today, regardless of whether any vendor ever adopts it.

## Deliverables
- A policy-evaluation layer that can hook into an agent framework's tool-call lifecycle (starting with whatever hook/interception points Claude Code exposes — e.g. its hooks system — since that's the best-understood integration point from this project's own use) and apply the Phase 16 rules before a mutating call executes.
- Policy expressed as data/config (a rules file), not hardcoded logic, so it's portable across agent frameworks with different hook mechanisms.
- Self-test: run the Phase 6 scenario library through an agent WITH the gate installed and confirm scores improve relative to Phase 10's ungated baseline — the gate needs to prove itself against the same benchmark that motivated it.

## Acceptance Criteria
- Gate demonstrably prevents at least the two original seed-incident scenarios from reaching an unconfirmed mutating call.
- Gate's overhead/friction on non-ambiguous, non-destructive actions is negligible — verified by running a normal, non-adversarial coding session with the gate installed and confirming it doesn't nag on routine actions.

## Dependencies
Phase 16 (proposals to implement), Phase 9 (harness to test the gated agent against).

## Risks / Notes
This is the first component of the project that's a real, standalone, potentially load-bearing piece of infrastructure rather than pure benchmark tooling — treat its own code quality, test coverage, and documentation to a higher bar than the benchmark internals, since Phase 19 later spins it out as its own adoptable project.
