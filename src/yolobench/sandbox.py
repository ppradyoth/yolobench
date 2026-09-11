"""Shared sandbox helpers -- Phase 3/9.

Every subprocess launched against a scenario's mock shim uses SCRUBBED_ENV,
never the parent process's own environment -- this is what actually makes
"no real cloud account is touched" true rather than aspirational (a naive
setup that inherits GOOGLE_APPLICATION_CREDENTIALS or .netrc from the
parent shell would leave a real credential reachable around the shim). See
design/COST_AND_CONTROL.md #5 and design/MOCK_INFRA.md.
"""
from __future__ import annotations

SCRUBBED_ENV = {"PATH": "/usr/bin:/bin", "HOME": "/tmp"}
