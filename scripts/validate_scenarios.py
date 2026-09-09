#!/usr/bin/env python3
"""Validate every scenario under scenarios/: schema conformance (Phase 6),
shim present and executable, and blind-mode audit invocations leak no
self-identifying strings (Phase 3/4/5's blind-mode checklist, automated).

Zero AI, zero network calls, zero cost -- pure local validation per
design/COST_AND_CONTROL.md. Run: python3 scripts/validate_scenarios.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml
from pydantic import ValidationError

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from yolobench.schema import Scenario  # noqa: E402

BANNED_STRINGS = ["yolobench", "benchmark", "mock", "fixture", "scenario"]
SCENARIOS_DIR = ROOT / "scenarios"
# Minimal, scrubbed env for the shim subprocess -- never the parent's own
# environment, and deliberately does not set FIXTURE_DEBUG_MODE (or
# whatever a given shim's debug gate is named), so this always exercises
# the blind path an agent under test would actually see.
SCRUBBED_ENV = {"PATH": "/usr/bin:/bin", "HOME": "/tmp"}


def check_scenario(scenario_dir: Path) -> list[str]:
    errors: list[str] = []
    yaml_path = scenario_dir / "scenario.yaml"
    if not yaml_path.exists():
        return [f"{scenario_dir.name}: missing scenario.yaml"]

    data = yaml.safe_load(yaml_path.read_text())
    try:
        scenario = Scenario(**data)
    except ValidationError as e:
        return [f"{scenario_dir.name}: schema invalid -- {e}"]

    if scenario.id != scenario_dir.name:
        errors.append(
            f"{scenario_dir.name}: scenario.yaml id '{scenario.id}' != directory name"
        )

    shim_path = scenario_dir / "fixtures" / "bin" / scenario.mock_backend
    if not shim_path.exists():
        errors.append(f"{scenario_dir.name}: shim not found at {shim_path}")
        return errors
    if not shim_path.stat().st_mode & 0o111:
        errors.append(f"{scenario_dir.name}: shim not executable (chmod +x)")

    for argv in scenario.blind_mode_audit:
        result = subprocess.run(
            [str(shim_path), *argv],
            capture_output=True,
            text=True,
            env=SCRUBBED_ENV,
        )
        combined = (result.stdout + result.stderr).lower()
        leaked = [s for s in BANNED_STRINGS if s in combined]
        if leaked:
            errors.append(
                f"{scenario_dir.name}: blind-mode leak for "
                f"`{scenario.mock_backend} {' '.join(argv)}` -- found {leaked}"
            )

    return errors


def main() -> int:
    if not SCENARIOS_DIR.exists():
        print("no scenarios/ directory found")
        return 1

    scenario_dirs = sorted(p for p in SCENARIOS_DIR.iterdir() if p.is_dir())
    all_errors: list[str] = []
    for d in scenario_dirs:
        all_errors.extend(check_scenario(d))

    print(f"checked {len(scenario_dirs)} scenario(s): {[d.name for d in scenario_dirs]}")
    if all_errors:
        print(f"\n{len(all_errors)} problem(s):")
        for e in all_errors:
            print(f"  - {e}")
        return 1

    print("\nall scenarios valid: schema OK, shims executable, no blind-mode leaks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
