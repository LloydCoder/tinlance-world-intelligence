from dataclasses import dataclass
from enum import StrEnum
class CorroborationLevel(StrEnum): NONE="none"; PARTIAL="partial"; INDEPENDENT="independent"; CONTRADICTED="contradicted"
@dataclass(frozen=True,slots=True)
class SourceDependency:
 source_id:str; depends_on_source_id:str; relationship:str
@dataclass(frozen=True,slots=True)
class Contradiction:
 contradiction_id:str; assertion_ids:tuple[str,...]; reason:str; severity:float
@dataclass(frozen=True,slots=True)
class Corroboration:
 assertion_id:str; supporting_assertion_ids:tuple[str,...]; level:CorroborationLevel; independent_count:int
