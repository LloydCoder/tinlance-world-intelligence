BEGIN;
CREATE TABLE world_intelligence.temporal_assertions(id uuid PRIMARY KEY DEFAULT gen_random_uuid(),subject_ref text NOT NULL,predicate text NOT NULL,object_value jsonb NOT NULL,valid_from timestamptz NOT NULL,valid_to timestamptz,observed_at timestamptz NOT NULL,known_at timestamptz NOT NULL,status text NOT NULL CHECK(status IN('asserted','retracted')),provenance_id uuid,created_at timestamptz NOT NULL DEFAULT now(),CHECK(valid_to IS NULL OR valid_to>valid_from));
CREATE TABLE world_intelligence.world_snapshots(id uuid PRIMARY KEY DEFAULT gen_random_uuid(),generated_at timestamptz NOT NULL,world_cutoff timestamptz NOT NULL,knowledge_cutoff timestamptz NOT NULL,ontology_version text NOT NULL,pipeline_version text NOT NULL);
CREATE INDEX temporal_assertion_subject_valid_idx ON world_intelligence.temporal_assertions(subject_ref,valid_from,valid_to);
CREATE INDEX temporal_assertion_known_idx ON world_intelligence.temporal_assertions(known_at);
COMMIT;