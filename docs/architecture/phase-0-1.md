# Phase 0-1: Foundation and Source & Artifact

## Scope

Phase 0 establishes stable contracts, ontology, CI, documentation, database boundaries,
and a security baseline. Phase 1 adds source registration, a connector interface,
immutable artifact identity, content hashing/deduplication, and source health.

## Canonical boundary

SOURCE -> ACQUISITION -> RAW ARTIFACT -> OBSERVATION

Phase 1 intentionally stops before observation extraction. Acquisition cannot directly
write entities, events, signals, or authority state.

## Artifact invariants

1. Hash exact acquired bytes before parsing or normalization.
2. SHA-256 is the canonical content identity in Phase 1.
3. Identical bytes produce one canonical artifact.
4. Retrieval/reference records remain distinct from artifacts.
5. A 304/not-modified response is a retrieval outcome, not a new artifact.
6. Accepted artifact metadata is immutable by contract.
7. Source attribution remains explicit even when content is deduplicated.
8. Blob storage is behind a storage URI.

## Source registry

A source has identity, canonical URI, source type, enablement, expected cadence, and
licensing metadata. Later phases can extend reliability, coverage, independence, parser,
and schema metadata without redefining source identity.

## Acquisition interface

Connectors return the versioned acquisition response and preserve ETag and Last-Modified
when supplied. Conditional retrieval should be preferred where supported. The acquisition
boundary is not an intelligence-writing boundary.

## Source health

Health records distinguish a quiet source from a failed source. At minimum, health
tracks state, check time, consecutive failures, latency, last success, last failure,
and a machine-readable error code.

## Database integrity

The database enforces primary keys, uniqueness, foreign keys, not-null constraints,
and domain checks. Artifact content is globally deduplicated while retrieval provenance
remains source-specific.

## Security

Remote input is hostile. Network adapters must enforce DNS/IP checks at connection time,
redirect revalidation, credential isolation, response/decompression limits, timeouts,
and parser isolation. The Python helper provides deterministic preflight checks but is
not a complete SSRF defense.
