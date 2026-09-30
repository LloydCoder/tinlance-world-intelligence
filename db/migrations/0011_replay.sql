BEGIN;
CREATE TABLE world_intelligence.replay_runs(id uuid PRIMARY KEY DEFAULT gen_random_uuid(),manifest jsonb NOT NULL,status text NOT NULL CHECK(status IN('queued','running','completed','failed')),started_at timestamptz,completed_at timestamptz,error text,created_at timestamptz NOT NULL DEFAULT now());
CREATE INDEX replay_runs_status_idx ON world_intelligence.replay_runs(status,created_at DESC);
COMMIT;