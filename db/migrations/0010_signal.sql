BEGIN;
CREATE TABLE world_intelligence.signal_rules(id uuid PRIMARY KEY DEFAULT gen_random_uuid(),rule_id text NOT NULL,version text NOT NULL,name text NOT NULL,condition jsonb NOT NULL,created_at timestamptz NOT NULL DEFAULT now(),UNIQUE(rule_id,version));
CREATE TABLE world_intelligence.signals(id uuid PRIMARY KEY DEFAULT gen_random_uuid(),rule_id text NOT NULL,rule_version text NOT NULL,generated_at timestamptz NOT NULL,severity text NOT NULL,explanation text NOT NULL,evidence_ids uuid[] NOT NULL DEFAULT '{}');
CREATE TABLE world_intelligence.signal_evaluations(id uuid PRIMARY KEY DEFAULT gen_random_uuid(),signal_id uuid NOT NULL REFERENCES world_intelligence.signals(id) ON DELETE RESTRICT,expected boolean NOT NULL,actual boolean NOT NULL,outcome text NOT NULL);
COMMIT;