BEGIN;
CREATE TABLE world_intelligence.fusion_assessments (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    subject_ref text NOT NULL,
    predicate text NOT NULL,
    support_score numeric(5,4) NOT NULL CHECK (support_score BETWEEN 0 AND 1),
    contradiction_score numeric(5,4) NOT NULL CHECK (contradiction_score BETWEEN 0 AND 1),
    independent_support_groups integer NOT NULL CHECK (independent_support_groups >= 0),
    supporting_evidence_ids uuid[] NOT NULL DEFAULT '{}',
    contradicting_evidence_ids uuid[] NOT NULL DEFAULT '{}',
    status text NOT NULL CHECK (status IN ('unknown','supported','mixed','contradicted')),
    generated_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX fusion_assessments_subject_idx ON world_intelligence.fusion_assessments(subject_ref,generated_at DESC);
CREATE INDEX fusion_assessments_status_idx ON world_intelligence.fusion_assessments(status,generated_at DESC);
COMMIT;
