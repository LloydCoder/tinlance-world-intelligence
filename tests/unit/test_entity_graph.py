import unittest
from services.entity_graph.resolution import MatchCandidate, MatchDecision, decide
from services.entity_graph.traverse import Edge, bounded_paths

class EntityGraphTests(unittest.TestCase):
    def test_traversal_is_bounded_and_cycle_safe(self):
        edges=[Edge("a","b","owns",1),Edge("b","c","operates",0.9),Edge("c","a","related",0.8)]
        paths=bounded_paths(edges,"a",max_depth=3)
        self.assertIn(("a","b","c"),[p.nodes for p in paths])
        self.assertTrue(all(len(p.nodes)<=4 for p in paths))
        self.assertTrue(all(p.nodes[-1]!="a" for p in paths))
    def test_high_confidence_requires_reason(self):
        candidate=MatchCandidate("a","b",0.99,())
        self.assertEqual(decide(candidate),MatchDecision.REVIEW)
    def test_same_entity_is_never_match_candidate(self):
        candidate=MatchCandidate("a","a",1.0,("same-id",))
        self.assertEqual(decide(candidate),MatchDecision.REJECT)
    def test_low_confidence_is_rejected(self):
        self.assertEqual(decide(MatchCandidate("a","b",0.4,("name",))),MatchDecision.REJECT)

if __name__=="__main__": unittest.main()
