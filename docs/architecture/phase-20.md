# Phase 20 — Temporal & Geospatial Runtime

Phase 20 makes temporal and spatial semantics executable at the service boundary instead of leaving them as schema contracts only.

## Implemented
- half-open valid-time interval semantics;
- explicit knowledge-as-of filtering;
- deterministic point-radius distance calculation using WGS84-compatible latitude/longitude inputs;
- composition of world-time, knowledge-time, and spatial-radius constraints;
- additional database indexes for temporal status/subject and spatial entity/type plus validity windows.

## Semantics
Event/valid time and knowledge time are distinct. A record can be valid in the world but unavailable to the system at an earlier knowledge cutoff. Radius queries use great-circle distance and are a runtime reference implementation; production PostGIS queries remain authoritative for large datasets.

The service does not convert absence from a spatial/temporal query into a negative world assertion.

## Interoperability
The spatial contract remains aligned with OGC-style feature semantics and WGS84 coordinates. PostGIS remains the persistence/query engine for production-scale spatial predicates.
