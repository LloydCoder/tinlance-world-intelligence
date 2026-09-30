# Contributing

## Engineering standard

Contributions must preserve the core distinctions and boundaries of Tinlance World Intelligence.

Before introducing a change, verify:

1. It belongs in World Intelligence.
2. It does not duplicate ReconOS, TADS, Agent OS, or Agent Platform responsibilities.
3. Provenance remains available.
4. Temporal semantics remain explicit.
5. Unknown and contradictory states remain representable.
6. External input remains untrusted.
7. Contracts remain versioned and testable.
8. Tests cover the changed behavior.
9. Documentation is updated for architectural changes.

## Vertical slices

Prefer small vertical slices over large disconnected scaffolds. A slice should connect source/acquisition, artifact, observation, world state, API, tests, and documentation where applicable.

## Pull requests

PRs should explain:

- problem and scope
- architectural impact
- data/provenance impact
- security impact
- migration impact
- testing performed
- follow-up work

Do not commit secrets, credentials, raw private data, or generated local state.
