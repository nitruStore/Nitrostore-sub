import socket
from urllib.parse import urlsplit
import requests

def endpoint_from_uri(uri: str):
    try:
        p = urlsplit(uri)
        host = p.hostname
        port = p.port
        return host, port
    except Exception:
        return None, None

def tcp_health(uri: str, timeout: int) -> tuple[bool, str]:
    host, port = endpoint_from_uri(uri)
    if not host or not port:
        return False, "missing endpoint"

    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True, "tcp reachable"
    except Exception as e:
        return False, type(e).__name__

def health_check(uri: str, timeout: int = 8, target: str = "") -> tuple[bool, str]:
    # This is deliberately a conservative endpoint reachability check.
    # It does not attempt to authenticate to or abuse a remote service.
    return tcp_health(uri, timeout)
