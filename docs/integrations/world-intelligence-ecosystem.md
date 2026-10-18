# Phase 15 — Tinlance Ecosystem

## Boundaries

- **ReconOS** supplies acquisition/recon inputs; World Intelligence canonicalizes them.
- **TADS** consumes canonical entities/events/signals; it does not own world state.
- **Agent OS** consumes bounded intelligence capabilities; it does not receive unrestricted database access.
- **Agent Platform** remains the authority for identity, policy, approval, budgets, execution, and governance.
- **External APIs/SDKs** expose stable read/query contracts with evidence and provenance references.

World Intelligence supplies information and evidence, not authorization. Agent Platform remains
the enforcement authority. All governed capability requests must carry tenant/purpose context and
receive an explicit authorization result before sensitive data is returned.

## TWI source-evidence intake

Tinlance Web Intelligence can submit a bounded `POST /v1/source-evidence` envelope after its
citation verifier confirms that an excerpt matches a successful, caller-authorized fetch or
browser capture. The intake endpoint:

- authenticates the TWI service with `WORLD_INTELLIGENCE_SOURCE_EVIDENCE_TOKEN`, a dedicated credential separate from the query API bearer token;
- requires an idempotency key and validates a versioned, strict JSON contract;
- accepts only a pseudonymous SHA-256 tenant reference, not the raw tenant identifier;
- stores source URL, retrieval time, source artifact digest, normalized excerpt, excerpt digest,
  verifier version, and report digest;
- rejects raw HTML, arbitrary extra fields, invalid trace context, URL credentials, invalid hashes,
  and idempotency-key reuse with a different payload;
- records the payload as **candidate source evidence**. It does not create canonical entities,
  events, relationships, or observations and does not assert that a claim is true.

The Postgres migration is `0022_twi_source_evidence.sql`. The in-memory store exists only for
development and tests. Production/staging deployments must use PostgreSQL and the dedicated source-evidence credential kept in the secret manager. The intake endpoint never falls back to the general query API token. Downstream normalization and promotion remain World Intelligence
responsibilities, subject to tenant policy and TSIC conformance.
