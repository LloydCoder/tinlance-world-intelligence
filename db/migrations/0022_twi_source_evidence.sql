BEGIN;

CREATE TABLE world_intelligence.external_source_evidence (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    source_system text NOT NULL CHECK (source_system = 'tinlance-web-intelligence'),
    tenant_ref char(64) NOT NULL CHECK (tenant_ref ~ '^[0-9a-f]{64}$'),
    source_job_id varchar(64) NOT NULL CHECK (btrim(source_job_id) <> ''),
    claim_id varchar(64) NOT NULL CHECK (claim_id ~ '^[A-Za-z0-9._:-]{1,64}$'),
    statement varchar(500) NOT NULL CHECK (btrim(statement) <> ''),
    source_url varchar(4096) NOT NULL CHECK (source_url ~ '^https?://[^[:space:]]+
    media_type varchar(128) NOT NULL CHECK (btrim(media_type) <> ''),
    artifact_sha256 char(64) NOT NULL CHECK (artifact_sha256 ~ '^[0-9a-f]{64}$'),
    quote varchar(350) NOT NULL CHECK (char_length(btrim(quote)) >= 8),
    quote_sha256 char(64) NOT NULL CHECK (quote_sha256 ~ '^[0-9a-f]{64}$'),
    verifier_version varchar(64) NOT NULL
        CHECK (verifier_version ~ '^twi-citation-verifier/[0-9]+\.[0-9]+\.[0-9]+$'),
    report_sha256 char(64) NOT NULL CHECK (report_sha256 ~ '^[0-9a-f]{64}$'),
    idempotency_key varchar(128) NOT NULL CHECK (idempotency_key ~ '^[A-Za-z0-9._:-]{16,128}$'),
    payload_sha256 char(64) NOT NULL CHECK (payload_sha256 ~ '^[0-9a-f]{64}$'),
    request_id varchar(128) NOT NULL CHECK (btrim(request_id) <> ''),
    traceparent char(55)
        CHECK (traceparent IS NULL OR traceparent ~ '^[0-9a-f]{2}-[0-9a-f]{32}-[0-9a-f]{16}-[0-9a-f]{2}$'),
    status text NOT NULL DEFAULT 'candidate'
        CHECK (status IN ('candidate','accepted','rejected')),
    received_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (tenant_ref, idempotency_key)
);

CREATE INDEX external_source_evidence_tenant_received_idx
    ON world_intelligence.external_source_evidence (tenant_ref, received_at DESC);
CREATE INDEX external_source_evidence_source_time_idx
    ON world_intelligence.external_source_evidence (source_url, retrieved_at DESC);
CREATE INDEX external_source_evidence_candidate_idx
    ON world_intelligence.external_source_evidence (status, received_at)
    WHERE status = 'candidate';

COMMIT;
),
    source_url_redacted boolean NOT NULL DEFAULT false,
    retrieved_at timestamptz NOT NULL,
    media_type varchar(128) NOT NULL CHECK (btrim(media_type) <> ''),
    artifact_sha256 char(64) NOT NULL CHECK (artifact_sha256 ~ '^[0-9a-f]{64}$'),
    quote varchar(350) NOT NULL CHECK (char_length(btrim(quote)) >= 8),
    quote_sha256 char(64) NOT NULL CHECK (quote_sha256 ~ '^[0-9a-f]{64}$'),
    verifier_version varchar(64) NOT NULL
        CHECK (verifier_version ~ '^twi-citation-verifier/[0-9]+\.[0-9]+\.[0-9]+$'),
    report_sha256 char(64) NOT NULL CHECK (report_sha256 ~ '^[0-9a-f]{64}$'),
    idempotency_key varchar(128) NOT NULL CHECK (idempotency_key ~ '^[A-Za-z0-9._:-]{16,128}$'),
    payload_sha256 char(64) NOT NULL CHECK (payload_sha256 ~ '^[0-9a-f]{64}$'),
    request_id varchar(128) NOT NULL CHECK (btrim(request_id) <> ''),
    traceparent char(55)
        CHECK (traceparent IS NULL OR traceparent ~ '^[0-9a-f]{2}-[0-9a-f]{32}-[0-9a-f]{16}-[0-9a-f]{2}$'),
    status text NOT NULL DEFAULT 'candidate'
        CHECK (status IN ('candidate','accepted','rejected')),
    received_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (tenant_ref, idempotency_key)
);

CREATE INDEX external_source_evidence_tenant_received_idx
    ON world_intelligence.external_source_evidence (tenant_ref, received_at DESC);
CREATE INDEX external_source_evidence_source_time_idx
    ON world_intelligence.external_source_evidence (source_url, retrieved_at DESC);
CREATE INDEX external_source_evidence_candidate_idx
    ON world_intelligence.external_source_evidence (status, received_at)
    WHERE status = 'candidate';

COMMIT;
