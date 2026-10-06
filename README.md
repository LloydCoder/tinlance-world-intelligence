# Tinlance World Intelligence

> Provenance-first temporal intelligence infrastructure for engineering teams that need traceable entities, events, world state, change, signals, and intelligence.

[![CI](https://github.com/LloydCoder/tinlance-world-intelligence/actions/workflows/ci.yml/badge.svg)](https://github.com/LloydCoder/tinlance-world-intelligence/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/LloydCoder/tinlance-world-intelligence)](LICENSE)
[![Python](https://img.shields.io/badge/Python-%3E%3D3.12-blue)](pyproject.toml)
[![Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)

## Visual proof

The repository currently ships a first-party World Monitor surface, but no public deployment or committed screenshot/GIF is claimed as a live demo. The architecture below is rendered directly by GitHub and shows the executable semantic boundary:

```mermaid
flowchart LR
  S[External Sources] --> A[Acquisition]
  A --> R[Raw Artifact Ledger]
  R --> O[Observations]
  O --> E[Entity / Event / Relationship]
  E --> W[Temporal World State]
  W --> C[Change]
  C --> G[Correlation / Contradiction / Coverage]
  G --> Q[Signals]
  Q --> I[Intelligence API]
  I --> M[World Monitor]
  I --> T[TADS]
  I --> OS[Agent OS]
  OS --> AP[Agent Platform]
```

> [!NOTE]
> A real screenshot or short demo GIF should be added when a maintained deployment is available. The project does not use a fabricated “live demo” claim.

## Why this project

World Intelligence separates **what was observed** from **what was inferred** and preserves the path back to source material. That makes it suitable as a shared intelligence layer rather than a dashboard-specific data store.

| Problem | World Intelligence approach |
| --- | --- |
| Mutable “current state” loses history | Temporal state with observation, valid, event, and ingestion times |
| AI output becomes indistinguishable from evidence | Explicit observation, evidence, finding, signal, and intelligence boundaries |
| Conflicting sources disappear during normalization | Contradictions and source dependence remain representable |
| Source outages look like negative facts | Source health and coverage are first-class metadata |
| External content can contain hostile instructions | Acquisition and parsing are treated as untrusted-data boundaries |
| Consumers need different interfaces | Read/query APIs and bounded integration contracts |
| Reprocessing changes historical results | Immutable artifacts, hashes, provenance, and deterministic replay |

The first application built on the fabric is **Tinlance World Monitor**. World Monitor consumes the fabric; it does not define its semantics.

## Quick Start

For the repository gate, no database or third-party Python package is required.

```bash
git clone https://github.com/LloydCoder/tinlance-world-intelligence.git
cd tinlance-world-intelligence
python -m unittest discover -s tests -v
```

The same checks are available through:

```bash
make check
make test
```

> [!TIP]
> Use Python 3.12 or newer. The CI gate currently validates Python 3.12.

## Installation

### Prerequisites

- Git
- Python 3.12+
- PostgreSQL 16 + PostGIS 3.5 when using persistent storage
- Optional: GitHub CLI for repository workflows

The project is currently operated from the source tree. The `pyproject.toml` also declares the optional PostgreSQL runtime dependency.

### Optional PostgreSQL runtime dependency

```bash
python -m pip install "tinlance-world-intelligence[runtime]"
```

Equivalent direct dependency:

```bash
python -m pip install "psycopg[binary,pool]==3.3.6"
```

### Database validation

CI uses a PostGIS 16/3.5 service and applies migrations `0001` through `0021`. See [db/README.md](db/README.md) and [phase verification](docs/operations/phase-0-1-verification.md).

## Usage

### Run the bounded HTTP runtime

The runtime reads configuration from environment variables.

```bash
export WORLD_INTELLIGENCE_ENV=development
export WORLD_INTELLIGENCE_STORAGE_MODE=memory
export WORLD_INTELLIGENCE_REQUIRE_AUTH=true
export WORLD_INTELLIGENCE_BEARER_TOKEN=local-development-token
python -c "from runtime.server import serve; serve()"
```

Then, from another terminal:

```bash
curl http://127.0.0.1:8080/healthz
curl -H "Authorization: Bearer local-development-token" \
  "http://127.0.0.1:8080/v1/entities?limit=10&cursor=0"
```

Health and readiness endpoints are public; intelligence endpoints require authentication when `WORLD_INTELLIGENCE_REQUIRE_AUTH=true`.

### PostgreSQL-backed runtime

Production and staging configuration requires PostgreSQL persistence and authentication:

```bash
export WORLD_INTELLIGENCE_ENV=production
export WORLD_INTELLIGENCE_STORAGE_MODE=postgres
export WORLD_INTELLIGENCE_REQUIRE_AUTH=true
export WORLD_INTELLIGENCE_BEARER_TOKEN="$WORLD_INTELLIGENCE_BEARER_TOKEN"
export DATABASE_URL="postgresql://USER:PASSWORD@HOST:5432/world_intelligence"
python -c "from runtime.server import serve; serve()"
```

> [!WARNING]
> Do not put production credentials in shell history, source files, issues, logs, fixtures, or committed `.env` files. Use the deployment platform's secret store.

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `WORLD_INTELLIGENCE_ENV` | `development` | Runtime environment; production/staging enforce persistence requirements |
| `WORLD_INTELLIGENCE_HOST` | `127.0.0.1` | HTTP bind address |
| `WORLD_INTELLIGENCE_PORT` | `8080` | HTTP port |
| `WORLD_INTELLIGENCE_STORAGE_MODE` | `memory` | `memory` or `postgres` |
| `DATABASE_URL` | unset | PostgreSQL connection string when persistent storage is enabled |
| `WORLD_INTELLIGENCE_REQUIRE_AUTH` | `true` | Require bearer authentication for intelligence endpoints |
| `WORLD_INTELLIGENCE_BEARER_TOKEN` | unset | Bearer token used by the bounded runtime |
| `WORLD_INTELLIGENCE_RATE_LIMIT_PER_MINUTE` | `120` | Fixed-window request limit |
| `WORLD_INTELLIGENCE_MAX_BODY_BYTES` | `1048576` | Maximum accepted request body size |

See [.env.example](.env.example) for the development configuration surface.

## Features

| Capability | Status | Primary location |
| --- | --- | --- |
| Source registry and source health | Implemented | `services/source_registry/` |
| Immutable artifact identity and deduplication | Implemented | `services/artifact_ingestion/`, `packages/provenance/` |
| Observation contracts and validation | Implemented | `packages/contracts/`, `services/observation_pipeline/` |
| Entity, event, and relationship intelligence | Implemented | `services/entity_pipeline/`, `services/event_pipeline/`, `services/relationship_pipeline/` |
| Temporal and geospatial queries | Implemented | `services/temporal/`, `services/temporal_geospatial/` |
| Change, contradiction, correlation, and signals | Implemented | `services/change_engine/`, `services/correlation/`, `services/signal_engine/` |
| Replay and backtesting | Implemented | `services/replay/` |
| Read/query API | Implemented | `api/`, `schemas/api/openapi.yaml` |
| Bounded HTTP runtime | Implemented | `runtime/` |
| World Monitor application surface | Implemented | `apps/world-monitor/` |
| Security, governance, reliability, and observability contracts | Implemented | `services/security/`, `services/reliability/`, `services/observability/` |

“Implemented” describes repository functionality covered by the current code and CI gates; it does not imply a public production deployment or a guarantee of operational performance.

## Documentation

The documentation is organized around the Diátaxis model:

- **Tutorials:** [docs/tutorials/](docs/tutorials/)
- **How-to guides:** [docs/how-to/](docs/how-to/)
- **Explanation:** [docs/explanation/](docs/explanation/)
- **Reference:** [docs/reference/](docs/reference/)
- **Architecture phases:** [docs/architecture/](docs/architecture/)
- **API contract:** [schemas/api/openapi.yaml](schemas/api/openapi.yaml)
- **Database:** [db/README.md](db/README.md)
- **Security boundary:** [docs/security/acquisition-boundary.md](docs/security/acquisition-boundary.md)
- **Contributing:** [CONTRIBUTING.md](CONTRIBUTING.md)
- **Security policy:** [SECURITY.md](SECURITY.md)
- **Changelog:** [CHANGELOG.md](CHANGELOG.md)

## Semantic boundaries

The project deliberately preserves these distinctions:

- Observation ≠ Evidence
- Evidence ≠ Finding
- Finding ≠ Intelligence
- Intelligence ≠ Authority
- Freshness ≠ Truth
- Absence ≠ Negative Evidence
- Correlation ≠ Causation
- Multiple Sources ≠ Independent Corroboration
- AI Output ≠ Ground Truth

External content is untrusted data. AI may assist extraction, classification, correlation, and synthesis, but it does not become the authoritative source of world state.

## Ecosystem boundaries

| System | Responsibility |
| --- | --- |
| World Intelligence | World-state semantics, provenance, temporal modeling, entities/events/relationships, changes, signals, intelligence APIs |
| ReconOS | Governed acquisition and reconnaissance capabilities |
| TADS | Target and demand intelligence |
| Agent OS | Controlled intelligence consumption and agent workspace/lifecycle |
| Agent Platform | Policy, authorization, approvals, execution, runtime governance |

World Intelligence provides information; it does not become execution authority.

## Contributing

Start with [CONTRIBUTING.md](CONTRIBUTING.md). Changes should preserve provenance, temporal semantics, explicit uncertainty, security boundaries, and versioned contracts.

## License and acknowledgements

Licensed under the [Apache License 2.0](LICENSE).

Tinlance World Intelligence is maintained by Tinlance Limited. The architecture is intentionally compatible with the broader Tinlance ecosystem while keeping execution authority outside this repository.

## Status

The repository has completed its documented Phase 0–27 implementation sequence and has a CI-backed enterprise validation gate. Operational deployment, external-source coverage, and production workload validation remain evidence-driven activities.

> [!NOTE]
> The repository is young and currently has no published releases. Treat `main` as the development baseline until a signed release process is established.

<details>
<summary>Troubleshooting</summary>

### Tests fail locally

Confirm Python 3.12+:

```bash
python --version
```

Then run the same commands used by CI:

```bash
python -m compileall packages services api tests
python -m unittest discover -s tests -v
python scripts/enterprise_audit.py
python scripts/security_baseline.py
```

### PostgreSQL checks fail

Use PostgreSQL 16 with PostGIS 3.5 and apply migrations in numeric order. CI is the canonical database validation environment.

</details>

<details>
<summary>Support</summary>

See [SUPPORT.md](SUPPORT.md) for questions, documentation requests, and issue-routing guidance. Security vulnerabilities belong in [SECURITY.md](SECURITY.md), not public issues.

</details>
