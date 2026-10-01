# Phase 25 — Observability & Operations

Phase 25 establishes a common telemetry vocabulary and SLO/error-budget model.

## Implemented
- counter, histogram, and span reference primitives;
- trace/span identifiers for correlation;
- HTTP-oriented metric naming compatible with OpenTelemetry semantic conventions;
- SLO and error-budget calculations;
- persistent operational events;
- persistent SLO measurements;
- operational indexes for service, severity, SLO, and time.

## Operational model
Telemetry is diagnostic evidence about system behavior, not evidence about the external world. World Intelligence source observations and operational telemetry remain separate domains.

OpenTelemetry semantic conventions guide names and attributes. Production exporters/collectors should use the official OpenTelemetry SDK and backend rather than treating the dependency-free reference collector as a full telemetry stack.

SLOs provide measurable service objectives and error budgets. They are operational controls, not product promises until an external SLA explicitly adopts them.
