# Phase 21 — Fusion & Advanced Signals

Phase 21 strengthens multi-source reasoning without turning correlation or scoring into a claim of truth.

## Implemented
- contradiction-aware evidence fusion;
- explicit independence groups to prevent syndicated sources from being counted as independent corroboration;
- capped support and contradiction scores;
- mixed state when support and contradiction coexist;
- preserved supporting and contradicting evidence identifiers;
- expanded deterministic signal DSL with numeric comparison, membership, and negation;
- explainable evaluation for every supported operator;
- persistent fusion-assessment records.

## Semantic boundary
A fusion score measures structured support/contradiction under the declared independence grouping. It is not a probability that an assertion is true. Unsupported operators fail closed. Contradictory evidence remains visible rather than being silently discarded.

The system still distinguishes correlation from causation and information from authority.
