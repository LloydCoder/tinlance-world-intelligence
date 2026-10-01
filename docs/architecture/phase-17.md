# Phase 17 — Acquisition & Ingestion Fabric

Phase 17 turns the acquisition boundary into an explicit ingestion orchestration layer while preserving the rule that acquisition never becomes intelligence.

## Implemented
- bounded ingestion work queue;
- immutable job envelope with source identity and acquisition request;
- deterministic bounded retry policy;
- explicit retry exhaustion rather than silent failure;
- injected acquisition-client boundary so network implementation remains replaceable and testable;
- conditional 304/not-modified handling;
- successful payloads are hashed and written through the artifact ledger;
- artifact identity is content-addressed by SHA-256;
- ingestion results distinguish stored, not-modified, and failed outcomes.

## Operational semantics
Retries are bounded and deterministic. A failed source is not interpreted as an empty world state. A 304 response does not create a new artifact. Upstream non-2xx responses are represented as acquisition failures.

The coordinator intentionally does not parse content into observations. Artifact acquisition and intelligence extraction remain separate trust boundaries.

## Enterprise follow-on
A production deployment still needs durable queues, distributed workers, persistent object storage, scheduler/webhook adapters, source-level circuit breakers, connection-time SSRF enforcement, credential isolation, byte/time decompression limits, and replayable ingestion telemetry. Those are not silently claimed by this phase.
