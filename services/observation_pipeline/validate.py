"""Observation validation; invalid observations never become canonical state."""
from packages.contracts.observation import Observation

class ObservationValidationError(ValueError): pass

def validate_observation(o:Observation)->Observation:
    if not o.observation_id or not o.artifact_id or not o.source_id or not o.subject_ref:
        raise ObservationValidationError("identity fields are required")
    if not o.predicate: raise ObservationValidationError("predicate is required")
    if o.observed_at.tzinfo is None or o.extracted_at.tzinfo is None:
        raise ObservationValidationError("timestamps must be timezone-aware")
    if o.valid_from and o.valid_from.tzinfo is None: raise ObservationValidationError("valid_from must be timezone-aware")
    if o.valid_to and o.valid_to.tzinfo is None: raise ObservationValidationError("valid_to must be timezone-aware")
    if o.valid_from and o.valid_to and o.valid_from>o.valid_to:
        raise ObservationValidationError("valid interval is inverted")
    return o
