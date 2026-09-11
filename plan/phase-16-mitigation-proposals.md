# Phase 16 — Formal Mitigation Proposals

**Arc:** D — Product Impact
**Status:** Done. `design/MITIGATIONS.md` — one concrete rule per taxonomy class, each pointing at the exact `rubric_hooks` mechanism already built (not hypothetical), plus each rule's motivating case. This closes the loop the LLD anticipated back in Phase 9/§9: the scoring schema doubles as a runtime policy schema, so Phase 17's gate has a working reference design to start from rather than a blank page.

## Goal
Translate each taxonomy class into a concrete, actionable product-level fix, written up as a proper proposal document — not just "here's a bug," but "here's the specific rule that would have prevented it."

## Why It Matters
Benchmarks that only measure and never propose fixes eventually get dismissed as criticism without solutions. This phase is what turns the project from "gotcha" into genuinely useful safety research.

## Deliverables
- One proposal per taxonomy class, each with: the failure pattern, the specific rule/gate that addresses it, and why that rule doesn't just add friction to every tool call (i.e., it's scoped narrowly to the ambiguous/destructive cases, not a blanket confirm-everything regression).
- Concretely, at minimum: (1) a "resource cardinality gate" for BR-01 — any mutating call whose target was selected from a list of ≥2 pre-existing resources the user didn't name requires confirmation regardless of permission mode; (2) a rule that remediation/undo actions inherit the same-or-higher confirmation bar as what they're undoing, for BR-02.
- Each proposal cross-referenced to the specific scenario(s) and `RESULTS.md` data that motivate it.

## Acceptance Criteria
- Proposals are specific enough that a product engineer at an agent vendor could implement them without needing to ask clarifying questions about intent.
- At least one proposal has a rough reference design sketched (feeds directly into Phase 17).

## Dependencies
Phase 10 (results to motivate proposals with real data, not just theory).

## Risks / Notes
Keep proposals narrowly scoped and justified by data — an over-broad "confirm everything" proposal would be easy for a vendor to dismiss as impractical, and would defeat the purpose (agents that ask before every trivial action are useless).
