# Phase 15 — Regression Tracking Across Agent Releases

**Arc:** D — Product Impact
**Status:** "Every commit: Reference Backend only" done and proven — `.github/workflows/validate.yml` now regenerates results and runs `scripts/check_regression.py` on every push, which diffs the freshly-generated results against whatever's committed in git HEAD and fails the build on any pass→fail flip or score drop. Verified for real: deliberately broke a scenario locally, confirmed the checker caught the exact right failure (`b_asked_before_mutation` pass→fail, score 4/4→3/4), then restored it and confirmed clean again.

**Real-backend regression tracking (the phase's original main point) is NOT active.** It can't be yet — there's no second `AgentBackend` implementation (Phase 9 deferred that), and this project holds no agent-vendor API credentials to run one on a schedule even if there were. A scheduled/`workflow_dispatch` workflow for this is documented below as a template for when a real backend exists, not added as a live (and therefore silently-broken-or-costly) workflow file today.

## Goal
CI job that reruns the full scenario library whenever a tracked agent ships a new version, diffing scores against the previous run and updating the leaderboard's historical view (Phase 11).

## Why It Matters
A single snapshot report says "here's how things stood on one date." A regression pipeline says "here's whether this is getting better or worse over time" — genuinely new accountability that doesn't currently exist publicly for this failure class.

## Deliverables
- **Every commit:** full scenario suite against the Reference Backend only — free, fast, deterministic. This is what "tests pass" means for this repo's own code (`design/COST_AND_CONTROL.md` §4).
- **Real-backend runs** (the actual point of this phase — tracking Claude Code, Codex CLI, etc. over time): scheduled (e.g. weekly), never on every commit, and never funded by this project — whoever triggers a real-backend run supplies their own local auth, same as any other use of this harness.
- Scheduled CI job (e.g. weekly, plus on-demand trigger) that checks for new pinned-agent-version availability and reruns the harness against real backends if a new version is found.
- Diff report: which scenarios flipped pass→fail or fail→pass since the last run, surfaced prominently rather than buried in a full re-listing.
- Alerting/notification path (even just a GitHub Issue auto-filed) when a regression (previously-passing scenario now fails) is detected — this is the signal most worth a human looking at quickly.

## Acceptance Criteria
- A simulated version bump (manually pointing the harness at a different pinned version) correctly produces a diff report without manual intervention.
- Historical trend data feeds Phase 11's site without manual data entry.

## Dependencies
Phase 9 (harness), Phase 10 (baseline results to diff against), Phase 11 (site to display trends).

## Risks / Notes
Agent versioning/availability isn't always clean (some ship continuously, not as discrete named releases) — the design needs a sensible definition of "a new version worth rerunning against" per backend, documented in the LLD rather than assumed uniform across all agents.
