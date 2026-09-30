BEGIN;
CREATE TABLE world_intelligence.spatial_features(id uuid PRIMARY KEY DEFAULT gen_random_uuid(),entity_id uuid REFERENCES world_intelligence.entities(id) ON DELETE RESTRICT,feature_type text NOT NULL,geom geometry(Geometry,4326) NOT NULL,valid_from timestamptz,valid_to timestamptz,created_at timestamptz NOT NULL DEFAULT now(),CHECK(valid_to IS NULL OR valid_to>=valid_from),CHECK(ST_IsValid(geom)));
CREATE INDEX spatial_features_geom_gix ON world_intelligence.spatial_features USING GIST(geom);
CREATE INDEX spatial_features_time_idx ON world_intelligence.spatial_features(valid_from,valid_to);
CREATE TABLE world_intelligence.geofences(id uuid PRIMARY KEY DEFAULT gen_random_uuid(),name text NOT NULL,geom geometry(Polygon,4326) NOT NULL,CHECK(ST_IsValid(geom)));
CREATE INDEX geofences_geom_gix ON world_intelligence.geofences USING GIST(geom);
COMMIT;