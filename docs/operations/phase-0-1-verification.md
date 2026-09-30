# Phase 0-1 verification contract

A Phase 0-1 implementation is complete only when all of these are true:

- Python sources compile.
- Unit and contract tests pass.
- Repository secret baseline passes.
- PostgreSQL/PostGIS migration applies with ON_ERROR_STOP.
- PostGIS is enabled.
- Exactly five Phase 0-1 tables exist in the world_intelligence schema.
- Artifact content SHA-256 is unique.
- Retrieval references remain separate from deduplicated artifacts.
- Stored references require an artifact; non-stored outcomes do not.
- Source health has explicit failure-state transitions.
- CI uses least-privilege contents read permission.
- Third-party GitHub Actions are pinned to full commit SHAs.
- Documentation matches the implemented boundaries.

The database job is deliberately executed against a real PostGIS container rather
than validating SQL with string matching.
