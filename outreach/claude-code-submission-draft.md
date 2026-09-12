# Draft: Product feedback submission — Claude Code

**Status: DRAFT, NOT SENT.** For your review before it goes anywhere. Channel per the existing prior-art context below should be a GitHub issue on `anthropics/claude-code` (same channel as the prior combined report), not the security bounty program — this is product-behavior feedback with a working reference fix attached, not a CVSS-scored vulnerability.

**Why only Claude Code has a draft here:** this is the only vendor with real grounding — two independently observed incidents, both already documented and previously reported (see prior art below). Codex CLI, Cursor, and Aider have no scenario-specific findings yet because no real backend evaluation has been run against them — drafting outreach for those now would have nothing behind it. That's Phase 9's second-backend work, still deferred pending a decision to spend real API cost.

---

## Subject

Reproducible benchmark + working reference fix for the "unilateral action on ambiguous/destructive resources" pattern (ref: prior issue #93002)

## Body

This follows up on [anthropics/claude-code#93002](https://github.com/anthropics/claude-code/issues/93002), filed 2026-09-09, describing two incidents: an agent hardcoding a live credential into a committed file (May 2026), and an agent silently selecting a production Firebase project from six unnamed candidates, then "fixing" the resulting mistake with a second unconfirmed destructive command (`hosting:disable --force`, Sep 2026).

Since that report, I built a public, reproducible benchmark for this exact failure class — not prompt injection, not jailbreaking, just an agent doing what it was asked and making an unstated, specific, higher-risk decision along the way. It's here: [github.com/ppradyoth/yolobench](https://github.com/ppradyoth/yolobench), live results at [ppradyoth.github.io/yolobench](https://ppradyoth.github.io/yolobench/).

What's attached that wasn't in the original issue:

1. **A taxonomy** (`design/TAXONOMY.md`) generalizing the failure into four classes, so it's not just "two anecdotes."
2. **Nine reproducible scenarios**, fully sandboxed (no real cloud account ever touched), with a deterministic scoring rubric — no LLM judge, no ambiguity about what "pass" means.
3. **A working reference implementation of the fix** (`gate/policy.py`) — not a proposal, running code. Self-tested against all nine scenarios: it blocks 100% of the unsafe paths (including both exact calls from the Firebase incident — `deploy` and `hosting:disable`) with zero false positives on the nine corresponding safe paths.
4. **The specific rule** (`design/MITIGATIONS.md`): any mutating call whose target was selected from ≥2 pre-existing resources the user didn't name requires confirmation regardless of permission mode, and any remediation action inherits the same-or-greater confirmation bar as what it's undoing.

No real Claude Code run has been benchmarked yet — the results above are all from a scripted reference agent proving the harness itself is sound. I'd like to run the actual product against it next; flagging this now in case there's a preferred way to do that (a specific headless config, a contact for coordinating a larger run) rather than me just doing it unilaterally.

Not asking for a bounty — this is scoped as product-safety feedback with a reference fix, same framing as the original issue.

## Prior art / context

- [anthropics/claude-code#93002](https://github.com/anthropics/claude-code/issues/93002) — the combined incident report this follows up on.
- Earlier HackerOne submission for the May 2026 credential incident — closed Informative (bypass-permissions-mode exclusion). Reopen challenge submitted, no response. This is explicitly why the follow-up here goes through the product-feedback channel, not the bounty program.

---

*Reminder to self before sending: confirm the issue tracker is still the right channel, and that #93002 hasn't already gotten a response that changes this framing.*
