# Phase 24 — Reliability & Distributed Systems

Phase 24 establishes the semantics required for safe at-least-once distributed processing.

## Implemented
- deterministic idempotency-key derivation;
- circuit-breaker state machine;
- explicit worker leases with expiration;
- persistent ingestion job and attempt schema;
- unique job idempotency keys;
- ready/lease indexes for worker scheduling;
- explicit retryable versus permanent attempt outcomes.

## Reliability semantics
At-least-once delivery is expected to create duplicates unless every side effect has an idempotency boundary. Idempotency keys therefore precede durable job execution. Leases expire so abandoned work can be recovered by another worker.

Circuit breakers protect unhealthy sources without turning outages into world-state assertions. Dead-letter state is explicit and auditable.

This phase does not claim multi-region HA by itself. Database replication, object-store durability, queue clustering, backup/restore, failover automation, and SLO enforcement are operational follow-ons.
