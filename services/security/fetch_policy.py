"""SSRF-aware acquisition target policy with connection-time DNS validation hooks."""
from __future__ import annotations
import ipaddress
import socket
from urllib.parse import urlsplit

class UnsafeFetchTarget(ValueError):
    pass

def validate_target(uri: str, *, resolver=socket.getaddrinfo, allowed_hosts: frozenset[str] | None=None) -> tuple[str,...]:
    parsed=urlsplit(uri)
    if parsed.scheme.lower() not in {"http","https"} or not parsed.hostname:
        raise UnsafeFetchTarget("only HTTP(S) URLs with a hostname are allowed")
    if parsed.username is not None or parsed.password is not None or parsed.fragment:
        raise UnsafeFetchTarget("userinfo and fragments are forbidden")
    host=parsed.hostname.lower().rstrip(".")
    if allowed_hosts is not None and host not in allowed_hosts:
        raise UnsafeFetchTarget("host is not allowlisted")
    try:
        literal=ipaddress.ip_address(host)
        addresses=(literal,)
    except ValueError:
        try:
            infos=resolver(host, parsed.port or (443 if parsed.scheme=="https" else 80), type=socket.SOCK_STREAM)
        except OSError as exc:
            raise UnsafeFetchTarget("DNS resolution failed") from exc
        addresses=tuple({ipaddress.ip_address(info[4][0]) for info in infos})
        if not addresses:
            raise UnsafeFetchTarget("hostname resolved to no addresses")
    for address in addresses:
        if address.is_private or address.is_loopback or address.is_link_local or address.is_multicast or address.is_reserved or address.is_unspecified:
            raise UnsafeFetchTarget("target resolves to a non-public address")
    return tuple(str(address) for address in addresses)
