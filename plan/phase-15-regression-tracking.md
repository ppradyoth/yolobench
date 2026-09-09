# Phase 15 — Regression Tracking Across Agent Releases

**Arc:** D — Product Impact

## Goal
CI job that reruns the full scenario library whenever a tracked agent ships a new version, diffing scores against the previous run and updating the leaderboard's historical view (Phase 11).

## Why It Matters
A single snapshot report says "here's how things stood on one date." A regression pipeline says "here's whether this is getting better or worse over time" — genuinely new accountability that doesn't currently exist publicly for this failure class.

## Deliverables
- Scheduled CI job (e.g. weekly, plus on-demand trigger) that checks for new pinned-agent-version availability and reruns the harness if a new version is found.
- Diff report: which scenarios flipped pass→fail or fail→pass since the last run, surfaced prominently rather than buried in a full re-listing.
- Alerting/notification path (even just a GitHub Issue auto-filed) when a regression (previously-passing scenario now fails) is detected — this is the signal most worth a human looking at quickly.

## Acceptance Criteria
- A simulated version bump (manually pointing the harness at a different pinned version) correctly produces a diff report without manual intervention.
- Historical trend data feeds Phase 11's site without manual data entry.

## Dependencies
Phase 9 (harness), Phase 10 (baseline results to diff against), Phase 11 (site to display trends).

## Risks / Notes
Agent versioning/availability isn't always clean (some ship continuously, not as discrete named releases) — the design needs a sensible definition of "a new version worth rerunning against" per backend, documented in the LLD rather than assumed uniform across all agents.
