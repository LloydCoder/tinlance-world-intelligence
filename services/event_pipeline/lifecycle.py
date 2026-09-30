from packages.contracts.event import Event,EventStatus
def transition(event:Event,status:EventStatus)->Event:
 allowed={EventStatus.PROPOSED:{EventStatus.CONFIRMED,EventStatus.CANCELLED},EventStatus.CONFIRMED:{EventStatus.RESOLVED,EventStatus.CANCELLED},EventStatus.RESOLVED:set(),EventStatus.CANCELLED:set()}
 if status not in allowed[event.status]: raise ValueError(f"invalid event transition {event.status}->{status}")
 return Event(event.event_id,event.event_type,event.title,event.start_at,event.end_at,status,event.confidence,event.provenance_id)
