from datetime import datetime
from packages.contracts.temporal import TemporalAssertion,AssertionStatus
def state_as_of(assertions:list[TemporalAssertion],world_at:datetime,known_at:datetime)->list[TemporalAssertion]:
 return [a for a in assertions if a.status==AssertionStatus.ASSERTED and a.valid_from<=world_at and (a.valid_to is None or world_at<a.valid_to) and a.known_at<=known_at]
