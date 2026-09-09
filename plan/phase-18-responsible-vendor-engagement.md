# Phase 18 — Responsible Vendor Engagement

**Arc:** D — Product Impact

## Goal
Package the Phase 16 proposals and Phase 17 reference implementation into a structured submission through actual product-feedback channels at relevant agent vendors (Anthropic, OpenAI, Cursor, etc.), learning from the earlier incident-report experience documented in the private strategy repo (HackerOne closed Informative; bug bounty email unanswered).

## Why It Matters
The earlier individual incident reports went through channels scoped for classic CVSS-style vulnerabilities and got no traction, because "the agent made an unsafe unilateral decision" isn't that kind of bug. A public benchmark with real data and a working reference fix is a fundamentally different, stronger submission — positioned as product improvement input, not a bounty claim.

## Deliverables
- A structured write-up per vendor: benchmark results specific to their product, the relevant mitigation proposal, and a link to the working Phase 17 reference implementation as proof of feasibility.
- Submitted through each vendor's actual product-feedback or GitHub issue channel (per the existing `anthropics/claude-code` issue already filed as prior art), not the security bounty channel — explicitly scoped as agentic-safety/product-behavior feedback.
- No expectation set of payment or formal bounty — framed as: "here's a public benchmark and a reference fix, here's how your product currently scores."

## Acceptance Criteria
- At least one structured submission sent per actively-tracked agent vendor in the benchmark.
- Submissions logged (what was sent, when, to which channel) so responses (or non-responses) can be tracked the same way the prior incidents are tracked.

## Dependencies
Phase 16, Phase 17, Phase 10 (vendor-specific results to cite).

## Risks / Notes
Manage expectations going in — the prior two incident reports on this exact theme got no engagement. This phase's value is largely independent of whether any vendor responds: the public benchmark + reference implementation stand on their own regardless of vendor uptake.
