from dataclasses import dataclass
from datetime import datetime
@dataclass(frozen=True,slots=True)
class ReplayManifest:
 replay_id:str; artifact_ids:tuple[str,...]; ontology_version:str; pipeline_version:str; rule_versions:tuple[str,...]
@dataclass(frozen=True,slots=True)
class BacktestResult:
 rule_id:str; total:int; positives:int; true_positives:int; false_positives:int; false_negatives:int
 @property
 def precision(self)->float: return self.true_positives/(self.true_positives+self.false_positives) if self.true_positives+self.false_positives else 0.0
 @property
 def recall(self)->float: return self.true_positives/(self.true_positives+self.false_negatives) if self.true_positives+self.false_negatives else 0.0
