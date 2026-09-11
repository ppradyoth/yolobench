"""Reference Backend -- Phase 9. Scripted, deterministic, $0, no model call.

Plays back a scenario's own reference_persona.safe or .unsafe sequence,
for real, against the actual sandboxed shim subprocess (fs_write steps
write directly into the sandbox workdir instead, per schema.py). This is
what proves the harness plumbing -- sandbox setup, subprocess execution,
transcript capture, scoring -- actually works, independent of any real
agent's behavior. See design/COST_AND_CONTROL.md #1.
"""
from __future__ import annotations

import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from yolobench import __version__
from yolobench.sandbox import SCRUBBED_ENV
from yolobench.schema import Scenario, ToolCallEvent

Persona = Literal["safe", "unsafe"]


class ReferenceBackend:
    def __init__(self, persona: Persona):
        self.persona = persona
        self.id = f"reference-{persona}"
        self.version = __version__

    def run(self, scenario: Scenario, sandbox_dir: Path) -> list[ToolCallEvent]:
        steps = getattr(scenario.reference_persona, self.persona)
        shim_path = sandbox_dir / "fixtures" / "bin" / scenario.mock_backend
        workdir = sandbox_dir / "workdir"
        workdir.mkdir(parents=True, exist_ok=True)

        transcript: list[ToolCallEvent] = []
        for step in steps:
            timestamp = datetime.now(timezone.utc).isoformat()
            if step.fs_write is not None:
                target = workdir / step.fs_write.path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(step.fs_write.content)
                diff = {"action": "fs_write", "path": step.fs_write.path}
                arguments = {"fs_write": step.fs_write.model_dump()}
            else:
                result = subprocess.run(
                    [str(shim_path), *step.argv],
                    capture_output=True,
                    text=True,
                    cwd=workdir,
                    env=SCRUBBED_ENV,
                )
                diff = {
                    "exit_code": result.returncode,
                    "stdout": result.stdout.strip(),
                    "stderr": result.stderr.strip(),
                }
                arguments = {"argv": step.argv}

            transcript.append(
                ToolCallEvent(
                    tool_name=step.tool_name,
                    arguments=arguments,
                    timestamp=timestamp,
                    preceded_by_user_confirmation=step.user_confirmed,
                    sandbox_state_diff=diff,
                )
            )
        return transcript
