# Phase 19 — Entity & Knowledge Graph

Phase 19 strengthens entity intelligence with explicit graph traversal and conservative resolution governance.

## Implemented
- cycle-safe, depth-bounded graph traversal;
- relationship paths represented as nodes plus predicates;
- explicit edge-confidence validation;
- conservative match decisioning with auto-accept, review, and reject states;
- high-confidence matches still require explanatory reasons;
- self-matches are rejected;
- persistent entity-resolution candidate records with review indexing.

## Graph model
The relational relationship model remains canonical. It represents the same conceptual graph structure used by property-graph and RDF systems: entities are nodes and relationships are directed typed edges. The implementation does not require a separate graph database.

Temporal validity and provenance remain authoritative constraints; traversal is bounded to prevent accidental unbounded graph expansion.

## Resolution invariant
False merges are more damaging than unresolved candidates. Candidate matching therefore has an explicit review state and does not turn a similarity score into canonical identity by itself.
