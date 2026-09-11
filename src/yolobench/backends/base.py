"""AgentBackend interface -- Phase 9. See design/LLD.md #6."""
from __future__ import annotations

from pathlib import Path
from typing import Protocol

from yolobench.schema import Scenario, ToolCallEvent


class AgentBackend(Protocol):
    """Executes a scenario's task, headless, inside a sandbox with the
    scenario's mock shim on PATH, and returns a structured transcript.
    Real backends normalize their own execution log into ToolCallEvents
    here -- the rubric never needs backend-specific logic."""

    id: str
    version: str

    def run(self, scenario: Scenario, sandbox_dir: Path) -> list[ToolCallEvent]: ...
