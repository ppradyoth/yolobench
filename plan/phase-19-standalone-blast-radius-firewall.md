# Phase 19 — Standalone Blast-Radius Firewall

**Arc:** E — Moonshot

## Goal
Generalize the Phase 17 middleware gate beyond "component of this benchmark" into a standalone, independently adoptable open-source safety layer — installable via pip/npm and as a Claude Code plugin — for any team running agents in autonomous/YOLO mode.

## Why It Matters
This is the piece with genuine product/consulting legs beyond the benchmark itself. A safety layer for agentic CLI tools addresses a real, current gap, and this project would own the only public benchmark that both motivates it and proves it works — a defensible, hard-to-replicate position.

## Deliverables
- Extracted into its own package/repo (or a clearly separable module within this one — decide based on how much independent adoption interest exists by this phase), with its own README, install instructions, and policy-authoring docs aimed at teams, not just this project's maintainers.
- Policy library expanded beyond the original 4 taxonomy classes based on real-world usage feedback once external teams start adopting it.
- Integration guides for multiple agent frameworks, not just Claude Code — this is where the multi-backend investment from Phase 9 pays off again.

## Acceptance Criteria
- At least one external team (not the project maintainer) installs and uses it in a real (non-benchmark) agentic workflow.
- Package has real versioning/release discipline (semver, changelog) — it's now infrastructure other people depend on, not just research tooling.

## Dependencies
Phase 17 (working reference implementation), ideally some signal from Phase 18 (vendor engagement) about what integration points matter most.

## Risks / Notes
This phase only makes sense to pursue seriously if Phase 17's self-test and any early informal interest suggest real demand — treat the go/no-go on investing further here as a genuine decision point, not an assumed next step.
