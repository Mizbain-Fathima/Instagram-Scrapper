import os
import json
from datetime import datetime

BASE_DIR = "data"

def save_snapshot(result):

    if not result:
        return

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    if result["type"] == "profile":
        folder = os.path.join(BASE_DIR, "profiles", result["username"])

    elif result["type"] == "post":
        folder = os.path.join(BASE_DIR, "posts", result["shortcode"])

    else:
        return

    os.makedirs(folder, exist_ok=True)

    path = os.path.join(folder, f"{timestamp}.json")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print("💾 Stored snapshot →", path)