from datetime import datetime
from packages.contracts.relationship import Relationship
def active_at(r:Relationship,at:datetime)->bool:
 return r.valid_from<=at and (r.valid_to is None or at<r.valid_to)
