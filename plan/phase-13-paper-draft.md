# Phase 13 — Paper Draft

**Arc:** C — Credibility & Reach

## Goal
Write a paper using the benchmark and Phase 10 results as its evidentiary core: "Judgment Under Ambiguity: A Benchmark for Agentic Blast-Radius Awareness in Coding Assistants" (working title).

## Why It Matters
Pairs with the existing conference/paper track already underway in the private strategy repo. A reproducible public benchmark is far stronger paper evidence than incident write-ups alone — reviewers can independently verify claims.

## Deliverables
- Paper structure: motivation (the two seed incidents, generalized and already sanitized — no confidential third-party data involved here, this is the author's own tooling use), taxonomy (Phase 1), methodology (Phases 3–9), results (Phase 10), related work (position against capability benchmarks and existing prompt-injection-focused red-team literature), limitations, and the Phase 16 mitigation proposals as a forward-looking contribution.
- Target venue selection using the existing conference tracker in the private strategy repo — this paper's angle (agentic tool safety, not chatbot content safety) may fit different venues than the Jack & Jill work.

## Acceptance Criteria
- Every empirical claim in the paper traces to a specific `RESULTS.md` entry or reproducible harness run — no claims that outrun the actual data.
- Draft reviewed against the existing paper-review skill/process already used for other submissions in this workflow.

## Dependencies
Phase 10 (needs real results), ideally Phase 11 (a live, citable leaderboard strengthens a submission).

## Risks / Notes
Keep this paper's scope distinct from the Jack & Jill / WSR paper tracks already in flight — this is a new, separate contribution (agentic tool safety benchmark), not a rehash. Cross-reference rather than duplicate.
