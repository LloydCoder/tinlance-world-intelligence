from __future__ import annotations

import unittest
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from unittest.mock import patch

import jwt
from cryptography.hazmat.primitives.asymmetric import rsa

from runtime.platform_token import PlatformTokenVerifier


class FakeJWKClient:
    key = None

    def __init__(self, *_args, **_kwargs):
        pass

    def get_signing_key_from_jwt(self, _token):
        return SimpleNamespace(key=self.key)


class PlatformTokenVerifierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        FakeJWKClient.key = cls.private_key.public_key()

    @staticmethod
    def verifier():
        return PlatformTokenVerifier(
            issuer="https://identity.tinlance.test",
            audience="world-intelligence",
            jwks_url="https://identity.tinlance.test/.well-known/jwks.json",
        )

    @classmethod
    def token(cls, **overrides):
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
        return jwt.encode(
            claims,
            cls.private_key,
            algorithm="RS256",
            headers={"typ": "at+jwt", "kid": "test-key"},
        )

    def verify(self, token):
        with patch("runtime.platform_token.jwt.PyJWKClient", FakeJWKClient):
            return self.verifier().verify(token)

    def test_verifies_signed_platform_identity_and_scoped_purpose(self):
        principal = self.verify(self.token())
        self.assertEqual(principal.tenant_id, "tenant-a")
        self.assertEqual(principal.subject_id, "agent-17")
        self.assertEqual(principal.client_id, "agent-platform")
        self.assertEqual(principal.purpose, "account_research")
        self.assertEqual(principal.scopes, frozenset({"world-intelligence:query"}))

    def test_rejects_invalid_identity_authority_claims(self):
        invalid_claims = (
            {"aud": "another-service"},
            {"iss": "https://evil.example"},
            {"tenant_id": "tenant-a", "tid": "tenant-b"},
            {"scope": "unrelated:scope"},
            {"purpose": ""},
            {"principal_type": "unknown"},
        )
        for claims in invalid_claims:
            with self.subTest(claims=claims):
                with self.assertRaises(PermissionError):
                    self.verify(self.token(**claims))

    def test_rejects_http_jwks_and_unsupported_algorithms(self):
        with self.assertRaises(ValueError):
            PlatformTokenVerifier(
                issuer="https://identity.tinlance.test",
                audience="world-intelligence",
                jwks_url="http://identity.tinlance.test/.well-known/jwks.json",
            )
        with self.assertRaises(ValueError):
            PlatformTokenVerifier(
                issuer="https://identity.tinlance.test",
                audience="world-intelligence",
                jwks_url="https://identity.tinlance.test/.well-known/jwks.json",
                algorithms=("HS256",),
            )


if __name__ == "__main__":
    unittest.main()
