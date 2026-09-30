BEGIN;
CREATE TABLE world_intelligence.events(id uuid PRIMARY KEY DEFAULT gen_random_uuid(),event_type text NOT NULL,title text NOT NULL,start_at timestamptz NOT NULL,end_at timestamptz,status text NOT NULL CHECK(status IN('proposed','confirmed','resolved','cancelled')),confidence numeric(5,4) NOT NULL CHECK(confidence BETWEEN 0 AND 1),provenance_id uuid,created_at timestamptz NOT NULL DEFAULT now(),CHECK(end_at IS NULL OR end_at>=start_at));
CREATE TABLE world_intelligence.event_observations(event_id uuid NOT NULL REFERENCES world_intelligence.events(id) ON DELETE RESTRICT,observation_id uuid NOT NULL REFERENCES world_intelligence.observations(id) ON DELETE RESTRICT,PRIMARY KEY(event_id,observation_id));
CREATE TABLE world_intelligence.event_correlations(id uuid PRIMARY KEY DEFAULT gen_random_uuid(),event_ids uuid[] NOT NULL,relation text NOT NULL,confidence numeric(5,4) NOT NULL CHECK(confidence BETWEEN 0 AND 1),created_at timestamptz NOT NULL DEFAULT now());
CREATE INDEX events_time_idx ON world_intelligence.events(start_at DESC);
CREATE INDEX events_type_time_idx ON world_intelligence.events(event_type,start_at DESC);
COMMIT;