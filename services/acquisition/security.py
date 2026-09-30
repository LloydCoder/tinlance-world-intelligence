"""Deterministic URL checks for the acquisition boundary."""
from __future__ import annotations
import ipaddress
from urllib.parse import urlsplit

class UnsafeFetchTarget(ValueError):
    pass

_ALLOWED_SCHEMES=frozenset({"http","https"})

def validate_fetch_uri(uri: str)->str:
    parsed=urlsplit(uri)
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise UnsafeFetchTarget("only http and https acquisition targets are allowed")
    if not parsed.hostname:
        raise UnsafeFetchTarget("acquisition target must contain a hostname")
    if parsed.username is not None or parsed.password is not None:
        raise UnsafeFetchTarget("userinfo in acquisition URLs is forbidden")
    if parsed.fragment:
        raise UnsafeFetchTarget("URL fragments are forbidden")
    try:
        address=ipaddress.ip_address(parsed.hostname)
    except ValueError:
        return parsed.geturl()
    if (address.is_private or address.is_loopback or address.is_link_local or
        address.is_multicast or address.is_reserved or address.is_unspecified):
        raise UnsafeFetchTarget("literal local/private/reserved IP targets are forbidden")
    return parsed.geturl()
