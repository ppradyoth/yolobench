#!/usr/bin/env python3
"""Phase 15: diff two results/*.json payloads and flag any
(scenario_id, backend_id) pair whose composite_score dropped or whose
criteria flipped from pass to fail. Zero AI, zero network, zero cost.

Default usage compares the version already committed in git HEAD against
whatever results/latest.json currently is on disk (e.g. after re-running
scripts/publish_results.py with local scenario/rubric changes):

  python3 scripts/check_regression.py

Explicit usage:

  python3 scripts/check_regression.py <previous.json> <current.json>

This is the "every commit: Reference Backend only" regression check from
design/COST_AND_CONTROL.md #4 -- catching a scenario or rubric edit that
silently breaks a previously-passing check, independent of and prior to
any real (paid) backend regression tracking.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _load_previous_from_git() -> dict | None:
    try:
        raw = subprocess.run(
            ["git", "show", "HEAD:results/latest.json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except subprocess.CalledProcessError:
        return None  # no committed results yet -- first run, nothing to diff against
    return json.loads(raw)


def _index(payload: dict) -> dict[tuple[str, str], dict]:
    return {(r["scenario_id"], r["backend_id"]): r for r in payload["results"]}


def diff(previous: dict, current: dict) -> list[str]:
    prev_idx = _index(previous)
    curr_idx = _index(current)
    problems: list[str] = []

    for key, prev_result in prev_idx.items():
        curr_result = curr_idx.get(key)
        if curr_result is None:
            problems.append(f"{key[0]} / {key[1]}: present in previous run, missing in current")
            continue

        if curr_result["composite_score"] < prev_result["composite_score"]:
            problems.append(
                f"{key[0]} / {key[1]}: score dropped "
                f"{prev_result['composite_score']}/4 -> {curr_result['composite_score']}/4"
            )

        for crit, prev_val in prev_result["criteria"].items():
            curr_val = curr_result["criteria"].get(crit)
            if prev_val and curr_val is False:
                problems.append(f"{key[0]} / {key[1]}: criterion '{crit}' flipped pass -> fail")

    return problems


def main() -> int:
    if len(sys.argv) == 3:
        previous = json.loads(Path(sys.argv[1]).read_text())
        current = json.loads(Path(sys.argv[2]).read_text())
    elif len(sys.argv) == 1:
        previous = _load_previous_from_git()
        current_path = ROOT / "results" / "latest.json"
        if not current_path.exists():
            print("no results/latest.json on disk -- run scripts/publish_results.py first")
            return 1
        current = json.loads(current_path.read_text())
        if previous is None:
            print("no committed results/latest.json in git HEAD -- nothing to compare, first run")
            return 0
    else:
        print("usage: check_regression.py [<previous.json> <current.json>]")
        return 2

    problems = diff(previous, current)
    if problems:
        print(f"{len(problems)} regression(s) found:")
        for p in problems:
            print(f"  - {p}")
        return 1

    print("no regressions: every (scenario, backend) pair holds or improves vs. the previous committed run")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
