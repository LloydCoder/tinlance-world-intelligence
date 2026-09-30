from dataclasses import dataclass
from datetime import datetime
@dataclass(frozen=True,slots=True)
class SignalRule:
 rule_id:str; version:str; name:str; condition:dict
@dataclass(frozen=True,slots=True)
class Signal:
 signal_id:str; rule_id:str; rule_version:str; generated_at:datetime; severity:str; explanation:str; evidence_ids:tuple[str,...]
@dataclass(frozen=True,slots=True)
class SignalEvaluation:
 signal_id:str; expected:bool; actual:bool; outcome:str
