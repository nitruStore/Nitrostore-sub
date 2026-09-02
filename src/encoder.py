import base64

def encode_subscription(configs) -> str:
    payload = "\n".join(c["uri"] for c in configs) + ("\n" if configs else "")
    return base64.b64encode(payload.encode("utf-8")).decode("ascii") + "\n"
