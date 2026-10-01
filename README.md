# Tinlance World Intelligence

**A provenance-first temporal intelligence fabric for modeling, correlating, and monitoring real-world entities, events, relationships, and change.**

> **Status:** Phase 0–27 enterprise roadmap implemented; final validation and operational deployment remain evidence-driven activities  
> **Repository:** `LloydCoder/tinlance-world-intelligence`

## Overview

Tinlance World Intelligence is the intelligence fabric underlying Tinlance's world-awareness systems. It transforms heterogeneous external information into a structured, traceable, temporal representation of the world.

```text
SOURCE → ACQUISITION → RAW ARTIFACT → OBSERVATION
→ ENTITY / EVENT / RELATIONSHIP → TEMPORAL WORLD STATE
→ CHANGE → CORRELATION / CONTRADICTION / COVERAGE
→ SIGNAL → INTELLIGENCE
```

The first application built on the fabric is **Tinlance World Monitor**, a visual interface for exploring entities, events, changes, signals, evidence, and source provenance.

**World Monitor is a consumer of the intelligence fabric—not the definition of it.**

## Goals

- Real-world entity, event, and relationship modeling
- Temporal world-state reconstruction
- Geospatial intelligence
- Evidence and provenance traceability
- Cross-source correlation and contradiction detection
- Change detection and explainable signals
- Source health, freshness, and coverage awareness
- Deterministic replay and historical analysis
- Machine-readable intelligence APIs
- Safe integration with TADS, Agent OS, and other Tinlance systems

## Core semantic model

```text
Source → Raw Artifact → Observation
                         ├→ Entity
                         ├→ Event
                         └→ Relationship
                                  ↓
                           Temporal World State
                                  ↓
                                Change
                                  ↓
                                Signal
                                  ↓
                             Intelligence
```

These concepts are deliberately distinct:

- **Observation ≠ Evidence**
- **Evidence ≠ Finding**
- **Finding ≠ Intelligence**
- **Intelligence ≠ Authority**
- **Freshness ≠ Truth**
- **Absence ≠ Negative Evidence**
- **Correlation ≠ Causation**
- **Multiple Sources ≠ Independent Corroboration**
- **AI Output ≠ Ground Truth**

## Architecture

```text
SOURCE REGISTRY
      ↓
ACQUISITION / CONNECTORS
      ↓
RAW ARTIFACT LEDGER ─────────→ PROVENANCE
      ↓
NORMALIZATION
      ↓
OBSERVATIONS
      ├───────────────┬────────────────┐
      ↓               ↓                ↓
ENTITY RESOLUTION  EVENT EXTRACTION  RELATIONSHIP RESOLUTION
      └───────────────┴────────────────┘
                      ↓
              TEMPORAL WORLD MODEL
                      │
          ┌───────────┼────────────┐
          ↓           ↓            ↓
      CORRELATION  CONTRADICTION  COVERAGE
          └───────────┼────────────┘
                      ↓
                 CHANGE ENGINE
                      ↓
                 SIGNAL ENGINE
                      ↓
              INTELLIGENCE API
                 │      │      │
                 ↓      ↓      ↓
          World Monitor TADS  Agent OS
                                ↓
                         Agent Platform
```

## Data flow

```text
External Source
 ↓ Source Registry
 ↓ Acquisition Connector
 ↓ Raw Artifact + Content Hash
 ↓ Normalization / Deduplication
 ↓ Observation Extraction
 ↓ Validation
 ↓ Entity / Event / Relationship Resolution
 ↓ Temporal World State
 ↓ Change Detection
 ↓ Signal Evaluation
 ↓ Intelligence API
 ↓ Consumers
```

Intermediate representations are preserved rather than collapsing the pipeline into an opaque AI transformation.

## Temporal intelligence

World Intelligence is designed around temporal state, not only mutable current-state records.

Important timestamps include:

- `event_time`
- `valid_time`
- `observed_at`
- `ingested_at`
- future: `knowledge_as_of`

This supports current-state, historical-state, and knowledge-as-of queries.

## Provenance

Important intelligence objects should be traceable toward their source material:

```text
INTELLIGENCE
 ↓ SIGNAL
 ↓ CHANGE
 ↓ WORLD-STATE ASSERTION
 ↓ OBSERVATION
 ↓ RAW ARTIFACT
 ↓ SOURCE
```

Provenance records should include source attribution, artifact identity, content hashes, transformation lineage, extractor/model versions, rule versions, and evidence references.

AI-generated output is never evidence merely because an AI system produced it.

## Source, freshness, and coverage

The platform explicitly distinguishes:

```text
No observation ≠ Negative assertion
No observation ≠ No event
No observation ≠ Source failure
No observation ≠ Source outage
No observation ≠ Parser failure
No observation ≠ Stale data
```

Source health and coverage are first-class intelligence metadata.

## Change and signals

Changes are first-class objects with before/after state, effective and detection times, significance, confidence, supporting evidence, contradictions, and provenance.

Signals operate downstream of structured world state. They should be versioned, explainable, reproducible, testable, and backtestable.

## AI boundary

External content is untrusted data.

```text
UNTRUSTED CONTENT
 ↓ ACQUISITION ISOLATION
 ↓ RAW ARTIFACT
 ↓ PARSER / EXTRACTOR
 ↓ CANDIDATE OBSERVATION
 ↓ VALIDATION
 ↓ RESOLUTION
 ↓ WORLD STATE
```

AI may assist extraction, classification, correlation, and synthesis. It does not become the authoritative source of world state.

## Repository structure

```text
tinlance-world-intelligence/
├── apps/world-monitor/
├── packages/
│   ├── contracts/
│   ├── ontology/
│   ├── provenance/
│   ├── temporal/
│   ├── geospatial/
│   ├── entity-resolution/
│   ├── event-intelligence/
│   ├── relationship-intelligence/
│   ├── change-engine/
│   ├── signal-engine/
│   ├── coverage/
│   └── intelligence/
├── services/
│   ├── acquisition/
│   ├── artifact-ingestion/
│   ├── observation-pipeline/
│   ├── entity-pipeline/
│   ├── event-pipeline/
│   ├── relationship-pipeline/
│   ├── change-pipeline/
│   ├── signal-pipeline/
│   └── replay/
├── api/
├── integrations/
├── db/
│   ├── migrations/
│   ├── seeds/
│   ├── functions/
│   └── views/
├── schemas/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── contract/
│   ├── end-to-end/
│   ├── adversarial/
│   ├── data-quality/
│   └── golden/
├── docs/
├── config/
├── scripts/
└── .github/workflows/
```

## Development setup

Prerequisites: Git, GitHub CLI, Python 3.12+, Node.js 24+, PostgreSQL + PostGIS, and Docker.

```bash
git clone https://github.com/LloydCoder/tinlance-world-intelligence.git
cd tinlance-world-intelligence
```

Never commit credentials. Local configuration belongs in `.env`, based on `.env.example` when present.

The initial repository gate is:

```bash
python -m compileall packages services api tests
python -m unittest discover -s tests -v
```

## Implementation principles

1. **Evidence before intelligence.**
2. **Provenance is first-class.**
3. **Temporal state over destructive mutation.**
4. **Unknown is valid.**
5. **Absence is not automatically negative evidence.**
6. **AI is not authority.**
7. **External content is untrusted.**
8. **Contradictions are preserved.**
9. **Source independence matters.**
10. **Freshness matters.**
11. **Coverage matters.**
12. **Replay matters.**
13. **Contracts before coupling.**
14. **Security boundaries are architectural boundaries.**
15. **Prefer simple infrastructure until measured workload requires more.**
16. **Build vertical slices.**

## Integration boundaries

- **ReconOS:** acquisition/recon capabilities and stable ingestion contracts.
- **TADS:** consumes world intelligence for target, account, and demand intelligence.
- **Agent OS:** consumes controlled intelligence capabilities.
- **Agent Platform:** owns policy, authorization, approvals, execution, and runtime governance.

World Intelligence provides information; it does not become execution authority.

## Non-goals

This repository is not a generic chatbot, CRM, autonomous decision authority, unrestricted surveillance system, replacement for ReconOS/TADS/Agent Platform, AI truth engine, or dashboard-centric architecture.

## Development strategy

Implementation proceeds through vertical slices:

```text
Source → Artifact → Observation → World State → Change
→ API → World Monitor → Tests
```

Each completed slice should be observable, testable, documented, provenance-aware, secure, and reproducible.

## Security

Security concerns include untrusted-source isolation, SSRF, prompt injection, malicious documents and feeds, secret handling, authorization, provenance integrity, dependency/supply-chain security, API abuse, auditability, privacy, and retention.

See [SECURITY.md](SECURITY.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Apache-2.0. See [LICENSE](LICENSE).

## CI verification

The repository foundation is continuously checked by GitHub Actions.

## Status

The repository is under active development. Architecture will evolve through implementation evidence, adversarial testing, operational measurements, and real workload requirements.

The objective is a **traceable, temporal, geospatial, evidence-backed representation of changing real-world state** that can safely serve humans, applications, analytical systems, and governed agents.


## Historical foundation (Phases 0–1)

Phase 0 and Phase 1 are implemented in the current repository boundary:

- versioned Python contracts for sources, acquisition, artifacts, and source health;
- universal ontology enums for entities, events, relationships, and intelligence objects;
- SHA-256 content identity and a reference artifact ledger with deduplication semantics;
- source registry with canonical-URI uniqueness;
- source-health state tracking with explicit degradation/unavailability transitions;
- acquisition interface plus deterministic URL preflight security checks;
- PostgreSQL + PostGIS schema for source registry, artifact ledger, retrieval references,
  source health, and schema metadata;
- JSON Schemas for source and raw-artifact contracts;
- repository security baseline and database-backed CI verification;
- CI action references pinned to immutable commit SHAs.

### Phase 0-1 invariants

The raw artifact is the exact acquired byte sequence. Hashing occurs before parsing or
normalization. Deduplication is global by content hash, while every source retrieval is
retained separately for provenance. A not-modified retrieval does not create a new artifact.

The acquisition security helper is a preflight layer, not the complete SSRF boundary.
Concrete network adapters must perform connection-time DNS/IP validation, redirect
revalidation, credential isolation, resource limits, and parser isolation.

See:
- docs/architecture/phase-0-1.md
- docs/operations/phase-0-1-verification.md
- docs/security/acquisition-boundary.md
- db/README.md


## Implemented enterprise sequence

Phases 0–27 are implemented as a serial, CI-gated progression:

0. Foundation — contracts, ontology, CI, database, security.
1. Source & Artifact — source registry, acquisition boundary, immutable SHA-256 artifact ledger, deduplication, source health.
2. Observation — extraction contracts, normalization, validation, provenance.
3. Entity Intelligence — identifiers, aliases, conservative resolution, merge/split history.
4. Event Intelligence — event ontology, lifecycle, temporal correlation, provenance.
5. Temporal World State — valid time, observation time, knowledge-as-of, snapshots.
6. Geospatial Intelligence — PostGIS geometry, indexes, geofences, spatial-temporal contracts.
7. Relationship Intelligence — temporal relationships and bounded traversal.
8. Change Engine — before/after state, significance, source-vs-world-change distinction.
9. Correlation & Contradiction — source dependence, contradiction records, corroboration.
10. Signal Engine — versioned deterministic rules and explanations.
11. Intelligence API — query/routing/OpenAPI contracts.
12. World Monitor — first-party visual investigation surface.
13. Replay & Backtesting — deterministic replay and regression metrics.
14. Advanced Intelligence — independence graph, anomaly candidates, intelligence cards.
15. Tinlance Ecosystem — bounded ReconOS/TADS/Agent OS/Agent Platform contracts.
16. Production Runtime — runnable HTTP service, health/readiness, authentication, request IDs.
17. Acquisition & Ingestion — bounded queues, retries, conditional retrieval, artifact handoff.
18. Evidence & Data Quality — evidence objects, fingerprints, deterministic quality validation.
19. Entity & Knowledge Graph — bounded traversal and conservative resolution governance.
20. Temporal & Geospatial Runtime — executable time/knowledge/spatial query semantics.
21. Fusion & Advanced Signals — contradiction-aware fusion and expanded signal DSL.
22. Intelligence API & Developer Platform — signed cursors, subscriptions, expanded read-only SDK.
23. Security, Privacy & Governance — SSRF-aware target policy, authorization, redaction, audit.
24. Reliability & Distributed Systems — idempotency, leases, circuit breakers, durable job schema.
25. Observability & Operations — telemetry vocabulary, SLOs, error budgets, operational events.
26. World Monitor Enterprise — investigation UX, safe DOM rendering, browser security policy.
27. Enterprise Validation & Scale — final repository validation gate and standards-aligned audit.
