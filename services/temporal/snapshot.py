from datetime import datetime,timezone
from packages.contracts.temporal import WorldSnapshot
def make_snapshot(snapshot_id:str,world_cutoff:datetime,knowledge_cutoff:datetime,ontology_version:str,pipeline_version:str)->WorldSnapshot:
 for d in (world_cutoff,knowledge_cutoff):
  if d.tzinfo is None: raise ValueError("cutoffs must be timezone-aware")
 return WorldSnapshot(snapshot_id,datetime.now(timezone.utc),world_cutoff,knowledge_cutoff,ontology_version,pipeline_version)
