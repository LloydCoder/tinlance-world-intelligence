import unittest
from services.fusion.assess import Support, assess

class FusionTests(unittest.TestCase):
    def test_duplicate_syndication_group_is_not_double_counted(self):
        result=assess([Support("e1","s1","wire-a",0.6),Support("e2","s2","wire-a",0.9),Support("e3","s3","independent-b",0.4)])
        self.assertAlmostEqual(result.support_score,1.0)
        self.assertEqual(result.independent_support_groups,2)
        self.assertEqual(result.supporting_evidence_ids,("e2","e3"))
    def test_contradictions_remain_visible(self):
        result=assess([Support("e1","s1","a",0.7),Support("e2","s2","b",0.5,True)])
        self.assertEqual(result.status,"mixed")
        self.assertEqual(result.contradicting_evidence_ids,("e2",))
    def test_empty_is_unknown(self):
        self.assertEqual(assess([]).status,"unknown")

if __name__=="__main__": unittest.main()
