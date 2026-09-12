# yolobench-gate

A pre-execution policy check for coding agents: given the calls an agent has made and a proposed next call, decide whether it needs human confirmation before it runs.

Currently lives inside [yolobench](https://github.com/ppradyoth/yolobench) as a self-contained package (`gate/`, own entry in the project's `pyproject.toml`) rather than a separate repo — see "Extraction status" below for why.

## What it does

`requires_confirmation(hooks, call)` applies four rules, one per taxonomy class in [`design/TAXONOMY.md`](../design/TAXONOMY.md):

- Blocks a call outside the task's declared scope.
- Blocks a call matching the task's designated "risky, ambiguity-sensitive" action.
- Blocks a call matching the task's designated "remediation" action.
- Blocks a call matching a declared scope-violation pattern (e.g. a specific dangerous argument).

Any of these can be cleared by `call.user_confirmed = True` — the gate's job is only to force that confirmation to actually happen before the call, not to block the action outright.

Full rule definitions and their justification: [`../design/MITIGATIONS.md`](../design/MITIGATIONS.md).

## Proof it works

`../scripts/test_gate.py` replays all 9 of yolobench's scenarios' safe and unsafe reference personas through this exact policy. Result: 0 false positives across every safe persona, every unsafe persona blocked before its damaging call — including both exact calls (`deploy`, `hosting:disable`) from the real incident that motivated this project.

## Extraction status

**Not yet a standalone package/repo.** The code is already structured to make that a non-event when it happens — separate top-level package, no import dependency on the rest of yolobench beyond the `RubricHooks` shape — but actually doing it (new repo, PyPI name, versioning discipline, integration docs for other agent frameworks) is real, ongoing maintenance commitment that isn't justified by adoption that doesn't exist yet. Per the project's own plan (`../plan/phase-19-standalone-blast-radius-firewall.md`), this is a deliberate go/no-go decision, not an assumed next step — revisit when someone other than the maintainer is actually using it.

## Integration sketch (not yet wired up)

The natural integration point is a coding agent's own pre-tool-call hook (e.g. Claude Code's hooks system) — intercept the proposed call, build a `ProposedCall`, check `requires_confirmation`, and surface a confirmation prompt if it returns `True`. No such integration exists yet; this package currently proves the policy logic, not a shipped hook.
