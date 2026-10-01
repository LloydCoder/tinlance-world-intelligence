"""Environment-backed runtime configuration with safe defaults."""
from __future__ import annotations
from dataclasses import dataclass
import os

class ConfigurationError(ValueError):
    pass

@dataclass(frozen=True, slots=True)
class RuntimeConfig:
    environment: str = "development"
    host: str = "127.0.0.1"
    port: int = 8080
    max_body_bytes: int = 1_048_576
    bearer_token: str | None = None
    require_auth: bool = True

    @classmethod
    def from_env(cls) -> "RuntimeConfig":
        env = os.getenv("WORLD_INTELLIGENCE_ENV", "development").strip() or "development"
        host = os.getenv("WORLD_INTELLIGENCE_HOST", "127.0.0.1").strip() or "127.0.0.1"
        try:
            port = int(os.getenv("WORLD_INTELLIGENCE_PORT", "8080"))
            max_body = int(os.getenv("WORLD_INTELLIGENCE_MAX_BODY_BYTES", "1048576"))
        except ValueError as exc:
            raise ConfigurationError("port and max body size must be integers") from exc
        if not 1 <= port <= 65535:
            raise ConfigurationError("port must be 1..65535")
        if not 1024 <= max_body <= 100 * 1024 * 1024:
            raise ConfigurationError("max body size must be 1KiB..100MiB")
        token = os.getenv("WORLD_INTELLIGENCE_BEARER_TOKEN") or None
        require = os.getenv("WORLD_INTELLIGENCE_REQUIRE_AUTH", "true").lower() not in {"0", "false", "no"}
        if env in {"production", "staging"} and require and not token:
            raise ConfigurationError("bearer token is required when authentication is enabled")
        return cls(env, host, port, max_body, token, require)
