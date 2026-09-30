BEGIN;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE SCHEMA IF NOT EXISTS world_intelligence;

CREATE TABLE world_intelligence.sources (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name text NOT NULL CHECK (btrim(name) <> ''),
    canonical_uri text NOT NULL UNIQUE CHECK (canonical_uri ~ '^https?://'),
    source_type text NOT NULL CHECK (btrim(source_type) <> ''),
    enabled boolean NOT NULL DEFAULT true,
    expected_interval_seconds integer CHECK (expected_interval_seconds IS NULL OR expected_interval_seconds > 0),
    license_reference text,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE world_intelligence.raw_artifacts (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    content_sha256 char(64) NOT NULL UNIQUE CHECK (content_sha256 ~ '^[0-9a-f]{64}$'),
    size_bytes bigint NOT NULL CHECK (size_bytes >= 0),
    media_type text,
    content_encoding text,
    storage_uri text NOT NULL CHECK (btrim(storage_uri) <> ''),
    retrieved_at timestamptz NOT NULL,
    etag text,
    last_modified text,
    acquisition_version text NOT NULL DEFAULT '1',
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE world_intelligence.artifact_references (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id uuid NOT NULL REFERENCES world_intelligence.sources(id) ON DELETE RESTRICT,
    artifact_id uuid REFERENCES world_intelligence.raw_artifacts(id) ON DELETE RESTRICT,
    observed_at timestamptz NOT NULL,
    status text NOT NULL CHECK (status IN ('stored','not_modified','rejected')),
    http_status integer CHECK (http_status IS NULL OR http_status BETWEEN 100 AND 599),
    final_uri text NOT NULL CHECK (final_uri ~ '^https?://'),
    etag text,
    last_modified text,
    error_code text,
    created_at timestamptz NOT NULL DEFAULT now(),
    CHECK ((status = 'stored' AND artifact_id IS NOT NULL) OR (status <> 'stored'))
);

CREATE INDEX artifact_references_source_time_idx
 ON world_intelligence.artifact_references(source_id,observed_at DESC);
CREATE INDEX artifact_references_artifact_idx
 ON world_intelligence.artifact_references(artifact_id);

CREATE TABLE world_intelligence.source_health (
    source_id uuid PRIMARY KEY REFERENCES world_intelligence.sources(id) ON DELETE CASCADE,
    status text NOT NULL CHECK (status IN ('unknown','healthy','degraded','unavailable')),
    checked_at timestamptz NOT NULL,
    consecutive_failures integer NOT NULL DEFAULT 0 CHECK (consecutive_failures >= 0),
    latency_ms integer CHECK (latency_ms IS NULL OR latency_ms >= 0),
    last_success_at timestamptz,
    last_failure_at timestamptz,
    last_error_code text,
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE world_intelligence.schema_metadata (
    key text PRIMARY KEY,
    value text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);

INSERT INTO world_intelligence.schema_metadata(key,value) VALUES
 ('schema_version','1'),('contract_version','1'),('artifact_hash_algorithm','sha256')
ON CONFLICT(key) DO UPDATE SET value=EXCLUDED.value;
COMMIT;
