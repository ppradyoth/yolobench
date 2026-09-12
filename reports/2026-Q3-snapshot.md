# State of Agentic Blast-Radius Safety — 2026-Q3

Snapshot #2 (by count of prior `reports/*.md` files). Generated 2026-09-12T18:52:12.786870+00:00.

## What this snapshot can and can't claim

This is snapshot #2 — a quarter-over-quarter comparison becomes meaningful starting from the second one onward, via `scripts/check_regression.py` against each prior committed run.

No real coding agent has been benchmarked yet — every backend below is the scripted, zero-cost Reference Backend (`design/COST_AND_CONTROL.md` §1), not a claim about Claude Code, Codex CLI, Cursor, or Aider's actual behavior. This report format exists so that once real-backend runs start (Phase 9's second backend, Phase 18's cost-incurring step), each quarter's comparison is automatic rather than assembled by hand.

## This snapshot

- Scenarios: 9 across all 4 taxonomy classes (`design/TAXONOMY.md`)
- Backends evaluated: reference-safe, reference-unsafe
- Full results: [`results/latest.json`](../results/latest.json), [`RESULTS.md`](../RESULTS.md)
- Live leaderboard: https://ppradyoth.github.io/yolobench/

## Cadence plan

Quarterly, once real-backend data exists to make quarter-over-quarter comparison meaningful. Until then, snapshots are generated ad hoc as the benchmark itself develops (new scenarios, rubric changes) rather than on a fixed calendar — a fixed cadence with nothing new to report each time would train readers to stop reading, which defeats the point.
