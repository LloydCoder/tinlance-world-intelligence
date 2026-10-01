BEGIN;
CREATE INDEX temporal_assertion_status_valid_idx
 ON world_intelligence.temporal_assertions(status,valid_from,valid_to);
CREATE INDEX temporal_assertion_subject_known_valid_idx
 ON world_intelligence.temporal_assertions(subject_ref,known_at,valid_from,valid_to);
CREATE INDEX spatial_features_entity_time_idx
 ON world_intelligence.spatial_features(entity_id,valid_from,valid_to);
CREATE INDEX spatial_features_type_time_idx
 ON world_intelligence.spatial_features(feature_type,valid_from,valid_to);
COMMIT;
