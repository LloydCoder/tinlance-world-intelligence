# Phase 13 — Replay & Backtesting
Replay is manifest-driven: artifact identities, ontology version, pipeline version, and rule
versions are pinned. Backtests calculate explicit precision/recall and use golden fixtures for
regression. Replay does not mutate canonical world state; it produces reproducible outputs for
comparison and audit.