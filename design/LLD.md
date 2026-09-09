# Low-Level Design — blast-radius-bench

**Status:** Design only. No code has been written against this LLD yet — implementation starts at Phase 6 (`plan/phase-06-scenario-library-v1.md`) per the structured development approach: plan → design → build, in that order, per phase.

This document incorporates the full 20-phase plan (`plan/00-overview.md` + `plan/phase-*.md`) into one coherent system design, so that when implementation starts, every component has an agreed shape before the first line of code lands.

---

## 1. Scope

Covers the design of every component the plan calls for, end to end: scenario definition → sandboxed execution → structured scoring → results publication → regression tracking → the later mitigation middleware. Sections are tagged with the phase(s) that deliver them so the plan and design stay traceable to each other.

---

## 2. System Architecture

```mermaid
flowchart TB
    subgraph Authoring["Scenario Authoring (Phase 6, 12)"]
        SchemaDef["Scenario Schema\n(YAML + Pydantic model)"]
        ScenarioLib["scenarios/*.yaml\n(scenario library)"]
    end

    subgraph Sandbox["Mock Infra Layer (Phase 3, 9)"]
        Shims["CLI shims\n(firebase, gcloud, aws, git, npm...)"]
        SandboxDir["Per-run sandbox dir\n+ scoped PATH"]
    end

    subgraph Harness["Harness / Runner (Phase 9)"]
        Runner["Runner"]
        Backend1["AgentBackend: Claude Code"]
        Backend2["AgentBackend: Codex CLI"]
        Backend3["AgentBackend: Cursor CLI / Aider / ..."]
    end

    subgraph Scoring["Scoring (Phase 7, 8)"]
        Rubric["Deterministic rubric\n(state machine over tool-call events)"]
        Judge["Structured judge\n(last-match, tool-call output only)"]
    end

    subgraph Publish["Results & Tracking (Phase 10, 11, 15)"]
        ResultsData["results/*.json (source of truth)"]
        ResultsMd["RESULTS.md (generated)"]
        Site["Leaderboard static site (generated)"]
        CI["Regression CI\n(scheduled + on new agent version)"]
    end

    subgraph Mitigation["Mitigation (Phase 16, 17, 19)"]
        Policy["Policy rules\n(data-driven, per taxonomy class)"]
        Gate["Middleware Gate\n(hooks into agent tool-call lifecycle)"]
    end

    ScenarioLib --> Runner
    SchemaDef -.validates.-> ScenarioLib
    Runner --> SandboxDir
    SandboxDir --> Shims
    Runner --> Backend1 & Backend2 & Backend3
    Backend1 & Backend2 & Backend3 --> Transcript["Structured transcript\n(tool-call events)"]
    Transcript --> Rubric
    Rubric -->|ambiguous free-text case only| Judge
    Rubric --> ResultsData
    Judge --> ResultsData
    ResultsData --> ResultsMd
    ResultsData --> Site
    CI --> Runner
    CI --> ResultsData
    Policy --> Gate
    Gate -.wraps.-> Backend1
    Transcript -.self-test.-> Gate
```

---

## 3. Repo layout (target, once implementation starts)

```
blast-radius-bench/
  plan/                     # existing — phase-wise roadmap
  design/                   # this file + taxonomy detail as it hardens
  scenarios/                # Phase 6+ — one dir per scenario, YAML + fixture data
    br-01-multi-project-deploy/
      scenario.yaml
      fixtures/
  src/
    blast_radius_bench/
      schema.py             # Pydantic models — Scenario, Transcript, ToolCallEvent, ScoreResult
      mockinfra/             # Phase 3/9 — PATH shims per mocked CLI
      backends/               # Phase 9 — one module per AgentBackend
        claude_code.py
        codex_cli.py
        cursor_cli.py
        aider.py
      rubric.py              # Phase 7 — deterministic scoring
      judge.py               # Phase 8 — structured, last-match judge
      runner.py              # Phase 9 — orchestrates a scenario run
      report.py              # Phase 10/11 — RESULTS.md + site data generation
  results/                   # Phase 10 — results/*.json, one per run, + latest.json
  site/                      # Phase 11 — generated static leaderboard (build output, gitignored or a gh-pages branch)
  gate/                      # Phase 17/19 — middleware gate, may split to its own repo at Phase 19
    policy/                 # rules files, data-driven
  .github/workflows/         # Phase 15 — regression CI
  tests/
```

No `src/` or `scenarios/` content exists yet — per Phase 2, Arc A stays plan/design-only until Phase 6.

---

## 4. Core data models (Phase 6/9, formalized as Pydantic)

### Scenario
```
Scenario:
  id: str                     # e.g. "br-01-multi-project-deploy"
  taxonomy_ids: list[str]     # primary + secondary BR-IDs, from Phase 1
  severity: Literal["reversible", "recoverable", "irreversible"]
  task_prompt: str            # exact prompt given to the agent
  mock_fixtures: dict         # what each shimmed CLI command returns
  safe_trace: list[ToolCallPattern]    # what a "safe" run's tool calls should look like
  unsafe_trace: list[ToolCallPattern]  # what an "unsafe" run's tool calls look like
```

### ToolCallEvent (transcript unit)
```
ToolCallEvent:
  tool_name: str
  arguments: dict
  timestamp: datetime
  preceded_by_user_confirmation: bool   # derived: was there a user-facing question immediately before this call
  sandbox_state_diff: dict              # filesystem/env diff caused by this call, if any
```

### ScoreResult
```
ScoreResult:
  scenario_id: str
  backend_id: str
  backend_version: str
  criteria: dict[str, bool]   # (a) enumerated options, (b) asked before first mutation,
                               # (c) remediation caution >= original, (d) stayed in authorized scope
  composite_score: int         # 0-4
  transcript_ref: str          # pointer to stored raw transcript
  run_timestamp: datetime
```

These three models are the contract every other component (backends, rubric, judge, report generator) is built against — get them right once at Phase 6/7, avoid reshaping them later since scenarios and historical results depend on schema stability.

---

## 5. Mock Infrastructure Layer (Phase 3, implemented Phase 9)

- **Mechanism:** per-run sandbox directory with a scoped `PATH` prepended with a shim directory. Shim scripts (e.g. `firebase`, `gcloud`, `git`) intercept the exact subcommands a scenario needs (`projects:list`, `deploy`, `remote -v`, etc.) and return scripted fixture output defined in `Scenario.mock_fixtures`.
- **Fail-loud boundary:** any shimmed command invoked with arguments not covered by the scenario's fixture returns a non-zero exit and a clear stderr message (`"blast-radius-bench: unscripted invocation, no real call made"`) rather than silently no-op'ing or falling through to a real binary. This is the property Phase 3 explicitly calls out as needing its own design review.
- **Isolation escalation path:** start with temp-dir + `PATH` shims (fast, simple, sufficient while backends only shell out to CLIs). If a backend's tool-call surface expands to things that can't be caught by `PATH` interception alone (raw HTTP calls, SDK calls bypassing CLIs), escalate to network-level sandboxing (e.g. running the backend inside a container with an egress allowlist of nothing) — noted as a Phase 3 open decision, revisit once Phase 9 backends are real and their actual call surface is known.

---

## 6. Harness / Runner (Phase 9)

### `AgentBackend` interface
```
class AgentBackend(Protocol):
    def run(self, scenario: Scenario, sandbox_dir: Path) -> Transcript:
        """Execute the scenario's task_prompt against this agent, headless,
        inside sandbox_dir with the mocked PATH active. Return a structured
        Transcript (list[ToolCallEvent]) plus final sandbox filesystem state."""
```

Each concrete backend (Claude Code, Codex CLI, Cursor CLI, Aider, Copilot CLI) implements this by driving the respective tool's non-interactive/headless mode and parsing its own execution log format into the shared `ToolCallEvent` shape — the normalization into a common event format happens in the backend adapter, so the rubric never needs backend-specific logic.

### Run sequence (single scenario × single backend)

```mermaid
sequenceDiagram
    participant Runner
    participant Sandbox as Sandbox Dir + Shims
    participant Backend as AgentBackend
    participant Rubric
    participant Judge
    participant Results as results/*.json

    Runner->>Sandbox: materialize fixtures, scoped PATH
    Runner->>Backend: run(scenario, sandbox_dir)
    Backend->>Sandbox: tool calls (intercepted by shims)
    Sandbox-->>Backend: scripted fixture responses
    Backend-->>Runner: structured Transcript
    Runner->>Rubric: score(transcript, scenario)
    alt free-text criterion ambiguous
        Rubric->>Judge: classify(specific text span)
        Judge-->>Rubric: structured verdict (last-match parsed)
    end
    Rubric-->>Runner: ScoreResult
    Runner->>Results: append ScoreResult
```

---

## 7. Scoring Rubric (Phase 7) and Judge (Phase 8)

- Rubric is a pure function over `Transcript` + `Scenario` → the four boolean criteria in `ScoreResult.criteria`, computed from tool-call sequencing and arguments — never from the agent's narrated reasoning alone (Phase 7's explicit anti-goal).
- Judge is invoked only when a criterion genuinely can't be resolved from structured events (e.g. judging whether a free-text agent message constitutes "asking" vs. "informing after the fact"). Judge output is a structured tool-call response, and if any text parsing is needed, it takes the **last** matching block, not the first — direct mitigation of the T-14 judge-verdict-hijacking class documented in the adversarial testing library. Phase 8's acceptance criterion (self-test with an embedded fake verdict) is implemented as a standing unit test, not a one-time manual check.

---

## 8. Results & Publication (Phase 10, 11, 15)

- `results/<run-id>.json` is the source of truth (one file per full benchmark run — all scenarios × all backends). `RESULTS.md` and the leaderboard site are both **generated** from this data, never hand-edited, so they can't drift apart.
- Leaderboard site (Phase 11): plain static HTML/CSS + vanilla JS reading the results JSON directly (no heavy frontend framework — this is a research artifact, not a product; a TS/React build would be justified later only if interactivity needs genuinely outgrow a static table + chart).
- Regression CI (Phase 15): scheduled GitHub Action reruns the harness against pinned agent versions, diffs the new `results/*.json` against the previous run, and opens a GitHub Issue automatically on any pass→fail flip.

---

## 9. Mitigation Middleware Gate (Phase 16, 17, 19)

- Policy expressed as data (a rules file per taxonomy class), evaluated by a small policy engine that intercepts tool calls before execution — not hardcoded per-agent logic, so the same policy file works across backends that expose a hook point.
- First integration target: Claude Code's own hooks system, since it's the best-understood interception point from this project's own tooling.
- Self-test requirement (Phase 17): running the Phase 6 scenario library through a gated agent must show measurable improvement over the Phase 10 ungated baseline, using the exact same harness and rubric — the gate is validated by the same benchmark that motivated it, not a separate ad hoc test.
- Phase 19 extraction: if the gate proves useful standalone, it moves to its own package/repo with independent versioning — this LLD's `gate/` module is written from the start to be extractable without a rewrite (no hidden coupling to the benchmark's internal result-storage format).

---

## 10. Tech stack

- **Core engine (schema, mock infra, runner, rubric, judge, report generation): Python** — matches existing stack conventions, and the CLI-shim/subprocess-heavy nature of the mock infra layer is a natural fit. Pydantic for schema validation.
- **Scenario definitions:** YAML (human-writable, diffable in PRs — matters for Phase 12 community contributions).
- **Leaderboard site:** static HTML/CSS/vanilla JS initially; revisit only if interactivity requirements grow.
- **CI:** GitHub Actions.
- **Middleware gate:** Python core, packaged for pip; a Node/TS wrapper considered later only if adoption (Phase 19) demands integration with JS-based agent frameworks.

---

## 11. Phase-to-design traceability

| Plan phase | LLD section(s) delivered |
|---|---|
| 1 | Taxonomy (referenced throughout, own doc) |
| 2 | §3 repo layout (scaffold only, no code yet) |
| 3 | §5 Mock Infra (design) |
| 4–5 | §4 data models (first concrete instance), validated by hand |
| 6 | §4 data models (formalized/coded), scenario library |
| 7 | §7 rubric |
| 8 | §7 judge |
| 9 | §5 (implemented), §6 harness |
| 10 | §8 results generation |
| 11 | §8 leaderboard site |
| 12 | §4 schema stability (contribution format) |
| 13–14 | (no new components — consumes §8 outputs) |
| 15 | §8 regression CI |
| 16 | §9 policy design |
| 17 | §9 gate implementation |
| 18 | (no new components — consumes §9 + §8 outputs) |
| 19 | §9 extraction |
| 20 | §8 (recurring generation of the same artifacts, scheduled) |

---

## 12. Open design questions (to resolve before Phase 6 code starts)

1. Containerization vs. `PATH`-shim-only sandboxing — revisit once real backend call surfaces (Phase 9) are known (§5).
2. Exact definition of "a new agent version worth rerunning against" per backend for Phase 15 — some agents version discretely, some ship continuously.
3. Whether the middleware gate (§9) stays inside this repo through Phase 17 or gets its own repo immediately — current plan says extract at Phase 19, but early extraction is worth reconsidering if external interest appears sooner.
