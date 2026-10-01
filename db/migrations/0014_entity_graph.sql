BEGIN;
CREATE TABLE world_intelligence.entity_resolution_candidates (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    left_entity_id uuid NOT NULL REFERENCES world_intelligence.entities(id) ON DELETE RESTRICT,
    right_entity_id uuid NOT NULL REFERENCES world_intelligence.entities(id) ON DELETE RESTRICT,
    score numeric(5,4) NOT NULL CHECK (score BETWEEN 0 AND 1),
    decision text NOT NULL CHECK (decision IN ('auto_accept','review','reject')),
    reasons jsonb NOT NULL DEFAULT '[]'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    CHECK (left_entity_id <> right_entity_id)
);
CREATE INDEX entity_resolution_candidates_left_idx ON world_intelligence.entity_resolution_candidates(left_entity_id,created_at DESC);
CREATE INDEX entity_resolution_candidates_right_idx ON world_intelligence.entity_resolution_candidates(right_entity_id,created_at DESC);
CREATE INDEX entity_resolution_candidates_review_idx ON world_intelligence.entity_resolution_candidates(decision) WHERE decision='review';
COMMIT;
