BEGIN;
CREATE TABLE world_intelligence.api_subscriptions (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id text NOT NULL CHECK (btrim(tenant_id) <> ''),
    event_type text NOT NULL CHECK (event_type IN ('change','signal','event')),
    resource text NOT NULL CHECK (btrim(resource) <> ''),
    callback_url text NOT NULL CHECK (callback_url ~ '^https://'),
    active boolean NOT NULL DEFAULT true,
    created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX api_subscriptions_tenant_idx ON world_intelligence.api_subscriptions(tenant_id,active);
CREATE INDEX api_subscriptions_dispatch_idx ON world_intelligence.api_subscriptions(event_type,resource) WHERE active;

CREATE TABLE world_intelligence.api_delivery_attempts (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    subscription_id uuid NOT NULL REFERENCES world_intelligence.api_subscriptions(id) ON DELETE CASCADE,
    event_id text NOT NULL,
    attempt integer NOT NULL CHECK (attempt >= 1),
    status text NOT NULL CHECK (status IN ('pending','delivered','failed')),
    attempted_at timestamptz,
    response_status integer CHECK (response_status IS NULL OR response_status BETWEEN 100 AND 599)
);
CREATE INDEX api_delivery_subscription_event_idx ON world_intelligence.api_delivery_attempts(subscription_id,event_id,attempt);
COMMIT;
