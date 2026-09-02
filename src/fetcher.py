import base64
import requests

def fetch_subscription(url: str, timeout: int = 20) -> tuple[str, dict]:
    if not url:
        raise ValueError("Subscription URL is empty")

    r = requests.get(
        url,
        timeout=timeout,
        headers={"User-Agent": "NitrU-Subscription-Updater/1.0"},
    )
    r.raise_for_status()
    raw = r.content

    text = raw.decode("utf-8-sig", errors="replace").strip()
    meta = {"status": r.status_code, "bytes": len(raw), "url": url}

    # Most subscription providers return Base64, while some return plain URI text.
    if "://" in text:
        return text, meta

    compact = "".join(text.split())
    try:
        decoded = base64.b64decode(compact + "=" * (-len(compact) % 4), validate=False)
        decoded_text = decoded.decode("utf-8", errors="replace").strip()
        if "://" in decoded_text:
            return decoded_text, meta
    except Exception:
        pass

    return text, meta
