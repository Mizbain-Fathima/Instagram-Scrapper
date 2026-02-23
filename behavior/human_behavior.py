import random
import time
from identity_pool.memory_manager import MemoryManager


class HumanBehavior:

    def __init__(self, session, identity_name):
        self.s = session
        self.identity_name = identity_name
        self.memory = MemoryManager()

    def _wait(self, a=2, b=7):
        time.sleep(random.uniform(a, b))

    def visit_home(self):
        self.s.get("https://www.instagram.com/")
        self._wait()

    def visit_explore(self):
        self.s.get("https://www.instagram.com/explore/")
        self._wait()

    def visit_profile(self, username):
        self.s.get(f"https://www.instagram.com/{username}/")
        self.memory.remember_profile(self.identity_name, username)
        self._wait()

    def warmup(self):
        self.visit_home()

        # 80% users watch stories first
        if random.random() < 0.8:
            self.watch_stories()

        known = self.memory.get_random_known_profile(self.identity_name)

        if known and random.random() < 0.7:
            self.visit_profile(known)
        else:
            self.visit_explore()

        self._wait(5, 12)


    def watch_stories(self):
        """
        Simulate watching story tray
        """
        # fetch story tray
        self.s.get("https://www.instagram.com/api/v1/feed/reels_tray/")
        self._wait(1.5, 4)

        # simulate opening few stories
        for _ in range(random.randint(1, 3)):
            self._wait(2, 5)

