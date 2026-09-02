import os

def env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()

SOURCE_1 = env("SOURCE_1")
SOURCE_2 = env("SOURCE_2")
BOT_TOKEN = env("BOT_TOKEN")
CHAT_ID = env("CHAT_ID")

MAX_CONFIGS = max(1, int(env("MAX_CONFIGS", "200")))
HEALTH_CHECK_ENABLED = env("HEALTH_CHECK_ENABLED", "true").lower() in {"1", "true", "yes", "on"}
HEALTH_TIMEOUT = max(1, int(env("HEALTH_TIMEOUT", "8")))
HEALTH_TARGET = env("HEALTH_TARGET", "https://www.gstatic.com/generate_204")

REMARK = "@nitruStore"
