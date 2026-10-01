BEGIN;
CREATE TABLE world_intelligence.tenant_policies (
    tenant_id text PRIMARY KEY CHECK (btrim(tenant_id) <> ''),
    allowed_capabilities jsonb NOT NULL DEFAULT '[]'::jsonb,
    allowed_purposes jsonb NOT NULL DEFAULT '[]'::jsonb,
    retention_days integer NOT NULL DEFAULT 365 CHECK (retention_days BETWEEN 1 AND 36500),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE world_intelligence.security_audit_events (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    actor_id text NOT NULL,
    tenant_id text NOT NULL,
    action text NOT NULL,
    outcome text NOT NULL CHECK (outcome IN ('allowed','denied','error')),
    occurred_at timestamptz NOT NULL,
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX security_audit_tenant_time_idx ON world_intelligence.security_audit_events(tenant_id,occurred_at DESC);
CREATE INDEX security_audit_action_time_idx ON world_intelligence.security_audit_events(action,occurred_at DESC);

CREATE OR REPLACE FUNCTION world_intelligence.prevent_audit_mutation() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
    RAISE EXCEPTION 'security audit events are append-only';
END;
$$;
CREATE TRIGGER security_audit_no_update_delete
BEFORE UPDATE OR DELETE ON world_intelligence.security_audit_events
FOR EACH ROW EXECUTE FUNCTION world_intelligence.prevent_audit_mutation();
COMMIT;
