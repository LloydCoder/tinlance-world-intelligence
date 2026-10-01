import unittest
from datetime import datetime, timedelta, timezone
from services.data_quality.fingerprint import assertion_fingerprint
from services.data_quality.validate import validate_evidence

class EvidenceQualityTests(unittest.TestCase):
    def test_fingerprint_is_canonical(self):
        a=assertion_fingerprint("e1","name",{"b":2,"a":1})
        b=assertion_fingerprint("e1","name",{"a":1,"b":2})
        self.assertEqual(a,b)
        self.assertEqual(len(a),64)
    def test_complete_evidence_is_valid(self):
        now=datetime.now(timezone.utc)
        report=validate_evidence(source_id="s",artifact_id="a",observation_id="o",observed_at=now,provenance_id="p",object_value={"ok":True},now=now)
        self.assertTrue(report.valid); self.assertEqual(report.score,1.0)
    def test_missing_provenance_is_rejected(self):
        now=datetime.now(timezone.utc)
        report=validate_evidence(source_id="s",artifact_id="a",observation_id="o",observed_at=now,provenance_id=None,object_value={"ok":True},now=now)
        self.assertFalse(report.valid)
        self.assertTrue(any(i.code=="missing_provenance" for i in report.issues))
    def test_future_observation_is_warning_not_truth(self):
        now=datetime.now(timezone.utc)
        report=validate_evidence(source_id="s",artifact_id="a",observation_id="o",observed_at=now+timedelta(minutes=1),provenance_id="p",object_value={"ok":True},now=now)
        self.assertTrue(report.valid)
        self.assertTrue(any(i.code=="future_observation" for i in report.issues))

if __name__=="__main__": unittest.main()
