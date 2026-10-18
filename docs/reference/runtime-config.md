# Runtime configuration reference

Configuration is defined in `runtime/config.py`.

| Variable | Default | Validation / behavior |
| --- | --- | --- |
| `WORLD_INTELLIGENCE_ENV` | `development` | production/staging require PostgreSQL persistence |
| `WORLD_INTELLIGENCE_HOST` | `127.0.0.1` | Bind address |
| `WORLD_INTELLIGENCE_PORT` | `8080` | 1–65535 |
| `WORLD_INTELLIGENCE_MAX_BODY_BYTES` | `1048576` | 1 KiB–100 MiB |
| `WORLD_INTELLIGENCE_BEARER_TOKEN` | unset | Required in production/staging when auth is enabled for query APIs |
| `WORLD_INTELLIGENCE_SOURCE_EVIDENCE_TOKEN` | unset | Dedicated credential for `POST /v1/source-evidence`; mandatory in production/staging and never falls back to the query API token |
| `WORLD_INTELLIGENCE_REQUIRE_AUTH` | `true` | Bearer authentication control |
| `WORLD_INTELLIGENCE_STORAGE_MODE` | `memory` | `memory` or `postgres` |
| `DATABASE_URL` | unset | Required for PostgreSQL storage |
| `WORLD_INTELLIGENCE_RATE_LIMIT_PER_MINUTE` | `120` | Must be positive |

Production/staging configuration fails closed unless storage mode is PostgreSQL, `DATABASE_URL` is present, and both query API authentication and the dedicated source-evidence service credential are configured. Source-evidence intake always requires its dedicated credential, even when query API authentication is disabled in a development environment.
