from urllib.parse import urlsplit, unquote

KNOWN = ("vless://", "trojan://", "ss://")


def _lines(text: str):
    for line in text.replace("\r", "\n").split("\n"):
        line = line.strip()
        if line:
            yield line


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

        # VMess and unsupported protocols are ignored
        if not lower.startswith(KNOWN):
            ignored += 1
            continue

        remark = _fragment(line)

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
