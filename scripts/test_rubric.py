#!/usr/bin/env python3
"""Phase 7 self-test: for every scenario, build a transcript directly from
its safe/unsafe reference_persona and confirm the rubric scores them as
expected -- the safe persona must pass every criterion in the scenario's
own primary_criteria_mapping, and the unsafe persona must fail at least
one. This is a pure logic check against the rubric, no shim execution --
scripts/run_reference_benchmark.py (Phase 9/10) is the real end-to-end run
through the actual sandboxed shims. Zero AI, zero network, zero cost.

Run: python3 scripts/test_rubric.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from yolobench.rubric import composite_score, score_criteria  # noqa: E402
from yolobench.schema import PersonaStep, Scenario, ToolCallEvent  # noqa: E402

SCENARIOS_DIR = ROOT / "scenarios"


def _step_to_event(step: PersonaStep, i: int) -> ToolCallEvent:
    args = {"argv": step.argv} if step.argv else {"fs_write": step.fs_write.model_dump()}
    return ToolCallEvent(
        tool_name=step.tool_name,
        arguments=args,
        timestamp=f"2026-01-01T00:00:{i:02d}Z",
        preceded_by_user_confirmation=step.user_confirmed,
    )


def check_scenario(scenario_dir: Path) -> list[str]:
    errors: list[str] = []
    data = yaml.safe_load((scenario_dir / "scenario.yaml").read_text())
    scenario = Scenario(**data)

    safe_transcript = [_step_to_event(s, i) for i, s in enumerate(scenario.reference_persona.safe)]
    unsafe_transcript = [
        _step_to_event(s, i) for i, s in enumerate(scenario.reference_persona.unsafe)
    ]

    safe_criteria = score_criteria(scenario, safe_transcript)
    unsafe_criteria = score_criteria(scenario, unsafe_transcript)

    primary_keys = list(scenario.primary_criteria_mapping.keys())
    if not primary_keys:
        errors.append(f"{scenario.id}: no primary_criteria_mapping declared")

    for key in primary_keys:
        if not safe_criteria.get(key, False):
            errors.append(
                f"{scenario.id}: safe persona FAILED primary criterion '{key}' "
                f"(criteria={safe_criteria})"
            )

    if primary_keys and all(unsafe_criteria.get(key, True) for key in primary_keys):
        errors.append(
            f"{scenario.id}: unsafe persona did not fail ANY primary criterion "
            f"(criteria={unsafe_criteria})"
        )

    pad = " " * (len(scenario.id) + 2)
    print(f"  {scenario.id}: safe={composite_score(safe_criteria)}/4 {safe_criteria}")
    print(f"  {pad}unsafe={composite_score(unsafe_criteria)}/4 {unsafe_criteria}")
    return errors


def main() -> int:
    scenario_dirs = sorted(p for p in SCENARIOS_DIR.iterdir() if p.is_dir())
    all_errors: list[str] = []
    print(f"scoring {len(scenario_dirs)} scenario(s) against their own reference personas:\n")
    for d in scenario_dirs:
        all_errors.extend(check_scenario(d))

    if all_errors:
        print(f"\n{len(all_errors)} problem(s):")
        for e in all_errors:
            print(f"  - {e}")
        return 1

    print(
        "\nrubric self-test passed: every safe persona scores clean on its "
        "primary criteria, every unsafe persona fails at least one"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
