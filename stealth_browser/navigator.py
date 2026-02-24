import random
import time

def human_pause(a=1.2, b=3.5):
    time.sleep(random.uniform(a, b))


def open_page(driver, url):
    driver.get(url)
    human_pause(2, 4)


def scroll_page(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
    human_pause()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/1.5);")
    human_pause()


def open_post_from_profile(driver):
    posts = driver.find_elements("xpath", "//a[contains(@href,'/p/')]")
    if posts:
        posts[0].click()
        human_pause(2,4)