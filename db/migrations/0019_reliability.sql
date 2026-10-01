BEGIN;
CREATE TABLE world_intelligence.ingestion_jobs (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    idempotency_key char(64) NOT NULL UNIQUE CHECK (idempotency_key ~ '^[0-9a-f]{64}$'),
    source_id uuid NOT NULL REFERENCES world_intelligence.sources(id) ON DELETE RESTRICT,
    payload jsonb NOT NULL,
    status text NOT NULL CHECK (status IN ('queued','leased','succeeded','failed','dead_letter')),
    attempts integer NOT NULL DEFAULT 0 CHECK (attempts >= 0),
    available_at timestamptz NOT NULL DEFAULT now(),
    lease_owner text,
    lease_expires_at timestamptz,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    CHECK ((status='leased' AND lease_owner IS NOT NULL AND lease_expires_at IS NOT NULL) OR status<>'leased')
);
CREATE INDEX ingestion_jobs_ready_idx ON world_intelligence.ingestion_jobs(status,available_at);
CREATE INDEX ingestion_jobs_lease_idx ON world_intelligence.ingestion_jobs(lease_expires_at) WHERE status='leased';

CREATE TABLE world_intelligence.ingestion_job_attempts (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id uuid NOT NULL REFERENCES world_intelligence.ingestion_jobs(id) ON DELETE CASCADE,
    attempt integer NOT NULL CHECK (attempt >= 1),
    worker_id text NOT NULL,
    started_at timestamptz NOT NULL,
    finished_at timestamptz,
    outcome text NOT NULL CHECK (outcome IN ('success','retryable_failure','permanent_failure')),
    error_code text
);
CREATE UNIQUE INDEX ingestion_job_attempt_unique ON world_intelligence.ingestion_job_attempts(job_id,attempt);
COMMIT;
