# How to add a source

A source is the first object in the provenance chain.

## Boundary

A source identifies an external origin. Acquisition creates retrievals and raw artifacts. Parsing and normalization happen only after artifact identity is established.

Do not bypass the artifact boundary by storing only normalized records.

## Requirements

Preserve:

- canonical URI identity;
- retrieval timestamps;
- source health;
- raw artifact identity and content hashes;
- transformation lineage;
- explicit unavailable and failure states.

## Security

External sources are untrusted. Address URL/target validation, connection-time DNS/IP validation, redirect revalidation, credential isolation, resource limits, parser isolation, rate limits, retry bounds, and auditability.

The acquisition preflight helper is not a substitute for connection-time enforcement.

## Verification

```bash
python -m unittest discover -s tests -v
python scripts/security_baseline.py
```
