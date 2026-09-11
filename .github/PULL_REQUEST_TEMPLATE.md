<!-- New scenario PR? Fill out the checklist below -- see CONTRIBUTING.md for the full walkthrough.
     Not a new scenario (docs, code, a fix)? Delete this template and just describe the change. -->

## New scenario: `<scenario-id>`

- **Taxonomy class(es):** BR-0_
- **One-sentence summary of the ambiguity/failure this tests:**

### Checklist

- [ ] `scenario.yaml` + shim(s) under `scenarios/<id>/`, following the blind-mode pattern (`design/MOCK_INFRA.md`)
- [ ] `notes:` field discloses whether this is generalized from something real or invented from scratch (no real company/product/account named either way)
- [ ] Ran locally and all three pass:
  - [ ] `python3 scripts/validate_scenarios.py`
  - [ ] `python3 scripts/test_rubric.py`
  - [ ] `python3 scripts/run_reference_benchmark.py`
- [ ] This isn't a reskin of an existing scenario — it tests a genuinely different ambiguity

### Anything reviewers should know

<!-- Edge cases in your rubric_hooks design, why you chose this taxonomy class, anything you're unsure about -->
