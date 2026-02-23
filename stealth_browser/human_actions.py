import random
import time

def human_delay(a=1.2, b=3.5):
    time.sleep(random.uniform(a, b))

def slow_scroll(driver, times=3):

    for _ in range(times):
        driver.execute_script(
            f"window.scrollBy(0, {random.randint(300, 900)});"
        )
        human_delay(1, 2.5)