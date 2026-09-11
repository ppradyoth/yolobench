"""Orchestrates one (scenario, backend) run -- Phase 9. See design/LLD.md #6.

Materializes a fresh, isolated sandbox per run (never reused across runs,
never the scenario's own source directory -- a backend must not be able to
write into scenarios/<id>/ and corrupt the fixture), launches the backend,
scores the resulting transcript, and returns a ScoreResult.
"""
from __future__ import annotations

import json
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from yolobench.backends.base import AgentBackend
from yolobench.rubric import composite_score, score_criteria
from yolobench.schema import Scenario, ScoreResult


def run_scenario(
    scenario: Scenario,
    backend: AgentBackend,
    scenario_dir: Path,
    transcripts_dir: Path | None = None,
) -> ScoreResult:
    """Run `backend` against `scenario` (whose fixtures live in
    `scenario_dir`) inside a fresh temp sandbox, score the result, and
    optionally persist the transcript under `transcripts_dir`."""
    with tempfile.TemporaryDirectory(prefix="yolobench-") as tmp:
        sandbox_dir = Path(tmp)

        shim_src = scenario_dir / "fixtures" / "bin"
        shim_dst = sandbox_dir / "fixtures" / "bin"
        shutil.copytree(shim_src, shim_dst)

        workdir_src = scenario_dir / "fixtures" / "workdir"
        workdir_dst = sandbox_dir / "workdir"
        workdir_dst.mkdir(parents=True, exist_ok=True)
        if workdir_src.exists():
            shutil.copytree(workdir_src, workdir_dst, dirs_exist_ok=True)

        transcript = backend.run(scenario, sandbox_dir)

    criteria = score_criteria(scenario, transcript)
    score = composite_score(criteria)
    run_timestamp = datetime.now(timezone.utc).isoformat()

    transcript_ref = "not-persisted"
    if transcripts_dir is not None:
        transcripts_dir.mkdir(parents=True, exist_ok=True)
        path = transcripts_dir / f"{scenario.id}__{backend.id}.json"
        path.write_text(json.dumps([e.model_dump() for e in transcript], indent=2))
        try:
            transcript_ref = str(path.relative_to(Path.cwd()))
        except ValueError:
            transcript_ref = str(path)  # not run from repo root -- fall back to absolute

    return ScoreResult(
        scenario_id=scenario.id,
        backend_id=backend.id,
        backend_version=backend.version,
        criteria=criteria,
        composite_score=score,
        transcript_ref=transcript_ref,
        run_timestamp=run_timestamp,
    )
