# Phase 11 — Live Leaderboard Site

**Arc:** C — Credibility & Reach

## Goal
Static site (GitHub Pages) auto-generated from `RESULTS.md` / the underlying results data, versioned per agent release, so scores are comparable over time.

## Why It Matters
A markdown table in a repo gets read once. A live, linkable leaderboard gets shared, cited, and revisited — it's the artifact that turns a one-time report into an ongoing reference.

## Deliverables
- Static site generator (kept simple — plain HTML/CSS/JS or a minimal static-site tool, no heavy framework) reading a results data file (JSON) as its source of truth, so the site and `RESULTS.md` never drift out of sync — one generates the other, or both generate from the same underlying data.
- Per-agent, per-version historical view (line chart or table showing score trend across agent versions over time), not just a current snapshot.
- Clear "last updated" and "methodology" links on every page — the same honesty requirement as Phase 10's report, now user-facing.

## Acceptance Criteria
- Site auto-deploys on merge to `main` (or on a results-data update) via GitHub Actions — no manual publish step.
- A visitor with zero prior context can understand what's being measured within one screen of reading, without needing to read the full plan/design docs.

## Dependencies
Phase 10 (needs real results data to render).

## Risks / Notes
Keep the design plain and credible-looking rather than flashy — this is a research artifact, not a marketing page. Overly slick design on thin data undermines trust.
