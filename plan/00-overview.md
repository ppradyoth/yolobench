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

## Arc structure

- **Arc A — Foundation** (Phases 1–5): taxonomy, repo scaffold, mock infra layer, first hand-built scenario, manual POC.
- **Arc B — Core Benchmark** (Phases 6–10): scenario library, scoring rubric, judge robustness, multi-agent harness, first public results.
- **Arc C — Credibility & Reach** (Phases 11–14): leaderboard site, community scenario format, paper draft, conference/blog content.
- **Arc D — Product Impact** (Phases 15–18): regression tracking across agent releases, formal mitigation proposals, reference middleware gate, responsible vendor engagement.
- **Arc E — Moonshot** (Phases 19–20): standalone blast-radius firewall as adoptable OSS infra, continuous industry-tracking report.

## How to use this folder

One file per phase (`phase-01-*.md` … `phase-20-*.md`). Each follows the same template: Arc, Goal, Why It Matters, Deliverables, Acceptance Criteria, Dependencies, Risks/Notes. Read in order — later phases assume earlier ones are done. Nothing in `plan/` is code; implementation starts only after `design/LLD.md` is agreed (see that file's own status note).
