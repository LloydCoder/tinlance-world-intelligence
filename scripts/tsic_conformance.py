#!/usr/bin/env python3
"""Fail-closed verification of World Intelligence against TSIC contracts."""

from __future__ import annotations

import json
from urllib.request import Request, urlopen

TSIC_REVISION = "109d9bebd9d34cc1c920202c57958c7f0155c7ac"
RAW_ROOT = f"https://raw.githubusercontent.com/LloydCoder/tinlance-system-integration/{TSIC_REVISION}"
REQUIRED = {"identity-context", "event-envelope", "delivery-semantics", "trace-context", "economic-attribution"}


def fetch_json(path: str) -> dict:
    request = Request(
        f"{RAW_ROOT}/{path}",
        headers={"Accept": "application/json", "User-Agent": "tinlance-world-intelligence-ci"},
    )
    with urlopen(request, timeout=15) as response:
        if response.status != 200:
            raise RuntimeError(f"TSIC contract fetch failed for {path}: HTTP {response.status}")
        return json.load(response)


def main() -> None:
    manifest = fetch_json("manifests/ecosystem.json")
    adapter = fetch_json("integrations/world-intelligence/adapter.json")
    registry = fetch_json("catalog/contracts/registry.json")

    system = next(item for item in manifest["systems"] if item["id"] == "world-intelligence")
    if system["repository"] != "LloydCoder/tinlance-world-intelligence":
        raise AssertionError("TSIC World Intelligence repository mapping is stale")
    if system["governance_role"] != "world_intelligence_authority":
        raise AssertionError("World Intelligence governance role drifted")

    if adapter["source_system"] != "tsic" or adapter["target_system"] != "world-intelligence":
        raise AssertionError("invalid TSIC World Intelligence adapter endpoints")
    bindings = {item["tsic_contract"] for item in adapter["contract_bindings"]}
    if bindings != REQUIRED:
        raise AssertionError(f"contract binding drift: expected {sorted(REQUIRED)}, got {sorted(bindings)}")

    registered = {item["id"] for item in registry["contracts"]}
    if not registered >= REQUIRED:
        raise AssertionError("TSIC registry is missing a World Intelligence contract")

    authority = adapter["authority"]
    if authority["integration_contracts"] != "tsic":
        raise AssertionError("TSIC must remain integration-contract authority")
    if authority["world_state_semantics"] != "world-intelligence":
        raise AssertionError("World Intelligence semantic authority drift")
    if authority["execution_authority"] != "agent-platform":
        raise AssertionError("execution authority must remain Agent Platform")

    required_invariants = {
        "external_content_is_untrusted_data",
        "observation_is_not_evidence",
        "evidence_is_not_intelligence",
        "intelligence_is_not_authority",
        "historical_artifacts_are_immutable",
        "provenance_is_preserved",
        "tsic_remains_integration_authority",
        "agent-platform_remains_execution_authority",
    }
    if set(adapter["invariants"]) != required_invariants:
        raise AssertionError("World Intelligence authority invariants drifted")

    print(f"PASS World Intelligence TSIC conformance: revision={TSIC_REVISION} contracts={len(bindings)}")


if __name__ == "__main__":
    main()
