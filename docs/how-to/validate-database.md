# How to validate the database

CI validates PostgreSQL 16 with PostGIS 3.5 and applies migrations `0001` through `0021`.

## Local validation

Use an isolated disposable database:

```bash
export PGPASSWORD=postgres
for migration in db/migrations/*.sql; do
  psql -h 127.0.0.1 -U postgres -d world_intelligence -v ON_ERROR_STOP=1 -f "$migration"
done
```

Verify PostGIS:

```bash
psql -h 127.0.0.1 -U postgres -d world_intelligence \
  -Atc "SELECT extname FROM pg_extension WHERE extname='postgis';"
```

Verify the schema baseline:

```bash
psql -h 127.0.0.1 -U postgres -d world_intelligence \
  -Atc "SELECT count(*) FROM information_schema.tables WHERE table_schema='world_intelligence';"
```

The current CI gate expects 44 tables.

> [!WARNING]
> Never point migration tests at production.
