import requests
from datetime import datetime, timezone

def send_report(token, chat_id, stats):
    if not token or not chat_id:
        return False

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    text = (
        "🟢 *NΞTRU SUBSCRIPTION UPDATE*\n\n"
        f"🕒 `{now}`\n\n"
        f"📥 Source 1: `{stats['source1']}` configs\n"
        f"📥 Source 2: `{stats['source2']}` configs\n"
        f"📦 Total parsed: `{stats['parsed']}`\n"
        f"♻️ Duplicates removed: `{stats['duplicates']}`\n"
        f"❌ Health failures: `{stats['health_failed']}`\n"
        f"❤️ Healthy: `{stats['healthy']}`\n"
        f"🏆 Published: `{stats['published']}` / `{stats['limit']}`\n"
        f"⏱ Duration: `{stats['duration']:.2f}s`\n\n"
        "🔗 Output: `output/subscription`\n"
        "🔐 Output encoding: Base64\n"
    )

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    r = requests.post(
        url,
        json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"},
        timeout=20,
    )
    r.raise_for_status()
    return True
