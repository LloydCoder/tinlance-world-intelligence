BEGIN;
CREATE TABLE world_intelligence.evidence (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    observation_id uuid NOT NULL REFERENCES world_intelligence.observations(id) ON DELETE RESTRICT,
    artifact_id uuid NOT NULL REFERENCES world_intelligence.raw_artifacts(id) ON DELETE RESTRICT,
    source_id uuid NOT NULL REFERENCES world_intelligence.sources(id) ON DELETE RESTRICT,
    assertion_fingerprint char(64) NOT NULL CHECK (assertion_fingerprint ~ '^[0-9a-f]{64}$'),
    status text NOT NULL CHECK (status IN ('candidate','validated','rejected')),
    quality_score numeric(5,4) NOT NULL CHECK (quality_score BETWEEN 0 AND 1),
    observed_at timestamptz NOT NULL,
    provenance_id uuid,
    created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX evidence_observation_idx ON world_intelligence.evidence(observation_id);
CREATE INDEX evidence_source_time_idx ON world_intelligence.evidence(source_id,observed_at DESC);

CREATE TABLE world_intelligence.data_quality_reports (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    evidence_id uuid NOT NULL REFERENCES world_intelligence.evidence(id) ON DELETE CASCADE,
    valid boolean NOT NULL,
    score numeric(5,4) NOT NULL CHECK (score BETWEEN 0 AND 1),
    issue_count integer NOT NULL CHECK (issue_count >= 0),
    checked_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX data_quality_reports_evidence_idx ON world_intelligence.data_quality_reports(evidence_id);
COMMIT;
