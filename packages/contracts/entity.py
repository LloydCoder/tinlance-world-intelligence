from dataclasses import dataclass,field
from enum import StrEnum
class EntityStatus(StrEnum): ACTIVE="active"; MERGED="merged"; SPLIT="split"; RETIRED="retired"
@dataclass(frozen=True,slots=True)
class Identifier: scheme:str; value:str
@dataclass(frozen=True,slots=True)
class Entity:
 entity_id:str; entity_type:str; canonical_name:str; status:EntityStatus=EntityStatus.ACTIVE; confidence:float=1.0
@dataclass(frozen=True,slots=True)
class EntityAlias: entity_id:str; alias:str; normalized_alias:str
@dataclass(frozen=True,slots=True)
class EntityResolution:
 candidate_entity_id:str; method:str; confidence:float; matched_identifier:Identifier|None=None; matched_alias:str|None=None
@dataclass(frozen=True,slots=True)
class EntityMergeSplit:
 operation_id:str; operation:str; from_entity_ids:tuple[str,...]; to_entity_ids:tuple[str,...]; reason:str; confidence:float
