BEGIN;
CREATE TABLE world_intelligence.provenance_records (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_ref text NOT NULL,
    activity_type text NOT NULL,
    agent_ref text,
    derivation_of text,
    attributed_to text,
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX provenance_entity_time_idx ON world_intelligence.provenance_records(entity_ref,created_at DESC);
CREATE INDEX provenance_activity_time_idx ON world_intelligence.provenance_records(activity_type,created_at DESC);

ALTER TABLE world_intelligence.observations
    ADD CONSTRAINT observations_provenance_fk
    FOREIGN KEY (provenance_id) REFERENCES world_intelligence.provenance_records(id) ON DELETE RESTRICT;
ALTER TABLE world_intelligence.events
    ADD CONSTRAINT events_provenance_fk
    FOREIGN KEY (provenance_id) REFERENCES world_intelligence.provenance_records(id) ON DELETE RESTRICT;
ALTER TABLE world_intelligence.temporal_assertions
    ADD CONSTRAINT temporal_assertions_provenance_fk
    FOREIGN KEY (provenance_id) REFERENCES world_intelligence.provenance_records(id) ON DELETE RESTRICT;
ALTER TABLE world_intelligence.relationships
    ADD CONSTRAINT relationships_provenance_fk
    FOREIGN KEY (provenance_id) REFERENCES world_intelligence.provenance_records(id) ON DELETE RESTRICT;
ALTER TABLE world_intelligence.evidence
    ADD CONSTRAINT evidence_provenance_fk
    FOREIGN KEY (provenance_id) REFERENCES world_intelligence.provenance_records(id) ON DELETE RESTRICT;
COMMIT;
