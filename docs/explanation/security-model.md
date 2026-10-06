# Security model

Security is an architectural property because the platform processes untrusted external information.

```text
UNTRUSTED SOURCE
  ↓
ACQUISITION ISOLATION
  ↓
RAW ARTIFACT
  ↓
PARSER / EXTRACTOR
  ↓
CANDIDATE OBSERVATION
  ↓
VALIDATION
  ↓
RESOLUTION
  ↓
WORLD STATE
  ↓
CONTROLLED API
```

Primary risks include SSRF, malicious feeds/documents, prompt injection, credential leakage, resource exhaustion, unauthorized access, provenance tampering, dependency compromise, and unsafe rendering.

Security invariants include fail-closed authorization, immutable artifact identity, bounded request/pagination/resource use, secret-free logs, production persistence requirements, and separation from arbitrary agent execution.

See [SECURITY.md](../../SECURITY.md) and [the acquisition boundary](../security/acquisition-boundary.md).
