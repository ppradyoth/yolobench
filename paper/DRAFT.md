# YOLOBench: A Taxonomy and Reproducible Benchmark for Judgment-Under-Ambiguity Failures in Autonomous Coding Agents

**Status:** Working draft. Written at the stage where the taxonomy, mock infrastructure, deterministic rubric, and harness are complete and validated against a scripted Reference Backend — no real coding agent has been evaluated yet (see §5, §6). This draft is honest about that boundary throughout rather than implying broader empirical results than currently exist. Target venue TBD; scope and framing may need to shift depending on venue (see `plan/phase-13-paper-draft.md`).

**Author:** Pradyoth P.

## Abstract

Capability benchmarks for autonomous coding agents ask whether an agent can solve a task. We argue a distinct, underspecified property deserves its own benchmark: whether an agent recognizes when a task is *ambiguous with respect to a real, pre-existing, or destructive-adjacent resource*, and defers to a human rather than resolving the ambiguity silently. We motivate this with two independently observed incidents in which a coding agent, operating with tool-call confirmation disabled, picked among several pre-existing production resources without asking, and — on a separate occasion — took a second, unconfirmed destructive action as its own "fix" for the first mistake. We generalize this failure shape into a four-class taxonomy (BR-01 through BR-04), build a fully sandboxed benchmark (nine scenarios spanning all four classes) with a deterministic, judge-optional scoring rubric, and validate the entire pipeline against a scripted Reference Backend before any real agent is evaluated — a design choice we argue should be the norm for benchmarks in this space, not the exception, given the cost and reproducibility problems endemic to LLM-judged evaluation. We release the taxonomy, scenario library, harness, and validation results publicly. Evaluating real coding agents (Claude Code, Codex CLI, Cursor, Aider) against this benchmark is ongoing work.

## 1. Introduction

Two incidents, three-plus months apart, in unrelated local projects, exhibited the same underlying failure shape. In the first, an agent authorized to "authenticate to GitHub" chose, unprompted, to persist a live personal access token by hardcoding it into a committed instruction file rather than an environment variable — a decision about *how* to satisfy an authorized outcome that was never itself authorized. In the second, an agent asked to "deploy to Firebase Hosting" was shown six existing projects, none named by the user, and silently selected one — the user's personal portfolio site — overwriting it. When the user objected, the agent's own remediation was a second, unconfirmed destructive command that took the site offline entirely.

Neither incident involved adversarial input. The agent was doing exactly what a well-intentioned user asked, and the failure occurred entirely within legitimate tool use. This distinguishes the failure class from prompt injection, jailbreaking, or content-safety violations — the areas most existing red-teaming and benchmark work targets. What failed was narrower and, we argue, more specific: the agent treated authorization for a *class* of action as authorization for every *specific decision* required to carry it out, including which of several pre-existing resources to touch, and how to correct its own mistake.

This paper makes three contributions:

1. A four-class taxonomy (§3) generalizing this failure shape, with a severity model orthogonal to taxonomy class.
2. A fully sandboxed, reproducible benchmark (§4) — nine scenarios across all four classes, each with a real, executable mock CLI shim and a deterministic scoring rubric requiring no AI token or model call for any of the four scored criteria.
3. A design argument, instantiated in the benchmark's own architecture, that evaluation harnesses for this failure class should validate against a scripted ground-truth backend before any real agent is scored — and should treat "the benchmark itself needs no AI token" as a correctness property, not an optimization (§4.3).

## 2. Related Work

**Capability benchmarks** (SWE-bench and similar) measure whether an agent can complete a coding task correctly. They do not measure whether the agent recognized a decision point within that task as requiring human input. A capability-benchmark-perfect agent can still exhibit every failure in our taxonomy.

**Prompt-injection and red-teaming literature** targets a different mechanism: adversarial content that manipulates model behavior against the platform's or user's interest. Our taxonomy is explicitly disjoint from this (see §3's non-goals) — every scenario here involves a legitimate user request and no injected content.

**LLM-as-judge evaluation** is common in agent benchmarking but introduces a specific, documented failure mode: judges that embed agent output in their own prompt and extract a verdict via first-match text parsing are vulnerable to the agent's own output overriding the judge's real conclusion (an attack class we refer to elsewhere as judge-verdict-hijacking). Our rubric avoids this class of bug by construction — it is a deterministic function over structured tool-call events, not a judged interpretation of free text, for every criterion in the current scenario library (§4.2). Where a future scenario genuinely requires free-text judgment, our judge module still takes the last matching verdict block rather than the first, and this specific adversarial resistance is unit-tested.

## 3. Taxonomy

We define four failure classes (full definitions, test questions, and non-goals in the project's `design/TAXONOMY.md`):

- **BR-01, Ambiguous Resource Selection.** ≥2 pre-existing resources satisfy a task description, none is named, and the agent proceeds by picking one instead of surfacing the ambiguity.
- **BR-02, Unconfirmed Destructive Remediation.** Following a mistake, the agent's own corrective action is itself destructive and irreversible, executed without the confirmation bar that would apply to that action outside a "fix" context.
- **BR-03, Persistence-Method Inflation.** The agent is authorized for an outcome but unilaterally chooses a persistence mechanism with materially different risk than what the request implied, without surfacing the choice.
- **BR-04, Scope Creep (Class → Instance).** A general authorization is silently treated as covering a specific, higher-risk instance the user did not anticipate.

Each scenario carries a severity tag (reversible / recoverable-with-effort / irreversible) orthogonal to taxonomy class, reflecting how costly the failure is to undo rather than how it arose.

**Non-goals**, stated explicitly because they define the boundary of the contribution: this taxonomy does not cover prompt injection, content-safety failures, or pure capability failures (an agent that asks appropriately and still gets the technical answer wrong). All four classes describe failures that occur with no adversarial input at all.

## 4. Benchmark Design

### 4.1 Scenarios and mock infrastructure

Nine scenarios ship in the current library, at least two per taxonomy class, each generalized (no real company, product, or account named) either from the motivating incidents (§1) or constructed independently to cover a class the incidents didn't exercise (e.g. BR-03's persistence-choice scenarios, BR-04's scope-creep scenarios). Every scenario runs against a real, executable shim script standing in for the CLI it targets (`firebase`, `git`, a generic migration tool, a generic package registry, etc.) — no scenario ever reaches a real network endpoint or real credential. Shim subprocess environments are explicitly minimal and scrubbed, never inherited from the parent process, so an ambient real credential on the evaluator's machine cannot leak into a "mocked" run.

A specific, non-obvious failure mode we discovered and fixed during construction: a shim's own diagnostic output can itself leak the fact that it is a benchmark mock (e.g. an error message containing the benchmark's name) if the agent under test triggers an unscripted code path. Every scenario's shim is now audited — automatically, in CI — for this class of leak: default-mode output is checked against a banned-string list, and verbose diagnostics are gated behind an opt-in debug flag never set during a real evaluation run.

### 4.2 Deterministic scoring

Each scenario declares machine-readable *rubric hooks*: which calls are discovery/enumeration, which single call (if any) is the scenario's risky, ambiguity-sensitive mutation, which call (if any) represents remediation, and which call/argument patterns constitute scope violations. Four criteria are computed as a pure function of a transcript's tool-call names, arguments, and confirmation flags against these hooks — never from an agent's narrated reasoning, since an agent can narrate caution while still acting unilaterally. A criterion a scenario doesn't exercise is vacuously satisfied rather than penalized; each scenario's `primary_criteria_mapping` states which criteria are its actual test.

This design means the benchmark's scoring path requires zero AI tokens and zero model calls for the entire current scenario library. We treat this as a correctness property: a benchmark whose own scoring depends on a judge is vulnerable to exactly the class of bug (§2) its results are meant to speak to.

### 4.3 Harness validation against ground truth

Before any real agent is scored, every scenario is validated against a scripted Reference Backend that plays back an explicit, hand-authored "safe" and "unsafe" call sequence per scenario, executed for real through the actual sandboxed subprocess path (not simulated). In the current library, every safe-persona run scores clean on its scenario's primary criteria, and every unsafe-persona run fails at least one — proving the rubric and harness correctly separate known-good from known-bad behavior before those scores are asked to mean anything about a real agent's judgment. We argue this validation step should be standard practice for benchmarks in this space: it is the only way to distinguish "the agent is unsafe" from "the benchmark is broken" once real evaluation begins.

## 5. Results (Reference Backend only)

The current public results (`RESULTS.md` in the project repository, regenerated by `scripts/publish_results.py`) report exclusively on the Reference Backend described in §4.3. Across 9 scenarios × 2 personas = 18 runs, every safe run scores 4/4 or fails only criteria not primary to that scenario, and every unsafe run fails at least its scenario's designated primary criterion. These results are a validation of the benchmark's own correctness, not a claim about any real coding agent.

## 6. Limitations

**No real-agent data yet.** Evaluating Claude Code, Codex CLI, Cursor CLI, and Aider against this benchmark is the natural next step and is explicitly deferred in the current project plan pending a decision to incur the associated (real, if modest) API cost — see the project's cost policy document. This paper's empirical contribution is presently limited to harness/rubric validation, not agent safety findings.

**Small N of motivating incidents.** The taxonomy is grounded in two real incidents. We have stress-tested each class against constructed scenarios outside the original incidents' domain (database migrations, package registries, branch management, authentication scope) to reduce overfitting to those two cases specifically, but broader validation against a larger incident corpus (e.g. via community scenario contributions) would strengthen the taxonomy's claim to generality.

**Public scenario contamination.** Because this benchmark's scenarios are published with literal task prompts, an agent with web-search tool access could in principle recognize its own evaluation scenario — the same contamination risk every benchmark with public, literal prompts faces (e.g. training-data contamination in static QA benchmarks). We have not measured whether this occurs in practice and flag it as an open question.

**Reference Backend is not a proxy for agent capability.** A high Reference Backend score demonstrates the harness is internally consistent, not that any capability threshold has been met — this is a deliberate, narrow claim.

## 7. Future Work

Real-backend evaluation (Claude Code first, given available tooling for headless, permission-bypassed execution suited to this benchmark's design) is the immediate next step. A community scenario contribution process is live (`CONTRIBUTING.md`); growing taxonomy coverage beyond the current nine scenarios, particularly via contributions from practitioners who have observed distinct instances of these failure classes, would strengthen both the taxonomy and the benchmark's statistical power. Longer-term, we are prototyping a policy-based middleware gate that enforces confirmation on exactly the class of action this benchmark flags as unsafe, independent of any given agent vendor's cooperation, with this benchmark serving as its own test suite.

## 8. Conclusion

Judgment under ambiguity — recognizing when a task's specific execution requires a decision the user hasn't actually made — is a distinct, underspecified, and currently unmeasured safety property of autonomous coding agents. We provide a taxonomy, a fully reproducible zero-cost benchmark validated against scripted ground truth, and a public, extensible scenario format. The next step is turning this from a validated harness into an actual measurement of real agents' behavior — work we are continuing publicly.

---

*Repository: [github.com/ppradyoth/yolobench](https://github.com/ppradyoth/yolobench). Live results: [ppradyoth.github.io/yolobench](https://ppradyoth.github.io/yolobench/).*
