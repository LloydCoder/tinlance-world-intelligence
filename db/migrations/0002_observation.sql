BEGIN;
CREATE TABLE world_intelligence.observations (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), artifact_id uuid NOT NULL REFERENCES world_intelligence.raw_artifacts(id) ON DELETE RESTRICT,
 source_id uuid NOT NULL REFERENCES world_intelligence.sources(id) ON DELETE RESTRICT, subject_ref text NOT NULL CHECK(btrim(subject_ref)<>''), predicate text NOT NULL CHECK(btrim(predicate)<>''),
 object_value jsonb NOT NULL, observed_at timestamptz NOT NULL, extracted_at timestamptz NOT NULL, valid_from timestamptz, valid_to timestamptz, location jsonb,
 extraction_method text NOT NULL, extraction_version text NOT NULL, status text NOT NULL CHECK(status IN('candidate','validated','rejected')), provenance_id uuid,
 created_at timestamptz NOT NULL DEFAULT now(), CHECK(valid_from IS NULL OR valid_to IS NULL OR valid_from<=valid_to)
);
CREATE INDEX observations_subject_time_idx ON world_intelligence.observations(subject_ref,observed_at DESC);
CREATE INDEX observations_source_time_idx ON world_intelligence.observations(source_id,observed_at DESC);
CREATE INDEX observations_artifact_idx ON world_intelligence.observations(artifact_id);
COMMIT;
