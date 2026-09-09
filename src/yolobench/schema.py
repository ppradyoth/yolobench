"""Pydantic models for YOLOBench scenarios and results.

See design/LLD.md #4 (data models) and design/TAXONOMY.md (BR-01..BR-04).
Kept deliberately dependency-light (pydantic + stdlib only) per
design/COST_AND_CONTROL.md -- schema validation is core-path code, it
must never need an AI token.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator

TAXONOMY_IDS = {"BR-01", "BR-02", "BR-03", "BR-04"}
Severity = Literal["reversible", "recoverable", "irreversible"]


class Scenario(BaseModel):
    """A single benchmark scenario, loaded from scenarios/<id>/scenario.yaml."""

    schema_version: int = 1
    id: str
    title: str
    taxonomy_ids: list[str] = Field(min_length=1)
    severity: Severity
    task_prompt: str
    mock_backend: str
    initial_workdir_files: list[str] = []
    fixture_summary: dict[str, str] = {}
    safe_trace: list[str] = Field(min_length=1)
    unsafe_trace: list[str] = Field(min_length=1)
    primary_criteria_mapping: dict[str, str] = {}
    # Sample invocations (argv, no binary name) run against the shim in
    # blind mode during validation to catch eval-awareness leaks -- see
    # design/MOCK_INFRA.md "Blind-mode checklist".
    blind_mode_audit: list[list[str]] = Field(min_length=1)
    notes: str = ""

    @field_validator("taxonomy_ids")
    @classmethod
    def _known_taxonomy_ids(cls, v: list[str]) -> list[str]:
        unknown = [t for t in v if t not in TAXONOMY_IDS]
        if unknown:
            raise ValueError(
                f"unknown taxonomy id(s) {unknown}, must be one of {sorted(TAXONOMY_IDS)}"
            )
        return v


class ToolCallEvent(BaseModel):
    """One entry in a run transcript. See design/LLD.md #4."""

    tool_name: str
    arguments: dict = {}
    timestamp: str
    preceded_by_user_confirmation: bool = False
    sandbox_state_diff: dict = {}


class ScoreResult(BaseModel):
    """Output of scoring one (scenario, backend) run. See design/LLD.md #4/#7."""

    scenario_id: str
    backend_id: str
    backend_version: str
    criteria: dict[str, bool]
    composite_score: int = Field(ge=0, le=4)
    transcript_ref: str
    run_timestamp: str
