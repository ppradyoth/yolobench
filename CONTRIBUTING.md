# Contributing a Scenario

YOLOBench grows by adding scenarios that exercise one of the four taxonomy classes (`design/TAXONOMY.md`) against a plausible, generalized task. This doc is the whole process — read it, copy the worked example, open a PR.

## The non-negotiable rule

**Every scenario must be fully mockable.** No real cloud account, no real network call, no real credential, ever — regardless of what CLI or product it's generalized from. If you can't build a convincing shim for it, it's not a scenario, per `design/MOCK_INFRA.md`. CI enforces this automatically (see below) but read that doc first so you're not surprised by a rejected PR.

## Steps

1. **Pick a taxonomy class** (`BR-01` ambiguous resource selection, `BR-02` unconfirmed destructive remediation, `BR-03` persistence-method inflation, `BR-04` scope creep) from `design/TAXONOMY.md`. Multiple tags are fine if your scenario genuinely tests more than one — see `br-01-multi-project-deploy` for an example (BR-01 primary, BR-02 secondary).

2. **Generalize, don't copy.** If your scenario is inspired by something you actually saw an agent do, strip anything identifying (company names, real usernames, real URLs) — every existing scenario's `notes:` field says explicitly whether it's generalized from a real incident or invented from scratch, and none of them name a real company or product.

3. **Create the directory:**
   ```
   scenarios/<your-scenario-id>/
     scenario.yaml
     fixtures/
       bin/<mock_backend>       # your shim script(s)
       workdir/                 # optional, only if initial_workdir_files is non-empty
   ```

4. **Write the shim.** Copy the structure of an existing one (e.g. `scenarios/br-01-multi-project-deploy/fixtures/bin/firebase`) — the blind-mode pattern (default output reveals nothing about being a mock; `FIXTURE_DEBUG_MODE=1` unlocks verbose diagnostics for your own authoring) is required, not optional. See `design/MOCK_INFRA.md`'s blind-mode checklist.

5. **Write `scenario.yaml`.** Every field is validated by `src/yolobench/schema.py` — required fields, taxonomy IDs, and a self-check that your `rubric_hooks` reference tool names that actually appear in your `reference_persona`. Start from an existing scenario.yaml as a template rather than from scratch; the shape is consistent across all 9 current scenarios.

6. **Write both reference personas.** `reference_persona.safe` and `.unsafe` are exact, deterministic call sequences the zero-cost Reference Backend plays — see `design/COST_AND_CONTROL.md` §1. These are what actually get executed in CI, against your real shim, to prove the scenario works.

7. **Validate locally before opening the PR:**
   ```bash
   pip install -e .
   python3 scripts/validate_scenarios.py     # schema + shim + blind-mode leak audit
   python3 scripts/test_rubric.py            # your safe persona must pass its primary criteria, unsafe must fail at least one
   python3 scripts/run_reference_benchmark.py  # same check, through the real sandbox/subprocess path
   ```
   All three must pass. This is exactly what CI runs on your PR.

8. **Open the PR** using the template — it asks for the same things §3–7 above just produced, so filling it out should be quick if you followed the steps in order.

## What review actually checks

Not just "does it pass CI." A human reviews for:
- Does this genuinely test a *new* ambiguity, or is it a reskinned version of an existing scenario with different names?
- Does the `notes:` field honestly disclose whether this is generalized from something real or invented?
- Is the `task_prompt` something a real user could plausibly ask, not a strawman?

Low-effort or duplicate submissions get a comment asking for the above, not a silent close — but they don't get merged until addressed.
