import unittest
from services.observability.observability import placeholder if False else None
from services.observability.slo import SLO
from services.observability.telemetry import Counter,Histogram,Tracer

class ObservabilityTests(unittest.TestCase):
    def test_counter_and_histogram(self):
        counter=Counter("http.server.requests"); counter.add(); counter.add(2); self.assertEqual(counter.value,3)
        histogram=Histogram("http.server.request.duration"); histogram.observe(0.2); self.assertEqual(histogram.count,1)
    def test_span_has_trace_and_span_ids(self):
        tracer=Tracer(); span,start=tracer.start_span("http.server.request",{"http.request.method":"GET"})
        self.assertEqual(len(span.trace_id),32); self.assertGreaterEqual(tracer.end_span(span,start),0)
    def test_slo_error_budget(self):
        slo=SLO("api-availability",0.999)
        self.assertAlmostEqual(slo.error_budget(),0.001)
        self.assertEqual(slo.remaining_budget(0.998),0)

if __name__=="__main__": unittest.main()
