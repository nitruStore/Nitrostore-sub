from urllib.parse import urlsplit, parse_qs, unquote
import base64
import json
import re

KNOWN = ("vmess://", "vless://", "trojan://", "ss://")

def _lines(text: str):
    for line in text.replace("\r", "\n").split("\n"):
        line = line.strip()
        if line:
            yield line

def _vmess_remark(uri: str) -> str:
    try:
        payload = uri[len("vmess://"):].strip()
        data = base64.b64decode(payload + "=" * (-len(payload) % 4)).decode()
        obj = json.loads(data)
        return obj.get("ps", "")
    except Exception:
        return ""

def _fragment(uri: str) -> str:
    try:
        return unquote(urlsplit(uri).fragment or "")
    except Exception:
        return ""

def parse(text: str) -> tuple[list[dict], int]:
    configs = []
    ignored = 0

    for line in _lines(text):
        lower = line.lower()
        if not lower.startswith(KNOWN):
            ignored += 1
            continue

        remark = _vmess_remark(line) if lower.startswith("vmess://") else _fragment(line)
        configs.append({
            "uri": line,
            "scheme": lower.split("://", 1)[0],
            "remark": remark,
        })

    return configs, ignored

def canonical_key(uri: str) -> str:
    # Deduplication key intentionally keeps the endpoint/credentials intact,
    # while normalizing surrounding whitespace.
    return uri.strip()
