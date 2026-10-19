from __future__ import annotations

import json

from scripts import tsic_conformance


def test_fetch_json_reads_from_the_supplied_pinned_tsic_checkout(tmp_path, monkeypatch) -> None:
    payload = {"systems": [{"id": "world-intelligence"}]}
    (tmp_path / "manifests").mkdir()
    (tmp_path / "manifests" / "ecosystem.json").write_text(
        json.dumps(payload), encoding="utf-8"
    )
    monkeypatch.setattr(tsic_conformance, "TSIC_ROOT", str(tmp_path))
    assert tsic_conformance.fetch_json("manifests/ecosystem.json") == payload


def test_local_tsic_revision_must_match_the_pinned_sha(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(tsic_conformance, "TSIC_ROOT", str(tmp_path))
    monkeypatch.setattr(tsic_conformance, "TSIC_REVISION", "a" * 40)
    # A non-repository path fails closed; the canonical workflow supplies a real pinned checkout.
    try:
        tsic_conformance.verify_local_revision()
    except RuntimeError as exc:
        assert "TSIC checkout revision mismatch" in str(exc)
    else:
        raise AssertionError("a non-repository TSIC path must not pass revision verification")
