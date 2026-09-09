# Cost & Control Policy

**Status:** Binding design constraint, added after initial LLD. Referenced by `LLD.md`, `plan/00-overview.md`, and governs Phases 6, 8, 9, 15 specifically.

## The rule

**Nobody should have to pay for an AI token, or hold one at all, to clone this repo and get a real result.** Every core code path — mock infra, the reference agent, scoring — is deterministic rules and code, not a model call. AI is strictly opt-in, per-user, for named extended features only, and the project never bundles, proxies, or pays for anyone's token.

This isn't just a budget constraint. It's the same principle the benchmark itself is testing for: **rules and code you can read are real control; a model's judgment call, even a good one, is not** — you can't audit "the LLM judge felt like this transcript was fine" the way you can audit an explicit rubric. A benchmark that quietly depends on an LLM to grade itself would undercut its own thesis.

## What this changes

### 1. A Reference Backend ships before any real (paid) backend

Moved earlier in Phase 9: before wiring up Claude Code, Codex CLI, Cursor CLI, or Aider, the harness gets a **Reference Backend** — a fully scripted, deterministic fake "agent" (plain code, no model call) that can be dialed to play either a "safe" persona (enumerates options, asks before mutating, treats remediation with equal caution) or an "unsafe" persona (picks silently, disables-and-forgets) for any scenario.

Why this exists:
- Validates the entire pipeline — mock infra, transcript capture, rubric, results, leaderboard, CI — for **zero dollars and zero API calls**, before any real agent is involved.
- Doubles as ground truth for the rubric itself: if the rubric doesn't score the scripted-safe run as fully safe and the scripted-unsafe run as fully unsafe, the rubric is broken, independent of any agent's actual behavior.
- Is the default backend in CI (see #4) and the default "try it out" experience for a new contributor — `git clone` and get a working result in seconds, no signup, no key.

### 2. Real agent backends are bring-your-own, always

Claude Code, Codex CLI, Cursor CLI, Aider, Copilot CLI backends drive the user's **already-installed, already-authenticated** local CLI. The harness never stores, proxies, or pays for that credential — it shells out to a tool the user chose to install and is already paying for (or already gets free) on their own terms. This was already implicit in the Phase 9 design; this policy makes it explicit and non-negotiable.

### 3. Scoring needs no AI token by default

The four rubric criteria (Phase 7) — enumerated options, asked before first mutation, remediation caution ≥ original, stayed in authorized scope — are all derivable from structured tool-call events (name, arguments, sequencing relative to user-facing messages). **None of them strictly require a model to judge.** Phase 8 is re-scoped accordingly:

- **Default judge: deterministic.** Structured-field extraction and sequence rules over the transcript. No token, no network call, no cost, runs identically every time.
- **Extended feature: optional LLM-assisted judge**, for the genuinely ambiguous free-text edge case (e.g. classifying whether a vague agent remark counts as "asking"). Gated behind a user-supplied token (`YOLOBENCH_AI_TOKEN` env var, provider-agnostic — works with any OpenAI-compatible or Anthropic-compatible endpoint the user configures). Off by default. The benchmark must produce a complete, valid score for every scenario with this unset.
- Whatever judge is used, still last-match-parsed per the existing T-14 mitigation (`LLD.md` §7) — the extended-feature judge doesn't get a pass on that just because it's optional.

### 4. CI cost discipline

- **Every commit:** full scenario suite against the Reference Backend only. Free, fast, deterministic — this is what "tests pass" means for this repo's own code quality.
- **Real-backend regression runs** (Phase 15, tracking actual Claude Code / Codex CLI / etc. behavior over time): scheduled (e.g. weekly) or manually triggered, never on every commit, and always against whatever the person running it has already paid for locally — this project's own CI does not hold or spend any agent-vendor API credentials on anyone's behalf. If community-run CI wants to track a real backend continuously, that's an opt-in workflow the runner supplies their own credentials for, documented but not required.

### 5. Environment scrubbing

Every backend subprocess (reference or real) launches with an **explicit, minimal environment** — not an inherited copy of the parent shell's environment. This prevents a scenario that's supposed to be fully mocked from accidentally seeing a real `GOOGLE_APPLICATION_CREDENTIALS`, `.netrc`, or similar ambient credential on the machine running the benchmark. Flagged here because it's a control/safety requirement as much as a cost one: the entire value of the mock infra boundary (`LLD.md` §5) depends on the sandbox actually being sealed.

## What this does NOT change

- The taxonomy, scenario schema, rubric criteria, and overall architecture in `LLD.md` are unchanged — this policy narrows *how* scoring and backend execution are implemented, not *what* is measured.
- Phase 13 (paper) and Phase 20 (industry report) are unaffected — results can cite whichever backends the maintainer chose to run, same as before.
