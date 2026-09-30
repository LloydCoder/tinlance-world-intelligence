from packages.contracts import AcquisitionResponse
class ReconOSAdapter:
 def ingest(self,response:AcquisitionResponse)->dict:
  return {"status":"accepted","final_uri":response.final_uri,"retrieved_at":response.retrieved_at.isoformat()}
