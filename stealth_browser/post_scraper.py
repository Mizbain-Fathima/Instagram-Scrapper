from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from .navigator import open_page, human_pause
import time
import re


def scrape_post(shortcode, driver):

    url = f"https://www.instagram.com/p/{shortcode}/"
    open_page(driver, url)

    wait = WebDriverWait(driver, 25)

    # wait for caption block (real hydration indicator)
    wait.until(
        EC.presence_of_element_located((By.XPATH, "//article//ul"))
    )

    human_pause(2,4)

    def safe(xpath):
        try:
            return driver.find_element(By.XPATH, xpath).text
        except:
            return None

    username = safe("//header//a[contains(@href,'/')]")
    caption = safe("//article//ul//span") or ""

    hashtags = re.findall(r"#\w+", caption)

    # likes
    likes = safe("//section//span[contains(text(),'like')]/preceding::span[1]")

    # scroll to load comments
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    comments = safe("//section//span[contains(text(),'comment')]")

    # date
    try:
        post_date = driver.find_element(By.TAG_NAME, "time").get_attribute("datetime")
    except:
        post_date = None

    # media type
    if driver.find_elements(By.TAG_NAME, "video"):
        media_type = "video"
    elif driver.find_elements(By.XPATH, "//div[@role='button' and @tabindex='0']"):
        media_type = "carousel"
    else:
        media_type = "image"

    return {
        "shortcode": shortcode,
        "username": username,
        "likes": likes,
        "comments": comments,
        "caption": caption,
        "hashtags": hashtags,
        "media_type": media_type,
        "posted_at": post_date,
        "scraped_at": datetime.utcnow().isoformat()
    }