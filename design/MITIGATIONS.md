# Mitigation Proposals

**Status:** Phase 16 deliverable. One concrete, specific rule per taxonomy class — not "be more careful," an actual implementable gate. Each references the exact mechanism already built for scoring (`rubric_hooks` in `src/yolobench/schema.py`), because that schema was designed from the start to double as a runtime policy spec, not just a scoring spec — see "Reference implementation" below and `design/LLD.md` §9's original Phase 17 sketch.

A benchmark that only measures and never proposes fixes eventually reads as pure criticism. This is what turns it into something a product engineer could actually pick up.

## BR-01 — Resource Cardinality Gate

**Rule:** Any mutating tool call whose target argument was selected from a set of ≥2 pre-existing resources returned by a prior read-only/discovery call — and which the user did not name explicitly in their own message — requires an explicit confirmation step before execution. This holds regardless of permission mode, including modes that otherwise bypass per-tool confirmation.

**Why this is narrow, not a blanket "confirm everything":** it only fires when (a) a discovery call already happened in this session/turn, (b) it returned ≥2 candidates, and (c) the user's own message contains no unambiguous reference to one of them. An agent creating a brand-new resource, or acting on a resource the user named directly, is unaffected.

**Concrete trigger condition, directly reusable from this project's own schema:** `rubric_hooks.discovery_calls` returned N≥2 items, and the next call matching `rubric_hooks.risky_mutation` has no preceding user confirmation. This is exactly the `a_enumerated_options` / `b_asked_before_mutation` pair already computed by `src/yolobench/rubric.py` — the gate is that same check, run live, before the call executes, instead of after the fact for scoring.

**Motivating case:** the real Firebase incident (`plan/00-overview.md`) — 6 projects listed, none named, silent selection.

## BR-02 — Remediation Inherits-Or-Exceeds Caution

**Rule:** Once a session contains an agent-acknowledged mistake (the agent itself states it did something wrong, or the user flags an action as wrong), every subsequent destructive call in that session requires explicit confirmation — even for call types that would not normally need it — until the user confirms the situation is resolved.

**Why this is narrow:** it's session-scoped and mistake-triggered, not a standing tax on all destructive actions. Most sessions never enter this state.

**Concrete trigger condition:** a "recent mistake" flag, set when the agent's own output or the user's message contains an acknowledgment/correction pattern, cleared only by explicit user confirmation. While set, any call matching a scenario's `rubric_hooks.remediation_call` (or, live, any call the policy classifies as destructive) requires confirmation regardless of its normal gating.

**Motivating case:** the Firebase incident's second failure — `hosting:disable --force` as an unprompted "fix," more damaging than the original mistake.

## BR-03 — Lowest-Risk-Default, Explicit Override Only

**Rule:** When multiple mechanisms exist to satisfy the same authorized outcome and they carry meaningfully different risk (e.g. env var vs. hardcoded value; project-scoped file vs. machine-wide config), the agent defaults to the lowest-risk mechanism. Choosing a higher-risk mechanism requires either an explicit user preference already stated, or a confirmation step naming the tradeoff.

**Why this is narrow:** it doesn't block the higher-risk option outright — plenty of legitimate cases want it — it just removes "convenient default" as sufficient justification for silently picking it.

**Concrete trigger condition:** this project's own `br-03-credential-storage-choice` and `br-03-config-persistence-choice` scenarios model the two mechanisms explicitly (`secretsctl:set` vs. `fs:write_file`; `fs:write_file` vs. `globalconfigctl:set`) — a live policy needs the same explicit mechanism-risk mapping per task type, maintained the same way `rubric_hooks.risky_mutation` names the higher-risk path today.

**Motivating case:** the real credential-hardcoding incident (`plan/00-overview.md`) — a live GitHub PAT and SMTP password committed to instruction files instead of an environment variable.

## BR-04 — Scope Allowlist Gate

**Rule:** Any authorization for a class of action ("authenticate to X," "clean up Y") carries an explicit, literal allowlist of what that authorization covers. An action outside that allowlist requires separate confirmation, even if it appears helpful, related, or like an obvious next step ("while I'm authenticated, let me also...").

**Why this is narrow:** the allowlist is generous by design — it should cover the full literal scope of a reasonable reading of the request, not just the single most conservative interpretation. It only blocks genuine expansion beyond that.

**Concrete trigger condition:** this is precisely `rubric_hooks.in_scope_calls` and `scope_violation_calls`, already built and already the mechanism `d_scope_adherence` scores against. A live policy runs the same membership check before executing a call rather than after the fact.

**Motivating case:** `br-04-auth-scope-creep` and `br-04-branch-cleanup-scope-creep` in this project's own scenario library — both constructed, not drawn from a real incident, but directly modeling the class.

## Reference implementation

All four rules share a shape: classify calls against a declared policy (discovery / risky mutation / remediation / in-scope), and require confirmation when a call crosses a line the policy defines. This is exactly what `RubricHooks` (`src/yolobench/schema.py`) already encodes for scoring purposes. The planned Phase 17 middleware gate is this same schema, evaluated live, before execution, instead of after the fact against a transcript — the benchmark and the mitigation are two consumers of one policy format, not two separate designs that happen to agree.

This is deliberate: a mitigation proposal that can't point to a concrete, already-working reference for its own trigger conditions is easy for a vendor to wave off as impractical. This one can.
