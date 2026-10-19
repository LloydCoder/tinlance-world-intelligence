"""HTTP route-to-capability mapping; capability is derived from the route, never from caller input."""
from dataclasses import replace
from dataclasses import dataclass
from urllib.parse import parse_qs, urlparse

from api.query.service import RESOURCE_CAPABILITIES

@dataclass(frozen=True, slots=True)
class Route:
    method: str
    path: str
    resource: str
    capability: str

class IntelligenceRouter:
    def __init__(self, service):
        self.service = service
        self.routes = tuple(
            Route("GET", f"/v1/{resource}", resource, RESOURCE_CAPABILITIES[resource])
            for resource in ("entities", "events", "world-state", "changes", "signals", "evidence", "provenance")
        )

    def dispatch(self, path: str, context=None, legacy_limit: int | None = None):
        parsed = urlparse(path)
        query = parse_qs(parsed.query, keep_blank_values=False)
        try:
            limit = int(query.get("limit", [str(legacy_limit if legacy_limit is not None else 100)])[0])
            cursor = int(query.get("cursor", ["0"])[0])
        except ValueError as exc:
            raise ValueError("cursor and limit must be integers") from exc
        if cursor < 0 or limit < 1 or limit > 1000:
            raise ValueError("invalid pagination")
        for route in self.routes:
            if parsed.path == route.path:
                if context is None:
                    raise PermissionError("query context required")
                # The route controls the required capability; caller headers cannot select a broader one.
                scoped_context = replace(context, capability=route.capability)
                return self.service.query(route.resource, context=scoped_context, cursor=cursor, limit=limit)
        raise KeyError(path)
