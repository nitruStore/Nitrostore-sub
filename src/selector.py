from .parser import canonical_key
from .health import health_check

def prepare(configs, max_configs, health_enabled, timeout, target):
    unique = []
    seen = set()
    duplicates = 0

    for c in configs:
        key = canonical_key(c["uri"])
        if key in seen:
            duplicates += 1
            continue
        seen.add(key)
        unique.append(c)

    healthy = []
    failed = 0

    for c in unique:
        if health_enabled:
            ok, reason = health_check(c["uri"], timeout, target)
            c["health"] = reason
            if not ok:
                failed += 1
                continue
        else:
            c["health"] = "skipped"
        healthy.append(c)

    # Stable deterministic selection. If fewer than max are healthy, publish all.
    selected = healthy[:max_configs]

    for i, c in enumerate(selected, start=1):
        c["remark"] = f"{i:03d} | @nitruStore"

    return selected, {
        "parsed_unique": len(unique),
        "duplicates": duplicates,
        "health_failed": failed,
        "healthy": len(healthy),
    }
