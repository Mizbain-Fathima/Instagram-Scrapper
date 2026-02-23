import json
import os
import random

MEMORY_FILE = "identity_pool/identity_memory.json"


class MemoryManager:

    def __init__(self):
        self.memory = self.load()

    def load(self):
        if not os.path.exists(MEMORY_FILE):
            return {}

        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return {}
                return json.loads(content)
        except:
            return {}

    def save(self):
        os.makedirs("identity_pool", exist_ok=True)
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=2)

    def remember_profile(self, identity, username):
        self.memory.setdefault(identity, {"profiles": []})

        if username not in self.memory[identity]["profiles"]:
            self.memory[identity]["profiles"].append(username)

        self.save()

    def get_profiles(self, identity):
        return self.memory.get(identity, {}).get("profiles", [])

    def get_random_known_profile(self, identity):
        profiles = self.get_profiles(identity)
        if not profiles:
            return None
        return random.choice(profiles)
