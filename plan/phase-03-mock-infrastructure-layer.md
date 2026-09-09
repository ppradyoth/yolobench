# Phase 3 — Mock Infrastructure Layer

**Arc:** A — Foundation

## Goal
Design (not yet implement — implementation is Arc B) the shim layer that lets scenarios present an agent with "6 existing Firebase projects" etc. without any real cloud account ever being touched.

## Why It Matters
This is the single design decision that makes the entire benchmark ethically and legally uncomplicated. Every scenario's safety depends on this boundary holding. It's worth a dedicated phase rather than folding it into "build a scenario."

## Deliverables
- A written spec (feeds into `design/LLD.md` §Mock Infra) for how CLI shims work: intercept `firebase`, `gcloud`, `aws`, `git remote -v`, `npm whoami`, etc. via `PATH` injection into a sandboxed working directory, returning scripted fixture output.
- A decision on isolation mechanism: per-scenario temp directory + modified `PATH`, vs. containerization (Docker) for stronger isolation. Recommendation to carry into the LLD: start with temp-dir + PATH shims for speed, revisit containerization once real agent backends (Phase 9) are wired in and file-write side effects need stronger sandboxing.
- Explicit list of "never mock" boundaries: the harness must never let a scenario accidentally shell out to a real credential or real network endpoint — shims fail loudly (non-zero exit + stderr warning) rather than silently falling through to the real binary if invoked outside their scripted surface.

## Acceptance Criteria
- Design reviewed against both seed incidents: can this layer fully reproduce the "6 Firebase projects, none named" setup and the "disable hosting" remediation step, with zero real network calls?

## Dependencies
Phase 1 (taxonomy defines what needs to be mockable).

## Risks / Notes
The biggest risk to the whole project's credibility is a mock leaking into a real call. Treat this phase's output as a security design, not just plumbing — it gets a real design review, not a rubber stamp, before Phase 4 scenario-building starts.
