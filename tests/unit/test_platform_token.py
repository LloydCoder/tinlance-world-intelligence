from __future__ import annotations

from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from unittest.mock import patch

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa

from runtime.platform_token import PlatformTokenVerifier


class FakeJWKClient:
    key = None

    def __init__(self, *_args, **_kwargs):
        pass

    def get_signing_key_from_jwt(self, _token):
        return SimpleNamespace(key=self.key)


@pytest.fixture
def signing_keys():
    private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    FakeJWKClient.key = private.public_key()
    return private


def _token(private, **overrides):
    now = datetime.now(UTC)
    claims = {
        "iss": "https://identity.tinlance.test",
        "aud": "world-intelligence",
        "sub": "agent-17",
        "client_id": "agent-platform",
        "jti": "token-123",
        "principal_type": "agent",
        "tenant_id": "tenant-a",
        "scope": "world-intelligence:query",
        "purpose": "account_research",
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=3)).timestamp()),
    }
    claims.update(overrides)
    return jwt.encode(claims, private, algorithm="RS256", headers={"typ": "at+jwt", "kid": "test-key"})


def _verifier():
    return PlatformTokenVerifier(
        issuer="https://identity.tinlance.test",
        audience="world-intelligence",
        jwks_url="https://identity.tinlance.test/.well-known/jwks.json",
    )


def test_verifies_signed_platform_identity_and_scoped_purpose(signing_keys):
    with patch("runtime.platform_token.jwt.PyJWKClient", FakeJWKClient):
        principal = _verifier().verify(_token(signing_keys))
    assert principal.tenant_id == "tenant-a"
    assert principal.subject_id == "agent-17"
    assert principal.client_id == "agent-platform"
    assert principal.purpose == "account_research"
    assert principal.scopes == frozenset({"world-intelligence:query"})


@pytest.mark.parametrize(
    "claims",
    [
        {"aud": "another-service"},
        {"iss": "https://evil.example"},
        {"tenant_id": "tenant-a", "tid": "tenant-b"},
        {"scope": "unrelated:scope"},
        {"purpose": ""},
        {"principal_type": "unknown"},
    ],
)
def test_rejects_invalid_identity_authority_claims(signing_keys, claims):
    with patch("runtime.platform_token.jwt.PyJWKClient", FakeJWKClient):
        with pytest.raises(PermissionError):
            _verifier().verify(_token(signing_keys, **claims))


def test_rejects_http_jwks_and_unsupported_algorithms():
    with pytest.raises(ValueError):
        PlatformTokenVerifier(
            issuer="https://identity.tinlance.test",
            audience="world-intelligence",
            jwks_url="http://identity.tinlance.test/.well-known/jwks.json",
        )
    with pytest.raises(ValueError):
        PlatformTokenVerifier(
            issuer="https://identity.tinlance.test",
            audience="world-intelligence",
            jwks_url="https://identity.tinlance.test/.well-known/jwks.json",
            algorithms=("HS256",),
        )
