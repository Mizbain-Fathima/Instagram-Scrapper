import json
import time
import os
from identity_pool.identity import Identity
from identity_pool.health_manager import HealthManager
health = HealthManager()

STORE = "identity_pool/identities.json"


class IdentityManager:

    def __init__(self):
        self.identities = self.load()

    # -------------------- storage --------------------

    def load(self):
        if not os.path.exists(STORE):
            return []

        try:
            with open(STORE, "r") as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except:
            return []


    def save(self):
        os.makedirs("identity_pool", exist_ok=True)
        with open(STORE, "w") as f:
            json.dump(self.identities, f, indent=2)

    # -------------------- selection --------------------

    def get_identity(self):
        """
        Returns a rested identity or creates a new one.
        Each identity keeps its own proxy + cookies lifetime.
        """
        now = time.time()

        # 1️⃣ reuse rested identity
        for data in self.identities:
            if health.is_blocked(data["name"]):
                continue

            if now - data["last_used"] > 120:
                data["last_used"] = now
                self.save()
                return Identity(name=data["name"], cookies=data.get("cookies", {}))


        # 2️⃣ create new identity
        name = f"user_{len(self.identities)+1}"

        identity_data = {
            "name": name,
            "last_used": now,
            "cookies": {}
        }

        self.identities.append(identity_data)
        self.save()

        return Identity(name=name, cookies={})
