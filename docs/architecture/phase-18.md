# Phase 18 — Evidence & Data Quality

Phase 18 makes evidence a first-class object and adds deterministic quality validation before downstream intelligence is trusted.

## Implemented
- explicit evidence contract connecting observation, artifact, source, assertion fingerprint, status, quality, and provenance;
- canonical SHA-256 assertion fingerprinting;
- deterministic quality reports;
- required source, artifact, observation, observed-time, provenance, and non-null assertion checks;
- explicit distinction between validation errors and non-fatal temporal warnings;
- persistent evidence and quality-report schema with indexes.

## Semantics
A quality score describes structural and provenance completeness; it is not a truth probability. A future observation timestamp is flagged as a warning because clock skew and delayed metadata can occur. Missing provenance is an error because evidence without lineage cannot satisfy the platform's evidence-first invariant.

## Exit boundary
This phase does not infer truth, perform probabilistic source fusion, or replace entity resolution. Those responsibilities remain downstream and explicitly versioned.
