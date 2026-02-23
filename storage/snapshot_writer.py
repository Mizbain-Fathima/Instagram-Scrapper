import json
import os
from datetime import datetime


def store_snapshot(result):

    if not result:
        return

    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Decide folder
    if result.get("type") == "profile":
        base = f"data/profiles/{result['username']}"
    else:
        base = f"data/posts/{result['shortcode']}"

    os.makedirs(base, exist_ok=True)

    path = f"{base}/{now}.json"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"💾 Stored snapshot → {path}")