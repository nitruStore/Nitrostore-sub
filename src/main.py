import json
import time
from pathlib import Path

from .config import (
    SOURCE_2, BOT_TOKEN, CHAT_ID, MAX_CONFIGS,
    HEALTH_CHECK_ENABLED, HEALTH_TIMEOUT, HEALTH_TARGET
)
from .fetcher import fetch_subscription
from .parser import parse
from .selector import prepare
from .encoder import encode_subscription
from .reporter import send_report

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output"
OUTPUT.mkdir(exist_ok=True)


def require_sources():
    if not SOURCE_2:
        raise RuntimeError("Missing required secret: SOURCE_2")


def main():
    require_sources()
    started = time.perf_counter()

    text2, _ = fetch_subscription(SOURCE_2)

    configs2, ignored2 = parse(text2)

    selected, detail = prepare(
        configs2,
        MAX_CONFIGS,
        HEALTH_CHECK_ENABLED,
        HEALTH_TIMEOUT,
        HEALTH_TARGET,
    )

    subscription = encode_subscription(selected)
    (OUTPUT / "subscription").write_text(subscription, encoding="utf-8")

    duration = time.perf_counter() - started

    metadata = {
        "updated_at_unix": int(time.time()),
        "published": len(selected),
        "limit": MAX_CONFIGS,
        "source2": len(configs2),
        "ignored_source2": ignored2,
        "parsed": len(configs2),
        **detail,
        "duration_seconds": round(duration, 3),
    }

    (OUTPUT / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    try:
        send_report(
            BOT_TOKEN,
            CHAT_ID,
            {
                "source2": len(configs2),
                "parsed": metadata["parsed"],
                "duplicates": metadata["duplicates"],
                "health_failed": metadata["health_failed"],
                "healthy": metadata["healthy"],
                "published": len(selected),
                "limit": MAX_CONFIGS,
                "duration": duration,
            },
        )
    except Exception as exc:
        print(f"Telegram report failed: {exc}")

    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
