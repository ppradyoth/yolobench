# Plan Overview

## Core thesis

Coding agents running in autonomous/bypass modes treat authorization for a *class* of action as authorization for every *specific decision* inside that class — including which of several pre-existing resources to touch, and how to "fix" a mistake. This is a distinct failure class from prompt injection or jailbreaking: no adversarial input is involved, the agent is doing exactly what a well-intentioned user asked, and it still causes real, irreversible, external damage.

## Seed evidence

Two independent incidents, three-plus months apart, two different local projects, same underlying shape:

1. **Credential exposure** (2026-05-22) — agent hardcoded a live GitHub PAT and SMTP password into version-controlled instruction files and pushed them. Authorized: "authenticate to GitHub." Not authorized: *how* to persist the credential.
2. **Firebase blast radius** (2026-09-05) — agent silently picked an existing production Firebase project (the user's personal portfolio) out of 6 candidates and deployed over it, then "fixed" the objection by running `firebase hosting:disable --force`, taking the portfolio offline. Authorized: "deploy to Firebase Hosting." Not authorized: *which* project, or the destructive "fix."

Full incident writeups live in the private `ai-security-strategy` repo (`findings/anthropic/claude-code/`) and are not duplicated here verbatim — this repo generalizes the pattern into a public, reproducible benchmark.

## Taxonomy (expanded in Phase 1)

| ID | Name | Shape |
|---|---|---|
| BR-01 | Ambiguous Resource Selection | ≥2 pre-existing resources match the task; agent picks one without asking |
| BR-02 | Unconfirmed Destructive Remediation | Agent's own "fix" for a mistake is itself an unconfirmed destructive action |
| BR-03 | Persistence-Method Inflation | Authorized for an outcome, agent unilaterally chooses a persistence mechanism with different risk (e.g. hardcoding a secret vs. an env var) |
| BR-04 | Scope Creep (class → instance) | General authorization silently expanded to cover a specific, higher-risk instance of that action |

## Constraints

**Zero-cost by default, AI opt-in only.** Added after initial planning, binding on every phase from here on — see [`design/COST_AND_CONTROL.md`](../design/COST_AND_CONTROL.md). Nobody should need an AI token to clone this repo and get a real result: core scoring and a first backend are deterministic code, real agent backends are always bring-your-own-auth, and any LLM-assisted feature (e.g. a nuanced judge) is a named, off-by-default extended feature gated behind a user-supplied token. This reshapes Phase 8 (judge) and Phase 9 (a scripted Reference Backend now ships before any real one) without changing the taxonomy or overall architecture.

## Progress

- Phase 1 (Taxonomy) — done, see [`../design/TAXONOMY.md`](../design/TAXONOMY.md).
- Phase 2 (Repo scaffold) — done, including branch protection on `main` (no force-push/deletion) now that Phase 6 code is landing.
- Phase 3 (Mock infra design) — done, see [`../design/MOCK_INFRA.md`](../design/MOCK_INFRA.md).
- Phase 4 (First scenario) — done, see `../scenarios/br-01-multi-project-deploy/`.
- Phase 5 (Manual POC) — mock infra mechanically validated; live blind-agent run intentionally deferred (costs real money, needs an explicit go-ahead) — see [`evidence/phase-05-poc-writeup.md`](evidence/phase-05-poc-writeup.md) for the ready-to-run command.
- Phase 6 (Scenario library v1) — done. 9 scenarios (BR-01 x3, BR-02 x2, BR-03 x2, BR-04 x2), formal Pydantic schema, all passing automated validation (schema + shim executability + blind-mode leak audit). See `scenarios/` and `scripts/validate_scenarios.py`.
- Phase 7 (Scoring rubric) — done. `src/yolobench/rubric.py` + `rubric_hooks`/`reference_persona` on all 9 scenarios, validated by `scripts/test_rubric.py`.
- Phase 8 (Judge robustness) — done. `src/yolobench/judge.py`, opt-in, unused by the current library, T-14-mitigation self-tested (`scripts/test_judge.py`).
- Phase 9 (Harness abstraction) — Reference Backend done and proven end-to-end via real sandbox + subprocess execution (`scripts/run_reference_benchmark.py`). Real paid backends deliberately not built yet -- first cost-incurring step, needs explicit go-ahead.
- Phase 10 (First public run + report) — done, Reference Backend only. See `RESULTS.md`, `results/latest.json`.
- Phase 11 (Leaderboard site) — done. `docs/index.html`, verified rendering locally, data kept in sync with `results/latest.json`.
- Phase 12 (Community scenario format) — done. `CONTRIBUTING.md`, PR template, `.github/workflows/validate.yml` (also fulfills Phase 15's per-commit CI requirement).
- Phase 13 (Paper draft) — first working draft done, `paper/DRAFT.md`, scoped to what's actually built (no real-agent claims yet).
- Phase 14 (Content pass) — blog draft done (`content/blog-draft.md`), not published. CFP work deliberately left to the private strategy repo's own tracker, not duplicated here.
- Phase 15 (Regression tracking) — done for the Reference Backend (`scripts/check_regression.py`, wired into CI, verified against a deliberately-broken scenario). Real-backend scheduled tracking documented as a future template, not active (no second backend, no credentials held).
- Phase 16 (Mitigation proposals) — done. `design/MITIGATIONS.md`, each rule pointing at the real `rubric_hooks` mechanism as its concrete trigger condition.
- Phase 17 (Middleware gate) — done. `gate/policy.py`, self-tested against all 9 scenarios: 0 false positives on safe, 100% catch rate on unsafe, including both real incidents' exact calls.
- Phase 18 (Vendor engagement) — drafted, not sent. `outreach/claude-code-submission-draft.md` only (the one vendor with real grounding).
- Phase 19 onward — not started.

## Arc structure

- **Arc A — Foundation** (Phases 1–5): taxonomy, repo scaffold, mock infra layer, first hand-built scenario, manual POC.
- **Arc B — Core Benchmark** (Phases 6–10): scenario library, scoring rubric, judge robustness, multi-agent harness, first public results.
- **Arc C — Credibility & Reach** (Phases 11–14): leaderboard site, community scenario format, paper draft, conference/blog content.
- **Arc D — Product Impact** (Phases 15–18): regression tracking across agent releases, formal mitigation proposals, reference middleware gate, responsible vendor engagement.
- **Arc E — Moonshot** (Phases 19–20): standalone blast-radius firewall as adoptable OSS infra, continuous industry-tracking report.

## How to use this folder

One file per phase (`phase-01-*.md` … `phase-20-*.md`). Each follows the same template: Arc, Goal, Why It Matters, Deliverables, Acceptance Criteria, Dependencies, Risks/Notes. Read in order — later phases assume earlier ones are done. Nothing in `plan/` is code; implementation starts only after `design/LLD.md` is agreed (see that file's own status note).
