from dataclasses import dataclass
from datetime import datetime
@dataclass(frozen=True,slots=True)
class Anomaly:
 anomaly_id:str; subject_ref:str; metric:str; observed:float; baseline:float; score:float; detected_at:datetime
@dataclass(frozen=True,slots=True)
class IntelligenceCard:
 card_id:str; title:str; summary:str; freshness:str; confidence:float; evidence_ids:tuple[str,...]; contradiction_ids:tuple[str,...]; provenance_ids:tuple[str,...]
@dataclass(frozen=True,slots=True)
class Explanation:
 intelligence_id:str; rule_id:str|None; change_ids:tuple[str,...]; observation_ids:tuple[str,...]; evidence_ids:tuple[str,...]; artifact_ids:tuple[str,...]; source_ids:tuple[str,...]
