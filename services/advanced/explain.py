from packages.contracts.advanced import Explanation
def explain_lineage(intelligence_id:str,rule_id:str|None,changes=(),observations=(),evidence=(),artifacts=(),sources=())->Explanation:
 return Explanation(intelligence_id,rule_id,tuple(changes),tuple(observations),tuple(evidence),tuple(artifacts),tuple(sources))
