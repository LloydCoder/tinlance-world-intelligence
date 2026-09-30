from packages.contracts.event import Event,EventCorrelation
def correlate(events:list[Event],window_seconds:int=86400)->list[EventCorrelation]:
 out=[]
 for i,a in enumerate(events):
  for b in events[i+1:]:
   delta=abs((a.start_at-b.start_at).total_seconds())
   if a.event_type==b.event_type and delta<=window_seconds:
    out.append(EventCorrelation(f"{a.event_id}:{b.event_id}",(a.event_id,b.event_id),"same_type_time_window",0.8))
 return out
