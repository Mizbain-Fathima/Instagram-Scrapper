import json
import os

FILE = "identity_pool/identity_health.json"


class HealthManager:

    def __init__(self):
        self.data = self.load()

    def load(self):
        if os.path.exists(FILE):
            with open(FILE, "r") as f:
                return json.load(f)
        return {}

    def save(self):
        with open(FILE, "w") as f:
            json.dump(self.data, f, indent=2)

    def mark_bad(self, identity):
        self.data[identity] = {"blocked": True}
        self.save()

    def mark_good(self, identity):
        self.data[identity] = {"blocked": False}
        self.save()

    def is_blocked(self, identity):
        return self.data.get(identity, {}).get("blocked", False)
