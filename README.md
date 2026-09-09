# blast-radius-bench

A benchmark for a failure class that existing agent evals don't measure: **judgment under ambiguity when an action touches a real, pre-existing, or destructive-adjacent resource.**

Capability benchmarks (SWE-bench and friends) ask "can the agent solve the task." This asks a different question: when a coding agent is authorized for a *class* of action ("deploy to hosting," "authenticate to GitHub") but the *specific* target is ambiguous — multiple existing cloud projects, multiple git remotes, an unspecified credential-storage method — does it stop and ask, or does it pick silently? And when it makes a mistake, does its own "fix" get the same scrutiny as the original action, or does it compound the damage?

This project exists because that exact failure pattern was observed twice, independently, months apart, in real Claude Code sessions running in `bypassPermissions` mode — see the taxonomy in [`plan/00-overview.md`](plan/00-overview.md) for the seed incidents. Two data points don't prove a trend. A reproducible, public benchmark does.

## Status

Planning. See [`plan/`](plan/) for the phase-wise roadmap (Phases 1–20, Arcs A–E) and [`design/LLD.md`](design/LLD.md) for the low-level design. No benchmark code exists yet — this repo currently holds the plan and design only, by design (see Arc A).

## Principles

- **Sandboxed only.** Every scenario runs against mocked CLI/infra shims. No real cloud accounts, no real production systems, ever.
- **Reproducible, not vibes.** Scoring is a structured rubric / state machine, not free-text LLM judgment trusted verbatim (see the judge-hijacking note in the LLD — we don't want to ship a benchmark vulnerable to the same class of bug we're testing for).
- **Neutral framing.** This is not a vendor takedown. It's an attempt to make a real, underspecified safety property (blast-radius awareness) measurable, public, and trackable over time — the same way OWASP Top 10 made web vulnerability classes legible.

## Layout

```
plan/     phase-wise roadmap, one file per phase, grouped into 5 arcs
design/   low-level design (LLD.md) covering architecture, data models, interfaces
```

## License

MIT — see [`LICENSE`](LICENSE).
