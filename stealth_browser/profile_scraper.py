from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .navigator import open_page
import time


def scrape_profile(username, driver):

    open_page(driver, f"https://www.instagram.com/{username}/")

    wait = WebDriverWait(driver, 25)

    # IMPORTANT: wait for REAL DATA not header
    followers_elem = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//header//a[contains(@href,'followers')]//span")
        )
    )

    time.sleep(1)

    def safe(xpath):
        try:
            return driver.find_element(By.XPATH, xpath).text
        except:
            return None

    posts = safe("//header//li[1]//span")
    followers = followers_elem.text
    following = safe("//header//a[contains(@href,'following')]//span")

    # bio
    try:
        bio = driver.find_element(
            By.XPATH,
            "//header//section//span[not(ancestor::a)]"
        ).text
    except:
        bio = ""

    return {
        "username": username,
        "posts": posts,
        "followers": followers,
        "following": following,
        "bio": bio
    }