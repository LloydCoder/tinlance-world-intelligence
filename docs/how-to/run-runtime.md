# How to run the runtime

The HTTP runtime is implemented in `runtime/`.

## Development mode

```bash
export WORLD_INTELLIGENCE_ENV=development
export WORLD_INTELLIGENCE_STORAGE_MODE=memory
export WORLD_INTELLIGENCE_REQUIRE_AUTH=true
export WORLD_INTELLIGENCE_BEARER_TOKEN=local-development-token
python -c "from runtime.server import serve; serve()"
```

| Method | Path | Authentication |
| --- | --- | --- |
| GET | `/healthz` | Public |
| GET | `/readyz` | Public |
| GET | `/v1/entities` | Bearer token when enabled |
| GET | `/v1/events` | Bearer token when enabled |
| GET | `/v1/world-state` | Bearer token when enabled |
| GET | `/v1/changes` | Bearer token when enabled |
| GET | `/v1/signals` | Bearer token when enabled |
| GET | `/v1/evidence` | Bearer token when enabled |
| GET | `/v1/provenance` | Bearer token when enabled |

Pagination uses integer `cursor` and `limit`; valid limits are 1–1000.

## PostgreSQL mode

Install the optional dependency:

```bash
python -m pip install "tinlance-world-intelligence[runtime]"
```

Then configure:

```bash
export WORLD_INTELLIGENCE_ENV=production
export WORLD_INTELLIGENCE_STORAGE_MODE=postgres
export WORLD_INTELLIGENCE_REQUIRE_AUTH=true
export WORLD_INTELLIGENCE_BEARER_TOKEN="$WORLD_INTELLIGENCE_BEARER_TOKEN"
export DATABASE_URL="postgresql://USER:PASSWORD@HOST:5432/world_intelligence"
python -c "from runtime.server import serve; serve()"
```

Production and staging fail closed unless PostgreSQL persistence and authentication requirements are satisfied.
