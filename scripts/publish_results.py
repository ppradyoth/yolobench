#!/usr/bin/env python3
"""Phase 10: run every scenario against the Reference Backend (both
personas) for real, and publish results/<run_id>.json, results/latest.json,
and RESULTS.md. Zero AI, zero network, zero cost -- see
design/COST_AND_CONTROL.md. Run: python3 scripts/publish_results.py
"""
from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from yolobench.backends.reference import ReferenceBackend  # noqa: E402
from yolobench.report import render_results_md, write_results_json  # noqa: E402
from yolobench.runner import run_scenario  # noqa: E402
from yolobench.schema import Scenario  # noqa: E402

SCENARIOS_DIR = ROOT / "scenarios"
RESULTS_DIR = ROOT / "results"
SITE_DATA_DIR = ROOT / "docs" / "data"


def main() -> int:
    run_id = "run-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    transcripts_dir = RESULTS_DIR / "transcripts" / run_id

    scenario_dirs = sorted(p for p in SCENARIOS_DIR.iterdir() if p.is_dir())
    scenarios: dict[str, Scenario] = {}
    results = []

    print(f"publishing run {run_id}\n")
    for scenario_dir in scenario_dirs:
        data = yaml.safe_load((scenario_dir / "scenario.yaml").read_text())
        scenario = Scenario(**data)
        scenarios[scenario.id] = scenario

        for persona in ("safe", "unsafe"):
            result = run_scenario(
                scenario, ReferenceBackend(persona), scenario_dir, transcripts_dir=transcripts_dir
            )
            results.append(result)
            print(f"  {scenario.id:38s} {result.backend_id:16s} {result.composite_score}/4")

    json_path = write_results_json(results, scenarios, RESULTS_DIR, run_id)
    md = render_results_md(results, scenarios, run_id)
    md_path = ROOT / "RESULTS.md"
    md_path.write_text(md)

    SITE_DATA_DIR.mkdir(parents=True, exist_ok=True)
    site_data_path = SITE_DATA_DIR / "latest.json"
    shutil.copyfile(RESULTS_DIR / "latest.json", site_data_path)

    print(f"\nwrote {json_path}")
    print(f"wrote {RESULTS_DIR / 'latest.json'}")
    print(f"wrote {md_path}")
    print(f"wrote {len(results)} transcripts under {transcripts_dir}")
    print(f"wrote {site_data_path} (docs/ site data, kept in sync with results/latest.json)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
