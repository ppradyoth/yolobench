# Phase 10 — First Public Run + Report

**Arc:** B — Core Benchmark
**Status:** Done, scoped to the Reference Backend. `scripts/publish_results.py` produces `results/<run_id>.json`, `results/latest.json`, `RESULTS.md`, and per-run transcripts, all committed for auditability. `RESULTS.md` leads with an explicit methodology note: Reference Backend only, no real agent benchmarked yet, don't read these numbers as agent safety claims.

## Goal
Run the full scenario library against every wired-up agent backend and publish real numbers as `RESULTS.md`.

## Why It Matters
This is the first artifact anyone outside this project can actually evaluate. Everything in Arc C (leaderboard, paper, talks) depends on having credible, honestly-caveated numbers to point to.

## Deliverables
- `RESULTS.md`: per-agent, per-scenario, per-taxonomy-class scores, with agent versions pinned and run dates recorded.
- Explicit methodology section: sample size, what "pass" means per Phase 7's rubric, known limitations (headless-mode caveat from Phase 9, mock-infra fidelity limits from Phase 3).
- Raw transcripts (or a subset) published alongside scores for auditability — a benchmark that hides its transcripts invites (justified) skepticism.

## Acceptance Criteria
- Numbers are reproducible: rerunning the harness against the same pinned agent version produces the same (or explainably similar, if the agent is non-deterministic) scores.
- Report is honest about small N — this is a first pass, not a definitive ranking.

## Dependencies
Phase 9.

## Risks / Notes
Resist the temptation to overstate findings from a small scenario set. The credibility of everything downstream (paper, vendor engagement) rests on this report being conservative and methodologically sound rather than maximally dramatic.
