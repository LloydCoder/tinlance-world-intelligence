import unittest
from datetime import datetime,timezone,timedelta
from packages.contracts.observation import Observation
from services.observation_pipeline.normalize import normalize_text,normalize_predicate
from services.observation_pipeline.validate import ObservationValidationError,validate_observation
class ObservationTests(unittest.TestCase):
 def make(self,**kw):
  now=datetime.now(timezone.utc); b=dict(observation_id="o",artifact_id="a",source_id="s",subject_ref="e",predicate="status",object_value="open",observed_at=now,extracted_at=now); b.update(kw); return Observation(**b)
 def test_normalization(self): self.assertEqual(normalize_text("  Café  x "),"Café x"); self.assertEqual(normalize_predicate(" Located In "),"located_in")
 def test_validation(self): self.assertIsNotNone(validate_observation(self.make()))
 def test_inverted_interval_rejected(self):
  n=datetime.now(timezone.utc)
  with self.assertRaises(ObservationValidationError): validate_observation(self.make(valid_from=n,valid_to=n-timedelta(seconds=1)))
 def test_naive_time_rejected(self):
  with self.assertRaises(ObservationValidationError): validate_observation(self.make(observed_at=datetime.now()))
