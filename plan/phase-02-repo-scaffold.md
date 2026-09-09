# Phase 2 — Repo Scaffold

**Arc:** A — Foundation
**Status:** Done. README/LICENSE/.gitignore/plan/design shipped at repo creation; branch protection on `main` (no force-push, no deletion, no PR requirement yet since it's solo-maintained and there's no CI to gate on) enabled once Phase 6 started landing real code, per the original deferral note below.

## Goal
Public GitHub repo, licensed, with a structure that can hold plan, design, and (later) code without reorganization.

## Why It Matters
A benchmark that wants community scenario submissions (Phase 12) and citation in a paper (Phase 13) needs a stable, professional public presence from day one — restructuring later breaks incoming links and PRs.

## Deliverables
- `README.md` — project pitch, status, principles, layout (done — see repo root).
- `LICENSE` (MIT) (done).
- `.gitignore` scoped for the eventual Python/Node mix (done).
- `plan/` and `design/` folders (this phase's actual output).
- GitHub repo created and pushed, public, description + topics set (`agentic-ai`, `ai-safety`, `red-teaming`, `llm-agents`).
- Branch protection on `main` deferred until Phase 6 (code starts landing) — not needed while the repo is plan/design only.

## Acceptance Criteria
- `git clone` from a clean machine reproduces the full plan + design tree.
- Repo is discoverable (public, has a description, has topics) — not just pushed silently.

## Dependencies
None.

## Risks / Notes
Do not add empty placeholder code directories (`src/`, `tests/`) yet — Arc A is explicitly plan/design-only. Empty scaffolding invites premature, unplanned code changes before the LLD is settled.
