# Final forensic gap fixes

The post-Phase-27 forensic review identified and repaired several material gaps between the foundational contracts and a production service boundary.

## Repaired

1. Provenance was previously represented by nullable identifiers without a canonical persisted provenance relation. Migration 0021 adds a provenance record table and foreign keys from observations, events, temporal assertions, relationships, and evidence.
2. The HTTP query service previously used only in-memory stores. A PostgreSQL-backed query service is now available with an allowlisted resource map and parameterized pagination values.
3. The runtime now has a bounded local rate-limiter primitive for deployment adapters.
4. The final CI schema gate includes the new provenance table.
5. PostgreSQL is the authoritative production persistence boundary; in-memory stores remain a test/development implementation.
6. The final audit remains explicit that external compliance, independent penetration testing, cloud HA, and customer-specific SLA evidence are not established by repository CI alone.

## Remaining deployment evidence

A production deployment still requires a real identity provider/API gateway, TLS termination, shared rate limiting, durable object storage, queue workers, source-specific network egress controls, backups/restore drills, and independent security assessment. These are deployment/runtime evidence rather than claims that can be truthfully inferred from source code alone.
