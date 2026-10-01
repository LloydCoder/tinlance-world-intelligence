BEGIN;
CREATE TABLE world_intelligence.operational_events (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type text NOT NULL,
    severity text NOT NULL CHECK (severity IN ('info','warning','error','critical')),
    service text NOT NULL,
    occurred_at timestamptz NOT NULL,
    trace_id text,
    attributes jsonb NOT NULL DEFAULT '{}'::jsonb
);
CREATE INDEX operational_events_service_time_idx ON world_intelligence.operational_events(service,occurred_at DESC);
CREATE INDEX operational_events_severity_time_idx ON world_intelligence.operational_events(severity,occurred_at DESC);

CREATE TABLE world_intelligence.slo_measurements (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    slo_name text NOT NULL,
    window_start timestamptz NOT NULL,
    window_end timestamptz NOT NULL,
    target numeric(8,7) NOT NULL CHECK (target > 0 AND target <= 1),
    observed_success_rate numeric(8,7) NOT NULL CHECK (observed_success_rate >= 0 AND observed_success_rate <= 1),
    measured_at timestamptz NOT NULL DEFAULT now(),
    CHECK (window_end > window_start)
);
CREATE INDEX slo_measurements_name_time_idx ON world_intelligence.slo_measurements(slo_name,window_end DESC);
COMMIT;
