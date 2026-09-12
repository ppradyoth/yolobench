#!/usr/bin/env python3
"""Phase 17 self-test: replay each scenario's safe and unsafe reference
persona through the gate, call by call, as if it were live and
pre-execution. The gate must require confirmation on at least one call in
every unsafe sequence (it would have stopped the incident) and on zero
calls in every safe sequence (it doesn't nag on already-legitimate
behavior). Zero AI, zero network, zero cost.

Run: python3 scripts/test_gate.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from gate.policy import ProposedCall, requires_confirmation  # noqa: E402
from yolobench.schema import PersonaStep, Scenario  # noqa: E402

SCENARIOS_DIR = ROOT / "scenarios"


def _to_call(step: PersonaStep) -> ProposedCall:
    return ProposedCall(tool_name=step.tool_name, argv=step.argv, user_confirmed=step.user_confirmed)


def check_scenario(scenario_dir: Path) -> list[str]:
    errors: list[str] = []
    data = yaml.safe_load((scenario_dir / "scenario.yaml").read_text())
    scenario = Scenario(**data)
    hooks = scenario.rubric_hooks

    safe_blocked = [
        s.tool_name for s in scenario.reference_persona.safe if requires_confirmation(hooks, _to_call(s))
    ]
    unsafe_blocked = [
        s.tool_name for s in scenario.reference_persona.unsafe if requires_confirmation(hooks, _to_call(s))
    ]

    if safe_blocked:
        errors.append(f"{scenario.id}: gate blocked the SAFE persona at {safe_blocked} -- false positive")
    if not unsafe_blocked:
        errors.append(f"{scenario.id}: gate did not block ANY call in the UNSAFE persona -- false negative")

    print(f"  {scenario.id}: safe_blocked={safe_blocked or 'none'}  unsafe_blocked={unsafe_blocked}")
    return errors


def main() -> int:
    scenario_dirs = sorted(p for p in SCENARIOS_DIR.iterdir() if p.is_dir())
    all_errors: list[str] = []
    print(f"replaying {len(scenario_dirs)} scenario(s) through the live gate:\n")
    for d in scenario_dirs:
        all_errors.extend(check_scenario(d))

    if all_errors:
        print(f"\n{len(all_errors)} problem(s):")
        for e in all_errors:
            print(f"  - {e}")
        return 1

    print(
        "\ngate self-test passed: every unsafe persona is blocked before its "
        "damaging call, every safe persona runs uninterrupted"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
