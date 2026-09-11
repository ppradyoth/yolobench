"""Pydantic models for YOLOBench scenarios and results.

See design/LLD.md #4 (data models) and design/TAXONOMY.md (BR-01..BR-04).
Kept deliberately dependency-light (pydantic + stdlib only) per
design/COST_AND_CONTROL.md -- schema validation is core-path code, it
must never need an AI token.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator

TAXONOMY_IDS = {"BR-01", "BR-02", "BR-03", "BR-04"}
Severity = Literal["reversible", "recoverable", "irreversible"]


class RubricHooks(BaseModel):
    """Machine-readable classification of a scenario's calls, so the rubric
    (Phase 7) can score a transcript deterministically instead of guessing
    from free text. See src/yolobench/rubric.py.

    scope_violation_calls entries are either a bare tool_name (any call with
    that name is a violation unless confirmed first) or "tool_name|substring"
    (a call with that name is a violation only if `substring` appears in its
    argv, joined -- e.g. "branch:delete|wip-feature-x" flags deleting that
    specific branch without flagging a delete of some other, safe branch).
    """

    discovery_calls: list[str] = []
    # Some scenarios (BR-01/BR-02 shape) have one specific "did it ask before
    # THIS call" mutation. Others (BR-04 shape) are scored purely by
    # scope_violation_calls instead -- leave this unset for those.
    risky_mutation: str | None = None
    remediation_call: str | None = None
    in_scope_calls: list[str] = Field(min_length=1)
    scope_violation_calls: list[str] = []


class FsWrite(BaseModel):
    """A direct sandbox file write the Reference Backend performs instead of
    invoking a shim -- represents a real agent's generic file-edit tool,
    which the mock infra never needs to intercept (see design/MOCK_INFRA.md)."""

    path: str
    content: str


class PersonaStep(BaseModel):
    """One tool call the Reference Backend (Phase 9) makes when playing a
    given persona for a scenario. Exactly one of (argv) or (fs_write) is
    meaningful: argv invokes the scenario's mock_backend shim; fs_write
    performs a direct sandbox file write instead."""

    tool_name: str
    argv: list[str] = []
    user_confirmed: bool = False
    fs_write: FsWrite | None = None

    @model_validator(mode="after")
    def _exactly_one_action(self) -> "PersonaStep":
        if bool(self.argv) == bool(self.fs_write):
            raise ValueError(
                f"PersonaStep '{self.tool_name}' must set exactly one of argv or fs_write"
            )
        return self


class ReferencePersona(BaseModel):
    """The exact, deterministic call sequences the zero-cost Reference
    Backend plays for this scenario -- see design/COST_AND_CONTROL.md #1."""

    safe: list[PersonaStep] = Field(min_length=1)
    unsafe: list[PersonaStep] = Field(min_length=1)


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
    rubric_hooks: RubricHooks
    reference_persona: ReferencePersona
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

    @model_validator(mode="after")
    def _hooks_reference_real_calls(self) -> "Scenario":
        # Only discovery/risky_mutation/remediation_call must actually be
        # exercised by the reference personas -- those are the crux of the
        # test, so an unexercised one is almost certainly a typo. in_scope
        # and scope_violation lists may legitimately describe the wider
        # space of calls a real agent could make beyond what these two
        # canned personas happen to exercise.
        all_tool_names = {
            step.tool_name
            for step in (*self.reference_persona.safe, *self.reference_persona.unsafe)
        }
        checks = [
            *[("discovery_calls", n) for n in self.rubric_hooks.discovery_calls],
            *([("risky_mutation", self.rubric_hooks.risky_mutation)] if self.rubric_hooks.risky_mutation else []),
            *([("remediation_call", self.rubric_hooks.remediation_call)] if self.rubric_hooks.remediation_call else []),
        ]
        for label, name in checks:
            if name not in all_tool_names:
                raise ValueError(
                    f"rubric_hooks.{label} references tool_name '{name}' that "
                    f"never appears in reference_persona.safe/unsafe"
                )
        return self


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
