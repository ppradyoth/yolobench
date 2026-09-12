#!/usr/bin/env python3
"""Phase 20: generate a dated "State of Agentic Blast-Radius Safety"
snapshot under reports/. Pulls from results/latest.json + counts how many
results/run-*.json snapshots exist so far (i.e. how many times this has
been run) -- it does NOT fabricate quarter-over-quarter trend claims when
there's only one data point. Zero AI, zero network, zero cost.

Run: python3 scripts/generate_industry_report.py
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

RESULTS_DIR = ROOT / "results"
REPORTS_DIR = ROOT / "reports"


def quarter_label(dt: datetime) -> str:
    q = (dt.month - 1) // 3 + 1
    return f"{dt.year}-Q{q}"


def main() -> int:
    latest_path = RESULTS_DIR / "latest.json"
    if not latest_path.exists():
        print("no results/latest.json -- run scripts/publish_results.py first")
        return 1
    payload = json.loads(latest_path.read_text())

    # Count actual prior REPORT snapshots, not every results/run-*.json --
    # the latter includes incidental runs from harness testing/CI, not
    # deliberate "take a report snapshot" moments.
    prior_reports = sorted(REPORTS_DIR.glob("*.md")) if REPORTS_DIR.exists() else []
    snapshot_number = len(prior_reports) + 1

    now = datetime.now(timezone.utc)
    label = quarter_label(now)
    out_path = REPORTS_DIR / f"{label}-snapshot.md"

    backends = sorted({r["backend_id"] for r in payload["results"]})
    scenario_count = len({r["scenario_id"] for r in payload["results"]})

    lines = [
        f"# State of Agentic Blast-Radius Safety — {label}",
        "",
        f"Snapshot #{snapshot_number} (by count of prior `reports/*.md` files). "
        f"Generated {now.isoformat()}.",
        "",
        "## What this snapshot can and can't claim",
        "",
        (
            "**This is a baseline, not a trend.**" if snapshot_number <= 1 else
            f"This is snapshot #{snapshot_number} — a quarter-over-quarter comparison becomes "
            "meaningful starting from the second one onward, via `scripts/check_regression.py` "
            "against each prior committed run."
        ),
        "",
        (
            "No real coding agent has been benchmarked yet — every backend below is the "
            "scripted, zero-cost Reference Backend (`design/COST_AND_CONTROL.md` §1), not a "
            "claim about Claude Code, Codex CLI, Cursor, or Aider's actual behavior. This "
            "report format exists so that once real-backend runs start (Phase 9's second "
            "backend, Phase 18's cost-incurring step), each quarter's comparison is automatic "
            "rather than assembled by hand."
        ),
        "",
        "## This snapshot",
        "",
        f"- Scenarios: {scenario_count} across all 4 taxonomy classes (`design/TAXONOMY.md`)",
        f"- Backends evaluated: {', '.join(backends)}",
        f"- Full results: [`results/latest.json`](../results/latest.json), [`RESULTS.md`](../RESULTS.md)",
        f"- Live leaderboard: https://ppradyoth.github.io/yolobench/",
        "",
        "## Cadence plan",
        "",
        "Quarterly, once real-backend data exists to make quarter-over-quarter comparison "
        "meaningful. Until then, snapshots are generated ad hoc as the benchmark itself "
        "develops (new scenarios, rubric changes) rather than on a fixed calendar — a fixed "
        "cadence with nothing new to report each time would train readers to stop reading, "
        "which defeats the point.",
        "",
    ]

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines))
    print(f"wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
