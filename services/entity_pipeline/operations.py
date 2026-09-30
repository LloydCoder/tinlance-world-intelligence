from packages.contracts.entity import Entity,EntityMergeSplit
def merge_entities(operation:EntityMergeSplit,entities:dict[str,Entity])->dict[str,Entity]:
 if operation.operation!="merge" or len(operation.to_entity_ids)!=1: raise ValueError("invalid merge")
 target=operation.to_entity_ids[0]
 if target not in entities: raise ValueError("target missing")
 return {k:(v if k not in operation.from_entity_ids else Entity(k,v.entity_type,v.canonical_name,v.status.MERGED,v.confidence)) for k,v in entities.items()}
def split_entities(operation:EntityMergeSplit)->tuple[str,...]:
 if operation.operation!="split" or not operation.to_entity_ids: raise ValueError("invalid split")
 return operation.to_entity_ids
