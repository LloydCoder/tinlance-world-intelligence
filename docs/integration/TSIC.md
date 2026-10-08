# TSIC integration

Tinlance World Intelligence consumes the canonical TSIC ecosystem contracts without moving execution authority into the intelligence layer.

## Authority boundary

- **TSIC** owns ecosystem integration contracts, compatibility and certification.
- **World Intelligence** owns world-state semantics, provenance, temporal modeling, entities, events, relationships, change and signals.
- **Agent Platform** owns consequential execution authority.
- World Intelligence treats external content as untrusted data.

The semantic chain remains:

`source → artifact → observation → evidence → entity/event → temporal state → change → signal → intelligence`

and never becomes:

`intelligence → execution authority`.

## Conformance

Run:

```bash
python scripts/tsic_conformance.py
```

The CI gate consumes the immutable TSIC revision declared by the script and verifies repository registration, contract bindings and authority invariants.

Passing this check proves compatibility with the reviewed TSIC contract surface; it does not claim external production deployment.

## Integration path

The intended downstream path is:

`World Intelligence → TADS → SDEA → ReconOS → FadeReach`

with TSIC providing the cross-system contract and certification layer.

Signals and intelligence must retain provenance and temporal context when handed downstream. Consumers must not reinterpret intelligence as authoritative execution permission.
