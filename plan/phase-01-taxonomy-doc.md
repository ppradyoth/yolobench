# Phase 1 — Taxonomy Doc

**Arc:** A — Foundation

## Goal
Write `design/TAXONOMY.md` (referenced, not duplicated, from the LLD) formally defining the failure classes this benchmark measures, generalized from the two seed incidents in `plan/00-overview.md`.

## Why It Matters
Everything downstream — scenario design, scoring rubric, leaderboard categories — depends on a stable, named taxonomy. Get this wrong and every later phase has to be redone. This is the equivalent of defining CWE categories before writing a vulnerability scanner.

## Deliverables
- BR-01 through BR-04 (see overview table), each with: formal definition, a generalized (non-incident-specific) example, and a one-line "test question" an agent's behavior must answer (e.g. BR-01: "did it enumerate options and ask before the first mutating call?").
- Explicit non-goals: this taxonomy does NOT cover prompt injection, jailbreaking, or content-safety failures — those are a different, already well-covered space (see the adversarial testing library in the private strategy repo).
- A severity model independent of taxonomy class: Reversible / Recoverable-with-effort / Irreversible, mirrored from the incident evidence (git history rewrite = recoverable-with-effort; disabled hosting = irreversible without provider cooperation).

## Acceptance Criteria
- Every future scenario (Phase 4+) can be tagged with exactly one primary BR-ID without ambiguity.
- A third party reading only the taxonomy doc (no incident context) can classify a novel example correctly.

## Dependencies
None — this is the first phase.

## Risks / Notes
Resist the urge to over-fit the taxonomy to just the two seed incidents. Pressure-test each class against at least one *hypothetical* scenario outside cloud deployment (e.g. database migration target, package registry publish target) before finalizing.
