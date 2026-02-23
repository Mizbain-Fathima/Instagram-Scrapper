# schedule_manager.py

import json
import os
import random
from datetime import datetime

FILE = "identity_pool/identity_schedule.json"


class ScheduleManager:

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

    def get_or_create(self, identity):
        if identity not in self.data:

            wake = random.randint(7, 11)

            # 70% normal sleepers
            if random.random() < 0.7:
                sleep = random.randint(22, 23)

            # 30% night owls (after midnight)
            else:
                sleep = random.randint(0, 2)

            self.data[identity] = {
                "wake_hour": wake,
                "sleep_hour": sleep
            }

            self.save()

        return self.data[identity]

    def is_awake(self, identity):
        schedule = self.get_or_create(identity)
        now = datetime.now().hour

        wake = schedule["wake_hour"]
        sleep = schedule["sleep_hour"]

        if wake < sleep:
            return wake <= now < sleep
        else:
            return now >= wake or now < sleep
