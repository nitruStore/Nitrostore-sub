import base64
from urllib.parse import urlsplit, urlunsplit, quote


def encode_subscription(configs) -> str:
    lines = []

    for config in configs:
        uri = config["uri"]
        remark = config.get("remark", "")

        if remark:
            parts = urlsplit(uri)

            uri = urlunsplit((
                parts.scheme,
                parts.netloc,
                parts.path,
                parts.query,
                quote(remark, safe=""),
            ))

        lines.append(uri)

    payload = "\n".join(lines) + ("\n" if lines else "")

    return base64.b64encode(
        payload.encode("utf-8")
    ).decode("ascii") + "\n"
