# rate_limiter.py

import random
import time

class RateLimiter:

    def wait(self):
        delay = random.uniform(6, 18)
        time.sleep(delay)
