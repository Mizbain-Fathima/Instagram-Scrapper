from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .browser import create_browser
from .cookie_store import load_cookies
import time


def scrape_profile(username):

    driver = create_browser()
    driver.get("https://www.instagram.com/")

    load_cookies(driver)
    driver.refresh()

    url = f"https://www.instagram.com/{username}/"
    driver.get(url)

    wait = WebDriverWait(driver, 20)

    # wait until profile name visible
    wait.until(
        EC.presence_of_element_located((By.XPATH, "//h2 | //h1"))
    )

    time.sleep(3)

    # -------- POSTS --------
    try:
        posts = driver.find_element(
            By.XPATH,
            f"//a[contains(@href,'/{username}/followers/')]/preceding::span[1]"
        ).text
    except:
        posts = None

    # -------- FOLLOWERS --------
    try:
        followers = driver.find_element(
            By.XPATH,
            f"//a[contains(@href,'/{username}/followers/')]//span"
        ).text
    except:
        followers = None

    # -------- FOLLOWING --------
    try:
        following = driver.find_element(
            By.XPATH,
            f"//a[contains(@href,'/{username}/following/')]//span"
        ).text
    except:
        following = None

    # -------- BIO --------
    bio = ""
    try:
        bio_elem = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//header//section//span[not(ancestor::a) and string-length(text()) > 0]")
            )
        )
        bio = bio_elem.text
    except:
        bio = ""

    result = {
        "username": username,
        "posts": posts,
        "followers": followers,
        "following": following,
        "bio": bio
    }

    driver.quit()
    return result