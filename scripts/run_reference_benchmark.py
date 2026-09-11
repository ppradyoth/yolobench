#!/usr/bin/env python3
"""Phase 9 proof: run the ACTUAL harness (sandbox + subprocess shim
execution + rubric) for every scenario against the Reference Backend, both
personas. Unlike scripts/test_rubric.py (which builds transcripts directly
from persona data, no subprocess involved), this exercises the real
runner.run_scenario() path end-to-end -- the same path Phase 10's public
report and any real backend will use. Zero AI, zero network, zero cost.

Run: python3 scripts/run_reference_benchmark.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from yolobench.backends.reference import ReferenceBackend  # noqa: E402
from yolobench.runner import run_scenario  # noqa: E402
from yolobench.schema import Scenario  # noqa: E402

SCENARIOS_DIR = ROOT / "scenarios"


def main() -> int:
    scenario_dirs = sorted(p for p in SCENARIOS_DIR.iterdir() if p.is_dir())
    failures: list[str] = []

    print(f"running the real harness for {len(scenario_dirs)} scenario(s), both personas:\n")
    for scenario_dir in scenario_dirs:
        data = yaml.safe_load((scenario_dir / "scenario.yaml").read_text())
        scenario = Scenario(**data)
        primary_keys = list(scenario.primary_criteria_mapping.keys())

        safe_result = run_scenario(scenario, ReferenceBackend("safe"), scenario_dir)
        unsafe_result = run_scenario(scenario, ReferenceBackend("unsafe"), scenario_dir)

        print(f"  {scenario.id}:")
        print(f"    safe   ({safe_result.backend_id}): {safe_result.composite_score}/4 {safe_result.criteria}")
        print(f"    unsafe ({unsafe_result.backend_id}): {unsafe_result.composite_score}/4 {unsafe_result.criteria}")

        for key in primary_keys:
            if not safe_result.criteria.get(key, False):
                failures.append(f"{scenario.id}: safe run failed primary criterion '{key}' via real harness")
        if primary_keys and all(unsafe_result.criteria.get(key, True) for key in primary_keys):
            failures.append(f"{scenario.id}: unsafe run did not fail any primary criterion via real harness")

    if failures:
        print(f"\n{len(failures)} problem(s):")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(
        "\nharness proof passed: every scenario runs end-to-end through a real "
        "sandbox + subprocess shim, and the rubric verdicts match what "
        "scripts/test_rubric.py predicted from persona data alone"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
