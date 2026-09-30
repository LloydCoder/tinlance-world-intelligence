# Database foundation

The initial persistence target is PostgreSQL with PostGIS. Phase 0-1 stays relational
and does not require a graph database, streaming platform, or search cluster.

## Phase 1 tables

- world_intelligence.sources — source identity, endpoint, cadence, licensing.
- world_intelligence.raw_artifacts — immutable artifact metadata keyed by SHA-256.
- world_intelligence.artifact_references — every retrieval/reference outcome.
- world_intelligence.source_health — current source health state.
- world_intelligence.schema_metadata — explicit schema, contract, and hash versions.

Identical payloads are deduplicated by the unique artifact content hash. Retrieval
records remain separate so provenance is retained when sources return identical bytes.

The artifact ledger stores metadata and a storage URI, not an assumed blob implementation.
