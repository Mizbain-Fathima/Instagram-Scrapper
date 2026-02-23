from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .browser import create_browser
from .cookie_store import load_cookies
import time


def scrape_post(shortcode):

    driver = create_browser()
    driver.get("https://www.instagram.com/")

    load_cookies(driver)
    driver.refresh()

    url = f"https://www.instagram.com/p/{shortcode}/"
    driver.get(url)

    wait = WebDriverWait(driver, 20)

    # Wait for like section
    wait.until(
        EC.presence_of_element_located((By.XPATH, "//section"))
    )

    time.sleep(3)

    # -------- LIKES --------
    try:
        likes_elem = driver.find_element(
            By.XPATH,
            "//section//span[contains(text(),'like')]/preceding::span[1]"
        )
        likes = likes_elem.text
    except:
        likes = None

    # -------- CAPTION --------
    try:
        caption_elem = driver.find_element(
            By.XPATH,
            "//ul//span"
        )
        caption = caption_elem.text
    except:
        caption = ""

    # -------- COMMENTS COUNT --------
    try:
        comments_elem = driver.find_element(
            By.XPATH,
            "//section//span[contains(text(),'comment')]"
        )
        comments = comments_elem.text
    except:
        comments = None

    result = {
        "shortcode": shortcode,
        "likes": likes,
        "comments": comments,
        "caption": caption
    }

    driver.quit()
    return result