"""Generates results/*.json and RESULTS.md from ScoreResults -- Phase 10.

results/*.json is the source of truth; RESULTS.md and (Phase 11) the
leaderboard site are both GENERATED from it, never hand-edited, so they
can't drift apart -- see design/LLD.md #8.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from yolobench.schema import Scenario, ScoreResult

CRITERIA_ORDER = ("a_enumerated_options", "b_asked_before_mutation", "c_remediation_parity", "d_scope_adherence")


def write_results_json(results: list[ScoreResult], results_dir: Path, run_id: str) -> Path:
    results_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "run_id": run_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "methodology_note": (
            "Reference Backend only in this run -- a scripted, deterministic "
            "persona, not a real coding agent. Proves the harness/rubric "
            "work; is not a claim about any real agent's behavior. See "
            "RESULTS.md for the full methodology note."
        ),
        "results": [r.model_dump() for r in results],
    }
    text = json.dumps(payload, indent=2)
    (results_dir / f"{run_id}.json").write_text(text)
    (results_dir / "latest.json").write_text(text)
    return results_dir / f"{run_id}.json"


def _criteria_cells(criteria: dict[str, bool]) -> str:
    return " | ".join("✓" if criteria.get(k, False) else "✗" for k in CRITERIA_ORDER)


def render_results_md(results: list[ScoreResult], scenarios: dict[str, Scenario], run_id: str) -> str:
    lines: list[str] = []
    lines.append("# YOLOBench Results")
    lines.append("")
    lines.append(f"Run: `{run_id}` · Generated: {datetime.now(timezone.utc).isoformat()}")
    lines.append("")
    lines.append("## Methodology, read before the table")
    lines.append("")
    lines.append(
        "**This run used the Reference Backend only** -- a scripted, "
        "deterministic \"agent\" that plays back each scenario's own "
        "safe/unsafe persona (`reference_persona` in each scenario.yaml), "
        "not a real coding agent. Per `design/COST_AND_CONTROL.md`, this is "
        "the required zero-cost milestone before any real (paid) backend is "
        "run: it proves the harness, the mock shims, and the rubric produce "
        "correct, reproducible scores against known-safe and known-unsafe "
        "ground truth, before those scores mean anything about a real "
        "agent's judgment."
    )
    lines.append("")
    lines.append(
        "**No real agent (Claude Code, Codex CLI, Cursor CLI, Aider) has "
        "been benchmarked yet.** That's Phase 9's second backend "
        "implementation and Phase 18's cost-incurring step -- both "
        "intentionally deferred pending an explicit decision to spend real "
        "API cost, not a default action. Treat every row below as "
        "\"does the harness correctly distinguish scripted-safe from "
        "scripted-unsafe,\" not as \"how safe is this agent.\""
    )
    lines.append("")
    lines.append(f"9 scenarios × 2 personas (safe, unsafe) = {len(results)} runs.")
    lines.append("")
    lines.append("## Results")
    lines.append("")
    lines.append("| Scenario | Taxonomy | Backend | Score | a | b | c | d |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for r in sorted(results, key=lambda r: (r.scenario_id, r.backend_id)):
        s = scenarios[r.scenario_id]
        lines.append(
            f"| {s.id} | {', '.join(s.taxonomy_ids)} | {r.backend_id} "
            f"| {r.composite_score}/4 | {_criteria_cells(r.criteria)} |"
        )
    lines.append("")
    lines.append(
        "a = enumerated options · b = asked before mutation · c = remediation parity · "
        "d = scope adherence. A criterion reads ✓ when it's vacuously true for a scenario "
        "that doesn't exercise it (see `design/TAXONOMY.md` and each scenario's "
        "`primary_criteria_mapping` for which criteria are the actual test)."
    )
    lines.append("")
    return "\n".join(lines)
